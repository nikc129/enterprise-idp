/*
=========================================
ECR Module Variables
=========================================
*/

variable "repository_name" {
  description = "Name of the ECR repository"
  type        = string
}

variable "image_tag_mutability" {
  description = "Allow image tags to be overwritten"
  type        = string
  default     = "MUTABLE"
}