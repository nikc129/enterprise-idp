output "vpc_id" {

  value = module.vpc.vpc_id

}

output "public_subnet_1" {

  value = module.networking.public_subnet_1_id

}

output "public_subnet_2" {

  value = module.networking.public_subnet_2_id

}

output "private_subnet_1" {

  value = module.networking.private_subnet_1_id

}

output "private_subnet_2" {

  value = module.networking.private_subnet_2_id

}

output "eks_cluster_role" {

  value = module.iam.eks_cluster_role_arn

}

# output "ecr_repository_url" {
#   value = module.ecr.repository_url
# }