# Comprehensive Terraform Infrastructure Project
## Overview
This project aims to provide a comprehensive and scalable infrastructure using Terraform on AWS. The infrastructure is designed to support web application deployments, focusing on provisioning a VPC, configuring subnets, launching EC2 instances for Jenkins Master and Slave, setting up security groups.

## Project Structure
The project is organized into several modules to logically separate the infrastructure components, making them easier to manage and reuse. The overall project structure is as follows:
```JavaScript
. 
├── main.tf
├── outputs.tf
├── provider.tf
└── modules/
    ├── loadbalancer/
    │   ├── main.tf
    │   ├── outputs.tf
    │   └── variables.tf
    ├── network/
    │   ├── main.tf
    │   └── outputs.tf
    └── server/
        ├── main.tf
        ├── outputs.tf
        ├── sg.tf
        └── variables.tf
```
## Prerequisites
Before deploying this infrastructure, ensure you have the following tools installed and configured:
- `Terraform`  (version 1.0 or later)
- `AWS CLI`  (configured with necessary credentials and permissions to create AWS resources)



## What I Created
### S3 Backend Configuration
- Configured to store Terraform state in an S3 bucket
- Includes DynamoDB table for state locking to prevent concurrent modifications

### modules/network/
- Creates a VPC with specified CIDR block, enabling DNS support and hostnames
- Within this VPC, it provisions three public subnets across different availability zones (us-east-1a, us-east-1b, us-east-1c) to ensure high availability and fault tolerance.
- An Internet Gateway (IGW) is attached to the VPC to allow communication with the internet.
- Finally, a public route table is configured to direct traffic from the public subnets through the IGW, making the resources within these subnets accessible from the internet.

### modules/server/
- This module provisions the EC2 instances required for the application. It deploys three instances: one designated as a master and two as nodes
- These instances are distributed across the public subnets created by the `network` module.
- The module also defines and attaches security groups to these instances, acting as virtual firewalls to control inbound and outbound traffic. 
- These security groups are meticulously configured to allow only necessary access, such as SSH for management and specific ports for application communication.
- An SSH key pair is also generated and associated with the instances, enabling secure remote access.

### modules/loadbalancer/
- This module sets up an Application Load Balancer (ALB) to efficiently distribute incoming web traffic across the EC2 instances provisioned by the server module.
- The ALB is configured as an internet-facing load balancer, listening on port 80 for HTTP traffic
- It uses a target group to register the master EC2 instance, directing traffic to port 8080 on that instance.
- Health checks are configured to monitor the health of the registered targets, ensuring that traffic is only routed to healthy instances.
- This setup significantly enhances the availability and scalability of the application by distributing the workload and automatically rerouting traffic away from unhealthy instances.


## Steps
### 1. Created Terraform Modules
- Network Module
- Servers Module
- loadbalancer Module

### 2. Configured Terraform Backend (S3)
- To store Terraform state remotely and enable team collaboration:

### 3. Created an EC2 Key Pair
- To securely access Jenkins instances:
```bash
aws ec2 create-key-pair --key-name jenkins-key --query 'KeyMaterial' --output text > my-jenkins-key.pem
chmod 400 my-jenkins-key.pem 
```
---

### 4. Deploy

- terraform init
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/terraform-init.png)
---

- terraform plan
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/terraform-plan2.png)
---

- terraform apply -auto-approve
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/terraform-apply.png)
---

#### you can show the outputs 
- terraform outputs
 ![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/terraform-outputs.png)
---

### 5. Verified AWS Resources
- VPC and subnet were created.
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/subnets.png)
---

- EC2 instances were running.
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/list%20ec2.png)
---

- Ebs for the master instanse (20 G) like the other two ec2
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/Ebs%20for%20the%20master%20like%20the%20other%20two%20ec2.png)
---

- loadbalancer set up .
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/loadbalancers.png)
---

- dynamodb set up
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/lock%20by%20dynamodb.png)
---

- s3 bucket & the tfstate inside it 
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/s3-bucket.png)
---

![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/tfstate%20in%20s3-bucket.png)
---


### Finally you can ssh to the master ec2 with :
```bash
ssh -i my-jenkins-key.pem ubuntu@<jenkins_master_public_ip>
```

![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Terraform-infra/images/ssh%20to%20the%20master%20ec2.png)
---


