from datetime import datetime

from pydantic import BaseModel


class EC2Create(BaseModel):
    instance_name: str
    instance_type: str = "t3.micro"
    subnet_id: str = ""
    security_group_ids: list[str] = []
    key_name: str = "idp"
    ami_id: str = ""
    iam_instance_profile: str = ""


class S3Create(BaseModel):
    bucket_name: str
    versioning: bool = True
    encryption: bool = True


class VPCCreate(BaseModel):
    vpc_name: str
    cidr_block: str = "10.0.0.0/16"


class RDSCreate(BaseModel):
    db_name: str
    instance_class: str = "db.t3.micro"
    engine: str = "postgres"
    engine_version: str = "16.4"
    allocated_storage: int = 20
    username: str = "admin"
    password: str


class ResourceResponse(BaseModel):
    id: int
    resource_type: str
    name: str
    cloud_id: str
    region: str
    status: str
    terraform_workspace: str
    config_json: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResourceListResponse(BaseModel):
    resources: list[ResourceResponse]
    total: int
