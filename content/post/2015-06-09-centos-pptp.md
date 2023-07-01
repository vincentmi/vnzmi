---
layout:     post
title:      "在CentOS下安装PPTP的VPN"
date:       2015-06-09 23:16:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - pptp
---

http://www.black-xstar.com/blog/691.html

最近买了个基于xen的VPS玩玩，安装LAMP没啥意思。国内网络环境不好，干脆安装个VPN试试。

对于Linux其实我什么都不会的，在google老师的帮助下，总算给我安装好了，记录下来以便查阅。

VPN常用有两种，一种是openvpn，另一种PPTP。前者开源跨平台功能强大，后者简单方便Windows下无需安装客户端。而且从安装上看，PPTP比openvpn简单一点，所以决定安装这个试试看。

这里罗嗦一下VPS吧，常见也两种，一种是基于openvz，另一种基于xen的。区别不多说了，自己问google吧。这里要说的是openvz的绝大多数不能安装PPTP，而xen的没有限制，两个都可以。


以下所有命令我都加了下划线，即加下划线的一定是在类似-bash-3.2#的提示符下输入。

SSH登陆VPS，我的系统是64的CentOS 5.4，绝大多数VPS都提供CentOS系统供选择。可以使用这个命令查询：

    cat /etc/issue

检查内核是否包含mppe，基本上CentOS都有的，输入这个命令，如果是ok就可以：

    modprobe ppp-compress-18 && echo ok

安装PPTP需要ppp和iptables这两个软件支持，这里用yum来安装，输入这个命令：

    yum install -y ppp iptables

![4f670a90f603738d88d1899eb31bb051f919ec5e.jpg][/img/in-post/1235339652.jpg]

然后进入tmp目录，需要把pptp软件下载回来，用这个命令：cd /tmp

去poptop官方网站，如果你和我系统一样，直接下载rpm包：

    wget http://poptop.sourceforge.net/yum/stable/packages/pptpd-1.3.4-1.rhel5.1.x86_64.rpm

![2.jpg][/img/in-post/3785427575.jpg]

×××如果上面命令无效，安装wget吧：`yum install -y wget`

接下来安装刚刚下载回来的rpm包，输入命令：`rpm -ivh pptpd-1.3.4-1.rhel5.1.x86_64.rpm`
![3.jpg][/img/in-post/3438269410.jpg]

×××如果上面命令无效，安装perl吧：`yum install -y perl`

接下来我们开始配置PPTP了，需要用到linux下的vi命令，如果不熟悉建议先google一下。

×××提示一下，编辑完成后按Esc键，然后输入:wq即可保存并退出。

输入vi /etc/ppp/options.pptpd开始编辑，输入以下内容：

    name pptpd 
    refuse-pap 
    refuse-chap 
    refuse-mschap 
    require-mschap-v2 
    require-mppe-128 
    proxyarp 
    lock 
    nobsdcomp 
    novj 
    novjccomp 
    nologfd 
    ms-dns 208.67.222.222 
    ms-dns 208.67.220.220

最后两行是dns服务器地址，这里用opendns，你也可以用主机商的dns。编辑完成后保存退出。

输入vi /etc/pptpd.conf开始编辑，输入以下内容：

    option /etc/ppp/options.pptpd 
    logwtmp 
    localip 192.168.8.1 
    remoteip 192.168.8.2-40

最后两行是vpn的ip地址分配，如果你不熟悉就别改了。编辑完成后保存退出。

输入vi /etc/ppp/chap-secrets开始编辑，输入以下内容：

    username1 pptpd password1 *
    
    username2 pptpd password2 *
    
    username3 pptpd password3 *

这个文件用来配置vpn的登陆用户和密码，一行一个。编辑完成后保存退出。

把username和password分别改成你需要的用户名密码即可，其他别改了。

输入vi /etc/sysctl.conf开始编辑，这个文件和上面不同，里面已经有内容：

找到

    net.ipv4.ip_forward = 0

改成

    net.ipv4.ip_forward = 1

保存并退出，然后执行`sysctl -p`这个命令。

这时，PPTP基本上配置好了，输入service pptpd start启动。

下面来配置iptables，首先输入service iptables start启动。

然后分别输入下面四条命令，每天输完后要记得按回车：

    iptables -A INPUT -p tcp --dport 1723 -j ACCEPT
    
    iptables -A INPUT -p tcp --dport 47 -j ACCEPT
    
    iptables -A INPUT -p gre -j ACCEPT
    
    iptables -t nat -A POSTROUTING -s 192.168.8.0/24 -o eth0 -j MASQUERADE

完成后输入/etc/init.d/iptables save保存，并且输入/etc/init.d/iptables restart重新启动。

如果你需要服务器启动时候自动启动VPN服务，还需要输入chkconfig pptpd on和chkconfig iptables on这两条命令。

这个时候，PPTP的VPN就已经全部配置好了，由于内容太多，就不截图了，说明已经很详细。

在Windows下新建一个VPN连接，输入服务器ip、用户名和密码，如无意外就能连上去了。

打开youtube或twitter（follow我@billzhong）试试，爽吧！

最后广告一下，我的 VPN 服务： http://pptp.us 提供PPTP、L2TP和OpenVPN三种方式哦。

 

参考文章：

http://blog.s135.com/pptp_vpn/

http://rashost.com/blog/centos5-pptpd-vpn

http://taiwanwolf.blogspot.com/2009/01/centos-v52-pptp-server.html


