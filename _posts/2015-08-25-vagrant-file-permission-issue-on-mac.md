---
layout:     post
title:      "Vagrant Mac 权限问题"
date:       2015-08-25 10:40:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - OP
    - Vagrant
---


Vagrant在windows下加载的文件全部是777，但是在Mac 下会是644
这样会导致文件权限问题。

解决方法如下：

```
    config.vm.synced_folder "/Users/vincent/www","/vagrant",:mount_options => ["dmode=777","fmode=777"]
```







