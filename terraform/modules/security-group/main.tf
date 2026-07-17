/*
=========================================
EC2 Security Group
=========================================
*/

resource "aws_security_group" "ec2" {

  name        = "ec2-security-group"
  description = "Security Group for EC2 Docker Host"
  vpc_id      = var.vpc_id

  # SSH (Restrict to your IP in production)
  ingress {
    description = "SSH"

    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  # HTTP
  ingress {
    description = "HTTP"

    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  # HTTPS
  ingress {
    description = "HTTPS"

    from_port = 443
    to_port   = 443
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  egress {

    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {
    Name = "enterprise-idp-ec2-sg"
  }

}

/*
=========================================
Database Security Group
(Optional for future RDS)
=========================================
*/

resource "aws_security_group" "database" {

  name        = "database-security-group"
  description = "Security Group for PostgreSQL"
  vpc_id      = var.vpc_id

  ingress {

    description = "PostgreSQL"

    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"

    security_groups = [
      aws_security_group.ec2.id
    ]
  }

  egress {

    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {
    Name = "enterprise-idp-db-sg"
  }

}