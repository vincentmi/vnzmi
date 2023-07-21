---
layout:     post
title:      "一些脚本"
date:       "2023-05-19 23:48:00"
author:     "Vincent"
image:  "/img/bulleye_red.svg"
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

# 查询数据量


```sql
SELECT 
CONCAT(TABLE_SCHEMA,'.',TABLE_NAME) AS '表名',
CONCAT(ROUND(TABLE_ROWS/10000,2),"W") AS '行数' ,
CONCAT(ROUND(DATA_LENGTH/1024/1024,2),'M') AS '数据量' 
FROM information_schema.TABLES 
ORDER BY TABLE_ROWS DESC;
```