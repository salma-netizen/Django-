# 🚀 Jenkins CI Pipeline using Shared Library on AWS EC2

This repository documents a Jenkins CI pipeline designed for Docker image lifecycle automation: build, scan, push to registry, update manifests, and GitHub commits. It uses a shared library for modular and reusable Groovy functions.
---



## 📌 Project Goal

Set up a secure and scalable Jenkins CI server on AWS to:

- Automate build pipelines.
- Trigger jobs from GitHub pushes.
- Run pipelines.
- 
---


## 🔧 Prerequisites

Make sure you have the following ready:

- ✅ AWS EC2 instance (Ubuntu 20.04 or newer).
- ✅ Public and private key pair (for SSH access).
- ✅ Inbound rules open for port `8080` (Jenkins).
- ✅ Jenkins master & agent are configured and connected.
- ✅ Docker and `kubectl` are installed on the Jenkins agent.
- ✅ GitHub repo is set with a valid `Jenkinsfile`.
- ✅ Credentials configured in Jenkins (see below).
- ✅ Shared library configured in **Manage Jenkins > Global Pipeline Libraries**.

---

## ⚙️ Jenkins Slave Configuration

> Make sure Jenkins Agent has:
- Access to Docker daemon (for building images).
- `kubectl` configured to communicate with your cluster.
- Proper SSH or Git credentials to clone your repo.

> Follow these steps to configure the Jenkins slave:
- Log in to the Jenkins master web interface
- Navigate to Manage Jenkins > Manage Nodes and Clouds
- Click New Node to create a new agent
- Enter "agent" as the node name and select Permanent Agent
- Configure the node with these settings:
    - Remote root directory: /home/ubuntu
    - Labels: Agent-node
    - Usage: Use this node as much as possible
    - Launch method: Launch agent via SSH
- Enter the Private IP address of Jenkins slave instance
- Add SSH credentials for the ubuntu user with the private key `my-jenkins-key.pem`
- Set Host Key Verification Strategy to Non verifying Verification Strategy
- Click Save to create the node
- Verify the slave connection appears online in the Nodes list like this:

![agent-node](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/agent-node.png)
---

## 🔐 Credentials Configuration

> Set up the required credentials in Jenkins:
- Docker Hub credentials:
     - Navigate to Manage Jenkins > Manage Credentials
     - Add new credentials with type Username with password
     - Enter your Docker Hub username and password
     - Set ID to "dockerhub-credentials"

- Git Hub credentials:
    - In the same credentials section
    - Add new credentials with type Username with password
    - Enter your Docker Hub username 
    - Enter your Docker access-token
    - Set ID to "github-credentials"
    
- Agent SSH credentials:
    - In the same credentials section
    - dd new credentials with type SSH Username with private key
    - Enter "ubunto" as username 
    - Paste your SSH private key
    - Set ID to "Agent-credentials"

![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/credentials.png)
---

## 📚 Shared Library Setup

1. Create a separate GitHub repository for the shared library (e.g. `project-shared-library`).
   - Clone the repository to local machine
   - Create the following directory structure in the repository
         . vars/ for global pipeline variables
   - Add the Groovy scripts for Docker operations and Git operations
   - Structure example:
        ```bash
        shared-libraries/
            └── vars/
                 └── buildImage.groovy
                 └── scanImage.groovy
                 └── pushImage.groovy
                 └── deleteImageLocally.groovy
                 └── updateManifests.groovy
                 └── pushManifests.groovy
        ```
   - Commit and push the initial implementation to the repository
   - In Jenkins:
         - Go to **Manage Jenkins > Configure System**
         - Scroll to **Global Pipeline Libraries**
         - Add a new library:
            - Name: `shared-Library`
            - Default version: `main`
            - Source: GitHub URL
            - Credentials: if private
         - Click Save to apply the configuration

   ![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/library.png)
   ---
   
## Pipeline Job Creation
> Create and configure the main pipeline job:
- From Jenkins dashboard, click New Item
-  Enter "Jenkins-CI-Workflow" as name
- Select Pipeline type and click OK
- In the configuration page:
    - Under Pipeline section, select Pipeline script from SCM
    - Choose Git as SCM
    - Enter application repository URL
    - Add Github credentials
    - Specify branch (main)
    - Set Script Path to jenkins/jenkinsfile
- Click Save to create the pipeline
you must see that :

![image](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/after%20create%20pipeline.png)
---


## Kubernetes Manifests Preparation
> Prepare your Kubernetes manifests repository with a clear structure :
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/kubernetes%20files.png)
---

> make sure that you Modified app-deployment.yaml to use image placeholder like this :
   - Set image field to use Docker image name with ex :latest <tag>
   - This will be updated by the pipeline

## 📌 Verification Steps &  Result:
### 1. After first Build success:
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/first%20build.png)
---
> you can check everything:       
1- Docker Image in docker hub:

![first image](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/first%20pipeline.png)
---

2- kubernetes manifests :
   - Check the Git repository commit history
   - Verify deployment.yaml was updated with new image tag

![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/image%20with%20tag%201.png)
---
   

### 2. After second Build success :
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/second%20build.png)
---
> you can check everything:
1- Docker Image in docker hub:

![second image](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/second%20pipeline.png)
---

2- kubernetes manifests :
   - Check the Git repository commit history
   - Verify deployment.yaml was updated with new image tag

![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/Jenkins/images/image%20with%20tag%202.png)
---


