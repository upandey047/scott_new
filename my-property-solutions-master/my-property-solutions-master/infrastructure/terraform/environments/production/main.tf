terraform {
  required_version = "= 0.12.9"

  backend "s3" {
    bucket = "my-property-solutions-production-infrastructure-tfstate"
    key    = "terraform.tfstate"
    region = "ap-southeast-2"
  }
}

provider "aws" {
  region  = var.region
  version = "~> 2.29"
}

provider "random" {
  version = "~> 2.2"
}


module "network" {
  source      = "../../modules/networks"
  environment = var.environment
  region      = var.region
}

resource "aws_sns_topic" "alerts" {
  name = "${var.environment}-alerts"
}

module "databases" {
  source                        = "../../modules/databases"
  alarm_arn                     = aws_sns_topic.alerts.arn
  db_subnets                    = module.network.private_subnet_ids
  environment_security_group_id = module.network.internal_security_group_id
  environment                   = var.environment
  allocated_storage             = var.database_allocated_storage
  instance_class                = var.database_instance_class
  db_master_password_version    = var.database_password_version
  vpc_id                        = module.network.vpc_id
  backup_retention_period       = var.database_backup_retention_period
  storage_encrypted             = var.database_storage_encrypted
}

module "application_servers" {
  source                        = "../../modules/application_servers"
  environment                   = var.environment
  vpc_id                        = module.network.vpc_id
  subnet_id                     = module.network.subnet_id
  aws_region                    = var.region
  public_key_path               = "../../files/terraform.pub"
  key_name                      = "my_property_solutions-${var.environment}"
  ami                           = var.application_ami
  ssl_certificate_arn           = var.load_balancer_ssl_certificate_arn
  environment_security_group_id = module.network.internal_security_group_id
}
