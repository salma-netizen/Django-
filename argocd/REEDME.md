# 🚀 ArgoCD Setup & Application Deployment

This guide helps you set up ArgoCD and configure it to sync and deploy your application automatically to your Kubernetes cluster.

## 📌 Prerequisites

- A running Kubernetes cluster (kubeadm on AWS cloud ).
- kubectl configured to access your cluster.
- helm (optional, for Helm-based apps).
- A Git repository containing your Kubernetes manifests or Helm charts.

## ⚙️ Setup Steps 

### ⚙️ Step 1: Install ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
you will see:
![setup success](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/success%20setup%20argocd%20on%20cluster.png)
---

### step2: convert argocd-server service to nodeport service 
```bash
kubectl patch svc  -n argocd -p '{"spec": {"type": "NodePort"}}'
```
![service for argocd](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/nodeport%20srevice%20for%20argocd.png)
---

### step3: Access argocd server 
To get the initial password:
```bash
kubectl get secret -n argocd
kubectl get secret argocd-initial-admin-secret -n argocd
kubectl get secret argocd-initial-admin-secret -n argocd -o yaml
echo -n "a29iSjlhR21tRWswbHBwMA==" | base64 -d
```
![initial password](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/to%20get%20the%20initial%20password%20of%20argocd.png)
---

then on the Browser :
```bash
http://<node-ip>:<nodeport>
```
![image](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/access%20argocd.png)
---


## ✅ Steps for creating cd-deployment 

### 🔹step1: Prepare Kubernetes Manifests Repository
- Add required manifest files like this [](https://github.com/Mohamedmagdy220/-CloudDevOpsProject.git)

### 🔹step2: Create New Application
1. Click "+ New App" button in top navigation
2. Configure application settings:

General Section:
   1. Application Name: WEB-APP-DEMO
   2. Project: default
   3. Sync Policy:
      ✓ Automatic sync
      ✓ Self-Heal

Source Section:
   1. Repository URL: [](https://github.com/Mohamedmagdy220/-CloudDevOpsProject.git)
   2. Revision: main
   3. Path: ./k8s/ (root directory of repo)

Destination Section:
   1. Cluster: in-cluster
   3. Namespace: ivolve

![new app](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/creating%20app.png)
---

after create the app you will see:
![]()
---

then you can refresh your app and after success you will see:
![image](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/app%20in%20argocd.png)
---

### 🔹Step3: Test Pipeline-Driven Deployment Flow
#### 1. Manually Trigger Pipeline

In Jenkins UI:
   - Navigate to your Jenkins-CI-Workflow job
   - Click Build Now
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/in%20jenkins.png)
#### 2. Verify Automated Manifest Update

Check Git commit (within 1 minute of pipeline completion):
![github](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/after%20run%20jenkins.png)
---

#### 3. Observe ArgoCD Response (Within 2 Minutes)

1.In ArgoCD UI:
   - Application status will transition:
   ```bash
    Synced → OutOfSync → Syncing → Synced
   ```
   - Health status may briefly show Progressing during rollout

![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/sunc%20again.png)
---

### 🔹Step4: list all resourses in your namespace to see the resourses created:
![list reasourses](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/get%20all%20resourses%20in%20namespace%20ivolve.png)
---

### 🔹Final step: Access Your application 
on your Browser:
```bash
http://<node-ip>:<nodepore>
```
you will see:
![image](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/argocd/images/access%20app%20with%20nodeport.png)
---

 







