#  📦 Container Orchestration with Kubernetes
## 🧠 Objective

Setup a production-ready Kubernetes environment for deploying and managing the django-web-app application.

## ✅ Overview
- 🚀 Setup Kubernetes cluster
- 🧱 Create `iVolve` namespace
- ⚙️ Configure `Deployments` and `Services` and `volumes` for the application


## 🔧 Prerequisites
- 3 EC2 installed on aws (1 > master , 2 > worker nodes)
- Basic understanding of YAML, pods, deployments, and services

## 📁 Project Structure
```cpp
.
├── k8s/
│   ├── db-pv.yaml
│   ├── db-pvc.yaml
│   ├── db-statefulset.yaml
│   ├── db-service.yaml
│   ├── configmab.yaml
│   ├── storadeclass.yaml
│   ├── app-pv.yaml
│   ├── app-deployment.yaml
│   ├── app-service.yaml
│   └── app.pvc.yaml
└── README.md
```
## Kubernetes 1.30 Cluster Setup on Ubuntu 24.04 LTS
### Step-by-Step Installation
#### Step 1: Disable Swap on All Nodes
```bash
swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```


#### Step 2: Enable IPv4 Packet Forwarding
##### sysctl params required by setup, params persist across reboots

```bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.ipv4.ip_forward = 1
EOF
```
##### Apply sysctl params without reboot
```bash
sudo sysctl --system
```

#### Step 3: Verify IPv4 Packet Forwarding
```bash
sysctl net.ipv4.ip_forward
```

#### Step 4: Install containerd
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update && sudo apt-get install containerd.io && systemctl enable --now containerd
```

#### Step 5: Install CNI Plugin
```bash
wget https://github.com/containernetworking/plugins/releases/download/v1.4.0/cni-plugins-linux-amd64-v1.4.0.tgz
mkdir -p /opt/cni/bin
tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.4.0.tgz
```
#### Step 6: Forward IPv4 and Configure iptables
```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system
sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward
modprobe br_netfilter
sysctl -p /etc/sysctl.conf
```


#### Step 7: Modify containerd Configuration for systemd Support
```bash
sudo cat > /etc/containerd/config.toml
```
##### Paste the configuration in the file and save it.
```
disabled_plugins = []
imports = []
oom_score = 0
plugin_dir = ""
required_plugins = []
root = "/var/lib/containerd"
state = "/run/containerd"
version = 2

[cgroup]
  path = ""

[debug]
  address = ""
  format = ""
  gid = 0
  level = ""
  uid = 0

[grpc]
  address = "/run/containerd/containerd.sock"
  gid = 0
  max_recv_message_size = 16777216
  max_send_message_size = 16777216
  tcp_address = ""
  tcp_tls_cert = ""
  tcp_tls_key = ""
  uid = 0

[metrics]
  address = ""
  grpc_histogram = false

