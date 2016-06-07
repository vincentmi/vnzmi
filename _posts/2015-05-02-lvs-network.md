---
layout:     post
title:      "LVS配置命令"
date:       2015-05-02 23:36:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - 运维
    - LVS
---

DirectorServer

```bash
ifconfig eth0:0 192.168.0.251 broadcast 192.168.0.251  netmask 255.255.255.255 up

route add -host 192.168.0.251 dev eth0:0 

echo "1" >/proc/sys/net/ipv4/ip_forward
```


realserver

```bash
ifconfig lo:0 192.168.0.251 broadcast 192.168.0.251 netmask 255.255.255.255 up


 vi /etc/sysctl.conf

net.ipv4.conf.all.arp_ignore = 1
net.ipv4.conf.all.arp_announce = 2
net.ipv4.conf.tunl0.arp_ignore = 1
net.ipv4.conf.tunl0.arp_announce = 2
```
2014-02-21
