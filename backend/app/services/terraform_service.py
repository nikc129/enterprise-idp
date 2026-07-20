import json
import logging
import shutil
from pathlib import Path

from app.core.config import settings
from app.integrations.terraform_cli import terraform_cli
from app.repositories.resource_repo import ResourceRepository
from app.schemas.infrastructure import EC2Create, S3Create, VPCCreate, RDSCreate

logger = logging.getLogger(__name__)


class TerraformService:
    def __init__(self, resource_repo: ResourceRepository):
        self.resource_repo = resource_repo
        self.workspace_base = Path(settings.TERRAFORM_WORKSPACE_DIR)
        self.modules_dir = Path(settings.TERRAFORM_MODULES_DIR).resolve()

    def _get_workspace(self, resource_type: str, resource_id: int) -> Path:
        return self.workspace_base / resource_type / str(resource_id)

    def _ensure_workspace(self, resource_type: str, resource_id: int) -> Path:
        ws = self._get_workspace(resource_type, resource_id)
        ws.mkdir(parents=True, exist_ok=True)
        return ws

    def _generate_backend_tf(self, resource_type: str, resource_id: int) -> str:
        state_key = f"{settings.TERRAFORM_STATE_KEY_PREFIX}/{resource_type}/{resource_id}/terraform.tfstate"
        return f'''
terraform {{
  backend "s3" {{
    bucket         = "{settings.TERRAFORM_STATE_BUCKET}"
    key            = "{state_key}"
    region         = "{settings.AWS_REGION}"
    dynamodb_table = "{settings.TERRAFORM_LOCK_TABLE}"
    encrypt        = true
  }}
}}
'''

    def _generate_providers_tf(self) -> str:
        return f'''
terraform {{
  required_version = ">= 1.14"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }}
  }}
}}

provider "aws" {{
  region = "{settings.AWS_REGION}"
}}
'''

    async def provision_ec2(self, params: EC2Create, user_id: int):
        resource = await self.resource_repo.create(
            resource_type="ec2",
            name=params.instance_name,
            cloud_id="",
            status="provisioning",
            terraform_workspace="",
            config=params.model_dump(),
            created_by=user_id,
        )
        ws = self._ensure_workspace("ec2", resource.id)

        modules_path = str(self.modules_dir)
        ami = params.ami_id or settings.EC2_AMI_ID
        subnet = params.subnet_id or settings.EC2_DEFAULT_SUBNET_ID
        sg_ids = json.dumps(params.security_group_ids) if params.security_group_ids else f'["{settings.EC2_DEFAULT_SECURITY_GROUP_ID}"]'
        iam = params.iam_instance_profile or settings.EC2_DEFAULT_IAM_PROFILE
        key = params.key_name or settings.EC2_DEFAULT_KEY_NAME
        user_data = settings.EC2_USER_DATA_FILE

        main_tf = f'''
terraform {{
  required_version = ">= 1.14"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }}
  }}
}}

provider "aws" {{
  region = "{settings.AWS_REGION}"
}}

module "ec2" {{
  source = "{modules_path}/ec2"

  instance_name        = "{params.instance_name}"
  instance_type        = "{params.instance_type}"
  ami_id               = "{ami}"
  subnet_id            = "{subnet}"
  security_group_ids   = {sg_ids}
  iam_instance_profile = "{iam}"
  key_name             = "{key}"
  user_data_file       = "{user_data}"
}}

output "instance_id" {{
  value = module.ec2.instance_id
}}

output "public_ip" {{
  value = module.ec2.public_ip
}}

output "public_dns" {{
  value = module.ec2.public_dns
}}

output "private_ip" {{
  value = module.ec2.private_ip
}}
'''
        (ws / "main.tf").write_text(main_tf)

        code, stdout, stderr = await terraform_cli.init(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform init failed: {stderr}")

        code, stdout, stderr = await terraform_cli.plan(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform plan failed: {stderr}")

        code, stdout, stderr = await terraform_cli.apply(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform apply failed: {stderr}")

        code, out_stdout, out_stderr = await terraform_cli.output(str(ws))
        outputs = {}
        if code == 0 and out_stdout.strip():
            outputs = json.loads(out_stdout)

        cloud_id = outputs.get("instance_id", {}).get("value", "")
        await self.resource_repo.update_status(resource.id, "active", cloud_id=cloud_id)
        resource = await self.resource_repo.get_by_id(resource.id)
        return resource

    async def provision_s3(self, params: S3Create, user_id: int):
        resource = await self.resource_repo.create(
            resource_type="s3",
            name=params.bucket_name,
            cloud_id=params.bucket_name,
            status="provisioning",
            terraform_workspace="",
            config=params.model_dump(),
            created_by=user_id,
        )
        ws = self._ensure_workspace("s3", resource.id)

        modules_path = str(self.modules_dir)
        main_tf = f'''
terraform {{
  required_version = ">= 1.14"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }}
  }}
}}

provider "aws" {{
  region = "{settings.AWS_REGION}"
}}

module "s3" {{
  source = "{modules_path}/s3"

  bucket_name = "{params.bucket_name}"
  versioning  = {str(params.versioning).lower()}
  encryption  = {str(params.encryption).lower()}
  tags = {{
    Name    = "{params.bucket_name}"
    Project = "enterprise-idp"
  }}
}}

output "bucket_id" {{
  value = module.s3.bucket_id
}}

output "bucket_arn" {{
  value = module.s3.bucket_arn
}}
'''
        (ws / "main.tf").write_text(main_tf)

        code, _, stderr = await terraform_cli.init(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform init failed: {stderr}")

        code, _, stderr = await terraform_cli.plan(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform plan failed: {stderr}")

        code, _, stderr = await terraform_cli.apply(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform apply failed: {stderr}")

        await self.resource_repo.update_status(resource.id, "active", cloud_id=params.bucket_name)
        return await self.resource_repo.get_by_id(resource.id)

    async def provision_vpc(self, params: VPCCreate, user_id: int):
        resource = await self.resource_repo.create(
            resource_type="vpc",
            name=params.vpc_name,
            cloud_id="",
            status="provisioning",
            terraform_workspace="",
            config=params.model_dump(),
            created_by=user_id,
        )
        ws = self._ensure_workspace("vpc", resource.id)

        modules_path = str(self.modules_dir)
        main_tf = f'''
terraform {{
  required_version = ">= 1.14"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }}
  }}
}}

provider "aws" {{
  region = "{settings.AWS_REGION}"
}}

module "vpc" {{
  source = "{modules_path}/vpc"

  vpc_name   = "{params.vpc_name}"
  cidr_block = "{params.cidr_block}"
}}

output "vpc_id" {{
  value = module.vpc.vpc_id
}}

output "vpc_cidr" {{
  value = module.vpc.vpc_cidr
}}
'''
        (ws / "main.tf").write_text(main_tf)

        code, _, stderr = await terraform_cli.init(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform init failed: {stderr}")

        code, _, stderr = await terraform_cli.plan(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform plan failed: {stderr}")

        code, _, stderr = await terraform_cli.apply(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform apply failed: {stderr}")

        code, out_stdout, _ = await terraform_cli.output(str(ws))
        outputs = json.loads(out_stdout) if code == 0 and out_stdout.strip() else {}
        cloud_id = outputs.get("vpc_id", {}).get("value", "")
        await self.resource_repo.update_status(resource.id, "active", cloud_id=cloud_id)
        return await self.resource_repo.get_by_id(resource.id)

    async def provision_rds(self, params: RDSCreate, user_id: int):
        resource = await self.resource_repo.create(
            resource_type="rds",
            name=params.db_name,
            cloud_id="",
            status="provisioning",
            terraform_workspace="",
            config=params.model_dump(exclude={"password"}),
            created_by=user_id,
        )
        ws = self._ensure_workspace("rds", resource.id)

        modules_path = str(self.modules_dir)
        main_tf = f'''
terraform {{
  required_version = ">= 1.14"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }}
  }}
}}

provider "aws" {{
  region = "{settings.AWS_REGION}"
}}

variable "db_password" {{
  type      = string
  sensitive = true
}}

module "rds" {{
  source = "{modules_path}/rds"

  db_name             = "{params.db_name}"
  engine              = "{params.engine}"
  engine_version      = "{params.engine_version}"
  instance_class      = "{params.instance_class}"
  allocated_storage   = {params.allocated_storage}
  username            = "{params.username}"
  password            = var.db_password
  private_subnet_ids  = []
  security_group_ids  = []
  tags = {{
    Name    = "{params.db_name}"
    Project = "enterprise-idp"
  }}
}}

output "rds_endpoint" {{
  value = module.rds.endpoint
}}

output "rds_arn" {{
  value = module.rds.rds_arn
}}
'''
        (ws / "main.tf").write_text(main_tf)

        tfvars = f'db_password = "{params.password}"\n'
        (ws / "terraform.tfvars").write_text(tfvars)

        code, _, stderr = await terraform_cli.init(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform init failed: {stderr}")

        code, _, stderr = await terraform_cli.plan(str(ws), var_file="terraform.tfvars")
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform plan failed: {stderr}")

        code, _, stderr = await terraform_cli.apply(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource.id, "failed")
            raise RuntimeError(f"Terraform apply failed: {stderr}")

        code, out_stdout, _ = await terraform_cli.output(str(ws))
        outputs = json.loads(out_stdout) if code == 0 and out_stdout.strip() else {}
        cloud_id = outputs.get("rds_endpoint", {}).get("value", "")
        await self.resource_repo.update_status(resource.id, "active", cloud_id=cloud_id)
        return await self.resource_repo.get_by_id(resource.id)

    async def destroy_resource(self, resource_id: int) -> bool:
        resource = await self.resource_repo.get_by_id(resource_id)
        if not resource:
            raise ValueError("Resource not found")

        await self.resource_repo.update_status(resource_id, "destroying")
        ws = self._get_workspace(resource.resource_type, resource_id)

        if not ws.exists():
            await self.resource_repo.delete(resource_id)
            return True

        code, _, stderr = await terraform_cli.init(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource_id, "active")
            raise RuntimeError(f"Terraform init failed during destroy: {stderr}")

        code, _, stderr = await terraform_cli.destroy(str(ws))
        if code != 0:
            await self.resource_repo.update_status(resource_id, "active")
            raise RuntimeError(f"Terraform destroy failed: {stderr}")

        shutil.rmtree(ws, ignore_errors=True)
        await self.resource_repo.delete(resource_id)
        return True

    async def get_terraform_logs(self, resource_id: int) -> str:
        resource = await self.resource_repo.get_by_id(resource_id)
        if not resource:
            return "Resource not found"
        ws = self._get_workspace(resource.resource_type, resource_id)
        log_file = ws / "terraform.log"
        if log_file.exists():
            return log_file.read_text()
        return "No logs available"
