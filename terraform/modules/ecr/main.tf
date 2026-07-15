/*
=========================================
Create Amazon ECR Repository
=========================================
*/

resource "aws_ecr_repository" "this" {

  # Repository name
  name = var.repository_name

  # Allow the same tag (like "latest") to be pushed again
  image_tag_mutability = var.image_tag_mutability

  # Enable image scanning for vulnerabilities
  image_scanning_configuration {
    scan_on_push = true
  }

  # Encrypt images at rest using AWS-managed keys
  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Name = var.repository_name
  }
}
/*
=========================================
Lifecycle Policy
Keep only the latest 20 images
=========================================
*/

resource "aws_ecr_lifecycle_policy" "this" {

  repository = aws_ecr_repository.this.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 20 images"

        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 20
        }

        action = {
          type = "expire"
        }
      }
    ]
  })
}