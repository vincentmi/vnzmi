---
layout:     post
title:      "集群安装Hadoop系列组件"
date:       2016-07-11 18:44:00
author:     "Vincent"
image:  "img/post-bg-line.jpg"
catalog: true
tags:
    - 大数据
    - Hadoop
    - HBase
    - Kafka
    - ZooKeeper
---
> 公司日志系统扩容,考虑到后续数据暴增,选用HBase来进行存储,在本地VM进行一下演练
> 记录下安装过程备查


> 配置之前请查阅兼容列表
> 目前安装的版本 HADOOP-2.5.2  HBASE-1.1.5 
>

# Hadoop 安装

### 1.配置
选择4台虚拟机作整个集群,配置如下

```
hdp1 10.0.0.30 #master
hdp2 10.0.0.31 #datanode
hdp3 10.0.0.32 #datanode
hdp4 10.0.0.33 #datanode
```
### 2.工具
远程执行命令

```sh
#!/bin/sh
#/opt/hdp/hdp_ssh
for i in 31 32 33 41 42 43; do
 echo -e "\033[33m - 10.0.0.${i} -  \033[0m"
 ssh root@10.0.0.$i $*
done ;
```

远程执行命令,无额外输出

```sh
#!/bin/sh
#/opt/hdp/hdp_cmd
for i in 31 32 33 41 42 43; do
 #echo -e "\033[33m - 10.0.0.${i} -  \033[0m"
 ssh root@10.0.0.$i $*
done ;
```

加了2个alias

```sh
#~/.bash_profile
alias r=/opt/hdp_ssh
alias rcp=/opt/hdp_scp
alias vi=vim
export HDP=/opt/hdp/hadoop-2.5.2
```
上传文件到主机

```sh
#!/bin/sh
#/opt/hdp/hdp_scp
for i in 31 32 33 41 42 43; do
  echo -e "\033[33m - 10.0.0.${i} -  \033[0m"
  scp -r $1 root@10.0.0.$i:$2
done ;
```

### 3.基础准备

##### 3.1 安装JAVA
hadoop推荐使用官方的JDK,所以先删除旧的jdk . 
因为我是新装没有这一步.

```sh
$ rpm -qa|grep openjdk -i #查找已经安装的OpenJDK，-i表示忽略“openjdk”的大小写
$ sudo yum remove java-1.6.0-openjdk-devel-1.6.0.0-6.1.13.4.el7_0.x86_64 \
java-1.7.0-openjdk-devel-1.7.0.65-2.5.1.2.el7_0.x86_64 \
java-1.7.0-openjdk-headless-1.7.0.65-2.5.1.2.el7_0.x86_64 \
java-1.7.0-openjdk-1.7.0.65-2.5.1.2.el7_0.x86_64 \
java-1.6.0-openjdk-1.6.0.0-6.1.13.4.el7_0.x86_64
```

下载官方JDK,解压拷贝到 ```/usr/lib/jdk```

```sh
$tar -zxf jdk-8u60-linux-x64.tar.gz -C /usr/lib/jdk 
```
检查下确保 ```/usr/lib/jdk/bin/java -version```可以显示内容类似即可.

```
[root@hdp1 opt]# /usr/lib/jdk/bin/java -version
java version "1.8.0_91"
Java(TM) SE Runtime Environment (build 1.8.0_91-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.91-b14, mixed mode)
```

环境变量,附加到 ```/etc/profile``` 的最后

```sh
## JAVA Environment
export JAVA_HOME=/usr/lib/jdk
export JRE_HOME=/usr/lib/jdk
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
export CLASSPATH=$CLASSPATH:.:$JAVA_HOME/lib:$JRE_HOME/lib
## JAVA Environment END
```

##### 3.2 SSH配置

SSH需要配置允许hadoop机器之间可以免密码访问.使用ssh key来实现.

打开ssh 的key登录

```sh
#/etc/ssh/sshd_config 去掉以下三行的注释
RSAAuthentication yes
PubkeyAuthentication yes
AuthorizedKeysFile      .ssh/authorized_keys
```

生成每台机器的ssh-key

