/*
=========================================
Security Group Outputs
=========================================
*/

output "ec2_security_group_id" {

  description = "EC2 Security Group ID"

  value = aws_security_group.ec2.id

}

output "database_security_group_id" {

  description = "Database Security Group ID"

  value = aws_security_group.database.id

}