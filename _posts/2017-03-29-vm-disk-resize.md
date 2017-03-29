---
layout:     post
title:      "VirtualBox调整磁盘空间"
date:       2017-03-29 16:00:00
author:     "Vincent"
header-img:  "img/post-bg-ball.jpg"
catalog: true
tags:
    - VirtualBox
    - Linux
    - op
    - LVM
---


## 调整VM磁盘文件大小

vm 版本需要4.0以上

```sh
VBoxManage modifyhd you_disk_file –resize 40960
```

也可以使用 ```uuid``` 替换 ```you_disk_file``` , 使用```VBoxManage list hdds```可以列出你的当前磁盘。

## 使用Parted扩容

如果没有```parted```则通过 ```yum install parted```安装

使用```print```查看当前分区情况

```sh
[root@p3 ~]# parted /dev/sda
GNU Parted 2.1
使用 /dev/sda
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print
Model: ATA VBOX HARDDISK (scsi)
Disk /dev/sda: 14.7GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos

Number  Start   End     Size    Type     File system  标志
 1      1049kB  525MB   524MB   primary  ext4         启动
 2      525MB   8590MB  8065MB  primary               lvm

(parted)

```

```print free``` 看下有多少空闲空间

```sh
(parted) print free
Model: ATA VBOX HARDDISK (scsi)
Disk /dev/sda: 14.7GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos

Number  Start   End     Size    Type     File system  标志
        32.3kB  1049kB  1016kB           Free Space
 1      1049kB  525MB   524MB   primary  ext4         启动
 2      525MB   8590MB  8065MB  primary               lvm
        8590MB  14.7GB  6090MB           Free Space
```


创建 PV

```sh
pvcreate /dev/sda3
```

扩展VG

```sh
mkfs  -t ext4 /dev/sda3
vgextend VolGroup /dev/sda3




```






