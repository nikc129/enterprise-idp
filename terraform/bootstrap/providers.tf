provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project     = "Enterprise-IDP"
      Environment = "bootstrap"
      ManagedBy   = "Terraform"
    }
  }
}