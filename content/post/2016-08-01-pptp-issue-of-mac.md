---
layout:     post
title:      "PPTP MAC断线问题"
date:       2016-08-01 14:45:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - PPTP 
    - MAC
    - VPN
---



## MAC连接pptp服务经常断线

日志内容如下

```
Aug  1 14:01:06 s1 pptpd[21666]: CTRL: Client 218.88.x.155 control connection finished
Aug  1 14:05:34 s1 pptpd[21965]: CTRL: Client 218.88.x.155 control connection started
Aug  1 14:05:34 s1 pptpd[21965]: CTRL: Starting call (launching pppd, opening GRE)
Aug  1 14:05:34 s1 pppd[21967]: Warning: can't open options file /home/xxxx/.ppprc: Permission denied
Aug  1 14:05:34 s1 pppd[21967]: Plugin /usr/lib64/pptpd/pptpd-logwtmp.so loaded.
Aug  1 14:05:34 s1 pppd[21967]: pptpd-logwtmp: $Version$
Aug  1 14:05:34 s1 pppd[21967]: Using interface ppp0
Aug  1 14:05:34 s1 pppd[21967]: Connect: ppp0 <--> /dev/pts/2
Aug  1 14:05:34 s1 pptpd[21965]: GRE: Bad checksum from pppd.
Aug  1 14:05:38 s1 pppd[21967]: MPPE 128-bit stateless compression enabled
Aug  1 14:05:41 s1 pppd[21967]: Unsupported protocol 'Apple Client Server Protocol Control' (0x8235) received
Aug  1 14:05:41 s1 pppd[21967]: Unsupported protocol 'IPv6 Control Protocol' (0x8057) received
Aug  1 14:05:41 s1 pppd[21967]: Unsupported protocol 'Apple Client Server Protocol Control' (0x8235) received
Aug  1 14:05:41 s1 pppd[21967]: Cannot determine ethernet address for proxy ARP
Aug  1 14:05:41 s1 pppd[21967]: local  IP address 192.168.x.1
Aug  1 14:05:41 s1 pppd[21967]: remote IP address 192.168.x.10
Aug  1 14:05:41 s1 pppd[21967]: pptpd-logwtmp.so ip-up ppp0 xxxxx 218.88.20.155
Aug  1 14:05:43 s1 pptpd[21965]: GRE: read(fd=7,buffer=6097c0,len=8260) from network failed: status = -1 error = Message too long
Aug  1 14:05:43 s1 pptpd[21965]: CTRL: GRE read or PTY write failed (gre,pty)=(7,6)
Aug  1 14:05:43 s1 pppd[21967]: Modem hangup
Aug  1 14:05:43 s1 pppd[21967]: pptpd-logwtmp.so ip-down ppp0
Aug  1 14:05:43 s1 pppd[21967]: Connect time 0.1 minutes.
Aug  1 14:05:43 s1 pppd[21967]: Sent 9063 bytes, received 3553 bytes.
Aug  1 14:05:43 s1 pppd[21967]: MPPE disabled
Aug  1 14:05:43 s1 pppd[21967]: Connection terminated.
Aug  1 14:05:43 s1 pppd[21967]: Exit.
Aug  1 14:05:43 s1 pptpd[21965]: CTRL: Client 218.88.20.155 control connection finished
```

主要错误是这句

```
GRE: read(fd=7,buffer=6097c0,len=8260) from network failed: status = -1
```

```GRE``` 通用路由封装（英语：Generic Routing Encapsulation，缩写为GRE），一种隧道协议，可以在虚拟点对点链路中封装多种网络层协议。由思科系统开发，在RFC 2784中定义。[Wiki](https://zh.wikipedia.org/wiki/%E9%80%9A%E7%94%A8%E8%B7%AF%E7%94%B1%E5%B0%81%E8%A3%85)

```MTU```最大传输单元（英语：Maximum Transmission Unit，缩写MTU）是指一种通信协议的某一层上面所能通过的最大数据包大小（以字节为单位）[wiki](https://zh.wikipedia.org/wiki/%E6%9C%80%E5%A4%A7%E4%BC%A0%E8%BE%93%E5%8D%95%E5%85%83)

如果超出MTU设置的值数据包可能会被分段传输.然后又可能会造成这个错误. 

尝试调整MTU设置 . 因为Windows的默认值是 1472 .因此将MAC的设置成1472.目前连接比较稳定.

# MAC MTU设置

![MAC set MTU](/img/in-post/mac_mtu_set.png)


# 连接L2TP协议的vpn， 填好信息报错“IPSec 共享密钥”丢失

在 ```/etc/ppp``` 目录下创建一个 ```options```目录

内容如下 

```
plugin L2TP.ppp
l2tpnoipsec
```