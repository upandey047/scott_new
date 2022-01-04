region      = "ap-southeast-2"
environment = "development"

database_instance_class          = "db.t2.micro"
database_allocated_storage       = "100" # GB
database_password_version        = 1
database_backup_retention_period = 7
database_storage_encrypted       = false

application_ami                   = "ami-0015c4dc277d33da3"
load_balancer_ssl_certificate_arn = "arn:aws:acm:ap-southeast-2:500434574192:certificate/1c123da5-cd42-4140-b7ef-4718c367b67f"
