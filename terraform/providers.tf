terraform {
  backend "s3" {
    bucket         = "enterprise-idp-tfstate-684707795435"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "enterprise-idp-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = "ap-south-1"
}