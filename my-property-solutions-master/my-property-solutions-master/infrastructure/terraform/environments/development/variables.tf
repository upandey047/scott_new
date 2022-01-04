variable "region" {
  type        = "string"
  description = "Which AWS region the infrastructure will go into."
}

variable "environment" {
  type        = "string"
  description = "Which deployment environment the infrastructue is for."
}

variable "database_allocated_storage" {
  type        = "string"
  description = "The amount of space to allocate to DB storage."
}

variable "database_instance_class" {
  type        = "string"
  description = "The instance class to use for the DB."
}

variable "database_password_version" {
  type        = "string"
  description = "Changing this value will cause a new DB password to be generated."
}

variable "database_backup_retention_period" {
  type        = "string"
  description = "Days to keep RDS backups"
}
variable "database_storage_encrypted" {
  type        = bool
  description = "Should the database be encrypted at rest?"
}

variable "application_ami" {
  type        = "string"
  description = "The AMI id to use for the application."
}

variable "load_balancer_ssl_certificate_arn" {
  type        = "string"
  description = "The SSL certificate ARN for the load balancer."
}
