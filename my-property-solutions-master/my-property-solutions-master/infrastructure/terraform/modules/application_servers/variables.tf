variable "environment" {
  type        = "string"
  description = "The environment the infrastructure in."
}

variable "vpc_id" {
  type        = "string"
  description = "The VPC id to add the application servers in."
}

variable "subnet_id" {
  type        = "string"
  description = "The subnet id to add the application servers in."
}

variable "aws_region" {
  description = "AWS region to launch servers."
}

variable "public_key_path" {
  description = <<DESCRIPTION
Path to the SSH public key to be used for authentication.
Ensure this keypair is added to your local SSH agent so provisioners can
connect.
Example: ~/.ssh/terraform.pub
DESCRIPTION
}

variable "key_name" {
  description = "Desired name of AWS key pair."
}

variable "ami" {
  description = "The AMI id to use."
}

variable "ssl_certificate_arn" {
  description = "The SSL certificate ARN for the load balancer."
}

variable "environment_security_group_id" {
  type        = "string"
  description = "The id of the environments security group."
}
