---
layout:     post
title:      "dockerpool CA 证书错误"
date:       2015-06-14 09:13:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - 运维
    - Docker
---

docker被墙后用，拉dockerpool的镜像会出现这个错误

```sh
> sudo docker pull dl.dockerpool.com:5000/centos:7
FATA[0000] Error response from daemon: v1 ping attempt failed with error: Get https://dl.dockerpool.com:5000/v1/_ping: tls: oversized record received with length 28012. If this private registry supports only HTTP or HTTPS with an unknown CA certificate, please add `--insecure-registry dl.dockerpool.com:5000` to the daemon's arguments. In the case of HTTPS, if you have access to the registry's CA certificate, no need for the flag; simply place the CA certificate at /etc/docker/certs.d/dl.dockerpool.com:5000/ca.crt 
```


解决方法，在/etc/sysconfig/docker添加
```sh
    INSECURE_REGISTRY='--insecure-registry dl.dockerpool.com:5000'
```

版本如下
> CentOS Linux release 7.1.1503 (Core) 
> Docker version 1.6.0, build 8aae715/1.6.0




