
resource "aws_security_group" "master_sg" {
  name        = "k8s-master-sg"
  description = "SG for Kubernetes master and Jenkins"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = [
      { from = 22,    to = 22,    protocol = "tcp", desc = "SSH" },
      { from = 8080,  to = 8080,  protocol = "tcp", desc = "Jenkins UI" },
      { from = 6443,  to = 6443,  protocol = "tcp", desc = "K8s API Server" },
      { from = 10250, to = 10250, protocol = "tcp", desc = "Kubelet API" },
      { from = 30000, to = 32767, protocol = "tcp", desc = "NodePort Services" },
      { from = 8472,  to = 8472,  protocol = "udp", desc = "Flannel VXLAN" }
    ]
    content {
      from_port   = ingress.value.from
      to_port     = ingress.value.to
      protocol    = ingress.value.protocol
      cidr_blocks = ["0.0.0.0/0"]
      description = ingress.value.desc
    }
  }

  # For Jenkins Master to accept JNLP agents
  ingress {
    from_port   = 50000
    to_port     = 50000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
    description = "Jenkins JNLP Agent Communication"
  }

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    self        = true
    description = "Internal Communication"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }
}



resource "aws_security_group" "worker_sg" {
  name        = "k8s-worker-sg"
  description = "SG for Kubernetes worker nodes"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = [
      { from = 22,    to = 22,    protocol = "tcp", desc = "SSH" },
      { from = 10250, to = 10250, protocol = "tcp", desc = "Kubelet API" },
      { from = 30000, to = 32767, protocol = "tcp", desc = "NodePort Services" },
      { from = 8472,  to = 8472,  protocol = "udp", desc = "Flannel VXLAN" }
    ]
    content {
      from_port   = ingress.value.from
      to_port     = ingress.value.to
      protocol    = ingress.value.protocol
      cidr_blocks = ["0.0.0.0/0"]
      description = ingress.value.desc
    }
  }

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    self        = true
    description = "Internal Communication"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }
}

#ingress {
#  from_port   = 22
#  to_port     = 22
#  protocol    = "tcp"
#  cidr_blocks = ["10.0.0.0/16"]
#  description = "SSH from Jenkins Master"
# }
