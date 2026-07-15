/*
=========================================
VPC
=========================================
*/

module "vpc" {

  source = "../../modules/vpc"

  vpc_name = "${var.project_name}-vpc"

  cidr_block = "10.0.0.0/16"

}
/*
=========================================
Networking
=========================================
*/

module "networking" {

  source = "../../modules/networking"

  vpc_id = module.vpc.vpc_id

  vpc_cidr = module.vpc.vpc_cidr

  public_subnet_1_cidr = "10.0.1.0/24"

  public_subnet_2_cidr = "10.0.2.0/24"

  private_subnet_1_cidr = "10.0.11.0/24"

  private_subnet_2_cidr = "10.0.12.0/24"

  az_1 = "ap-south-1a"

  az_2 = "ap-south-1b"

}
module "security_groups" {

  source = "../../modules/security-group"

  vpc_id = module.vpc.vpc_id

}
module "iam" {

  source = "../../modules/iam"

  project_name = var.project_name

}
/*
=========================================
Amazon ECR
=========================================
*/

# module "ecr" {

#   source = "../../modules/ecr"

#   repository_name = "${var.project_name}-repository"

# }