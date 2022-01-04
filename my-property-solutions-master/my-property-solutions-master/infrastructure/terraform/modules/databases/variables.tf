variable "alarm_arn" {
  type        = "string"
  description = "The environment the infrastructure in."
}

variable "db_subnets" {
  type        = "list"
  description = "The subnets to connect to the DB."
}

variable "environment_security_group_id" {
  type        = "string"
  description = "The id of the environments security group."
}

variable "environment" {
  type        = "string"
  description = "The environment the database is in."
}

variable "allocated_storage" {
  type        = "string"
  description = "The amount of space to allocate to DB storage."
}

variable "instance_class" {
  type        = "string"
  description = "The instance class to use for the DB."
}

variable "db_master_password_version" {
  type        = "string"
  description = "Changing this value will cause a new DB password to be generated."
}

variable "vpc_id" {
  type        = "string"
  description = "Id of the VPC."
}

variable "backup_retention_period" {
  type        = "string"
  description = "Days to keep RDS backups"
}

variable "storage_encrypted" {
  type        = bool
  description = "Should the database be encrypted at rest?"
}
