---
layout:     post
title:      "MemCache : could not compress错误"
date:       2015-05-02 22:35:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - 运维
---

## 问题

今天遇到这个坑爹的问题。产生问题的原因是不同版本的memcache客户端，PHP会报这个警告。

## 原因

集群里有一台5.5的机器 没有在LVS里，其他机器都是5.3。但是有job 因此关闭nginx 关闭yii的schema cache重启memcache和备份机恢复正常。


