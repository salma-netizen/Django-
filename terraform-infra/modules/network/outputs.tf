
output "vpc_id" {
  value = aws_vpc.main.id
}
output "public_subnet_1_id" {
  value = aws_subnet.public_subnet_1.id
}

output "public_subnet_2_id" {
  value = aws_subnet.public_subnet_2.id
}

output "public_subnet_3_id" {
  value = aws_subnet.public_subnet_3.id
}

output "internet_gateway_id" {
  value = aws_internet_gateway.igw.id
}
