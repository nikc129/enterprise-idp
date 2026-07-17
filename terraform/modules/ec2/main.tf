/*
===================================================
EC2 Instance
---------------------------------------------------
Creates an Ubuntu server that will become
our Docker platform.
===================================================
*/

resource "aws_instance" "this" {

  # Ubuntu AMI
  ami = var.ami_id

  # Instance size
  instance_type = var.instance_type

  # Launch inside the public subnet
  subnet_id = var.subnet_id

  # Attach Security Groups
  vpc_security_group_ids = var.security_group_ids

  # SSH Key Pair
  key_name = var.key_name

  # IAM permissions
  iam_instance_profile = var.iam_instance_profile

  # Execute bootstrap script
  user_data = file(var.user_data_file)

  # Enable detailed monitoring (CloudWatch)
  monitoring = true

  # Replace the instance safely if user_data changes
  user_data_replace_on_change = true

  tags = {
    Name = var.instance_name
    Role = "Application-Host"
  }
}