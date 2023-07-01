---
layout:     post
title:      "VirtualBox调整磁盘空间"
date:       2017-03-29 16:00:00
author:     "Vincent"
image:  "img/post-bg-ball.jpg"
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

## 建立物理分区

先查看当前分区情况

```sh
[root@p2 ~]# df -h
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/VolGroup-lv_root  6.5G  5.0G  1.2G  81% /
tmpfs                         372M   12K  372M   1% /dev/shm
/dev/sda1                     477M   49M  399M  11% /boot
```
目前 ```/```有6.5G

查看当前物理磁盘空间

```sh 
[root@p2 ~]# fdisk -l /dev/sda

Disk /dev/sda: 14.7 GB, 14680064000 bytes
255 heads, 63 sectors/track, 1784 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00013fb6

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1          64      512000   83  Linux
Partition 1 does not end on cylinder boundary.
/dev/sda2              64        1045     7875584   8e  Linux LVM
```

扩展后磁盘空间增加到了14.7G ,但是增加的部分没有没有纳入到分区中.下面创建分区来使用这部分磁盘


使用```fdisk```创建分区 

```sh
[root@p2 ~]# fdisk /dev/sda

WARNING: DOS-compatible mode is deprecated. It's strongly recommended to
         switch off the mode (command 'c') and change display units to
         sectors (command 'u').

Command (m for help): n
Command action
   e   extended
   p   primary partition (1-4)
p
Partition number (1-4): 3
First cylinder (1045-1784, default 1045):
Using default value 1045
Last cylinder, +cylinders or +size{K,M,G} (1045-1784, default 1784):
Using default value 1784
```

 打印看下 磁盘分区的情况
 
```sh
 Command (m for help): p

Disk /dev/sda: 14.7 GB, 14680064000 bytes
255 heads, 63 sectors/track, 1784 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00013fb6

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1          64      512000   83  Linux
Partition 1 does not end on cylinder boundary.
/dev/sda2              64        1045     7875584   8e  Linux LVM
/dev/sda3            1045        1784     5941372   83  Linux
```

```/dev/sda3```就是我们创建的分区.分区类型是```Linux``` 我们需要将其类型修改为```Linux LVM```

使用 ```t```命令

```sh
Command (m for help): t
Partition number (1-4): 3
Hex code (type L to list codes): 8E
Changed system type of partition 3 to 8e (Linux LVM)
```

再打印看下就变味 ```Linux LVM```了 .

最后使用 ```w```保存,并重启

```sh
Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.

WARNING: Re-reading the partition table failed with error 16: 设备或资源忙.
The kernel still uses the old table. The new table will be used at
the next reboot or after you run partprobe(8) or kpartx(8)
Syncing disks.
[root@p2 ~]# reboot
```

## 扩展LVM

查看当前 Volume Group 信息

```sh
[root@p2 ~]# vgdisplay
  --- Volume group ---
  VG Name               VolGroup
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               7.51 GiB
  PE Size               4.00 MiB
  Total PE              1922
  Alloc PE / Size       1922 / 7.51 GiB
  Free  PE / Size       0 / 0
  VG UUID               sgcZ0g-B6PJ-V983-zaT4-6ElU-BRIv-YTp3fn
  
[root@p2 ~]# lvscan
ACTIVE            '/dev/VolGroup/lv_root' [6.71 GiB] inherit
ACTIVE            '/dev/VolGroup/lv_swap' [816.00 MiB] inherit

```

将刚才的分区创建为物理卷

```sh
pvcreate /dev/sda3
```

将物理卷加入 Volume Group . 如果没创建物理卷,程序会自动创建.

```sh 
[root@p2 ~]# vgextend VolGroup /dev/sda3
  dev_is_mpath: failed to get device for 8:3
  No physical volume label read from /dev/sda3
  Physical volume /dev/sda3 not found
  Physical volume "/dev/sda3" successfully created
  Volume group "VolGroup" successfully extended
```

扩展逻辑卷,我们将该控件扩展给 ```/```

```sh 
[root@p2 ~]# lvextend /dev/VolGroup/lv_root /dev/sda3
  Extending logical volume lv_root to 12.38 GiB
  Logical volume lv_root successfully resized
```

应用尺寸改变

```sh 
[root@p2 ~]# resize2fs /dev/VolGroup/lv_root
resize2fs 1.41.12 (17-May-2010)
Filesystem at /dev/VolGroup/lv_root is mounted on /; on-line resizing required
old desc_blocks = 1, new_desc_blocks = 1
Performing an on-line resize of /dev/VolGroup/lv_root to 3244032 (4k) blocks.
The filesystem on /dev/VolGroup/lv_root is now 3244032 blocks long.
```

## 查看结果

```sh
[root@p2 ~]# lvscan
  ACTIVE            '/dev/VolGroup/lv_root' [12.38 GiB] inherit
  ACTIVE            '/dev/VolGroup/lv_swap' [816.00 MiB] inherit
[root@p2 ~]# df -h
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/VolGroup-lv_root   13G  4.9G  6.6G  43% /
tmpfs                         372M   12K  372M   1% /dev/shm
/dev/sda1                     477M   49M  399M  11% /boot
```

