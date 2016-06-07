---
layout:     post
title:      "CentOS 6.5 docker 错误"
date:       2015-06-10 17:16:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - 运维
    - Docker
---
Docker 在centos6.5中安装因为 device-mapper 不正确会报这个错

```
    \n三  6月 10 16:46:56 CST 2015\n
    time="2015-06-10T16:46:56+08:00" level="info" msg="+job serveapi(unix:///var/run/docker.sock)" 
    time="2015-06-10T16:46:56+08:00" level="info" msg="WARNING: You are running linux kernel version 2.6.32-431.el6.x86_64, which might be unstable running docker. Please upgrade your kernel to 3.8.0." 
    time="2015-06-10T16:46:56+08:00" level="info" msg="Listening for HTTP on unix (/var/run/docker.sock)" 
    /usr/bin/docker: relocation error: /usr/bin/docker: symbol dm_task_get_info_with_deferred_remove, version Base not defined in file libdevmapper.so.1.02 with link time reference
```

解决方法

```
    sudo yum install device-mapper-event-libs
    sudo yum reinstall docker
```


