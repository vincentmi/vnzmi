---
layout:     post
title:      "使用Consul Docker微服务平台实践"
date:       2017-03-24 10:26:00
author:     "Vincent"
header-img:  "img/post-bg-engine.jpg"
catalog: true
tags:
    - Consul
    - Linux
    - Docker
    - Registrator
    - Consul-template
---


## 基础环境

#### - CentOS6.6 内核升级
因为虚拟机的centos内核无法达到docker稳定运行，因此升级到3.1,执行

```sh
#导入key
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
#安装ELRepo到CentOS 6.6中
rpm -Uvh http://www.elrepo.org/elrepo-release-6-6.el6.elrepo.noarch.rpm
#安装长期支持版本kernel
yum --enablerepo=elrepo-kernel install kernel-lt -y
#编辑grub.conf文件，修改Grub引导顺序,选择3.1版本的内容(一般在第一个)
vim /etc/grub.conf

```
重启后 ```uname -r```检查是否是3.1的内核。

#### - device-mapper 问题

```
/usr/bin/docker: relocation error: /usr/bin/docker: symbol dm_task_get_info_with_deferred_remove, version Base not defined in file libdevmapper.so.1.02 with link time reference
```

安装device-mapper即可

```sh
    sudo yum install device-mapper-event-libs
    sudo yum reinstall docker
```


#### - Docker 镜像无法拉取
使用163的镜像，```CentOS``` 修改文件 ```/etc/sysconfig/docker```

```sh
DOCKER_OPTS="$DOCKER_OPTS --registry-mirror=http://hub-mirror.c.163.com"
```

## 安装私有 Registry

Registry 是无状态、高可用的服务端应用。可以帮助我们进行Docker镜像的分发。使用Registry可以
建立内部的镜像存储和分发流程。Registry兼容Docker引擎的版本为1.6+。


**使用步骤**

```sh
#启动Registry
docker run -d -p 5000:5000 --name registry registry:2
#拉一些镜像
docker pull ubuntu
#Tag一下这样他就指向了你的Reigstry
docker tag ubuntu localhost:5000/myfirstimage
#推到库中
docker push localhost:5000/myfirstimage
#拉下来看下
docker pull localhost:5000/myfirstimage
#停止服务并删除数据
docker stop registry && docker rm -v registry

```

默认的Registry数据保存为一个docker的数据卷到宿主机的文件系统。如果你需要指定注册的数据存储到宿主机的目标使用以下语法

```
docker run -d -p 5000:5000 --restart=always --name registry  -v /var/lib/registry/data:/var/lib/registry  registry:2
```

[配置其他存储查看这里](https://docs.docker.com/registry/configuration/#storage)

如果需要外部用户来使用则需要配置SSL

```sh
mkdir -p /var/lib/registry/certs
cd /var/lib/registry/certs
openssl genrsa -des3 -passout pass:x -out ssl.pass.key 2048
openssl rsa -passin pass:x -in ssl.pass.key -out ssl.key
rm ssl.pass.key -f
openssl req -new -key ssl.key -out ssl.csr
openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt
rm -f ssl.csr
```

删除容器

```sh
docker rmi registry
cd /var/lib/registry
docker run -d -p 5000:5000 --restart=always --name registry  -v /var/lib/registry/data:/var/lib/registry  -v /var/lib/registry/certs:/certs -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/ssl.crt  -e REGISTRY_HTTP_TLS_KEY=/certs/ssl.key registry:2


docker run -p 5000:5000 --restart=always --name registry1  -v /var/lib/registry/data:/var/lib/registry  -v /var/lib/registry/certs:/certs -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/ssl.crt  -e REGISTRY_HTTP_TLS_KEY=/certs/ssl.key registry:2


docker run -p 5000:5000 --restart=always --name registry1  -v /var/lib/registry/data:/var/lib/registry registry:2

```




































