/*
===========================================
Public Subnet A
===========================================
*/

resource "aws_subnet" "public_1" {

  vpc_id = var.vpc_id

  cidr_block = var.public_subnet_1_cidr

  availability_zone = var.az_1

  map_public_ip_on_launch = true

  tags = {
    Name = "Public-Subnet-A"
    Type = "Public"
  }

}

resource "aws_subnet" "public_2" {

  vpc_id = var.vpc_id

  cidr_block = var.public_subnet_2_cidr

  availability_zone = var.az_2

  map_public_ip_on_launch = true

  tags = {
    Name = "Public-Subnet-B"
    Type = "Public"
  }

}

resource "aws_subnet" "private_1" {

  vpc_id = var.vpc_id

  cidr_block = var.private_subnet_1_cidr

  availability_zone = var.az_1

  map_public_ip_on_launch = false

  tags = {
    Name = "Private-Subnet-A"
    Type = "Private"
  }

}

resource "aws_subnet" "private_2" {

  vpc_id = var.vpc_id

  cidr_block = var.private_subnet_2_cidr

  availability_zone = var.az_2

  map_public_ip_on_launch = false

  tags = {
    Name = "Private-Subnet-B"
    Type = "Private"
  }

}

/*
===========================================
Internet Gateway
Allows communication between the VPC
and the public Internet.
===========================================
*/

resource "aws_internet_gateway" "igw" {

  vpc_id = var.vpc_id

  tags = {
    Name = "enterprise-idp-igw"
  }
}
/*
===========================================
Elastic IP
Required for the NAT Gateway.
===========================================
*/

resource "aws_eip" "nat_eip" {

  domain = "vpc"

  tags = {
    Name = "enterprise-idp-nat-eip"
  }

}

/*
===========================================
NAT Gateway
Provides outbound Internet access
to private subnets.
===========================================
*/

resource "aws_nat_gateway" "nat" {

  allocation_id = aws_eip.nat_eip.id

  subnet_id = aws_subnet.public_1.id

  tags = {
    Name = "enterprise-idp-nat"
  }

  depends_on = [
    aws_internet_gateway.igw
  ]

}
/*
===========================================
Public Route Table
Routes Internet traffic to the IGW.
===========================================
*/

resource "aws_route_table" "public" {

  vpc_id = var.vpc_id

  route {

    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.igw.id

  }

  tags = {
    Name = "public-route-table"
  }

}
resource "aws_route_table_association" "public_a" {

  subnet_id = aws_subnet.public_1.id

  route_table_id = aws_route_table.public.id

}
resource "aws_route_table_association" "public_b" {

  subnet_id = aws_subnet.public_2.id

  route_table_id = aws_route_table.public.id

}

/*
===========================================
Private Route Table
Routes outbound traffic through
the NAT Gateway.
===========================================
*/

resource "aws_route_table" "private" {

  vpc_id = var.vpc_id

  route {

    cidr_block = "0.0.0.0/0"

    nat_gateway_id = aws_nat_gateway.nat.id

  }

  tags = {
    Name = "private-route-table"
  }

}
resource "aws_route_table_association" "private_a" {

  subnet_id = aws_subnet.private_1.id

  route_table_id = aws_route_table.private.id

}
resource "aws_route_table_association" "private_b" {

  subnet_id = aws_subnet.private_2.id

  route_table_id = aws_route_table.private.id

}