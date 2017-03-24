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

```
    sudo yum install device-mapper-event-libs
    sudo yum reinstall docker
```


#### - Docker 镜像无法拉取
使用163的镜像，```CentOS``` 修改文件 ```/etc/sysconfig/docker```

```
DOCKER_OPTS="$DOCKER_OPTS --registry-mirror=http://hub-mirror.c.163.com"
```

## 安装私有 Registry


















