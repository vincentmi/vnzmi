---
layout:     post
title:      "使用Mesos和Docker构建你的私有云平台"
date:       2015-06-12 23:11:00
author:     "Vincent"
header-img:  "img/post-bg-line.jpg"
catalog: true
tags:
    - 运维
    - Docker
    - Mesos
---

## 安装
如果没有安装epel源先安装

    yum install epel-release

先添加mesosphere源

    sudo rpm -Uvh http://repos.mesosphere.io/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm
安装mesos 以及运算框架marathon

    yum install mesos 
    yum install marathon 

安装zookeeper

    yum install mesosphere-zookeeper


<!--more-->


## 配置Master

### 准备工作
批量操作脚本 /opt/bin/all.sh

    #!/bin/sh
    
    if [ $# -lt  1 ] 
    then
     echo 'No command . use all.sh CMD to execute command in other server '
     exit
    fi
    
    for sIP in 195 196;
    do 
       echo
       ssh root@192.168.1.${sIP} "$*"
       echo 
       
    done

加了几个Alias

    alias s2="ssh root@192.168.1.196 "
    alias s3="ssh root@192.168.1.195 "
    alias all=/opt/bin/all.sh

### 配置ZooKeeper

设置每台机器的ID,首先需要为每个Master机器设置 1 到 255的唯一ID,

    #echo 1 > /var/lib/zookeeper/myid
    #ssh root@192.168.1.196
    #echo 2 > /var/lib/zookeeper/myid
    #ssh root@192.168.1.195
    #echo 3 > /var/lib/zookeeper/myid

设置zoo.cfg,我们需要将机器的ID映射到实际的IP ,因此在每台机器增加如下内容

    #配置本机
    #echo server.1=192.168.1.198:2888:3888 >> /etc/zookeeper/conf/zoo.cfg
    #echo server.2=192.168.1.196:2888:3888 >> /etc/zookeeper/conf/zoo.cfg
    #echo server.3=192.168.1.195:2888:3888 >> /etc/zookeeper/conf/zoo.cfg
    #其他机器
    #all " echo server.1=192.168.1.198:2888:3888 >> /etc/zookeeper/conf/zoo.cfg"
    #all " echo server.2=192.168.1.196:2888:3888 >> /etc/zookeeper/conf/zoo.cfg"
    #all " echo server.3=192.168.1.195:2888:3888 >> /etc/zookeeper/conf/zoo.cfg"

### Mesos配置

为Mesos设置ZooKeeper连接

    echo zk://192.168.1.198:2181,192.168.1.196:2181,192.168.1.195:2181/mesos > /etc/mesos/zk
    all "echo zk://192.168.1.198:2181,192.168.1.196:2181,192.168.1.195:2181/mesos > /etc/mesos/zk"

设置quorum，该数值确定机器的工作正常状态，设置为机器总量的50%，我们有3台Master所以设置为2

    echo 2 >  /etc/mesos-master/quorum
    all "echo 2 >  /etc/mesos-master/quorum"

设置IP地址和Hostname,他们保存在
> /etc/mesos-master/ip
> /etc/mesos-master/hostname

执行命令

    echo 192.168.1.198 > /etc/mesos-master/ip
    echo 192.168.1.198 > /etc/mesos-master/hostname
    s2  "echo 192.168.1.196 > /etc/mesos-master/hostname"
    s2  "echo 192.168.1.196 > /etc/mesos-master/ip"
    s3  "echo 192.168.1.195 > /etc/mesos-master/ip"
    s3  "echo 192.168.1.195 > /etc/mesos-master/hostname"

### Marathon配置

我们将在每个Master上运行Marathon实例，但是只有被推选出的Leader才会安排任务。其他的实例只将请求转发到Leader.Marathon的配置目录没有自动创建。需要手动进行创建。

    mkdir -p /etc/marathon/conf
    cp /etc/mesos-master/hostname /etc/marathon/conf
    all mkdir -p /etc/marathon/conf
    all cp /etc/mesos-master/hostname /etc/marathon/conf

设置ZooKeeper连接资料，因为和Mesos是一样的所以直接拷贝

    sudo cp /etc/mesos/zk /etc/marathon/conf/master
    all cp /etc/mesos/zk /etc/marathon/conf/master
    
这个连接允许我们读取到Mesos的集群。Marathon也需要存储自己的资料到ZooKeeper.
将连接修改下。

    echo zk://192.168.1.198:2181,192.168.1.196:2181,192.168.1.195:2181/marathon > /etc/marathon/conf/zk
    all "echo zk://192.168.1.198:2181,192.168.1.196:2181,192.168.1.195:2181/marathon > /etc/marathon/conf/zk"

 配置完成了

### 应用配置

下面需要重启服务来应用配置，先要确定我们的master只运行了Mater进程，先关闭 mesos的slave进程,并禁止开机启动。

    systemctl stop mesos-slave.service
    systemctl disable mesos-slave.service
    all systemctl stop mesos-slave.service
    all systemctl disable mesos-slave.service

下面启动服务

    systemctl restart zookeeper.service
    all systemctl restart zookeeper.service
    systemctl restart mesos-master.service
    all systemctl restart mesos-master.service
    systemctl restart marathon.service
    all systemctl restart marathon.service

完成后浏览器输入，其中一台Master检查

    http://192.168.1.198:5050/

如下图,如果你不是访问的Leader会被自动跳转到其他Leader服务器。
![/img/in-post/55670412.png](/img/in-post/55670412.png)


Marathon在8080端口
![2015-06-14_002056.png](/img/in-post/1713485223.png)

## 配置Slave

先禁用掉Slave上的mesos-master服务

    systemctl stop mesos-master.service
    systemctl disable mesos-master.service


#### 配置ZooKeeper

    echo zk://192.168.1.198:2181,192.168.1.196:2181,192.168.1.195:2181/mesos > /etc/mesos/zk

#### 设置IP和Hostname

    echo 192.168.1.201 > /etc/mesos-slave/ip
    echo 192.168.1.201 > /etc/mesos-slave/hostname
#### 启动Slave服务

    systemctl stop mesos-slave.service


## 参考文档

- [How To Configure a Production-Ready Mesosphere Cluster on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-configure-a-production-ready-mesosphere-cluster-on-ubuntu-14-04)
- [下一代云计算平台Apache Mesos定制自己的PaaS-1(Apache Mesos安装部署)](http://wiselyman.iteye.com/blog/2200267)



