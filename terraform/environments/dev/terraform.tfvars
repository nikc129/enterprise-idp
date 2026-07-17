aws_region = "ap-south-1"

project_name = "enterprise-idp-dev"

instance_name = "enterprise-idp-dev"

instance_type = "t3.micro"

# Ubuntu 22.04 AMI (Replace with the latest AMI for your region)
ami_id = "ami-01a00762f46d584a1"

key_name = "idp"

user_data_file = "../../../scripts/user-data.sh"