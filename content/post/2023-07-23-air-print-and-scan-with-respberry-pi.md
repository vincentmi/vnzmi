---
layout:     post
title:      "用树莓派实现局域网打印和扫描"
date:       "2023-07-23 21:44:00"
author:     "Vincent"
image:  "/img/post-bg-raspi.jpg"
catalog: true
tags:
    - Rasphberry PI
    - sane
    - cups
    - printer
    - scan
---

# 准备

买了个树莓派一没怎么用，现在家里有2台打印机，太占用桌面了，用树莓派给他们加上远程。这样可以搬远点。

## 选择系统
首先给树莓派烧录一个系统，我选择的是debian.可以从这里 [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/) 下载。

我选择的Debian

```sh
uname -a
Linux raspberrypi 4.14.98-v7+ #1200 SMP Tue Feb 12 20:27:48 GMT 2019 armv7l GNU/Linux
```

打开相关的一些服务```ssh```,```vnc```打开可以远程操作，方便一点。

![/img/in-post/raspi_setting.png](/img/in-post/raspi_setting.png)

## 配置网络

先连接上WIFI，然后。

打开编辑器编辑网络

```sh
sudo leafpad /etc/dhcpcd.conf 
```

因为我使用WIFI连接，设置WIIF的IP地址

```conf
SSID Vincent
inform 192.168.199.191
static routers=192.168.199.1
static domain_name_servers=114.114.114.114

SSID Vincent
inform 192.168.199.191
static routers=192.168.199.1
static domain_name_servers=114.114.114.114
```

> ```domain_name_servers```不设置的话会导致无法解析DNS



# 安装驱动

## HP 打印机Linux驱动

安装HP基础驱动,安装时会自动安装CUPS 打印服务。

```sh
sudo apt-get install hplip
```


将用户添加入lpadmin，我的用户名是pi。如果不添加，之后添加网络打印机，会报错：Unable to add printer forbidden。

```sh 
sudo usermod -a -G lpadmin pi
```

修改cups配置环境，为了安全起见，cups服务默认是只能本地用户localhost访问的。现在我们需要远程访问，需要修改配置文件```/etc/cups/cupsd.conf```。在修改配置文件前，先关掉cups服务，然后再开启。

```sh
sudo service cups stop           #关掉服务
sudo leafpad /etc/cups/cupsd.conf  #开始编辑
sudo service cups start          #开启服务
```


```conf
Port 631
#Listen /var/run/cups/cups.sock
Listen 0.0.0.0:631
```


## 使用了ZjStream协议的HP打印机

需要安装该驱动,foo2zjs是一个基于ZjStream协议的Linux开源驱动.源代码 ```https://github.com/koenkooi/foo2zjs```.可以直接安装二进制版本。

> 我的打印机是 HP Lasterjet M1136 MFP 打印报"filter fail" 安装该驱动解决了问题。


```sh
apt-get install -y printer-driver-foo2zjs
```



前往这里下载惠普打印机相关驱动 [https://developers.hp.com/hp-linux-imaging-and-printing/gethplip](https://developers.hp.com/hp-linux-imaging-and-printing/gethplip)


## HP驱动插件

插件网站地址 [https://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/](https://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/)

> 注意如果使用安装器无法成功安装，可以手动下载安装，下载与本机版本hplip版本一致的 插件版本。下载时同时下载```.asc```文件安装时会进行文件校验。

> 插件不安装也可以进行打印，但是无法进行扫描。```scanimage``` 命令发送过后会出现 硬件通讯错误。


下载文件：

```sh
wget --no-check-certification https://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/hplip-3.16.2-plugin.run

wget --no-check-certification https://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/hplip-3.16.2-plugin.run.asc
```

安装插件

```sh
hp-plugin
```

调用HP Plugin的UI界面来选择刚才下载的文件进行安装。

> 注意你可以使用 ```sudo apt list --installed | grep hplip ```来查看你安装的驱动版本，以选择正确的插件版本。

```sh
pi@raspberrypi:~ $ sudo apt list --installed | grep hplip

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

hplip/oldoldstable,now 3.16.11+repack0-3 armhf [已安装]
hplip-data/oldoldstable,now 3.16.11+repack0-3 all [已安装，自动]
hplip-gui/oldoldstable,now 3.16.11+repack0-3 all [已安装]
```




# 添加打印机

CUPS安装好之后可以通过  ```http://192.168.199.191:631```端口进行访问

![rapi_cups.jpg](/img/in-post/rapi_cups.jpg)

添加打印机得登录 ```https://192.168.199.191:631/admin/``` 使用```root```登录后进行添加


## 选择打印机

![raspi_add_printer.png](/img/in-post/raspi_add_printer.png)

## 选择共享
![raspi_add_printer2.png](/img/in-post/raspi_add_printer2.png)

## 选择驱动

如果你的型号不在列表中，选择同一系列理论上应该都可以
![raspi_add_printer.png](/img/in-post/raspi_add_printer3.png)

# 扫描仪

## 安装 ```sane```



```sh
sudo apt-get install -y sane

```

## 查看系统扫描仪

```sh
pi@raspberrypi:~ $ scanimage -L
device `hpaio:/usb/HP_LaserJet_Professional_M1136_MFP?serial=000000000QHCMMPKPR1a' is a Hewlett-Packard HP_LaserJet_Professional_M1136_MFP all-in-one
```

## 使用扫描仪

![raspi_xsane.png](/img/in-post/raspi_xsane.png)

## 扫描结果

![raspi_scan.png](/img/in-post/raspi_scan.png)


# ScanServ

写了一个小服务器用于局域网进行扫描，在Web端操作扫描仪进行扫描。


Python版本
```https://github.com/vincentmi/scanserv```

Golang 版本（树莓派python版本比较低Flask运行不了。还是golang方便点）

```https://github.com/vincentmi/scanserv-go```

![raspi_scanserv.jpg](/img/in-post/raspi_scanserv.jpg)


##  使用

```sh
 ./scanserv -h
Usage of ./scanserv:
  -f string
    	上传和中转文件路径 (default "./file")
  -m string
    	扫描命令 (default "/usr/bin/scanimage")
  -p int
    	监听端口 (default 8080)
```

