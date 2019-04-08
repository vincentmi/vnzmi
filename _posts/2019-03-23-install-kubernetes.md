---
layout:     post
title:      "搭建kubernetes集群(1)"
date:       2019-03-24 15:31:00
author:     "Vincent"
header-img:  "img/post-bg-engine.jpg"
catalog: true
tags:
    - kubernetes
    - k8s
    - kubeadm
---

# 1.准备

### 环境

- Ubuntu 16.04
-  Docker CE 18.09.3

### 安装Kubeadm,Kubelet,Kubectl

使用 ``` kubeadm config  images list``` 命令.列出当前版本中用到的镜像.

输入如下

```sh
k8s.gcr.io/kube-apiserver:v1.13.4
k8s.gcr.io/kube-controller-manager:v1.13.4
k8s.gcr.io/kube-scheduler:v1.13.4
k8s.gcr.io/kube-proxy:v1.13.4
k8s.gcr.io/pause:3.1
k8s.gcr.io/etcd:3.2.24
k8s.gcr.io/coredns:1.2.6
```




使用脚本拉取国内镜像

```sh
#!/bin/bash
images=(
kube-apiserver:v1.13.4
kube-controller-manager:v1.13.4
kube-scheduler:v1.13.4
kube-proxy:v1.13.4
pause:3.1
etcd:3.2.24
coredns:1.2.6
)
for imageName in ${images[@]} ; do
    docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/$imageName
    docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/$imageName k8s.gcr.io/$imageName
done
```

重新载入服务

```sh 
systemctl daemon-reload
systemctl restart kubelet
```

## 安装flannel插件

#### 安装 ETCD

配置网络:

```/coreos.com/network/config```
写入flannel的配置

UDP网络

```json
{
    "NetWork":"10.0.0.0/16", 
    "SubnetMin": "10.0.1.0", 
    "SubnetMax": "10.0.20.0"
}
```

vxlan网络

```json
{
    "NetWork":"10.0.0.0/16", 
    "Backend": {"Type": "vxlan"}
}
```

#### 建立FLannel服务

```sh
#/etc/systemd/system/flanneld.service
[Unit]
Description=Flanneld
Documentation=https://github.com/coreos/flannel
After=network.target
Before=docker.service

[Service]
User=root
ExecStart=/opt/flannel/flanneld \
--etcd-endpoints="http://192.168.1.201:2379,192.168.1.202:2379" \
--iface=192.168.2.210 \
--ip-masq
Restart=on-failure
Type=notify
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```
#### 启动flannel服务

```sh
systemctl start flanneld
```

#### 生成docker 启动参数

```sh
/opt/flannel/mk-docker-opts.sh -d /run/docker_opts.env -c
```

####  修改docker启动参数
```sh
# 编辑 systemd service 配置文件
$ vim /lib/systemd/system/docker.service
# 在启动时增加flannel提供的启动参数
ExecStart=/usr/bin/dockerd $DOCKER_OPTS
# 指定这些启动参数所在的文件位置(这个配置是新增的，同样放在Service标签下)
EnvironmentFile=/run/docker_opts.env
```

#### 删除旧的网络接口

```sh
ifconfig docker0 down
brctl delbr docker0
```

#### 重新启动docker

```sh
systemctl daemon-reload
systemctl restart docker
```

#### 拉取flannel镜像

```sh
sysctl net.bridge.bridge-nf-call-iptables=1 # 打开转发
docker pull quay.io/coreos/flannel:v0.10.1-amd64

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml

```


## 部署Dashboard

创建用户

```yaml
#dashboard-admin.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kube-system
  
#dashboard-bind.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
```

```sh
#创建
kubectl apply -f ./dashboard-admin.yaml
kubectl apply -f ./dashboard-bind.yaml
```

创建dashboard的development

```yaml
# ------------------- Dashboard Secrets ------------------- #

apiVersion: v1
kind: Secret
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-certs
  namespace: kube-system
type: Opaque

---

apiVersion: v1
kind: Secret
metadata:
"kubernetes-dashboard.yaml" 177L, 4823C                                                               18,1          Top
  selector:
    matchLabels:
      k8s-app: kubernetes-dashboard
  template:
    metadata:
      labels:
        k8s-app: kubernetes-dashboard
    spec:
      containers:
      - name: kubernetes-dashboard
        image: k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1
        ports:
        - containerPort: 8443
          protocol: TCP
        args:
          - --auto-generate-certificates
          # Uncomment the following line to manually specify Kubernetes API server Host
          # If not specified, Dashboard will attempt to auto discover the API server and connect
          # to it. Uncomment only if the default does not work.
          # - --apiserver-host=http://my-address:port
        volumeMounts:
        - name: kubernetes-dashboard-certs
          mountPath: /certs
          # Create on-disk volume to store exec logs
        - mountPath: /tmp
          name: tmp-volume
        livenessProbe:
          httpGet:
            scheme: HTTPS
            path: /
            port: 8443
          initialDelaySeconds: 30
          timeoutSeconds: 30
      volumes:
      - name: kubernetes-dashboard-certs
        secret:
          secretName: kubernetes-dashboard-certs
      - name: tmp-volume
        emptyDir: {}
      serviceAccountName: kubernetes-dashboard
      # Comment the following tolerations if Dashboard must not be deployed on master
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule

---
# ------------------- Dashboard Service ------------------- #

kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
spec:
  type: NodePort
  ports:
    - port: 443
      targetPort: 8443
      nodePort: 30001
  selector:
    k8s-app: kubernetes-dashboard
```

```sh
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')
```

##问题

#### 查看日志

```sh
#查看服务日志
journalctl -f -u kubelet

# 查看节点
kubectl describe node k8s1
```

#### - certificate 错误

 ```Unable to connect to the server: x509: certificate signed by unknown authority (possibly because of "crypto/rsa: verification error" while trying to verify candidate authority certificate "kubernetes")```

INIT 之后执行 

```sh
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

####  - 网络错误 

```failed to set bridge addr: "cni0" already has an IP address different from 10.244.4.1/24```
重置后重新加入集群

```sh 
#在master节点之外的节点进行操作
kubeadm reset
systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/cni/
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig docker0 down
ip link delete cni0
ip link delete flannel.1
##重启kubelet
systemctl restart kubelet
##重启docker
systemctl restart docker
```

#### Token过期

Join Token的有效期是24小时,如果TOKEN过期用 ```kubeadm token create``` 创建.


### Proxy 

```sh
kubectl proxy --address='172.20.0.113' --port=8086 --accept-hosts='^*$'
```
