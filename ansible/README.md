# Configuration Management with Ansible

## 📦 Overview

This playbook automates the process of installing **Jenkins**, **Java 17**, **Docker**, and other dependencies across **Master Node** and **Slave Nodes**. The setup uses **Ansible** to ensure consistency and automate the deployment across multiple EC2 instances on AWS.

### Features
- [x] **Install Java 17** on all nodes.
- [x] **Install Jenkins** on the **Master Node**.
- [x] **Install Docker, Git, Maven** on all nodes.
- [x] Ensures Jenkins service is started and enabled on the **Master Node**.

---
## 🧱 Project Structure
```yml
├── ansible/
│   ├── inventory/
│   │   └── aws_ec2.yml          # EC2 instance inventory configuration file
│   ├── playbook.yml             # Main playbook to run tasks
│   ├── roles/                   # Folder containing Ansible roles
│   │   ├── install_git/         # Role to install Git
│   │   ├── install_docker/      # Role to install Docker
│   │   ├── install_java/        # Role to install Java 17
│   │   ├── install_jenkins/     # Role to install Jenkins
│   │   └── install_maven/       # Role to install Maven
│   ├── ansible.cfg              # Ansible configuration file
│   └── README.md                # Project documentation (this file)
```

### Roles
- The playbook is divided into roles. Each role is responsible for installing and configuring a specific software. Here’s what each role does:

1- ``install_git``: Installs Git on the target nodes.
2- ``install_docker``: Installs Docker and its dependencies.
3- ``install_java``: Installs Java 17 on the target nodes.
4- ``install_maven``: Installs Maven on the target nodes.
5- ``install_jenkins``: Installs Jenkins on the Master Node.


## ✅ Prerequisites

### 1. **Ansible**
   - Ensure **Ansible** is installed on the control node (your local machine or server).
     ```bash
     sudo apt update
     sudo apt install ansible
     ```

### 2. **AWS EC2 Instances**
   - **Master Node** and **Slave Nodes** should be launched and running on AWS EC2.
   - Ensure that the EC2 instances are accessible via SSH, and you have the private key (`.pem` file) for authentication.

### 3. **AWS Credentials**
   - make sure that you have a file ine directory like this `.aws/credentials`:
     ```bash
     mkdir .aws/
     nano credentials
     ```
     you must add `access_key` and `secret_access_key` in it like this :
     ```bash
     [default]
      aws_access_key_id = YOUR_ACCESS_KEY
      aws_secret_access_key = YOUR_SECRET_KEY
      aws_session_token = YOUR_SESSION_TOKEN if you have
     ```
     
### 3. **Inventory File**
   - Create an inventory file (`aws_ec2.yml`) that lists all the EC2 instances. An example for the inventory is shown below:

```yaml
plugin: aws_ec2

regions:
  - us-east-1

filters:
  instance-state-name: running
  "tag:Name":
    - "k8s-master"
    - "k8s-node-1"
    - "k8s-node-2"

hostnames:
  - tag:Name
  - private-ip-address


## variables of connection
compose:
  ansible_host: public_ip_address | default(private_ip_address)
  ansible_user: ubuntu
  availability_zone: placement.availability_zone
  instance_name: tags.Name


groups:
  # Master node (in us-east-1a)
   master: tags.Name == "k8s-master"
#  master: placement.availability_zone == "us-east-1a"


# Worker nodes (in us-east-1b and us-east-1c)
   workers: tags.Name in ["k8s-node-1", "k8s-node-2"]
#  workers: placement.availability_zone in ["us-east-1b", "us-east-1c"]

```

 - This configuration filters instances by their state (running) and tags (k8s-master for the master node and k8s-node* for the slave nodes).
 - you can use more filters like AZ or anything else .

### 4. **Ansible Configuration (ansible.cfg)**
  Ensure you have an Ansible configuration file ``(ansible.cfg)``:
```yml
[defaults]
inventory = inventory/aws_ec2.yml
private_key_file = ~/.ssh/my-jenkins-key.pem
remote_user = ubuntu
host_key_checking = False
interpreter_python = auto_silent

[ssh_connection]
ssh_args = -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
pipelining = True
```

## STEPS
### 🔹 Steps to Write Roles

