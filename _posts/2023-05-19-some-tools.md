---
layout:     post
title:      "一些脚本"
date:       "2023-05-19 23:48:00"
author:     "Vincent"
header-img:  "img/post-bg-engine.jpg"
catalog: true
tags:
    - Linux
    - Docker
---


# Yearning SQL审核平台

拉代码 
```git clone git@github.com:cookieY/Yearning.git```

打包镜像

```cd Yearning.git && docker build -t yearning .```

```sh
docker run -it --rm  -e MYSQL_USER=root -e MYSQL_ADDR=172.17.0.1:3307 -e MYSQL_PASSWORD=root  -e MYSQL_DB=yearning yearning /opt/Yearning install

docker run --restart=always -d  --name yearning  -p 9001:8000 -e MYSQL_USER=root -e MYSQL_ADDR=172.17.0.1:3307 -e MYSQL_PASSWORD=root -e SECRET_KEY=mws1118888888888 -e MYSQL_DB=yearning  yearning
```