```sh
ssh-keygen 
```
更新每台机器的host-key,CentOS只需要删除原来的Key重启即可.

```sh
rm -f /etc/ssh/ssh_host_*
service sshd restart
```
将Key文件收集起来.在hdp1机器上执行

```sh
# 将hdp1的key加入文件
cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
# 将其他机器的key附加到authorized_keys
/opt/hdp/hdp_cmd cat /root/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
# 修改权限
chmod 600 ~/.ssh/authorized_keys
# 拷贝到其他机器
/opt/hdp/hdp_scp /root/.ssh/authorized_keys /root/.ssh/authorized_keys
```

收集服务器Key,这样就不用再ssh登录时还要打个Y

```sh
# 将hdp1的key加入文件
cat /etc/ssh/ssh_host_rsa_key.pub > ~/.ssh/known_hosts
# 将其他机器的key附加到known_hosts
/opt/hdp/hdp_cmd cat /etc/ssh/ssh_host_rsa_key.pub >> ~/.ssh/known_hosts
```

完成后需要进行一下,在key前面加上IP地址和主机名

```sh
hdp4 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAv3OFg8gwErGimjmtXAZ5wJBC/yA3WUcDKIGnpX8p/V5/yAoX11ZSgzw6wUSHh7qb5nU4yz/OafvLC48LEtT1NywZ7vfKANJ2hB/JxMxiInRAHDEVinujE7oZkSHSBBvCRcPqYx3uA6fAgxukAZmNEM7IdxUtIkBqIntNBq/OESQrZzqnB8sedSJP4hOFYN6UOWQED/V50ZK6iKZMUcFCQBzYulY3WiDMe4rKMDbyfaz9QzCvkHo82CvbjWg2i9DVyq4fPbXqd6E8cMznmV8PYPZTQhuIiJSkxboD4ui6s4/HdD3IShuxlXOaZR9WVq87WqU6UdxaFo9IiPFL8dtazw==
10.0.0.33 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAv3OFg8gwErGimjmtXAZ5wJBC/yA3WUcDKIGnpX8p/V5/yAoX11ZSgzw6wUSHh7qb5nU4yz/OafvLC48LEtT1NywZ7vfKANJ2hB/JxMxiInRAHDEVinujE7oZkSHSBBvCRcPqYx3uA6fAgxukAZmNEM7IdxUtIkBqIntNBq/OESQrZzqnB8sedSJP4hOFYN6UOWQED/V50ZK6iKZMUcFCQBzYulY3WiDMe4rKMDbyfaz9QzCvkHo82CvbjWg2i9DVyq4fPbXqd6E8cMznmV8PYPZTQhuIiJSkxboD4ui6s4/HdD3IShuxlXOaZR9WVq87WqU6UdxaFo9IiPFL8dtazw==
```

然后拷贝到其他机器

```sh
/opt/hdp/hdp_scp /root/.ssh/known_hosts /root/.ssh/known_hosts
```

编辑Host文件

```sh 
hdp1 10.0.0.30 #master
hdp2 10.0.0.31 #datanode
hdp3 10.0.0.32 #datanode
hdp4 10.0.0.33 #datanode
```

拷贝到其他机器

```sh
/opt/hdp/hdp_scp /etc/hosts /etc
```


在每台机器重启sshd  ```service sshd restart```即可.
可以在任意一台机器使用 ```ssh hdp1``` 进行登录,没有任何提示即可

### 4.HADOOP 配置

文件目录如下

```sh
[root@hdp1 hdp]# pwd
/opt/hdp
[root@hdp1 hdp]# ls
hadoop-2.5.2  hbase-1.1.5  test  zookeeper-3.4.8
```

##### 4.1 需要配置如下文件

```
/opt/hdp/hadoop-2.5.2/etc/hadoop/hadoop-env.sh
/opt/hdp/hadoop-2.5.2/etc/hadoop/yarn-env.sh
/opt/hdp/hadoop-2.5.2/etc/hadoop/slaves
/opt/hdp/hadoop-2.5.2/etc/hadoop/core-site.xml
/opt/hdp/hadoop-2.5.2/etc/hadoop/hdfs-site.xml
/opt/hdp/hadoop-2.5.2/etc/hadoop/mapred-site.xml
/opt/hdp/hadoop-2.5.2/etc/hadoop/yarn-site.xml
```

