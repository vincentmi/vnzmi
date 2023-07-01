---
layout:     post
title:      "Git index-pack failed 问题解决"
date:       2017-01-08 18:43:00
author:     "Vincent"
image:  "img/post-bg-water.jpg"
catalog: true
tags:
    - Git
---


## 问题

git 由于提交了比较大的文件，在服务端一直无法拉下来，错误如下

```bash
root@iZ94au:/wwwroot/app# git pull
remote: Counting objects: 168, done.
remote: Compressing objects: 100% (87/87), done.
Connection to bitbucket.org closed by remote host.0 KiB/s
fatal: The remote end hung up unexpectedly
fatal: early EOF
fatal: index-pack failed
```

## 解决方案


#### 解决1

根据stackoverflow的回答修改comporession=0 修改压缩的程度

```
compression = 9
```

设置为 -1， 0 9 均无效


#### 解决2

这个错误可能是由于git内存不够引起的，修改配置

```
[core] 
packedGitLimit = 512m 
packedGitWindowSize = 512m 
[pack] 
deltaCacheSize = 2047m 
packSizeLimit = 2047m 
windowMemory = 2047m
```

这个有效。












