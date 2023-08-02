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

# linux 查询端口

```sh

#分析独立IP数量
awk '{print $1}' /usr/local/nginx/logs/zsapp.log | sort -n | uniq | wc -l

#分析独立IP数量
grep "31/Jul/2023:2[0-3]" /usr/local/nginx/logs/zsapp.log | awk '{print $1}'  | sort -n | uniq | wc -l

#分析访问量
grep "31/Jul/2023:2[0-3]" /usr/local/nginx/logs/zsapp.log | awk '{print $1}' | sort | uniq -c| sort -nr | wc -l

#统计日期访问数量
grep "31/Jul/2023:1[2-6]" /usr/local/nginx/logs/zsapp.log | wc -l
grep "01/Aug/2023:2[1-3]" /usr/local/nginx/logs/zsapp.log | wc -l

#统计21-23点访问前20
grep "31/Jul/2023:2[1-3]" /usr/local/nginx/logs/zsapp.log | awk ' {print $1}'  |sort |sort |uniq -c |sort -nr |head -20


grep "31/Jul/2023" /usr/local/nginx/logs/zsapp.log | wc -l
grep "01/Aug/2023" /usr/local/nginx/logs/zsapp.log | wc -l


grep "02/Aug/2023" /usr/local/nginx/logs/zsapp.log | grep python-requests

#查看IP访问的呢额
grep "02/Aug/2023" /usr/local/nginx/logs/zsapp.log | grep 112.225.182.135 | tail 

# 查看该Agent的访问
grep "02/Aug/2023:21" /usr/local/nginx/logs/zsapp.log | grep python-requests | tail 

grep "02/Aug/2023:21"  /usr/local/nginx/logs/zsapp.log  | awk -F '"' '{print $6}' | uniq -c | sort -nr | head -100

#分析高访问IP
grep "02/Aug/2023:21" /usr/local/nginx/logs/zsapp.log | awk ' {print $1}'  | sort |sort |uniq -c |sort -nr |head -20

grep "01/Aug/2023:21" /usr/local/nginx/logs/zsapp.log | awk ' {print $1}'  | sort |sort |uniq -c |sort -nr |head -20

#统计每秒的请求数,top100的时间点(精确到秒)
awk '{print $4}' /usr/local/nginx/logs/zsapp.log |cut -c 14-21|sort|uniq -c|sort -nr|head -n 100

#统计每分钟的请求数,top100的时间点(精确到分钟)
awk '{print $4}' /usr/local/nginx/logs/zsapp.log |cut -c 14-18|sort|uniq -c|sort -nr|head -n 100

#统计每小时的请求数,top100的时间点(精确到小时)
awk '{print $4}' /usr/local/nginx/logs/zsapp.log |cut -c 14-15|sort|uniq -c|sort -nr|head -n 100

# TOP 100 IP 
awk '{print $1}' /usr/local/nginx/logs/zsapp.log | sort -n |uniq -c | sort -rn | head -n 100

#分析截止目前为止访问量最高的IP排行
awk ' {print $1}' /usr/local/nginx/logs/zsapp.log | sort |sort |uniq -c |sort -nr |head -20

#找到当前日志中502或者404错误的页面并统计。

awk '{print $0}' /usr/local/nginx/logs/zsapp.log |egrep "404|502"|awk '{print $1,$7,$9}'|more


#性能分析
cat /usr/local/nginx/logs/zsapp.log |awk '($NF > 3){print $7}'|sort -n|uniq -c|sort -nr|head -20


tcpdump -i eth0 -tnn dst port 80 -c 1000 | awk -F"." '{print $1"."$2"."$3"."$4}' | sort| uniq -c | sort -nr


#访问最频繁的IP 
awk '{print $1}' /usr/local/nginx/logs/zsapp.log |sort | uniq -c |sort -n -k 1 -r|more


# 统计服务器端口状态
netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'

#统计端口链接数量
netstat -nat | grep -i "5001"

#查看IP 链接数

netstat -nat|awk '{print$5}'|awk -F : '{print$1}'|sort|uniq -c|sort -rn


#监控端口连接数量 每3秒执行一次
watch -n 3 'netstat -nat | grep -i "5001"'
watch -n 3 'netstat -nat | grep -i "2510"'

# 监控连接数 每3秒执行一次
watch -n 3 'netstat -n | awk \'/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}\'‘

# 查看nginx worker 分配的核心
ps -eo pid,args,psr | grep [n]ginx


# java 打印GC 信息 每3秒执行一次 打印500次
jstat  -gc  7  3000  500

```

# NGINX 