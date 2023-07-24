---
layout:     post
title:      "用树莓派实现局域网打印和扫描"
date:       "2023-07-23 21:44:00"
author:     "Vincent"
image:  "/img/raspi.jpg"
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

## 配置网络


# 安装CUPS

# 解决驱动问题

## HP 打印机Linux驱动

前往这里下载惠普打印机相关驱动 [https://developers.hp.com/hp-linux-imaging-and-printing/gethplip](https://developers.hp.com/hp-linux-imaging-and-printing/gethplip)


#### HP驱动插件

插件网站地址 [https://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/](https://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/)

> 注意如果使用安装器无法成功安装，可以手动下载安装，下载与本机版本hplip版本一致的 插件版本。下载时同时下载```.asc```文件安装时会进行文件校验。




下载文件：

```sh
wget --no-check-certification https://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/hplip-3.16.2-plugin.run

wget --no-check-certification https://www.openprinting.org/download/printdriver/auxfiles/HP/plugins/hplip-3.16.2-plugin.run.asc
```

安装插件

```sh
chmod a+x hplip-3.16.2-plugin.run

./hplip-3.16.2-plugin.run
```


# 剩余的问题

