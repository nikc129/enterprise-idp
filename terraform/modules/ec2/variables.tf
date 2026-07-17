/*
===================================================
EC2 Module Variables
---------------------------------------------------
This module should be reusable.

The environment (dev/prod) provides
all these values.
===================================================
*/

# Name of the EC2 instance
variable "instance_name" {
  description = "EC2 Instance Name"
  type        = string
}

# EC2 instance size
variable "instance_type" {
  description = "EC2 Instance Type"
  type        = string
}

# Ubuntu AMI ID
variable "ami_id" {
  description = "Ubuntu AMI ID"
  type        = string
}

# Public subnet where EC2 will be launched
variable "subnet_id" {
  description = "Subnet ID"
  type        = string
}

# Security Groups attached to the instance
variable "security_group_ids" {
  description = "List of Security Groups"
  type        = list(string)
}

# IAM Instance Profile
variable "iam_instance_profile" {
  description = "IAM Instance Profile"
  type        = string
}

# SSH Key Pair
variable "key_name" {
  description = "EC2 Key Pair"
  type        = string
}

# User Data script
variable "user_data_file" {
  description = "Path to user-data.sh"
  type        = string
}