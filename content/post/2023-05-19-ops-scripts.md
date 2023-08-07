---
layout:     post
title:      "一些运维脚本"
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

# Docker 

```sh
#查询当前容器状态
docker stats --no-stream
docker stats $(docker ps --format={{.Names}})

#只输出指定容器
docker stats --no-stream registry mysql

#格式化输出结果
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

```

| 变量 |说明 |
| --- | --- |
|.Container  |  根据用户指定的名称显示容器的名称或 ID|
|.Name       |    容器名称|
|.ID        |         容器 ID|
|.CPUPerc   |    CPU 使用率|
|.MemUsage  |内存使用量|
|.NetIO     |      网络 I/O |     
|.BlockIO   |     磁盘 I/O|
|.MemPerc   |  内存使用率|
|.PIDs      |       PID 号|

# SQL


## 统计大表

```sql
SELECT 
CONCAT(TABLE_SCHEMA,'.',TABLE_NAME) AS '表名',
CONCAT(ROUND(TABLE_ROWS/10000,2),"W") AS '行数' ,
CONCAT(ROUND(DATA_LENGTH/1024/1024,2),'M') AS '数据量' 
FROM information_schema.TABLES 
ORDER BY TABLE_ROWS DESC;
```

# linux 

## 查询端口连接情况
```sh

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
watch -n 3 'netstat -n | awk \'/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}\''
```


# NGINX 

## 日志分析

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

# 统计请求数
grep "31/Jul/2023" /usr/local/nginx/logs/zsapp.log | wc -l
grep "01/Aug/2023" /usr/local/nginx/logs/zsapp.log | wc -l



#查看IP访问的资源
grep "02/Aug/2023" /usr/local/nginx/logs/zsapp.log | grep 112.225.182.135 | tail 

# 统计Agent访问次数
grep "02/Aug/2023" /usr/local/nginx/logs/zsapp.log | grep python-requests

# 查看该Agent的访问，最后时间
grep "02/Aug/2023:21" /usr/local/nginx/logs/zsapp.log | grep python-requests | tail 

# IP 访问前100
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


#访问最频繁的IP 
cat /usr/local/nginx/logs/zsapp.log |awk '($NF > 3){print $7}'|sort -n|uniq -c|sort -nr|head -20


tcpdump -i eth0 -tnn dst port 80 -c 1000 | awk -F"." '{print $1"."$2"."$3"."$4}' | sort| uniq -c | sort -nr


awk '{print $1}' /usr/local/nginx/logs/zsapp.log |sort | uniq -c |sort -n -k 1 -r|more

```


## Nginx 进程

```sh
# 查看nginx worker 分配的核心
ps -eo pid,args,psr | grep [n]ginx
```


## TIME_WAIT 问题

#### 原因
Nginx在实际应用中大流量情况下会出现大量```TIME_WAIT```状态，```TIME_WAIT```是因为在TCP协议中，主动关闭的一方在放送最后一个ACK之后会进入```TIME_WAIT```状态，然后等待```2*MSL```时间才会回到初始状态。因此进入```TIME_WAIT```这个连接就会被占用```2MSL```的时间。

> ```MSL``` 指报文的最长生存时间。单个```MSL```为2分钟或者1分钟。

产生这个问题主要由于：

- 大量短连接的存在
- HTTP请求 Header中 ```Connection: close``` 由服务端主动发起关闭

#### 解决

- 客户端，HTTP 头设置 ```Connection: keep-alive``` 保持连接存活一段时间，浏览器一般这样运行
- 服务端 ,允许```TIME_WAIT```的连接被重用，可能会降低稳定性。缩短MSL时间。

**使TCP连接可复用**

修改内核参数，可能会导致不稳定

```sh
vi /etc/sysctl.conf 
net.ipv4.tcp_syncookies = 1  
net.ipv4.tcp_tw_reuse=1 #让TIME_WAIT状态可以重用，这样即使TIME_WAIT占满了所有端口，也不会拒绝新的请求造成障碍 默认是0  
net.ipv4.tcp_tw_recycle=1 #让TIME_WAIT尽快回收 默认0，部分系统不支持这个选项，暂时未弄清楚为何
net.ipv4.tcp_fin_timeout=30 #时间修改有考究
#让修改生效  
/sbin/sysctl -p 
```

**upstream的```TIME_WAIT```**
NGINX作为反向代理，upstream服务器之间页会存在大量```TIME_WAIT```

增加 keepalive 设置

```conf
upstream http_backend {
    server 127.0.0.1:8080;
    keepalive 16;
}
```

>
> keepalive指令不限制nginxworker可以打开的连接总数，官方建议keepalive设置为upstream中服务器数量的两倍即可保持到所有服务器的连接，同时页足够小，upstream也可以创建新的连接。
> **keepalive指令最好放到最后面**，这个指令必须放到均衡算法指令之后。
> 

设置使用http1.1并且Connection头

```conf
server {
    ...

    location /http/ {
        proxy_pass http://http_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        ...
    }
}
```

>
> NGINX 默认使用 HTTP/1.0 连接上游服务器，并相应地将 Connection: close 标头添加到它所转发到服务器的请求中。这样尽管 upstream{} 块中包含了keepalive 指令，但每个连接仍然会在请求完成时关闭。
>


NGINX官方博客：

[https://www.nginx-cn.net/blog/avoiding-top-10-nginx-configuration-mistakes/](https://www.nginx-cn.net/blog/avoiding-top-10-nginx-configuration-mistakes/)

# JAVA

## JavaGC 

```sh
# java 打印GC 信息 每3秒执行一次 打印500次
jstat  -gc  7  3000  500
```