---
layout:     post
title:      "使用Consul Docker微服务平台实践"
date:       2017-03-24 10:26:00
author:     "Vincent"
header-img:  "img/post-bg-engine.jpg"
catalog: true
tags:
    - Consul
    - Linux
    - Docker
    - Registrator
    - Consul-template
---


## 基础环境

#### - CentOS6.6 内核升级
因为虚拟机的centos内核无法达到docker稳定运行，因此升级到3.1,执行

```sh
#导入key
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
#安装ELRepo到CentOS 6.6中
rpm -Uvh http://www.elrepo.org/elrepo-release-6-6.el6.elrepo.noarch.rpm
#安装长期支持版本kernel
yum --enablerepo=elrepo-kernel install kernel-lt -y
#编辑grub.conf文件，修改Grub引导顺序,选择3.1版本的内容(一般在第一个)
vim /etc/grub.conf

```
重启后 ```uname -r```检查是否是3.1的内核。

#### - device-mapper 问题

```
/usr/bin/docker: relocation error: /usr/bin/docker: symbol dm_task_get_info_with_deferred_remove, version Base not defined in file libdevmapper.so.1.02 with link time reference
```

安装device-mapper即可

```sh
    sudo yum install device-mapper-event-libs
    sudo yum reinstall docker
```


#### - Docker 镜像无法拉取
使用163的镜像，```CentOS``` 修改文件 ```/etc/sysconfig/docker```

```sh
DOCKER_OPTS="$DOCKER_OPTS --registry-mirror=http://hub-mirror.c.163.com"
```

## Consul集群安装 