[plugins]

  [plugins."io.containerd.gc.v1.scheduler"]
    deletion_threshold = 0
    mutation_threshold = 100
    pause_threshold = 0.02
    schedule_delay = "0s"
    startup_delay = "100ms"

  [plugins."io.containerd.grpc.v1.cri"]
    disable_apparmor = false
    disable_cgroup = false
    disable_hugetlb_controller = true
    disable_proc_mount = false
    disable_tcp_service = true
    enable_selinux = false
    enable_tls_streaming = false
    ignore_image_defined_volumes = false
    max_concurrent_downloads = 3
    max_container_log_line_size = 16384
    netns_mounts_under_state_dir = false
    restrict_oom_score_adj = false
    sandbox_image = "k8s.gcr.io/pause:3.5"
    selinux_category_range = 1024
    stats_collect_period = 10
    stream_idle_timeout = "4h0m0s"
    stream_server_address = "127.0.0.1"
    stream_server_port = "0"
    systemd_cgroup = false
    tolerate_missing_hugetlb_controller = true
    unset_seccomp_profile = ""

    [plugins."io.containerd.grpc.v1.cri".cni]
      bin_dir = "/opt/cni/bin"
      conf_dir = "/etc/cni/net.d"
      conf_template = ""
      max_conf_num = 1

    [plugins."io.containerd.grpc.v1.cri".containerd]
      default_runtime_name = "runc"
      disable_snapshot_annotations = true
      discard_unpacked_layers = false
      no_pivot = false
      snapshotter = "overlayfs"

      [plugins."io.containerd.grpc.v1.cri".containerd.default_runtime]
        base_runtime_spec = ""
        container_annotations = []
        pod_annotations = []
        privileged_without_host_devices = false
        runtime_engine = ""
        runtime_root = ""
        runtime_type = ""

        [plugins."io.containerd.grpc.v1.cri".containerd.default_runtime.options]

      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]

        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          base_runtime_spec = ""
          container_annotations = []
          pod_annotations = []
          privileged_without_host_devices = false
          runtime_engine = ""
          runtime_root = ""
          runtime_type = "io.containerd.runc.v2"

          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            BinaryName = ""
            CriuImagePath = ""
            CriuPath = ""
            CriuWorkPath = ""
            IoGid = 0
            IoUid = 0
            NoNewKeyring = false
            NoPivotRoot = false
            Root = ""
            ShimCgroup = ""
            SystemdCgroup = true

      [plugins."io.containerd.grpc.v1.cri".containerd.untrusted_workload_runtime]
        base_runtime_spec = ""
        container_annotations = []
        pod_annotations = []
        privileged_without_host_devices = false
        runtime_engine = ""
        runtime_root = ""
        runtime_type = ""

        [plugins."io.containerd.grpc.v1.cri".containerd.untrusted_workload_runtime.options]

    [plugins."io.containerd.grpc.v1.cri".image_decryption]
      key_model = "node"

    [plugins."io.containerd.grpc.v1.cri".registry]
      config_path = ""

      [plugins."io.containerd.grpc.v1.cri".registry.auths]

      [plugins."io.containerd.grpc.v1.cri".registry.configs]

      [plugins."io.containerd.grpc.v1.cri".registry.headers]

      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]

    [plugins."io.containerd.grpc.v1.cri".x509_key_pair_streaming]
      tls_cert_file = ""
      tls_key_file = ""

  [plugins."io.containerd.internal.v1.opt"]
    path = "/opt/containerd"

  [plugins."io.containerd.internal.v1.restart"]
    interval = "10s"

  [plugins."io.containerd.metadata.v1.bolt"]
    content_sharing_policy = "shared"

  [plugins."io.containerd.monitor.v1.cgroups"]
    no_prometheus = false

  [plugins."io.containerd.runtime.v1.linux"]
    no_shim = false
    runtime = "runc"
    runtime_root = ""
    shim = "containerd-shim"
    shim_debug = false

  [plugins."io.containerd.runtime.v2.task"]
    platforms = ["linux/amd64"]

  [plugins."io.containerd.service.v1.diff-service"]
    default = ["walking"]

  [plugins."io.containerd.snapshotter.v1.aufs"]
    root_path = ""

  [plugins."io.containerd.snapshotter.v1.btrfs"]
    root_path = ""

  [plugins."io.containerd.snapshotter.v1.devmapper"]
    async_remove = false
    base_image_size = ""
    pool_name = ""
    root_path = ""

  [plugins."io.containerd.snapshotter.v1.native"]
    root_path = ""

  [plugins."io.containerd.snapshotter.v1.overlayfs"]
    root_path = ""

  [plugins."io.containerd.snapshotter.v1.zfs"]
    root_path = ""

[proxy_plugins]

[stream_processors]

  [stream_processors."io.containerd.ocicrypt.decoder.v1.tar"]
    accepts = ["application/vnd.oci.image.layer.v1.tar+encrypted"]
    args = ["--decryption-keys-path", "/etc/containerd/ocicrypt/keys"]
    env = ["OCICRYPT_KEYPROVIDER_CONFIG=/etc/containerd/ocicrypt/ocicrypt_keyprovider.conf"]
    path = "ctd-decoder"
    returns = "application/vnd.oci.image.layer.v1.tar"

  [stream_processors."io.containerd.ocicrypt.decoder.v1.tar.gzip"]
    accepts = ["application/vnd.oci.image.layer.v1.tar+gzip+encrypted"]
    args = ["--decryption-keys-path", "/etc/containerd/ocicrypt/keys"]
    env = ["OCICRYPT_KEYPROVIDER_CONFIG=/etc/containerd/ocicrypt/ocicrypt_keyprovider.conf"]
    path = "ctd-decoder"
    returns = "application/vnd.oci.image.layer.v1.tar+gzip"

