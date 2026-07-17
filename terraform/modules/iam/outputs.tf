# output "eks_cluster_role_arn" {

#   value = aws_iam_role.eks_cluster_role.arn

# }

# output "eks_node_role_arn" {

#   value = aws_iam_role.eks_node_role.arn

# }
/*
=========================================
IAM Outputs
=========================================
*/

output "instance_profile_name" {

  description = "IAM Instance Profile Name"

  value = aws_iam_instance_profile.ec2_profile.name

}

output "ec2_role_arn" {

  description = "EC2 IAM Role ARN"

  value = aws_iam_role.ec2_role.arn

}