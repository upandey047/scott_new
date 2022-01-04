resource "aws_vpc" "default" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
}

resource "aws_route" "internet_access" {
  route_table_id         = aws_vpc.default.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.default.id
}

resource "aws_subnet" "default" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "private_az1" {
  vpc_id            = aws_vpc.default.id
  cidr_block        = "10.0.100.0/24"
  availability_zone = "${var.region}a"
}

resource "aws_subnet" "private_az2" {
  vpc_id            = aws_vpc.default.id
  cidr_block        = "10.0.120.0/24"
  availability_zone = "${var.region}b"
}

resource "aws_security_group" "internal" {
  description            = "Enable network access inside solution"
  revoke_rules_on_delete = true
  vpc_id                 = aws_vpc.default.id
}
