---
layout:     post
title:      "服务发现,Consul入门"
date:       2016-08-16 18:56:00
author:     "Vincent"
image:  "img/post-bg-dot.jpg"
catalog: true
tags:
    - Consul
    - SOA
---




翻译自官方文档 .

欢迎进入Consul的入门指南!这个指南是开始使用Consul的起点,通过这个指南了解Consul是什么,他可以解决哪些问题.它与现有软件的比较和怎么开始使用它.如果你对Consul已经有基本的了解,可以阅读 [文档](https://www.consul.io/docs/) ,它提供更多可用特性的参考.


###英文原版
[https://www.consul.io/intro/](https://www.consul.io/intro/)

### 翻译

 工作需要看了下,顺便翻译了。翻译有不当的地方请帮忙指正。

Vincent Mi   [http://vnzmi.com](http://vnzmi.com)  
miwenshu#gmail.com  # Summary

—


Consul包含多个组件,但是作为一个整体,为你的基础设施提供服务发现和服务配置的工具.他提供以下关键特性:

- **服务发现** Consul的客户端可用提供一个服务,比如 api 或者mysql ,另外一些客户端可用使用Consul去发现一个指定服务的提供者.通过DNS或者HTTP应用程序可用很容易的找到他所依赖的服务.

- **健康检查** Consul客户端可用提供任意数量的健康检查,指定一个服务(比如:webserver是否返回了200 OK 状态码)或者使用本地节点(比如:内存使用是否大于90%). 这个信息可由operator用来监视集群的健康.被服务发现组件用来避免将流量发送到不健康的主机.

- **Key/Value存储** 应用程序可用根据自己的需要使用Consul的层级的Key/Value存储.比如动态配置,功能标记,协调,领袖选举等等,简单的HTTP API让他更易于使用. 

- **多数据中心**: Consul支持开箱即用的多数据中心.这意味着用户不需要担心需要建立额外的抽象层让业务扩展到多个区域.

Consul面向DevOps和应用开发者友好.是他适合现代的弹性的基础设施.


# 基础架构

Consul是一个分布式高可用的系统. 这节将包含一些基础,我们忽略掉一些细节这样你可以快速了解Consul是如何工作的.如果要了解更多细节,请参考深入的架构描述.

每个提供服务给Consul的阶段都运行了一个Consul agent . 发现服务或者设置和获取 key/value存储的数据不是必须运行agent.这个agent是负责对节点自身和节点上的服务进行健康检查的.

Agent与一个和多个Consul Server 进行交互.Consul Server 用于存放和复制数据.server自行选举一个领袖.虽然Consul可以运行在一台server , 但是建议使用3到5台来避免失败情况下数据的丢失.每个数据中心建议配置一个server集群.

你基础设施中需要发现其他服务的组件可以查询任何一个Consul 的server或者 agent.Agent会自动转发请求到server .

每个数据中运行了一个Consul server集群.当一个跨数据中心的服务发现和配置请求创建时.本地Consul Server转发请求到远程的数据中心并返回结果.

## 使用Consul

Consul集群的每个节点都必须先安装Consul.安装非常容易,Consul发布为所支持的平台和架构的二进制包.这个指南不包含从源代码编译Consul的内容.

## 安装Consul

安装Consul,找到适合你系统的包下载他.Consul打包为一个'Zip'文件.

下载后解开压缩包.拷贝Consul到你的PATH路径中,在Unix系统中```~/bin```和```/usr/local/bin```是通常的安装目录.根据你是想为单个用户安装还是给整个系统安装来选择.在Windows系统中有可以安装到```%PATH%```的路径中.

### OS X ###

如果你使用```homebrew```作为包管理器,你可以使用命令 

```sh
brew install consul
```

来进行安装.

## 验证安装

完成安装后,通过打开一个新终端窗口检查```consul```安装是否成功.通过执行 ```consul```你应该看到类似下面的输出

```
[root@hdp2 ~]# consul
usage: consul [--version] [--help] <command> [<args>]

Available commands are:
    agent          Runs a Consul agent
    configtest     Validate config file
    event          Fire a new event
    exec           Executes a command on Consul nodes
    force-leave    Forces a member of the cluster to enter the "left" state
    info           Provides debugging information for operators
    join           Tell Consul agent to join cluster
    keygen         Generates a new encryption key
    keyring        Manages gossip layer encryption keys
    leave          Gracefully leaves the Consul cluster and shuts down
    lock           Execute a command holding a lock
    maint          Controls node or service maintenance mode
    members        Lists the members of a Consul cluster
    monitor        Stream logs from a Consul agent
    reload         Triggers the agent to reload configuration files
    rtt            Estimates network round trip time between nodes
    version        Prints the Consul version
    watch          Watch for changes in Consul
```

如果你得到一个```consul not be found```的错误,你的```PATH```可能没有正确设置.请返回检查你的```consul```的安装路径是否包含在```PATH```中.

# 运行Agent

完成Consul的安装后,必须运行agent. agent可以运行为server或client模式.每个数据中心至少必须拥有一台server . 建议在一个集群中有3或者5个server.部署单一的server,在出现失败时会不可避免的造成数据丢失.

其他的agent运行为client模式.一个client是一个非常轻量级的进程.用于注册服务,运行健康检查和转发对server的查询.agent必须在集群中的每个主机上运行.

查看启动数据中心的细节请查看[这里](https://www.consul.io/docs/guides/bootstrapping.html).

## 启动 Agent

为了更简单,现在我们将启动Consul agent的开发模式.这个模式快速和简单的启动一个单节点的Consul.这个模式不能用于生产环境,因为他不持久化任何状态.

```
[root@hdp2 ~]# consul agent -dev
==> Starting Consul agent...
==> Starting Consul agent RPC...
==> Consul agent running!
         Node name: 'hdp2'
        Datacenter: 'dc1'
            Server: true (bootstrap: false)
       Client Addr: 127.0.0.1 (HTTP: 8500, HTTPS: -1, DNS: 8600, RPC: 8400)
      Cluster Addr: 10.0.0.52 (LAN: 8301, WAN: 8302)
    Gossip encrypt: false, RPC-TLS: false, TLS-Incoming: false
             Atlas: <disabled>

==> Log data will now stream in as it occurs:

    2016/08/17 15:20:41 [INFO] serf: EventMemberJoin: hdp2 10.0.0.52
    2016/08/17 15:20:41 [INFO] serf: EventMemberJoin: hdp2.dc1 10.0.0.52
    2016/08/17 15:20:41 [INFO] raft: Node at 10.0.0.52:8300 [Follower] entering Follower state
    2016/08/17 15:20:41 [INFO] consul: adding LAN server hdp2 (Addr: 10.0.0.52:8300) (DC: dc1)
    2016/08/17 15:20:41 [INFO] consul: adding WAN server hdp2.dc1 (Addr: 10.0.0.52:8300) (DC: dc1)
    2016/08/17 15:20:41 [ERR] agent: failed to sync remote state: No cluster leader
    2016/08/17 15:20:42 [WARN] raft: Heartbeat timeout reached, starting election
    2016/08/17 15:20:42 [INFO] raft: Node at 10.0.0.52:8300 [Candidate] entering Candidate state
    2016/08/17 15:20:42 [DEBUG] raft: Votes needed: 1
    2016/08/17 15:20:42 [DEBUG] raft: Vote granted from 10.0.0.52:8300. Tally: 1
    2016/08/17 15:20:42 [INFO] raft: Election won. Tally: 1
    2016/08/17 15:20:42 [INFO] raft: Node at 10.0.0.52:8300 [Leader] entering Leader state
    2016/08/17 15:20:42 [INFO] raft: Disabling EnableSingleNode (bootstrap)
    2016/08/17 15:20:42 [DEBUG] raft: Node 10.0.0.52:8300 updated peer set (2): [10.0.0.52:8300]
    2016/08/17 15:20:42 [INFO] consul: cluster leadership acquired
    2016/08/17 15:20:42 [DEBUG] consul: reset tombstone GC to index 2
    2016/08/17 15:20:42 [INFO] consul: member 'hdp2' joined, marking health alive
    2016/08/17 15:20:42 [INFO] consul: New leader elected: hdp2
    2016/08/17 15:20:43 [INFO] agent: Synced service 'consul'
```

如你所见,Consul Agent 启动并输出了一些日志数据.从这些日志中你可以看到,我们的agent运行在server模式并且声明作为一个集群的领袖.额外的本地镀锌被标记为一个健康的成员.

> OS X用户注意: Consul 使用你的主机hostname作为默认的节点名字.如果你的主机名包含时间,到这个节点的DNS查询将不会工作.为了避免这个情况,使用```-node```参数来明确的设置node名.

## 集群成员

新开一个终端窗口运行```consul members```, 你可以看到Consul集群的成员.下一节我们将讲到加入集群.现在你应该只能看到一个成员,就是你自己:

```
[root@hdp2 ~]# consul members
Node  Address         Status  Type    Build  Protocol  DC
hdp2  10.0.0.52:8301  alive   server  0.6.4  2         dc1
```

这个输出显示我们自己的节点.运行的地址,健康状态,自己在集群中的角色,版本信息.添加```-detialed```选项可以查看到额外的信息.

```members```命令的输出是基于[gossip](https://www.consul.io/docs/internals/gossip.html)协议是最终一致的.意味着,在任何时候,通过你本地agent看到的结果可能不是准确匹配server的状态.为了查看到一致的信息,使用HTTP API(将自动转发)到Consul Server上去进行查询:

```
[root@hdp2 ~]#  curl localhost:8500/v1/catalog/nodes
[{"Node":"hdp2","Address":"10.0.0.52","TaggedAddresses":{"wan":"10.0.0.52"},"CreateIndex":3,"ModifyIndex":4}]
```
除了HTTP API ,DNS 接口也可以用来查询节点.注意,你必须确定将你的DNS查询指向Consul agent的DNS服务器,这个默认运行在 ```8600```端口.DNS条目的格式(例如:"Armons-MacBook-Air.node.consul")将在后面讲到.

```
$ dig @127.0.0.1 -p 8600 Armons-MacBook-Air.node.consul
...

;; QUESTION SECTION:
;Armons-MacBook-Air.node.consul.    IN  A

;; ANSWER SECTION:
Armons-MacBook-Air.node.consul. 0 IN    A   172.20.20.11
```

## 停止Agent

你可以使用Ctrl-C 优雅的关闭Agent. 中断Agent之后你可以看到他离开了集群并关闭.

在退出中,Consul提醒其他集群成员,这个节点离开了.如果你强行杀掉进程.集群的其他成员应该能检测到这个节点失效了.当一个成员离开,他的服务和检测也会从目录中移除.当一个成员失效了,他的健康状况被简单的标记为危险,但是不会从目录中移除.Consul会自动尝试对失效的节点进行重连.允许他从某些网络条件下恢复过来.离开的节点则不会再继续联系.

此外,如果一个agent作为一个服务器,一个优雅的离开是很重要的,可以避免引起潜在的可用性故障影响达成[一致性协议](https://www.consul.io/docs/internals/consensus.html).

查看[这里](https://www.consul.io/docs/internals/consensus.html)了解添加和移除server.# 注册服务

在之前的步骤我们运行了第一个agent.看到了集群的成员,查询节点,在这个指南我们将注册我们的第一个服务并查询这些服务.

## 定义一个服务

可以通过提供服务定义或者调用HTTP API来注册一个服务.服务定义文件是注册服务的最通用的方式.所以我们将在这一步使用这种方式.我们将会建立在前一步我们覆盖的代理配置。

首先,为Consul配置创建一个目录.Consul会载入配置文件夹里的所有配置文件.在Unix系统中通常类似 ```/etc/consul.d``` (.d 后缀意思是这个路径包含了一组配置文件).

```
$ sudo mkdir /etc/consul.d
```
然后,我们将编写服务定义配置文件.假设我们有一个名叫```web```的服务运行在 80端口.另外,我们将给他设置一个标签.这样我们可以使用他作为额外的查询方式:

```
echo '{"service": {"name": "web", "tags": ["rails"], "port": 80}}' \
    >/etc/consul.d/web.json
```
现在重启agent , 设置配置目录:

```
$ consul agent -dev -config-dir /etc/consul.d
==> Starting Consul agent...
...
    [INFO] agent: Synced service 'web'
...
```

你可能注意到了输出了 "synced" 了 web这个服务.意思是这个agent从配置文件中载入了服务定义,并且成功注册到服务目录.

如果你想注册多个服务,你应该在Consul配置目录创建多个服务定义文件.


## 查询服务

一旦agent启动并且服务同步了.我们可以通过DNS或者HTTP的API来查询服务.


### DNS API

让我们首先使用DNS API来查询.在DNS API中,服务的DNS名字是 ```NAME.service.consul```. 虽然是可配置的,但默认的所有DNS名字会都在```consul```命名空间下.这个子域告诉Consul,我们在查询服务,```NAME```则是服务的名称.

对于我们上面注册的Web服务.它的域名是 ```web.service.consul``` : 

```
[root@hdp2 consul.d]# dig @127.0.0.1 -p 8600 web.service.consul

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.47.rc1.el6 <<>> @127.0.0.1 -p 8600 web.service.consul
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 46501
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;web.service.consul.        IN      A

;; ANSWER SECTION:
web.service.consul.     0       IN      A       10.0.0.52

;; Query time: 0 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Wed Aug 17 19:07:05 2016
;; MSG SIZE  rcvd: 70
```

如你所见,一个```A```记录返回了一个可用的服务所在的节点的IP地址.```A``记录只能设置为IP地址. 有也可用使用 DNS API 来接收包含 地址和端口的 SRV记录:

```
[root@hdp2 ~]# dig @127.0.0.1 -p 8600 web.service.consul SRV

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.47.rc1.el6 <<>> @127.0.0.1 -p 8600 web.service.consul SRV
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 33415
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;web.service.consul.        IN      SRV

;; ANSWER SECTION:
web.service.consul.     0       IN      SRV     1 1 80 hdp2.node.dc1.consul.

;; ADDITIONAL SECTION:
hdp2.node.dc1.consul.   0       IN      A       10.0.0.52

;; Query time: 1 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Thu Aug 18 10:40:48 2016
;; MSG SIZE  rcvd: 130
```
```SRV```记录告诉我们 ```web``` 这个服务运行于节点```hdp2.node.dc1.consul``` 的```80```端口. DNS额外返回了节点的A记录.


最后,我们也可以用 DNS API 通过标签来过滤服务.基于标签的服务查询格式为```TAG.NAME.service.consul```. 在下面的例子中,我们请求Consul返回有 ```rails```标签的 ```web```服务.我们成功获取了我们注册为这个标签的服务:

```
[root@hdp2 ~]# dig @127.0.0.1 -p 8600 rails.web.service.consul SRV

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.47.rc1.el6 <<>> @127.0.0.1 -p 8600 rails.web.service.consul SRV
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 3517
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;rails.web.service.consul.      IN      SRV

;; ANSWER SECTION:
rails.web.service.consul. 0     IN      SRV     1 1 80 hdp2.node.dc1.consul.

;; ADDITIONAL SECTION:
hdp2.node.dc1.consul.   0       IN      A       10.0.0.52

;; Query time: 1 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Thu Aug 18 11:26:17 2016
;; MSG SIZE  rcvd: 142
```

### HTTP API

除了DNS API之外,HTTP API也可以用来进行服务查询:

```
[root@hdp2 ~]# curl http://localhost:8500/v1/catalog/service/web
[{"Node":"hdp2","Address":"10.0.0.52","ServiceID":"web","ServiceName":"web","ServiceTags":["rails"],"ServiceAddress":"","ServicePort":80,"ServiceEnableTagOverride":false,"CreateIndex":4,"ModifyIndex":254}]
```

目录API给出所有节点提供的服务.稍后我们会像通常的那样带上健康检查进行查询.就像DNS内部处理的那样.这是只查看健康的实例的查询方法:

```
[root@hdp2 ~]# curl http://localhost:8500/v1/catalog/service/web?passing
[{"Node":"hdp2","Address":"10.0.0.52","ServiceID":"web","ServiceName":"web","ServiceTags":["rails"],"ServiceAddress":"","ServicePort":80,"ServiceEnableTagOverride":false,"CreateIndex":4,"ModifyIndex":254}]
```

### 更新服务

服务定义可以通过配置文件并发送```SIGHUP```给agent来进行更新.这样你可以让你在不关闭服务或者保持服务请求可用的情况下进行更新.

另外 HTTP API可以用来动态的添加,移除和修改服务.



# 建立集群

我们开始了第一个agent并且在agent上注册并查询了服务.这些展示了Consul是如何的易用.但是我们还不知道Consul如何进行扩容成一个可扩展,面向生成环境的服务发现架构.这一章我们将创建我们第一个拥有多个成员的真正的集群.

当一个agent启动时,他开始不知道其他节点的信息,他是一个成员的孤立集群.为了了解其他集群成员这个agent必须加入一个已经存在的集群.要加入一个已经存在的集群,只需要知道一个已经存在的集群成员.通过与这个成员的沟通来发现其他成员,Consul agent可以加入任何agent而不只是出于server模式的agent.

## 启动Agent 

>
> 官方版本教程里使用了Vagrant来启动虚拟机.我已经创建了多个虚拟机
> 因此跳过这部分
>

我们启动了另外的2台主机,10.0.0.53 ,10.0.0.54 和之前安装的方式一样,将consul拷贝到```PATH```目录完成安装.

在之前的示例中,我们使用了```-dev```参数来快速的创建一个开发模式的server.然而这并不能充分的在集群环境下使用.现在我们将忽略掉```-dev```标签,用我们的集群选项来替换他.

每个集群中的节点都必须要一个唯一的名字.Consul默认会使用机器的hostname.我们可以使用```-node```手动覆盖他.

我们也可以使用[-bind](https://www.consul.io/docs/agent/options.html#_bind)指定一个绑定的地址让Consul在这个地址上进行监听,这个地址必须可以被其他集群成员访问到.绑定地址不是必须提供,Consul选择第一个私有IP进行监听,不过最好还是指定一个.生产环境的服务器通常有多个网络接口.所以指定一个不会让Consul绑错网络接口.

第一个节点将扮演集群的唯一server,我们使用```-server```指定他.

```-bootstrap-expect``` 选项提示Consul我们期待加入的server节点的数量.这个选项的作用是启动时推迟日志复制直到我们期望的server都成功加入时.你可以阅读[启动指南](https://www.consul.io/docs/guides/bootstrapping.html)了解更多.

最后,我们加入 ```config-dir```选项,指定服务和健康检查定义文件存放的路径.

加到一起,命令如下:

```
consul agent -server -bootstrap-expect 1  -data-dir /tmp/consul -node=hdp2 -bind=10.0.0.52  -config-dir /etc/consul.d
```

现在在另外一个终端,我们将连接第二个节点:

```
ssh hdp3
# 登录第二台机器
```

这一次我们设置绑定的IP地址为第二个节点的IP的地址,并指定节点名称.因为这个节点将不是Consule的server.我们没有打开```server```开关.命令如下:

```
consul agent -data-dir /tmp/consul -node=hdp3 -bind=10.0.0.53 -config-dir /etc/consul.d
```

现在,你有运行了两个Consul的agent,一个作为server另一个作为client.这两个agent还互相不知道对方,只是作为独立的单节点集群.为了验证这个你可以在每个agent运行```consul member```,只能看到各自自己这一个集群成员. 

## 加入一个集群

现在我们告诉第一个agent来加入第二个agent,在新的终端运行如下命令

```
ssh hdp2
consul join 10.0.0.53
Successfully joined cluster by contacting 1 nodes.
```

>
> 如果出现 ```Error joining the cluster: dial tcp 10.0.0.53:8301: getsockopt: no route to host```
> 
> 可能是业务防火墙的原因,检查端口```8301```是否被允许
>

你应该可以看到在每个agent的日志输出窗口的一些输出.如果你仔细阅读会发现.他们收到了加入信息,如果你在每个agent运行```consul members```你会看到类似下面的内容:

```
[root@hdp2 ~]# consul members
Node  Address         Status  Type    Build  Protocol  DC
hdp2  10.0.0.52:8301  alive   server  0.6.4  2         dc1
hdp3  10.0.0.53:8301  alive   client  0.6.4  2         dc1
```

>
>记住:为了加入集群,一个Consul的agent只需要了解一个已经存在的集群成员.加入集群后agent会自动交流传递完整的成员信息.
>

## 启动时自动加入集群

理想的情况,当一个新的节点在数据中心启动时,他应该自动加入到Consul的集群中,而不需要人为干预.为了达到这个效果你可以使用[HashiCorp的Atlas](https://atlas.hashicorp.com/)和```-atlas-join```选项.示例如下:

```
consul agent -atlas-join \
  -atlas=ATLAS_USERNAME/infrastructure \
  -atlas-token="YOUR_ATLAS_TOKEN"
```
Atlas的用户名和token可以通过创建Atlas账号获取.这样当心的节点启动后他会自动加入到你的Consul集群,不需要硬编码配置.

另一种选择,你可以通过```-join```选项和```start_join```配置将其他已知的agent的地址进行硬编码来在启动时加入集群.

## 查询节点

就像查询服务一样.Consul有一个API用来查询节点自己.你可以通过DNS和HTTP的API来进行.

DNS API中节点名称结构为 ```NAME.node.consul```或者```NAME.node.DATACENTER.consul```.如果数据中心名字省略,Consul只会查询本地数据中心.

例如 从节点```hdp2```我们可以查询节点```hdp3```的地址:

```
[root@hdp2 ~]# dig @127.0.0.1 -p 8600 hdp3.node.consul

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.47.rc1.el6 <<>> @127.0.0.1 -p 8600 hdp3.node.consul
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 5351
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;hdp3.node.consul.          IN      A

;; ANSWER SECTION:
hdp3.node.consul.       0       IN      A       10.0.0.53

;; Query time: 1 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Thu Aug 18 14:32:02 2016
;; MSG SIZE  rcvd: 66
```

除服务之外查询节点的能力对于系统管理任务非常重要.例如知道节点的SSH登录地址,可以简单的将节点加入到Consul集群并查询他.

## 离开集群 

离开集群,你可以```Ctrl-C```优雅的退出,也可以直接Kill掉agent进程.优雅的退出可以让节点转变为离开状态.否则节点将被标记为失败.详细的细节可以查看[这里](https://www.consul.io/intro/getting-started/agent.html#stopping).

# 健康检查

我们现在看到Consul运行时如此简单.添加节点和服务,查询节点和服务.在这一节.我们将继续添加健康检查到节点和服务.健康检查是服务发现的关键组件.预防使用到不健康的服务.

这一步建立在前一节的Consul集群创建之上.目前你应该有一个包含两个节点的Consul集群.

## 定义检查

和服务类似,一个检查可以通过检查定义或HTTP API请求来注册.

我们将使用和检查定义来注册检查.和服务类似,因为这是建立检查最常用的方式.

在第二个节点的配置目录建立两个定义文件:

```
vagrant@n2:~$ echo '{"check": {"name": "ping",
  "script": "ping -c1 163.com >/dev/null", "interval": "30s"}}' \
  >/etc/consul.d/ping.json

vagrant@n2:~$ echo '{"service": {"name": "web", "tags": ["rails"], "port": 80,
  "check": {"script": "curl localhost >/dev/null 2>&1", "interval": "10s"}}}' \
  >/etc/consul.d/web.json
```

第一个定义增加了一个主机级别的检查,名字为 "ping" . 这个检查每30秒执行一次,执行 ```ping -c1 163.com```. 在基于脚本的健康检查中,脚本运行在与Consul进程一样的用户下.如果这个命令以非0值退出的话这个节点就会被标记为不健康.这是所有基于脚本的健康检查的约定.

第二个命令定义了名为```web```的服务,添加了一个检查.每十分钟通过curl发送一个请求,确定web服务器可以访问.和主机级别的检查一样.如果脚本以非0值退出则标记为不健康.

现在重启第二个agent或者发送```SIGHUP```信号,你应该可以看到如下的日志内容输出:

```
==> Reloading configuration...
    2016/08/18 15:29:57 [INFO] agent: Synced service 'web'
    2016/08/18 15:29:57 [INFO] agent: Synced check 'ping'
    2016/08/18 15:29:58 [WARN] agent: Check 'service:web' is now critical
```

前几行检查到agent同步了新的定义.最后一行检查到web服务出于危险状态.这是因为我们实际上没有运行一个web服务器.所以```curl``的测试会一直失败!

## 检查健康状态

现在我们加入了一些简单的检查.我们能适应HTTP API来检查他们.首先我们检查有哪些失败的检查.使用这个命令(注意:这个命令可以运行在任何节点)

```
[root@hdp3 consul.d]# curl http://localhost:8500/v1/health/state/critical
[{"Node":"hdp3","CheckID":"service:web","Name":"Service 'web' check","Status":"critical","Notes":"","Output":"","ServiceID":"web","ServiceName":"web","CreateIndex":878,"ModifyIndex":878}]
```

我们可以看到,只有一个检查我们的```web```服务在```critical```状态

另外,我们可以尝试用DNS查询web服务,Consul将不会返回结果.因为服务不健康.

```
[root@hdp3 consul.d]# dig @127.0.0.1 -p 8600 web.service.consul

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.47.rc1.el6 <<>> @127.0.0.1 -p 8600 web.service.consul
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 33096
;; flags: qr aa rd; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;web.service.consul.        IN      A

;; AUTHORITY SECTION:
consul.         0       IN      SOA     ns.consul. postmaster.consul. 1471507354 3600 600 86400 0

;; Query time: 8 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; WHEN: Thu Aug 18 16:02:34 2016
;; MSG SIZE  rcvd: 104
```

## 下一步

在本章,你学到了如何鉴定的添加健康检查.检查定义可以通过配合文件并发送```SIGHUP```到agent进行更新.另外,HTTP API可以用来动态添加,移除和修改检查.API也运行使用 "死亡开关(dead man's swicth)" 一个基于生存时间(TTL)的检查.TTL可以让应用程序更紧密的与Consul集成.将检查的状态加入到业务逻辑的计算.# 键值数据存储

除了提供服务发现和健康检查的集成.Consul提供了一个易用的键/值存储.这可以用来保持动态配置,协助服务协调,领袖选举,做开发者可以想到的任何事情.

这一章假设你已经有至少一个Consul的agent在运行.

## 简单使用

为了演示如果简单的使用键值存储.我们将操作一些键.查询本地agent我们首先确认现在还没有存储任何key.

```
[root@hdp3 consul.d]# curl -v http://localhost:8500/v1/kv/?recurse
* About to connect() to localhost port 8500 (#0)
*   Trying ::1... 拒绝连接
*   Trying 127.0.0.1... connected
* Connected to localhost (127.0.0.1) port 8500 (#0)
> GET /v1/kv/?recurse HTTP/1.1
> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.21 Basic ECC zlib/1.2.3 libidn/1.18 libssh2/1.4.2
> Host: localhost:8500
> Accept: */*
>
< HTTP/1.1 404 Not Found
< X-Consul-Index: 1
< X-Consul-Knownleader: true
< X-Consul-Lastcontact: 0
< Date: Thu, 18 Aug 2016 08:21:39 GMT
< Content-Length: 0
< Content-Type: text/plain; charset=utf-8
<
* Connection #0 to host localhost left intact
* Closing connection #0
```

因为没有key所以我们得到了一个404响应.现在我们```PUT``一些示例的Key:

```
[root@hdp3 consul.d]# curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/key1
[root@hdp3 consul.d]# curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/key2?flags=42
[root@hdp3 consul.d]# curl -X PUT -d 'test'  http://localhost:8500/v1/kv/web/sub/key3
[root@hdp3 consul.d]# curl http://localhost:8500/v1/kv/?recurse
[{"LockIndex":0,"Key":"web/key1","Flags":0,"Value":"dGVzdA==","CreateIndex":1201,"ModifyIndex":1201},{"LockIndex":0,"Key":"web/key2","Flags":42,"Value":"dGVzdA==","CreateIndex":1205,"ModifyIndex":1206},{"LockIndex":0,"Key":"web/sub/key3","Flags":0,"Value":"dGVzdA==","CreateIndex":1217,"ModifyIndex":1217}]
```

我们创建了值为"test"的3个Key,注意返回的值是经过了base64编码的.用来支持非UTF8编码字符.对Key ```web/key2```我们设置了一个标志值为 ```42```.所有的key支持设置一个64位的整形数字标志.Consul内部不适用这个值.但是他可以被客户端适用来做一些元数据.

完成设置后,我们发起了一个```GET```请求来接收多个key的值,使用```?recurse```参数.

你可以获取单个的key

```
[root@hdp3 consul.d]# curl http://localhost:8500/v1/kv/web/key1
[{"LockIndex":0,"Key":"web/key1","Flags":0,"Value":"dGVzdA==","CreateIndex":1201,"ModifyIndex":1201}]
```

删除key也很简单.通过```DELETE```动作来完成.我们可以通过指定完整路径来删除一个单独的key.或者我们可以使用```?recurse```递归的删除主路径下所有key.

```
[root@hdp3 consul.d]# curl -X DELETE http://localhost:8500/v1/kv/web/sub?recurse
true
[root@hdp3 consul.d]# curl http://localhost:8500/v1/kv/web?recurse
[{"LockIndex":0,"Key":"web/key1","Flags":0,"Value":"dGVzdA==","CreateIndex":1201,"ModifyIndex":1201},{"LockIndex":0,"Key":"web/key2","Flags":42,"Value":"dGVzdA==","CreateIndex":1205,"ModifyIndex":1206}]
```

可以通过发送相同的URL并提供不同的消息体的```PUT```请求去修改一个Key.另外,Consul提供一个检查并设置的操作,实现原子的Key修改.通过```?cas=```参数加上```GET```中最近的```ModifyIndex```来达到. 例如我们想修改 "web/key1":

```
[root@hdp3 consul.d]# curl -X PUT -d 'newval' http://localhost:8500/v1/kv/web/key1?cas=1201
true
[root@hdp3 consul.d]# curl -X PUT -d 'newval' http://localhost:8500/v1/kv/web/key1?cas=1201
false
```

在这种情况下,第一次```CAS``` 更新成功因为```ModifyIndex```是```1201```.而第二次失败是因为```ModifyIndex```在第一次更新后已经不是```1201```了 .

我们也可以使用```ModifyIndex```来等待key值的改变.例如我们想等待```key2```被修改:

```
[root@hdp3 consul.d]# curl http://localhost:8500/v1/kv/web/key2
[{"LockIndex":0,"Key":"web/key2","Flags":42,"Value":"dGVzdA==","CreateIndex":1205,"ModifyIndex":1206}]

[root@hdp3 consul.d]# curl "http://localhost:8500/v1/kv/web/key2?index=1206&wait=5s"
[{"LockIndex":0,"Key":"web/key2","Flags":42,"Value":"dGVzdA==","CreateIndex":1205,"ModifyIndex":1206}]
```

通过提供 ```?index=```,我们请求等待key值有一个比```1206```更大的```ModifyIndex```.虽然```?wait=5s```参数限制了这个请求最多5秒,否则返回当前的未改变的值. 这样可以有效的等待key的改变.另外,这个功能可以用于等待一组key.直到其中的某个key有修改.

## 下一步

这里有一些说API可以支持的操作的例子,要查看完整文档.请查看[这里](https://www.consul.io/docs/agent/http/kv.html).

下面我们将看一看Consul支持的WebUI选项.# WEB界面

Consul同时提供了一个漂亮的功能齐全的WEB界面,开箱即用.界面可以用来查看所有的节点,可以查看健康检查和他们的当前状态.可以读取和设置K/V 存储的数据.UI自动支持多数据中心.

运行WebUI有两个选项.使用HashiCorp提供的Atlas来托管你的仪表盘或者使用Consul自己托管的开源UI

## Atlas托管的仪表盘

![atlas_web_ui-249f659e.png](/img/in-post/atlas_web_ui-249f659e.png)

为了设置Consul使用Atlas界面.你必须添加两个字段到你的配置文件:你的Atlas名称和TOKEN.下面是一个命令行示例用来配置agent的这些设置:

```
$ consul agent -atlas=ATLAS_USERNAME/demo -atlas-token="ATLAS_TOKEN"
```
获取Atlas用户名和token,[创建](https://atlas.hashicorp.com/account/new)一个账号并替换成你自己的配置.你可以查看线上[Demo](https://atlas.hashicorp.com/hashicorp/environments/consul-demo).

## Consul托管的仪表盘

![consul_web_ui-3a1e7bf9.png](/img/in-post/consul_web_ui-3a1e7bf9.png)

设置自托管的UI服务,启动Consul时使用```-ui``` 参数:

```
[root@hdp4 ~]# consul agent -ui
```

UI的路径在 ```ui```,使用HTTP API 相同的端口.默认为 ```http://localhost:8500/ui```.

>
> 译者注: ```-client```指定你要将HTTP绑定到的IP,绑定到一个公网IP一边可以从外部访问,否则只能在本机进行访问.所以我的启动命令是
> ```[root@hdp4 ~]# consul agent -ui -data-dir /tmp/consul -bind 10.0.0.54 -join 10.0.0.52```
>

你可以查看线上[Demo](http://demo.consul.io/).

线上Demo可以访问所有的数据中心.我们也设置了Demo的端点: AMS2 (阿姆斯特丹) , SF01(旧金山) 和 NY3(纽约).

## 下一步

我们的入门指南完成了.查看下一页来了解如何继续你与Consul的旅程!# Consul 简介和快速入门


# 接下来的

入门指南结束了,希望你能看到Consul是简单易用的.他拥有一些强大的功能.我们在这个指南里覆盖了所有这些功能的基础.

Consul采用对运维和开发者友好,让他完美的适用现代的弹性基础设施.

接下来可以使用这些资源做更深入的了解.

- 文档 - 文档是更深入的Consul功能参考.包括Consul内部操作的技术细节
- 指南 - 这部分提供很多Consul的入门指南,包括如何启动一个数据中心.

- 示例 - 这个Consul的Github库中还在进行中的示例目录包含很多使用示例,帮助你更好的根据你的需要使用Consul的功能.# Consul是什么
















