---
layout:     post
title:      "Linux 18.04 Tips"
date:       "2020-08-26 23:04:00"
author:     "Vincent"
header-img:  "img/bullseye-gradient_blue.svg"
catalog: true
tags:
    - Linux
    - Ubuntu
---

## 1. 设置启动界面

网上很多文章都是旧的,18.04 使用下列命令生效/.

### 切换为图形启动

```sudo systemctl set-default runlevel5.target```

### 切换为文本命令模式

```sudo systemctl set-default runlevel3.target```

命令行启动图形界面 使用```startx```






