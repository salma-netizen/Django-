module "network" {
  source = "./modules/network"
}

module "server" {
  source      = "./modules/server"
  vpc_id      = module.network.vpc_id
  subnet_id_1 = module.network.public_subnet_1_id
  subnet_id_2 = module.network.public_subnet_2_id
  subnet_id_3 = module.network.public_subnet_3_id
}

module "loadbalancer" {
  source             = "./modules/loadbalancer"
  vpc_id             = module.network.vpc_id
  public_subnet_ids  = [module.network.public_subnet_1_id, module.network.public_subnet_2_id, module.network.public_subnet_3_id]
  alb_sg_id          = module.server.master_sg_id
  master_instance_id = module.server.ec2_master_id
}


