
# test: Django-Web Application Dockerization on EC2
## 📦 Overview
This project demonstrates how to containerize a Flask application using Docker and deploy it on an AWS EC2 instance. The goal is to set up a Flask app, build a Docker image, and run the application inside a container.


## ✅ Prerequisites
1. [x] Docker: Installed and configured
2. [x] AWS EC2: An active EC2 instance running.
3. [x] Git: Installed.

you can git this from the folder of ansible.

## 🔹 Getting Started

### 1. Clone the Repository:
you can clone it to your EC2 instance using
```bash
git clone https://github.com/Mohamedmagdy220/Django-app.git
```

### 2. Navigate to the Project Directory:
```bash
cd blog
```
### 3. Create Dockerfile:
```Dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    libwebp-dev \
    libtiff-dev \
    libopenjp2-7-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

```

### 4. Building Docker Image
```bash
docker build -t blog-web-app .
```

This command will build the image with the name `blog-web-app`.

![build image](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/docker/images/docker%20images%20.png)
---

### 5. Create docker-compose.yml:
```bash

version: '3'
services:
  db:
    image: postgres
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  web_app:
    build: .
    command: >
      sh -c "./wait-for-postgres.sh &&
      python manage.py migrate &&
      python manage.py makemigrations &&
      python manage.py createsuperuser --noinput &&
      python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    environment:
      - DB_NAME=postgres
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_HOST=db
      - DJANGO_SUPERUSER_USERNAME=admin
      - DJANGO_SUPERUSER_EMAIL=admin@gmail.com
      - DJANGO_SUPERUSER_PASSWORD=123
    depends_on:
      - db


volumes:
  db_data: {}

```

### 5. Running the Application & database container
```bash
docker-compuse --build
```
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/docker/images/docker-compose%20--build.png)
---
This binds port 5000 inside the container to port 5000 on your EC2 instance, allowing you to access the application from the browser.
you can list your containers :

```bash
sudo docker container ls -a
```
![build image](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/docker/images/docker%20containers.png)
---

### final-step: Accessing the Application

To access the application from a browser, open the browser and enter the Public IP of your EC2 instance followed by the port `5000`:

```bash
http://<Public-IP>:5000
```
![access app](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/docker/images/test%20django%20container.png)
---


### 6.Additional step :Security Group Configuration

To allow external access to port 5000, you'll need to open the port in the EC2 security group.

1. Go to EC2 dashboard in the AWS console.
2. Select Security Groups from the sidebar.
3. Choose the Security Group associated with your EC2 instance.
4. Under the Inbound Rules tab, click Edit inbound rules.
5. Add a rule for Custom TCP Rule:
   - Port range: `5000`
   - Source: `0.0.0.0/0` (this allows access from any IP. You can limit this to specific IP ranges for security).
   - Click Save rules.



## Conclusion
By following the steps above, you have successfully containerized a django-web application using Docker and deployed it on an AWS EC2 instance. You can access the app via the EC2's public IP and port 5000.


🎉 **You're Done!**


## 👤 Author

Mohamed Magdy
DevOps & Cloud Enthusiast


