/*
=========================================
Remote Terraform State
=========================================

Store Terraform state in S3.

Lock state using DynamoDB.

This prevents multiple engineers from
modifying infrastructure simultaneously.
*/

terraform {

  backend "s3" {

    bucket = "enterprise-idp-tfstate-684707795435"

    key = "dev/terraform.tfstate"

    region = "ap-south-1"

    dynamodb_table = "enterprise-idp-lock"

    encrypt = true

  }

}