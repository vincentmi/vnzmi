---
layout:     post
title:      "Jenkins集成jekyll"
date:       2016-07-21 09:49:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - Jekyll 
    - Jenkins 
---

Jekyll 3 需要ruby 2.0 以上,CentOS上的yum包比较老.使用rvm进行安装

```sh
curl -L get.rvm.io | bash -s stable
```

导入

```
# root用户安装执行
source /usr/local/rvm/rvm.sh
# 其他用户安装
source ~/.rvm/rvm.sh
```
安装Ruby

```sh
rvm 2.0.0
```

Jekyll的路径如下

```
/usr/local/rvm/gems/ruby-2.0.0-p648/bin/jekyll
```

但是要正常运行需要用wrappers脚本处理下环境变量等等, 包裹下如下

```
cd $WORKSPACE
/usr/local/rvm/gems/ruby-2.0.0-p648/wrappers/jekyll build --source $WORKSPACE --destination $WORKSPACE/_sites
```

构建后scp拷贝到目标机器
 
```
Send files or execute commands over SSH after the build runs

Source files : _sites/**
Remove prefix : _sites/
Remote directory : vnzmi
```




