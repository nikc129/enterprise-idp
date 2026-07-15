output "vpc_id" {

  description = "VPC ID"

  value = aws_vpc.this.id

}

output "vpc_cidr" {

  description = "CIDR"

  value = aws_vpc.this.cidr_block

}