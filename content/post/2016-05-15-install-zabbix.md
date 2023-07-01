---
layout:     post
title:      "安装Zabbix监控"
date:       2016-05-15 20:44:00
author:     "Vincent"
image:  "img/post-bg-dot.jpg"
catalog: true
tags:
    - OP
    - 监控
---

> 
>  服务器 CentOS 6.5
> 


# 安装

因为Zabbix使用到了MySQL和PHP所以需要先安装MySQL

### 安装MySQL

```sh 
yum -y install mysql-server
```



### 安装Zabbix
服务器CentOS 6.6 安装如下

```sh
yum -y install zabbix22-web-mysql  zabbix22-server-mysql zabbix22-agent
```

创建zabbix数据库和用户,然后创建基本的数据结构

```sh
mysql> source /usr/share/zabbix-mysql/schema.sql
mysql> source /usr/share/zabbix-mysql/images.sql
mysql> source /usr/share/zabbix-mysql/data.sql
```

运行apache
```
service httpd start
```

进入 ```http://localhost/zabbix```执行安装程序

Zabbix会检查你的php.ini配置是否正确,根据提示修改即可.

然后填入数据库资料以及zabbix server的资料即可完成安装

登录账户 
> 账号:```admin``` 
> 密码:```zabbix```


# 问题

### 1. 无法选择中文语言

修改 ```/usr/share/zabbix/include/locales.inc.php``` 中的```zh_CN```的配置,如下

```php
'zh_CN' => array('name' => _('Chinese (zh_CN)'),        'display' => true),
```

可以顺手把其他多余的语言关掉

### 2. 图表中中文无法显示

因为GD库设置的字体没有中文显示,找一个中文的```tff```字体 ,比如 ```msyh.tff``` (微软雅黑) 上传到 ```/usr/share/zabbix/include``` 目录下,修改 ```/usr/share/zabbix/include/defines.inc.php``` 如下2个项:

```php
efine('ZBX_FONTPATH','/usr/share/zabbix/include'); // where to search for font (GD > 2.0.18)
define('ZBX_FONT_NAME', 'msyh');
define('ZBX_GRAPH_FONT_NAME','msyh'); // font file name
```

### 3.历史记录中文无法显示
这个是因为数据库是```latin1``` 编码,创建时改成```utf8```