#### 1- Create Role Directory
Each role should be placed in the roles directory. For example, to create roles for **installing Git** **installing docker** **installing java** **installing maven** **installing jenkins** , run the following command:
```bach
mkdir -p ansible/roles
ansible-galaxy init install_git
ansible-galaxy init install_docker
ansible-galaxy init install_java
ansible-galaxy init install_maven
ansible-galaxy init install_jenkins
```

Each role can have the following structure:

- tasks/: Contains the main tasks.

- handlers/: Contains tasks triggered by other tasks (e.g., restarting a service).

- defaults/: Contains default variables for the role.

#### 2- under `install_git` >> `tasks` >> `main.yml` 
```yml
---
- name: Install Git
  apt:
    name: git
    state: present
```

#### 3- under `install_docker` >> `tasks` >> `main.yml` 
```yml
---
# tasks/main.yml

- name: Install dependencies for Docker
  apt:
    name:
      - apt-transport-https
      - ca-certificates
      - curl
      - software-properties-common
    state: present
    update_cache: yes

- name: Update apt repository cache
  apt:
    update_cache: yes

- name: Install Docker
  apt:
    name: docker-ce
    state: present

- name: Ensure Docker service is running
  service:
    name: docker
    state: started
    enabled: yes
```

#### 4- under `install_java` >> `tasks` >> `main.yml` 
```yml
---
- name: Install Java
  apt:
    name: openjdk-17-jdk
    state: present
```

#### 5- under `install_maven` >> `tasks` >> `main.yml` 
```yml
---
- name: Install Maven
  apt:
    name: maven
    state: present
```

#### 6- under `install_jenkins` >> `tasks` >> `main.yml` 
```yml
---
- name: Update apt cache
  apt:
        update_cache: yes
        cache_valid_time: 3600

- name: Install Java 11
  apt:
        name: openjdk-11-jdk
        state: present

- name: Add Jenkins GPG key
  apt_key:
        url: https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
        state: present

- name: Add Jenkins repository
  apt_repository:
        repo: "deb https://pkg.jenkins.io/debian-stable binary/"
        state: present
        update_cache: yes

- name: Install Jenkins
  apt:
        name: jenkins
        state: present

- name: Start and enable Jenkins service
  systemd:
        name: jenkins
        state: started
        enabled: yes

- name: Wait for Jenkins to start
  wait_for:
        port: 8080
        host: localhost
        delay: 30
        timeout: 300

- name: Get Jenkins initial admin password
  command: cat /var/lib/jenkins/secrets/initialAdminPassword
  register: jenkins_password
  changed_when: false

- name: Display Jenkins initial password
  debug:
        msg: "Jenkins initial admin password: {{ jenkins_password.stdout }}"
```


### 🔹 Steps to Write Playbook
#### - Create a Playbook File
In the `ansible/` directory, create the playbook file `(playbook.yml)`.

#### - Define Hosts and Roles in the Playbook
Define the roles to be executed for Slave Nodes and Master Node in the playbook.
```bash
nano ansible/playbook.yml:
```
```yml
---
- name: Install required packages on Slave Nodes
  hosts: all  # All nodes
  become: true
  roles:
    - install_git
    - install_docker
    - install_java
    - install_maven

- name: Install required packages on Master Node
  hosts: master  # Only Master Node
  become: true
  roles:
    - install_jenkins
```

### 🔹 Running the Playbook
To run the playbook, use the following command:
```bash
ansible-playbook -i inventory/aws_ec2.yml ansible/playbook.yml
```
This command will:

 - Install Java 17, Git, Docker, Maven on all nodes.
 - Install Jenkins on the Master Node and start the Jenkins service.

you can see like this :

![run playbook](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/ansible/images/run%20playbook.png)

### Additional testing 
you can run these commands in the master and slaves:
```bash
git --version
java --version
maven --version
systemctl status docker
systemctl status jenkins
```
you shoud see like this :
![test](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/ansible/images/test%20.png)
---

after success you can see this :
![test jenkins](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/ansible/images/test%20jenkins%20.png)
---
you can access jenkins by :
```bash
http://<your-server-ip>:8080
```
it will require initial password you can get it from this file :
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
![unlock jenkins](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/ansible/images/unlock%20jenkins.png)
---

after you unlock it you can see :
![jenkins](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/ansible/images/jenkins%20success.png)
---

🎉 **You're Done!**


## 👤 Author

Mohamed Magdy  
DevOps & Cloud Enthusiast