修改hadoop-env.sh 和yarn-env.sh 的 JAVA_HOME . 

```sh
# The java implementation to use.
export JAVA_HOME=/usr/lib/jdk
```

修改slave文件

```
hdp2
hdp3
hdp4
```

core-site.xml 文件设置端口信息

```xml
<configuration>
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://hdp1:9000</value>
</property>
<property>
    <name>io.file.buffer.size</name>
    <value>131072</value>
</property>
<property>
    <name>hadoop.tmp.dir</name>
    <value>file:/hdp/tmp</value>
    <description>Abasefor other temporary directories.</description>
</property>
<property>
    <name>hadoop.proxyuser.spark.hosts</name>
    <value>*</value>
</property>
<property>
    <name>hadoop.proxyuser.spark.groups</name>
    <value>*</value>
</property>
</configuration>
```

hdfs-site.xml 设置DFS的路径

```xml
<configuration>
<property>
      <name>dfs.namenode.secondary.http-address</name>
      <value>master:9001</value>
</property>
<property>
    <name>dfs.namenode.name.dir</name>
    <value>file:/hdp/dfs/name</value>
</property>
<property>
    <name>dfs.datanode.data.dir</name>
    <value>file:/hdp/dfs/data</value>
</property>
<property>
    <name>dfs.replication</name>
    <value>3</value>
</property>
<property>
    <name>dfs.webhdfs.enabled</name>
    <value>true</value>
</property>
</configuration>
```

 mapred-site.xml 
 
```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.address</name>
        <value>hdp1:10020</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.webapp.address</name>
        <value>hdp1:19888</value>
    </property>
</configuration>
```

yarn-site.xml 

```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <property>
        <name>yarn.resourcemanager.address</name>
        <value>hdp1:8032</value>
    </property>
    <property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>hdp1:8030</value>
    </property>
    <property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>hdp1:8035</value>
    </property>
    <property>
        <name>yarn.resourcemanager.admin.address</name>
        <value>hdp1:8033</value>
    </property>
    <property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>hdp1:8088</value>
    </property>
</configuration>
```


**ulimit配置**
HBase运行时会打卡很多句柄,因此需要修改可打开的最大句柄数量和最大进程数量,修改文件```/etc/security/limits.conf ``` ,原始内容如下

```sh
#<domain>      <type>  <item>         <value>
#*               soft    core            0
#*               hard    rss             10000
#@student        hard    nproc           20
#@faculty        soft    nproc           20
#@faculty        hard    nproc           50
#ftp             hard    nproc           0
#@student        -       maxlogins       4
```
修改对Hadoop的限制

```sh
# 以下内容添加到 /etc/security/limits.conf  文件后面
* hard nofile 10000
* soft nofile 10000 
* hard nproc 10000
* soft nproc 10000
```
然后重启所有机器 让配置生效,```*``` 可以换成你运行Hadoop的用户名.

将配置好的文件拷贝到所有机器

##### 4.2 格式化

```sh
# 格式化文件系统
/opt/hdp/hadoop-2.5.2/bin/hdfs namenode -format
# 启动dfs
/opt/hdp/hadoop-2.5.2/sbin/sbin/start-dfs.sh 
# 启动yarn
/opt/hdp/hadoop-2.5.2/sbin/sbin/start-yarn.sh 
# HDFS报告
/opt/hdp/hadoop-2.5.2/bin/hdfs dfsadmin -report
```

查看集群状态

