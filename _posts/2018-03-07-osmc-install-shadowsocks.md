---
layout:     post
title:      "树莓派OSMC 安装ShadowSocks"
date:       2018-03-07 10:07:00
author:     "Vincent"
header-img:  "img/post-bg-line.jpg"
catalog: true
tags:
    - HW
    - Go
    - Raspberrypi
    - Shaodwsocks
    
---

## 背景

最近买了一台QNAP NAS.

## 安装

考虑到以后可能会在树莓派上弄其他服务,所以打算在树莓派上装上GO,因此没有进行交叉编译.

#### 安装Git

```sh 
sudo  apt-get install git-core
```

#### 安装GO编译环境

```uname -a``` 可以看到 PI3  是ARM V7 版本的CPU.

```sh
Linux osmc 4.9.29-15-osmc #1 SMP PREEMPT Sat Jan 20 21:27:28 UTC 2018 armv7l GNU/Linux

```
下个GO的二进制包,因为是ARM V7 需要V6L版本的二级制包:

```sh 
wget https://dl.google.com/go/go1.10.linux-armv6l.tar.gz
```

先把GO执行程序添加到路径

```sh
sudo ln -s /home/osmc/go/bin/go /usr/bin/go
sudo ln -s /home/osmc/go/bin/godoc /usr/bin/godoc
sudo ln -s /home/osmc/go/bin/gofmt /usr/bin/gofmt
```

#### 下载 shadowsocks 

设置GOPATH

```sh
mkdir /home/osmc/gopath
export GOPATH=/home/osmc/gopath
```

因为用到了 CGO 所以要配置 GCC环境,需要安装

```sh
sudo apt-get install gcc libc6-dev
```

获取shadowsocks 客户端

```sh
go get github.com/shadowsocks/shadowsocks-go/cmd/shadowsocks-local
```

>
> **注意**:因为墙,可能会导致 ```golang.org/x/``` 下的包下载失败.可以到 ```https://gopm.io``` 下载相应的包,解压之后拷贝到你的GOPATH下 ```src/golang.org/x``` 目录下.然后重试即可.
>


### 配置

创建个目录

```sh
mkdir ss
```

添加一个文件 ```vi ss/ss```:

```sh
#!/bin/sh

/home/osmc/gopath/bin/shadowsocks-local -c /home/osmc/ss/ss.json
```

```
chmod a+x ss/ss
```

编辑配置```vi ss/ss.json```文件:

```json
{
 "server":"Shadowsocks服务器IP地址",
  "server_port":Shadowsocks服务器端口,
 "local_port":本地代理服务端口,
 "method":"加密方式",
 "password":"密码",
 "timeout":30
}
```
安装完成

```sh
osmc@osmc:~/ss$ ./ss
2018/03/07 11:05:52 available remote server x.x.x.x:xxxx
2018/03/07 11:05:52 starting local socks5 server at :xxxx ...

```

## 配置为服务

建个软连接

```sh
sudo ln -s /home/osmc/ss/ss /usr/bin/shadowsocks
```

在来个启动脚本 ``` sudo vi /etc/systemd/system/shadowsocks.service ```

```sh 
[Unit]
Description=Shadowsocks Client
[Service]
Type=simple
ExecStart=/usr/bin/shadowsocks
StandardOutput=syslog
StandardError=inherit
[Install]
WantedBy=multi-user.target
```
设置执行权限

```sh
sudo chmod a+x /etc/systemd/system/shadowsocks.service
```

查看下服务状态

```sh
osmc@osmc:~/ss$ sudo systemctl status shadowsocks.service
● shadowsocks.service - Shadowsocks Client
   Loaded: loaded (/etc/systemd/system/shadowsocks.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2018-03-07 12:08:36 CST; 11min ago
 Main PID: 7387 (shadowsocks)
   CGroup: /system.slice/shadowsocks.service
           ├─7387 /bin/sh /usr/bin/shadowsocks
           └─7388 /home/osmc/gopath/bin/shadowsocks-local -c /home/osmc/ss/ss.json

3月 07 12:08:36 osmc systemd[1]: Started Shadowsocks Client.
3月 07 12:08:36 osmc shadowsocks[7387]: 2018/03/07 12:08:36 available remote server x.x.x.x:xxxx
3月 07 12:08:36 osmc shadowsocks[7387]: 2018/03/07 12:08:36 starting local socks5 server at :xxxx ...
 
```
 
 
## 设置 OSMC
 







