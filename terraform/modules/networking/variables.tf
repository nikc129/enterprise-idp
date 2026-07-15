variable "vpc_id" {
  description = "VPC where resources will be created"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block of the VPC"
  type        = string
}

variable "public_subnet_1_cidr" {
  type = string
}

variable "public_subnet_2_cidr" {
  type = string
}

variable "private_subnet_1_cidr" {
  type = string
}

variable "private_subnet_2_cidr" {
  type = string
}

variable "az_1" {
  type = string
}

variable "az_2" {
  type = string
}