[http://hadoop1:50070/](HDFS)

[http://hadoop1:8088/](RM)


#### TIPS

- 执行控制台时可能会出现这个错误

```sh
WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
```

原因是因为Hadoop编译好的Native库有一个依赖库版本和操作系统的不一致.解决方法是自己重新编译. 可以使用``ldd```命令查看依赖库的情况.

```sh
[root@hdp1 hadoop-2.5.2]# ldd lib/native/libhadoop.so.1.0.0
lib/native/libhadoop.so.1.0.0: /lib64/libc.so.6: version `GLIBC_2.14' not found (required by lib/native/libhadoop.so.1.0.0)
	linux-vdso.so.1 =>  (0x00007fffdcb29000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007f07ef2b5000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f07eef20000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f07ef6db000)
```

修改 ```/opt/hdp/hadoop-2.5.2/etc/hadoop/log4j.properties```增加下面一行可以屏蔽掉这个错误.

```
log4j.logger.org.apache.hadoop.util.NativeCodeLoader=DEBUG
```


### 5.HBase 配置

##### 5.1  服务器

```
## HBASE HOSTS
10.0.0.41 p1  # HMaser zkMaster
10.0.0.42 p2  # HMaster backup zk 
10.0.0.43 p3
10.0.0.44 p4

```

和Hadoop类似,拷贝各个的key到authorized_keys已经known_hosts使主机之间可以无密码登录.

hbase-env.sh

```sh
export JAVA_HOME=/usr/lib/jdk
```

配置```hbase-site.xml``` , 配置Hbase的数据存放到hdfs的/hbase目录下 . 设置zk的数据路径

```xml
<configuration>
<property>
   <name>hbase.rootdir</name>
   <value>hdfs://hdp1:9000/hbase</value>
</property>
<property>
   <name>hbase.cluster.distributed</name>
   <value>true</value>
</property>
<property>
   <name>hbase.zookeeper.quorum</name>
   <value>p1,p2,p3</value>
</property>
<property>
   <name>hbase.zookeeper.property.dataDir</name>
   <value>/opt/zk</value>
</property>
</configuration>
```


启动HBase

```sh
/opt/hdp/hbase-1.1.5/bin/start-hbase.sh
```

用JPS检查整个集群的进程

```sh 
[root@hdp1 hbase-1.1.5]# r /usr/lib/jdk/bin/jps
 - 10.0.0.31 -
2289 NodeManager
2613 Jps
2200 DataNode
 - 10.0.0.32 -
2179 DataNode
2587 Jps
2268 NodeManager
 - 10.0.0.33 -
2517 Jps
2198 NodeManager
2109 DataNode
 - 10.0.0.41 -
2167 HMaster
1803 HQuorumPeer
2700 Jps
 - 10.0.0.42 -
2274 HMaster
1781 HQuorumPeer
2697 Jps
2203 HRegionServer
 - 10.0.0.43 -
2340 Jps
1672 HQuorumPeer
2012 HRegionServer
```




访问 [http://p1:16010/](http://p1:16010/)查看HBase运行情况

也可以启动REST API 玩玩. 

```sh 
/opt/hdp/hbase-1.1.5/bin/hbase rest start -p 8888
# 可以通过 http://p1:8888/test/schema访问 test表的schema
```



##### 5.2 错误问题


```sh
java.net.NoRouteToHostException: 没有到主机的路由
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method)
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717)
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361)
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081)
2016-07-12 14:32:26,877 INFO  [main-SendThread(hdp1:2181)] zookeeper.ClientCnxn: Opening socket connection to server hdp1/10.0.0.30:2181. Will not attempt to authenticate using SASL (unknown error)
2016-07-12 14:32:26,878 INFO  [main-SendThread(hdp1:2181)] zookeeper.ClientCnxn: Socket connection established to hdp1/10.0.0.30:2181, initiating session
2016-07-12 14:32:26,879 INFO  [main-SendThread(hdp1:2181)] zookeeper.ClientCnxn: Unable to read additional data from server sessionid 0x0, likely server has closed socket, closing socket connection and attempting reconnect
2016-07-12 14:32:27,325 INFO  [main-SendThread(hdp3:2181)] zookeeper.ClientCnxn: Opening socket connection to server hdp3/10.0.0.32:2181. Will not attempt to authenticate using SASL (unknown error)
```

出现该错误是因为端口没打开,关闭```service iptables stop``` 防火墙即可.


# 6 安装Kafka

Kafka的安装非常简单,解压后修改配置文件















