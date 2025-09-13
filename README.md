# iVolve CI/CD Infrastructure

A comprehensive end-to-end CI/CD infrastructure for containerized applications, featuring AWS provisioning, automated configuration management, continuous integration, and GitOps-based deployment to Kubernetes.

---
## Project Archticture
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/flow3.png)


## 🚀 Architecture Overview
This infrastructure includes the following major components:

### 1. AWS Infrastructure (Provisioned via Terraform)
- **EC2 Instance 1 (Master)**
  - Hosts Kubernetes Master
  - Hosts Jenkins Master to manage the CI pipeline.
  - Configured using Ansible playbooks.
- **EC2 Instance 2 (node1)**
  - it's a worker node in k8s cluster
  - hosts app pods in the cluster
  - Executes build jobs as a Jenkins Agent.
  - Handles resource-intensive tasks.
  - Configured via Ansible.
- **EC2 Instance 3 (node2)**  
  - it's a worker node in k8s cluster
  - hosts database pods in the cluster
  - Configured via Ansible.  
- **Supporting Services**
  - S3 Bucket: Stores Terraform backend state.
  - loadbalancer: to efficiently distribute incoming web traffic across the EC2 instances provisioned by the server module.
---
### 2. Development Environment (kubeadm)
- Kubernetes cluster built using `kubeadm`.
- Custom `iVolve` namespace.
- Manages Deployments, Services, and Ingress resources.
---
### 3. ArgoCD Implementation (GitOps)
- **Core Components**
  - Application Controller
  - Repository Server
  - API Server
  - GitOps Engine
- **Workflow**
  - Monitors GitHub repo for manifest changes.
  - Syncs desired configuration to Kubernetes cluster.
---
### 4. CI/CD Pipeline Flow
1. Developer pushes code to GitHub.
2. Jenkins Master triggers build and delegates to Slave.
3. Jenkins Pipeline steps:
   - Build Docker image
   - scan docker image
   - Push image to container registry
   - delete image locally
   - Update Kubernetes manifests
   - Commit changes to Git
4. ArgoCD detects manifest updates and syncs to cluster.
5. Application is deployed/updated automatically.


---

## 📋 Prerequisites
- AWS Account (with permissions)
- Docker
- Kubernetes Cluster (EKS or kubeadm on aws)
- Git
- Basic knowledge of:
  - Terraform
  - Ansible
  - Jenkins
  - Kubernetes

---


## 🛠️ Project Components

### Terraform
- Infrastructure as Code for AWS:
  - VPCs, subnets
  - EC2 instances (Jenkins Master/Slave)
  - Security groups
  - loadbalancer


### Ansible
- Configures:
  - Jenkins Master/Slave setup
  - install git, docker, java and maven.
  - Dependencies & services


### Jenkins
- Contains:
  - `Jenkinsfile`: Defines CI/CD pipeline
  - Shared libraries for reusable steps

### Docker
- Application containerization:
  - Dockerfile
  - docker-compose.yml
  - Optimized for Spring Boot apps

### K8s
- Manifests for deployment:
  - Namespace setup
  - Deployment, Service
  - Persistent storage config
  - statefulset 
  - 

### ArgoCD
- GitOps engine:
  - Sync policies
  - Repository integration
  - Application definitions

---

## 🗂️ Project Structure
```
├── Ansible/               # Ansible playbooks and roles
├── ArgoCD/                # ArgoCD configuration files
├── docker/                # Dockerfile and application source
├── Jenkins/               # Jenkinsfile and pipeline configs
├── k8s/                   # Kubernetes manifest files
├── terraform-infra/       # Terraform IaC configurations
└── README.md              # Project documentation
```

---

> For further details on individual components, refer to each respective directory's README or documentation.

---



**Author:** Mohamed Magdy 
**Project:** CloudDevOpsProject  
**License:** MIT
