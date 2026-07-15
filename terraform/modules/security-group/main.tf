
/*
=========================================
Application Load Balancer
Security Group
=========================================
*/

resource "aws_security_group" "alb" {

  name = "alb-security-group"

  description = "Security group for ALB"

  vpc_id = var.vpc_id

  ingress {

    description = "HTTP"

    from_port = 80

    to_port = 80

    protocol = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]

  }

  ingress {

    description = "HTTPS"

    from_port = 443

    to_port = 443

    protocol = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]

  }

  egress {

    from_port = 0

    to_port = 0

    protocol = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]

  }

  tags = {

    Name = "enterprise-idp-alb-sg"

  }

}
resource "aws_security_group" "eks_nodes" {

  name = "eks-node-security-group"

  description = "Security group for EKS worker nodes"

  vpc_id = var.vpc_id

  ingress {

    description = "Traffic from ALB"

    from_port = 30000

    to_port = 32767

    protocol = "tcp"

    security_groups = [
      aws_security_group.alb.id
    ]

  }

  egress {

    from_port = 0

    to_port = 0

    protocol = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]

  }

}
resource "aws_security_group" "database" {

  name = "database-security-group"

  description = "Security group for RDS"

  vpc_id = var.vpc_id

  ingress {

    description = "PostgreSQL"

    from_port = 5432

    to_port = 5432

    protocol = "tcp"

    security_groups = [
      aws_security_group.eks_nodes.id
    ]

  }

  egress {

    from_port = 0

    to_port = 0

    protocol = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]

  }

}