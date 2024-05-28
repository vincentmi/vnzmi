---
layout:     post
title:      "使用Kind搭建K8S学习环境"
date:       "2022-05-27 10:46:00"
author:     "Vincent"
image:  "img/post-bg-engine.jpg"
catalog: true
tags:
    - k8s
    - kind
    - ops
---

## 背景

K8S集群的搭建由于墙的存在比较麻烦而且也比较占用资源,个人学习搭建K8S学习使用和做一些测试推荐使用Kind来在本地搭建.

## 安装

前置条件需要先安装golang 1.16 或更新的版本.
低版本需要加上 ```GO111MODULE="on" ```

>
> 如果包无法下载,因为墙可以添加Go package的国内镜像,
> 设置阿里的镜像  ```go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct```
>

```sh
go install sigs.k8s.io/kind@latest

```

安装完成后就可以执行```kind create cluster```来创建本地集群.

>
> 安装完成后如果 ```kind``` 命令无法执行,可能是因为go的模块安装目录不在你的PATH目录下
> 使用 ``` whereis go``` 查看路径,找到kind执行文件加入到你的PATH即可
> 在```~/.bash_profile```或者```~/.bashrc```中增加 ```export PATH=/root/go/bin:$PATH```
> 编辑后记得 ```source ~/.bash_profile```或者重新登录下让配置生效.
>

如果需要创建多节点的集群,需要增加配置文件:


```yaml
# 三个节点的集群 cluster.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
```

### 安装k8s工具

安装```kubectl```,```kubeadm```,```kubelet```

```sh
apt update
apt install -y apt-transport-https ca-certificates curl
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add - # 添加apt证书
echo  "deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
apt update && apt  install -y kubelet kubeadm kubectl
```

使用 ```kind create cluster --config cluster.yaml```来创建该集群.