[timeouts]
  "io.containerd.timeout.shim.cleanup" = "5s"
  "io.containerd.timeout.shim.load" = "5s"
  "io.containerd.timeout.shim.shutdown" = "3s"
  "io.containerd.timeout.task.state" = "2s"

[ttrpc]
  address = ""
  gid = 0
  uid = 0
```

#### Step 8: Restart containerd and Check the Status

```bash
sudo systemctl restart containerd && systemctl status containerd
```
#### Step 9: Install kubeadm, kubelet, and kubectl

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update -y
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

#### Step 10: Initialize the Cluster and Install CNI In the master node
```bash
sudo kubeadm config images pull
sudo kubeadm init
```

##### apply the CNI yaml in Master node  
- here you can apply any cni plugin you nead (falnnel , weave , calico) i used in this repo `weave` :
```bash
#Apply the CNI YAML
kubectl apply -f https://reweave.azurewebsites.net/k8s/v1.30/net.yaml
```

#### Final step: Join Worker Nodes to the Cluster
- Run the command generated after initializing the master node on each worker node. For example:
```bash
kubeadm join 192.168.122.100:6443 --token zcijug.ye3vrct74itrkesp \
        --discovery-token-ca-cert-hash sha256:e9dd1a0638a5a1aa1850c16f4c9eeaa2e58d03f97fd0403f587c69502570c9cd
```

## test the cluster
- run this command on tha master node :
```bash
kubectl get pods -n kube-system
```
- you will see:
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/k8s/images/setup%20k8s%20success.png)

- run this command to list nodes :
```bash
kubectl get nodes
```
if all nodes are ready 🎉 You're Done with the installtion!
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/k8s/images/get%20nodes.png)
---




## steps for the deployment app:
### 1️⃣ Step: Create Namespace
```yml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ivolve
```

```bash
kubectl apply -f k8s/namespace.yaml
```
> you can see your namespaces :
```bash
kubectl get ns
```

![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/k8s/images/namespace.png)

### 2️⃣ Step: create yml files for db :
1. `db-pv.yml`  >>> for creating presestant volume for database
2. `db-pvc.yml` >>> for creating presestant volume claim for database (optional) you can let statefulset craete it
3. `db-statefulset.yml`  >>> for creating 2 replica of datatbase pod in the worker node `node2=database`
4. `db-service.yml`  >>> for creating a cluster ip service for the database pod with name `db` for dns resolution
5. `configmab.yml` and `secret.yml`  >>> for the environment variables which you pass them to the app and db
6. `storageclass.yml`   >>> for pv and pvc
7. `app-pv.yml` and `app-pvc.yml`  >>> (optional) for storing data from app
8. `app-deployment.yml`  >>> for creating 2 replica of app pod in the worker1 `node1=database`

you can see the content of these files in this repo. 

after you create them you should apply these files by order :
```bash
kubectl apply -f db-pv.yml
kubectl apply -f db-pvc.yml
kubectl apply -f db-statefulset.yml
kubectl apply -f db-service.yml
kubectl apply -f configmab.yml
kubectl apply -f storageclass.yml
kubectl apply -f app-pv.yml
kubectl apply -f app-pvc.yml
kubectl apply -f app-deployment.yml
```

## 🧪 Verification

After success created you can see the resourses with these commands :
```bash
kubectl get all -n ivolve
```
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/k8s/images/get%20all%20resourses%20in%20namespace%20ivolve.png)
---

- you can see the service of app is nodeport you can use ingress instead of this but in this repo i used nodeport:
- you can access the app using :
```bash
http://<nodeip>:<nodeport>
```
![](https://github.com/Mohamedmagdy220/-CloudDevOpsProject/blob/main/k8s/images/access%20app%20with%20node%20port.png)
---






