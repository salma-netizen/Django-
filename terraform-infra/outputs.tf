output "master_instance_id" {
  value = module.server.ec2_master_id
}

output "node1_instance_id" {
  value = module.server.ec2_node1_id
}

output "node2_instance_id" {
  value = module.server.ec2_node2_id
}

output "vpc_id" {
  value = module.network.vpc_id
}

output "internet_gateway_id" {
  value = module.network.internet_gateway_id
}

output "node1_public_ip" {
  value = module.server.node1_public_ip
}

output "node2_public_ip" {
  value = module.server.node2_public_ip
}

output "master_public_ip" {
  value = module.server.master_public_ip
}

output "alb_dns_name" {
  value = module.loadbalancer.alb_dns_name
}