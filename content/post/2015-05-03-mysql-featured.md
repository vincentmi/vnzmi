---
layout:     post
title:      "MySQL Featured"
date:       2015-05-03 8:36:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - 运维
    - MySQL
---

今天又经历了一起MYSQL错误，系统日志中是“服务 mysql 意外停止” Mysql日志中则是：“Plugin 'FEDERATED' is disabled”
网站找到第一条解决方案：

1、在MY.INI文件中的 ```[mysqld]``` 中增加一行
```tmpdir="D:/MySQL/data/"```
修改后，还是启动不了，接着我做了第二步，重启正常。

2、删除DATA目录下除数据库文件夹外的其他文件，重启mysql
 



