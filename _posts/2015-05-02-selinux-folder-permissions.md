---
layout:     post
title:      "SElinux 又蛋疼"
date:       2015-05-02 22:36:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - 运维
---

(13) Permission Denied 

https://wiki.apache.org/httpd/13PermissionDenied

Apache一直报这个错误。权限都是对的。原来是SElinux的问题

增加该目录即可

chcon -R -h -t httpd_sys_content_t /home/folder/
这个是解决socket无法连接

setsebool -P httpd_can_network_connect 1


SELinux 详解 http://wiki.centos.org/zh/HowTos/SELinux



PHP fsocketopen permission denied
该问题是因为SElinux引起 使用
getsebool -a 获取当前的selinux设置状态
setsebool -P httpd_can_network_connect on 设置运行创建网络连接
这个命令执行会花一些时间请等待。
