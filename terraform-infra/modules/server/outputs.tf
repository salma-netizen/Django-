output "master_sg_id" {
  value = aws_security_group.master_sg.id
}

# output "master_instance_id" {
#   value = aws_instance.ec2_master.id
# }


output "ec2_master_id" {
  value = aws_instance.ec2_master.id
}

output "ec2_node1_id" {
  value = aws_instance.ec2_node1.id
}

output "ec2_node2_id" {
  value = aws_instance.ec2_node2.id
}

output "node1_public_ip" {
  value       = aws_instance.ec2_node1.public_ip
  description = "Public IP of EC2 Node 1"
}

output "node2_public_ip" {
  value       = aws_instance.ec2_node2.public_ip
  description = "Public IP of EC2 Node 2"
}

output "master_public_ip" {
  value       = aws_instance.ec2_master.public_ip
  description = "Public IP of EC2 master"
}

