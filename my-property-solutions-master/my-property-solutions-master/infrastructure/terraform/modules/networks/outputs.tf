output "vpc_id" {
  value = aws_vpc.default.id
}

output "subnet_id" {
  value = aws_subnet.default.id
}

output "private_subnet_ids" {
  value = [aws_subnet.private_az1.id, aws_subnet.private_az2.id]
}

output "internal_security_group_id" {
  value = aws_security_group.internal.id
}
