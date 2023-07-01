---
layout:     post
title:      "CentOS搭建L2TP VPN服务"
date:       2016-08-04 09:49:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - VPN 
    - L2TP
---

>
> 参考 : http://longtimenoc.com/archives/centos%E4%B8%8Al2tp%E5%AE%89%E8%A3%85%E4%B8%8E%E9%85%8D%E7%BD%AE
>

## 准备

### 编译会用到的库

```sh
yum install -y ppp iptables make gcc gmp-devel xmlto bison flex xmlto libpcap-devel lsof vim-enhanced
```

### 安装openswan

```sh
wget https://download.openswan.org/openswan/openswan-latest.tar.gz
tar zxf openswan-latest.tar.gz
cd openswan-2.6.48
make programs install
 
```

### 安装xl2tpd

```sh
yum install xl2tpd
```

## 配置


### 配置```/etc/ipsec.conf```

```
config setup
    nat_traversal=yes
    virtual_private=%v4:10.0.0.0/8,%v4:192.168.0.0/16,%v4:172.16.0.0/12
    oe=off
    protostack=netkey
 
conn L2TP-PSK-NAT
    rightsubnet=vhost:%priv
    also=L2TP-PSK-noNAT
 
conn L2TP-PSK-noNAT
    authby=secret
    pfs=no
    auto=add
    keyingtries=3
    rekey=no
    ikelifetime=8h
    keylife=1h
    type=transport
    left=$vpsip #改你服务器的IP
    leftprotoport=17/1701
    right=%any
    rightprotoport=17/%any

``` 
### 配置 ```/etc/ipsec.secrets```

```
你的服务器IP %any: PSK  "你的密码"
```

### 编辑 ``` /etc/sysctl.conf```

```sh
net.ipv4.ip_forward = 1
net.ipv4.conf.default.rp_filter = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.log_martians = 0
net.ipv4.conf.default.log_martians = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.icmp_ignore_bogus_error_responses = 1
```

使sysctl生效

```
sysctl -p
```

### 验证配置

```
ipsec setup restart
ipsec verify
```

验证后输出

```sh 
Checking if IPsec got installed and started correctly:

Version check and ipsec on-path                   	[OK]
Openswan U2.6.48/K3.10.102-1.el6.elrepo.x86_64 (netkey)
See `ipsec --copyright' for copyright information.
Checking for IPsec support in kernel              	[OK]
 NETKEY: Testing XFRM related proc values
         ICMP default/send_redirects              	[OK]
         ICMP default/accept_redirects            	[OK]
         XFRM larval drop                         	[OK]
Hardware random device check                      	[N/A]
Two or more interfaces found, checking IP forwarding	[OK]
Checking rp_filter                                	[ENABLED]
 /proc/sys/net/ipv4/conf/docker0/rp_filter        	[ENABLED]
 /proc/sys/net/ipv4/conf/eth0/rp_filter           	[ENABLED]
 /proc/sys/net/ipv4/conf/veth2bad97f/rp_filter    	[ENABLED]
 /proc/sys/net/ipv4/conf/virbr0/rp_filter         	[ENABLED]
 /proc/sys/net/ipv4/conf/virbr0-nic/rp_filter     	[ENABLED]
Checking that pluto is running                    	[OK]
 Pluto listening for IKE on udp 500               	[OK]
 Pluto listening for IKE on tcp 500               	[NOT IMPLEMENTED]
 Pluto listening for IKE/NAT-T on udp 4500        	[OK]
 Pluto listening for IKE/NAT-T on tcp 4500        	[NOT IMPLEMENTED]
 Pluto listening for IKE on tcp 10000 (cisco)     	[NOT IMPLEMENTED]
Checking NAT and MASQUERADEing                    	[TEST INCOMPLETE]
Checking 'ip' command                             	[IP XFRM BROKEN]
Checking 'iptables' command                       	[OK]

ipsec verify: encountered errors
```

注意一堆红色的 居然不影响... 使用我没有管,继续下一步

## 配置 xltpd

编辑 ```/etc/xl2tpd/xltpd.conf```

```
[global]
ipsec saref = yes
listen-addr = $vpsip ;服务器地址
[lns default]
ip range = 192.168.12.10-192.168.12.100 ;分配给连接的IP
local ip = 192.168.12.1; ;网关IP
refuse chap = yes
refuse pap = yes
require authentication = yes
ppp debug = yes
pppoptfile = /etc/ppp/options.xl2tpd
length bit = yes
```

编辑 ```/etc/ppp/options.xl2tpd```

```
require-mschap-v2
ms-dns 8.8.8.8
ms-dns 8.8.4.4
asyncmap 0
auth
crtscts
lock
hide-password
modem
debug
name l2tpd
proxyarp
lcp-echo-interval 30
lcp-echo-failure 4
mtu 1500
mru 1500
```

编辑连接用户文件```/etc/ppp/chap-secrets```

```sh
# user server password ip
username * userpass * #改成你的用户名 密码
```

重启XL2TPD

```
service xl2tpd restart
```

## iptables配置

```

iptables -A INPUT -p 50 -j ACCEPT
iptables -A INPUT -p udp -d 服务器IP --dport 500 -j ACCEPT
iptables -A INPUT -p udp -d 服务器IP --dport 4500 -j ACCEPT
iptables -A INPUT -p udp -d 服务器IP --dport 1701 -j ACCEPT
iptables -t nat -A POSTROUTING -s 192.168.12.0/24 -o eth0 -j MASQUERADE
service iptables save
servie iptables restart
```

增加自启动

```sh 
chkconfig xl2tpd on
chkconfig iptables on
chkconfig ipsec on
```

## 其他 

安装squid代理

```
yum install squid

```















