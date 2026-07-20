from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# ==========================================================
# Project Paths (Not part of Settings)
# ==========================================================




# ==========================================================
# Application Settings
# ==========================================================

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    # enterprise-idp/
    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    # Terraform
    TERRAFORM_BINARY = "terraform"

    TERRAFORM_ROOT_DIR = PROJECT_ROOT / "terraform"
    TERRAFORM_BOOTSTRAP_DIR = TERRAFORM_ROOT_DIR / "bootstrap"
    TERRAFORM_ENVIRONMENTS_DIR = TERRAFORM_ROOT_DIR / "environments"
    TERRAFORM_MODULES_DIR = TERRAFORM_ROOT_DIR / "modules"
    TERRAFORM_WORKSPACE_DIR = TERRAFORM_ENVIRONMENTS_DIR / "dev"

    # Scripts
    SCRIPTS_DIR = PROJECT_ROOT / "scripts"
    EC2_USER_DATA_FILE = SCRIPTS_DIR / "user-data.sh"
    # ======================================================
    # Database
    # ======================================================

    DATABASE_URL: str = "sqlite+aiosqlite:///./idp.db"

    # ======================================================
    # JWT (Can be used later)
    # ======================================================

    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # ======================================================
    # AWS
    # ======================================================

    AWS_REGION: str = "ap-south-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # ======================================================
    # GitHub
    # ======================================================

    GITHUB_TOKEN: str = ""
    GITHUB_ORG: str = ""

    # ======================================================
    # Docker
    # ======================================================

    DOCKER_REGISTRY: str = ""

    # ======================================================
    # OpenAI
    # ======================================================

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    # ======================================================
    # EC2 Defaults
    # ======================================================

    EC2_AMI_ID: str = "ami-01a00762f46d584a1"
    EC2_DEFAULT_INSTANCE_TYPE: str = "t3.micro"

    EC2_DEFAULT_SUBNET_ID: str = ""
    EC2_DEFAULT_SECURITY_GROUP_ID: str = ""

    EC2_DEFAULT_IAM_PROFILE: str = "enterprise-idp-dev-instance-profile"
    EC2_DEFAULT_KEY_NAME: str = "idp"


# Singleton settings object
settings = Settings()