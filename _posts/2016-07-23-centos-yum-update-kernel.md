---
layout:     post
title:      "使用Yum快速升级CentOS6.6内核"
date:       2016-07-23 05:38:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - CentOS 
    - OP
    - Kernel
    - Yum 
---

>
> 因为要装Docker所以需要升级下Linux内核
> 记录下命令备忘
>

# 使用Yum快速升级CentOS6.6内核

## 导入public key

```sh
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
```

## 安装ELRepo到CentOS 6.6中

```sh
rpm -Uvh http://www.elrepo.org/elrepo-release-6-6.el6.elrepo.noarch.rpm
```

## 安装长期支持版本kernel

```sh
yum --enablerepo=elrepo-kernel install kernel-lt -y
```


## 编辑grub.conf文件，修改Grub引导顺序

```sh
vim /etc/grub.conf
```

确认刚刚安装的内核的位置，然后将default修改一下。

```ini
default=0
timeout=5
splashimage=(hd0,2)/boot/grub/splash.xpm.gz
hiddenmenu
title CentOS (3.10.71-1.el6.elrepo.x86_64)
    root (hd0,2)
    kernel /boot/vmlinuz-3.10.71-1.el6.elrepo.x86_64 ro root=UUID=4cfe1c56-3703-4d36-b57f-7efc1943c6f4 rd_NO_LUKS rd_NO_LVM LANG=en_US.UTF-8 rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=auto  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet elevator=noop
    initrd /boot/initramfs-3.10.71-1.el6.elrepo.x86_64.img
title CentOS (2.6.32-504.12.2.el6.x86_64)
    root (hd0,2)
    kernel /boot/vmlinuz-2.6.32-504.12.2.el6.x86_64 ro root=UUID=4cfe1c56-3703-4d36-b57f-7efc1943c6f4 rd_NO_LUKS rd_NO_LVM LANG=en_US.UTF-8 rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=auto  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet elevator=noop
    initrd /boot/initramfs-2.6.32-504.12.2.el6.x86_64.img
title CentOS (2.6.32-358.23.2.el6.x86_64)
    root (hd0,2)
    kernel /boot/vmlinuz-2.6.32-358.23.2.el6.x86_64 ro root=UUID=4cfe1c56-3703-4d36-b57f-7efc1943c6f4 rd_NO_LUKS rd_NO_LVM LANG=en_US.UTF-8 rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=auto  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet elevator=noop
    initrd /boot/initramfs-2.6.32-358.23.2.el6.x86_64.img
title CentOS (2.6.32-358.el6.x86_64)
    root (hd0,2)
    kernel /boot/vmlinuz-2.6.32-358.el6.x86_64 ro root=UUID=4cfe1c56-3703-4d36-b57f-7efc1943c6f4 rd_NO_LUKS rd_NO_LVM LANG=en_US.UTF-8 rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=auto  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet elevator=noop
    initrd /boot/initramfs-2.6.32-358.el6.x86_64.img
```
新装的内核位置为0，所以讲default修改为0，保存退出重启。

## 重启后检查内核

```sh
uname -r
```


## 参考

- [https://www.jslink.org/linux/centos-kernel-upgrade.html](https://www.jslink.org/linux/centos-kernel-upgrade.html)
- [http://www.dadclab.com/archives/5340.jiecao](http://www.dadclab.com/archives/5340.jiecao)


