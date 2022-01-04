# Security Group Config
resource "aws_security_group" "default" {
  description            = "RDS security group"
  revoke_rules_on_delete = true
  vpc_id                 = var.vpc_id
}

resource "aws_security_group_rule" "default_internal_ingress" {
  security_group_id        = aws_security_group.default.id
  from_port                = aws_db_instance.master.port
  to_port                  = aws_db_instance.master.port
  protocol                 = "tcp"
  type                     = "ingress"
  source_security_group_id = var.environment_security_group_id
}

resource "aws_security_group_rule" "default_egress" {
  security_group_id = aws_security_group.default.id
  from_port         = 0
  to_port           = 65535
  protocol          = "all"
  type              = "egress"

  cidr_blocks = [
    "0.0.0.0/0",
  ]
}

# Subnet config

resource "aws_db_subnet_group" "default" {
  description = "RDS DB Subnets"
  subnet_ids  = var.db_subnets
}

resource "random_string" "master_password" {
  length  = 30
  special = false

  keepers = {
    db_password_gen = var.db_master_password_version
  }
}

resource "aws_db_instance" "master" {
  instance_class                        = var.instance_class
  allocated_storage                     = var.allocated_storage
  backup_retention_period               = var.backup_retention_period
  deletion_protection                   = true
  enabled_cloudwatch_logs_exports       = []
  engine                                = "postgres"
  engine_version                        = "11.8"
  iam_database_authentication_enabled   = false
  identifier_prefix                     = "${var.environment}-main-"
  iops                                  = 0
  multi_az                              = false
  port                                  = 5432
  storage_encrypted                     = var.storage_encrypted
  storage_type                          = "gp2"
  username                              = "my_property_solutions"
  password                              = random_string.master_password.result
  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  skip_final_snapshot                   = false
  final_snapshot_identifier             = "my-property-soltions-snapshot"
  db_subnet_group_name                  = aws_db_subnet_group.default.name
  parameter_group_name                  = aws_db_parameter_group.master.name

  vpc_security_group_ids = [
    aws_security_group.default.id
  ]

  tags = {
    Name = "${var.environment}-database"
  }
}

resource "aws_db_parameter_group" "master" {
  family      = "postgres11"
  description = "Master DB optimized parameter group"

  parameter {
    name  = "log_min_duration_statement"
    value = "10000"
  }

  parameter {
    name  = "random_page_cost"
    value = "1"
  }

  parameter {
    name         = "rds.logical_replication"
    value        = "1"
    apply_method = "pending-reboot"
  }

  parameter {
    name  = "seq_page_cost"
    value = "1"
  }

  parameter {
    name         = "shared_preload_libraries"
    value        = "pglogical"
    apply_method = "pending-reboot"
  }

  parameter {
    name  = "wal_sender_timeout"
    value = "0"
  }

  tags = {
    "Name" = "Master Optimized"
  }
}


resource "aws_cloudwatch_metric_alarm" "master_free_storage_space" {
  alarm_name = "${var.environment}-FreeStorageSpaceAlarm"

  alarm_actions = [
    var.alarm_arn
  ]

  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = 5
  threshold           = "3000000000"
  alarm_description   = "Alarm if ms storage space <= 3 GB for 5 minutes"

  dimensions = {
    "DBInstanceIdentifier" = aws_db_instance.master.id
  }

  period      = 60
  statistic   = "Average"
  namespace   = "AWS/RDS"
  metric_name = "FreeStorageSpace"
}

resource "aws_cloudwatch_metric_alarm" "master_cpu_high_alarm" {
  alarm_name = "${var.environment}-CPUAlarmHigh"

  alarm_actions = [
    var.alarm_arn
  ]

  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 15
  threshold           = "90"
  alarm_description   = "Alarm if ms CPU > 90% for 15 minutes"

  dimensions = {
    "DBInstanceIdentifier" = aws_db_instance.master.id
  }

  metric_name        = "CPUUtilization"
  namespace          = "AWS/RDS"
  period             = 60
  statistic          = "Average"
  treat_missing_data = "missing"
}