- [服务发现,Consul入门](http://vnzmi.com/2016/08/16/consul-quick-guide/)

## 安装私有 Registry

Registry 是无状态、高可用的服务端应用。可以帮助我们进行Docker镜像的分发。使用Registry可以
建立内部的镜像存储和分发流程。Registry兼容Docker引擎的版本为1.6+。


**使用步骤**

```sh
#启动Registry
docker run -d -p 5000:5000 --name registry registry:2
#拉一些镜像
docker pull ubuntu
#Tag一下这样他就指向了你的Reigstry
docker tag ubuntu localhost:5000/myfirstimage
#推到库中
docker push localhost:5000/myfirstimage
#拉下来看下
docker pull localhost:5000/myfirstimage
#停止服务并删除数据
docker stop registry && docker rm -v registry

```

默认的Registry数据保存为一个docker的数据卷到宿主机的文件系统。如果你需要指定注册的数据存储到宿主机的目标使用以下语法

```
docker run -d -p 5000:5000 --restart=always --name registry  -v /var/lib/registry/data:/var/lib/registry  registry:2
```

[配置其他存储查看这里](https://docs.docker.com/registry/configuration/#storage)

如果需要外部用户来使用则需要配置SSL

```sh
mkdir -p /var/lib/registry/certs
cd /var/lib/registry/certs
openssl genrsa -des3 -passout pass:x -out ssl.pass.key 2048
openssl rsa -passin pass:x -in ssl.pass.key -out ssl.key
rm ssl.pass.key -f
openssl req -new -key ssl.key -out ssl.csr
openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt
rm -f ssl.csr
```

删除容器

```sh
docker rmi registry
cd /var/lib/registry
docker run -d -p 5000:5000 --restart=always --name registry  -v /var/lib/registry/data:/var/lib/registry  -v /var/lib/registry/certs:/certs -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/ssl.crt  -e REGISTRY_HTTP_TLS_KEY=/certs/ssl.key registry:2


docker run -p 5000:5000 --restart=always --name registry1  -v /var/lib/registry/data:/var/lib/registry  -v /var/lib/registry/certs:/certs -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/ssl.crt  -e REGISTRY_HTTP_TLS_KEY=/certs/ssl.key registry:2


docker run -p 5000:5000 --restart=always --name registry1  -v /var/lib/registry/data:/var/lib/registry registry:2

```

## 安装Registrator


### Registrator启动命令

```sh
docker run [docker options] gliderlabs/registrator[:tag] [options] <registry uri>
```

###### DOCKER参数
```--net=host``` 共用了宿主机的网络，使registrator可以获取到主机的名字IP等，也可以不使用Host模式使用-h $HOSTNAME来指定主机名，在Registrator选项中指定IP地址。

```--volume=/var/run/docker.sock:/tmp/docker.sock```  允许Registrator访问Docker的 API。
``` -e CONSUL_HTTP_TOKEN=<your acl token>``` 如果Consul使用了ACL则需要制定ACL_TOKEN

###### Registrator参数
```internal``` ,在registrator内部进行注册，注册docker内部映射的端口.而不是宿主机映射给docker的端口
```deregister <mode>```,是否注销所有服务,```always```,或者 ```on-success```,默认```always```
```ip <ip addr``` 强制registrator使用指定的IP地址来注册服务
```tags <tags>``` 使用逗号分割的tag来标记注册的服务
```-ttl <seconds>``` （后台运行时使用）服务存活期
```-ttl-refresh <seconds>``` （后台运行时使用）服务存活期
```resync <second>``` 控制registrator查询docker的容器并重新注册服务的时间间隔。每次注册均会使监控consul的进程得到通知。因此太过频繁可能会造成一些问题。默认值，0 不进行重新注册。

#### 启动命令

```sh
docker run -d --name=registrator   --net=host  --volume=/var/run/docker.sock:/tmp/docker.sock  gliderlabs/registrator:latest -tags=" `hostname`,`head /etc/issue -n 1`" --deregister=always consul://127.0.0.1:8500 
```

#### 运行Docker镜像

```sh
docker run -d -P --name=redis redis
```

运行之后我们即可在Consul里看到启动好的服务。这样注册的服务没有健康检测，仅有少量的Meta数据

#### 服务的Meta数据

Registrator 定义了如下类型：

```go
type Service struct {
    ID    string               // unique service instance ID
    Name  string               // 服务名称
    IP    string               // 服务的IP地址
    Port  int                  // 服务监听的端口
    Tags  []string             // 服务的标签
    Attrs map[string]string    // 额外的属性metadata
}
```

```Name```,```Tags```,```Attrs```,```ID```,可以通过用户定义的容器Meta数据来进行覆盖。使用前缀```SERVICE_```或者```SERVICE_x_```来设置,x是暴露的端口号码。例如 ```SERVICE_NAME=db``` ,```SERVICE_80_NAME=api``` ,```Attrs```保存余下的数据,目前Consul还不支持Attrs但是这些设置的Attrs可以用于健康检查。这些数据读取的是环境变量所以可以将默认值保存到 ```Dockerfile```里，后续也可以在```run```命令里覆盖默认设置。 

##### 注册单个服务

上面的redis注册为这样

```sh 
docker run -d -P --name=redis \
-e "SERVICE_NAME=redis1" \
-e "SERVICE_TAGS=master,session" \
-e "SERVICE_OWNER=med" \
 redis
```

#####注册多个服务端口

```sh 

docker run -d -P --name=nginx \
-e "SERVICE_80_NAME=med-svr-case-http" \
-e "SERVICE_80_TAGS=med,http,api" \
-e "SERVICE_80_OWNER=med" \
-e "SERVICE_443_NAME=med-svr-case-https" \
-e "SERVICE_443_TAGS=med,https,api" \
-e "SERVICE_443_OWNER=med" \
 nginx
 
```

#### 健康检查

##### HTTPS 检查

给容器指定额外的metadata数据

```ini
SERVICE_443_CHECK_HTTPS=/health/endpoint/path
SERVICE_443_CHECK_INTERVAL=15s
SERVICE_443_CHECK_TIMEOUT=1s  #不指定则使用Consul的默认
```

##### TCP检查

```ini
SERVICE_443_CHECK_TCP=true
SERVICE_443_CHECK_INTERVAL=15s
SERVICE_443_CHECK_TIMEOUT=3s  #不指定则使用Consul的默认
```

##### 脚本检查

脚本检查允许你在Consul里运行一个检查脚本。所以你需要确定consul的运行环境中可以正确执行这些脚本。示例：

```ini
SERVICE_CHECK_SCRIPT=curl --silent --fail example.com
```

##### TTL检查时间

```ini
SERVICE_CHECK_TTL=30s
```

##### 服务默认状态

服务被注册时默认状态是 ```critical```如果你希望设置为```passing```设置

```ini
SERVICE_CHECK_INITIAL_STATUS=passing
```















































