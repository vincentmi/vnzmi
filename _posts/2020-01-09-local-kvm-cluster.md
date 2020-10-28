---
layout:     post
title:      "搭建本地KVM和K8S集群"
date:       "2020-01-09 18:24:00"
author:     "Vincent"
header-img:  "img/home-bg-highway.jpg"
catalog: true
tags:
    - KVM
    - K8S
    - Rancher
---



## 准备工作

#### 版本

 - Ubuntu 16.04.6 LTS 
 - Linux version 4.4.0-142-generic
 - qemu-img version 2.5.0 (Debian 1:2.5+dfsg-5ubuntu10.42)

#### 检查

检查是否支持虚拟化

```sh
egrep -c '(svm|vmx)' /proc/cpuinfo
```
返回 0 则不支持,需要看下BIOS里是否没有打开虚拟化支持.

#### 安装KVM

```sh
sudo apt update
sudo apt install qemu qemu-kvm libvirt-bin  bridge-utils  virt-manager virt-sysperp
```

#### 配置自启动

```sh
sudo systemctl start libvirtd.service
sudo systemctl enable libvirtd.service
```

## 配置桥接网络



修改 ```/etc/network/interfaces```

```sh
# The loopback network interface
auto lo
iface lo inet loopback

# The bridge interface
auto br0
iface br0 inet static
     address 10.10.0.3
     netmask 255.255.255.0
     network 10.10.0.1
     broadcast 10.10.0.255
     gateway 10.10.0.1
     dns-nameservers 10.10.0.1
     bridge_ports enp1s0
     bridge_stp off
     bridge_fd 0
```

> ubuntu 18.04 使用了netplan 配置有点不同
> 文件位置 ```/etc/netplan/01-netcfg.yaml``` 文件内如如下
>

#### 原文件

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp2s0:
      addresses: [ 192.168.199.152/24 ]
      gateway4: 192.168.199.1
      nameservers:
          addresses:
              - "192.168.199.1"
```
#### 修改为 

```yaml 
network:
  version: 2
  renderer: networkd
  ethernets:
     enp2s0:
        dhcp4: no
        dhcp6: no
  bridges:
    br0:
        interfaces: [enp2s0]
        dhcp4: no
        addresses: [ 192.168.199.152/24 ]
        gateway4: 192.168.199.1
        nameservers:
            addresses:
                - "192.168.199.1"
```


#### 重启网络
 
 ```sh
 systemctl restart networking.service
 # netplan apply # for ubuntu 18.04
 ```
 
 >  有时候需要```reboot```一下.
 > 宿主机能正常上网而虚拟机获取不到ip，可能是ufw没有允许ip转发导致的，编辑```/etc/default/ufw```允许ip转发。设置 ```DEFAULT_FORWARD_POLICY="ACCEPT"```,之后```systemctl restart ufw.service```重启服务.
 
 
## 创建虚拟机

```sh 
#!/bin/sh
virt-install -n vm31  \
--description "ubuntu1604 64bit 1 0.10.0.31" \
--os-type=linux \
--os-variant=linux \
--memory  2048 \
--vcpus=2 \
--disk path=/opt/vms/vm31.img,bus=virtio,size=200 \
--network bridge:br0 \
--accelerate \
--graphics vnc,listen=0.0.0.0,port=5901,keymap=en-us \
--cdrom /opt/ubuntu1604.iso \
#--extra-args="console=tty0 console=ttyS0,115200n8"
```
以上命令创建了一个200G的linux 主机,挂载了ubuntu16.04的安装盘,执行后就可以打开VNC访问宿主机的5901端口进行系统安装.

## VM设置

#### 设置静态IP地址
```sh
source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto ens3
iface ens3 inet static
     address 10.10.0.31
     netmask 255.255.255.0
     network 10.10.0.1
     broadcast 10.10.0.255
      gateway 10.10.0.1
      dns-nameservers 10.10.0.1
```

如果有一些Perl语言配置的警告,设置 ```/etc/default/locale```添加

```sh
LANG="en_US.UTF-8"
LANGUAGE="en_US.UTF-8"
LC_ALL="en_US.UTF-8"
LC_CTYPE="en_US.UTF-8"
```

#### 安装NTP 

```sh
apt install ntp ntpdate #安装
systemctl start ntp #启动服务
systemctl enable ntp #设置为默认启动
```

#### 安装Docker

```sh
curl https://releases.rancher.com/install-docker/18.09.sh | sh
```

##  复制虚拟机


```sh
virsh dumpxml vm31 >  /etc/libvirt/qemu/vm32.xml #复制配置文件
cp /opt/vms/vm31.img  /opt/vms/vm32.img #复制磁盘文件
vi /etc/libvirt/qemu/vm32.xml #修改name,uuid,disk文件位置,mac地址
```

修改如下

```xml
  <name>vm32</name>
  <uuid>8fe99df1-c2ac-40ae-b02f-7eb132cdfd0f</uuid>
  ....
  <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/opt/vms/vm32.img'/>
      ...
<interface type='bridge'>
      <mac address='52:54:00:46:9a:32'/>
      ....
</interface>
...      
<seclabel type='dynamic' model='apparmor' relabel='yes'>
    <label>libvirt-8fe99df1-c2ac-32ae-b02f-7eb13ecdfd0f</label>
    <imagelabel>libvirt-8fe99df1-c2ac-32ae-b02f-7eb13ecdfd0f</imagelabel>
  </seclabel>
```

####  载入复制的虚拟机

```sh
virsh define /etc/libvirt/qemu/vm32.xml
vish start vm32
```

启动之后VNC进入虚拟机修改 hostname 修改IP地址 ,重新启动虚拟机.

#### 设置虚拟机自动启动

```sh
virsh autostart vm31
virsh autostart vm32
```

## 通过克隆创建虚拟机

```sh
virsh suspend vm31 # 停止虚拟机
virt-clone --connect qemu:///system --original vm31 --name vm_ubuntu16_64_docker \
--file /opt/img/vm_ubuntu16_64_docker.img #克隆
```
查看镜像

```sh
virsh list --all
```
 
 
 
 








 

