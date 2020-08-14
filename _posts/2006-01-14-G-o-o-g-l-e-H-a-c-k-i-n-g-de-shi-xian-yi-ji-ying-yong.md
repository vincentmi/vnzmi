---
layout:     post
title:      "Google Hacking 的实现以及应用"
date:       2006-01-14 12:27:58
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: true
tags:
    - 新浪博客
    - 技术文章
---



http://soft.yesky.com/security/hkjj/389/2082889.shtml
前言
　　google hacking其实并算不上什么新东西，在早几年我在一些国外站点上就看见过相关的介绍，但是由于当时并没有重视这种技术，认为最多就只是用来找找未改名的mdb或者别人留下的webshell什么的，并无太大实际用途。但是前段时间仔细啃了些资料才猛然发觉google hacking其实并非如此简单...
　　google hacking的简单实现
　　记得以前看见过一篇文章写的就是简单的通过用www.google.com来搜索dvbbs6.mdb或conn.inc来获得一些站点的敏感信息.其实使用google中的一些语法可以提供给我们更多的信息(当然也提供给那些习惯攻击的人更多他们所想要的.),下面就来介绍一些常用的语法. 
　　intext:　　这个就是把网页中的正文内容中的某个字符做为搜索条件.例如在google里输入:intext:动网.将返回所有在网页正文部分包含"动网"的网页.allintext:使用方法和intext类似.
intitle:　　和上面那个intext差不多,搜索网页标题中是否有我们所要找的字符.例如搜索:intitle:安全天使.将返回所有网页标题中包含"安全天使"的网页.同理allintitle:也同intitle类似.
　　cache:　　搜索google里关于某些内容的缓存,有时候也许能找到一些好东西哦.
　　define:　　搜索某个词语的定义,搜索:define:hacker,将返回关于hacker的定义.
　　filetype:　　这个我要重点推荐一下,无论是撒网式攻击还是我们后面要说的对特定目标进行信息收集都需要用到这个.搜索指定类型的文件.例如输入:filetype:doc.将返回所有以doc结尾的文件URL.当然如果你找.bak、.mdb或.inc也是可以的,获得的信息也许会更丰富:)
　　info: 　　查找指定站点的一些基本信息.
　　inurl:　　搜索我们指定的字符是否存在于URL中.例如输入:inurl:admin,将返回N个类似于这样的连接:http://www.xxx.com/xxx/admin,用来找管理员登陆的URL不错.allinurl也同inurl类似,可指定多个字符.
　　link:　　例如搜索:inurl:www.4ngel.net可以返回所有和www.4ngel.net做了链接的URL.
　　site:　　这个也很有用,例如:site:www.4ngel.net.将返回所有和4ngel.net这个站有关的URL.
　　对了还有一些操作符也是很有用的:+ 把google可能忽略的字列如查询范围 - 把某个字忽略~ 同意词. 单一的通配符* 通配符，可代表多个字母"" 精确查询 
 
　　下面开始说说实际应用(我个人还是比较习惯用google.com,以下内容均在google上搜索),对于一个居心叵测的攻击者来说,可能他最感兴趣的就是密码文件了.而google正因为其强大的搜索能力往往会把一些敏感信息透露给他们.用google搜索以下内容: 

intitle:"index of" etc intitle:"Index of" .sh_historyintitle:"Index of" .bash_historyintitle:"index of" passwdintitle:"index of" people.lstintitle:"index of" pwd.dbintitle:"index of" etc/shadowintitle:"index of" spwdintitle:"index of" master.passwdintitle:"index of" htpasswd"# -FrontPage-" inurl:service.pwd
　　有时候因为各种各样的原因一些重要的密码文件被毫无保护的暴露在网络上,如果被别有用心的人获得,那么危害是很大的.下面是我找到的一个FreeBSD系统的passwd文件(我已做过处理):
<img>图一
　　同样可以用google来搜索一些具有漏洞的程序,例如ZeroBoard前段时间发现个文件代码泄露漏洞,我们可以用google来找网上使用这套程序的站点:intext:ZeroBoard filetype:php
　　或者使用:　　inurl:outlogin.php?_zb_path= site:.jp
　　来寻找我们所需要的页面.phpmyadmin是一套功能强大的数据库操作软件,一些站点由于配置失误,导致我们可以不使用密码直接对phpmyadmin进行操作.我们可以用google搜索存在这样漏洞的程序URL:　　intitle:phpmyadmin intext:Create new database
<img>图二
　　还记得http://www.xxx.com/_vti_bin/..%5C..%5C....m32/cmd.exe?dir吗?用google找找，你也许还可以找到很多古董级的机器。同样我们可以用这个找找有其他cgi漏洞的页面。
 
allinurl：winnt system32 

<img>图三
　　前面我们已经简单的说过可以用google来搜索数据库文件,用上一些语法来精确查找能够获得更多东西(access的数据库,mssql、mysql的连接文件等等).举个例子示例一下:
allinurl:bbs datafiletype:mdb inurl:databasefiletype:inc conninurl:data filetype:mdbintitle:"index of" data //在一些配置不正确的apache+win32的服务器上经常出现这种情况
　　和上面的原理一样,我们还可以用google来找后台,方法就略了,举一反三即可,毕竟我写这篇文章的目的是让大家了解google hacking,而不是让你用google去破坏.安全是把双刃剑,关键在于你如何去运用.
　　利用google完全是可以对一个站点进行信息收集和渗透的，下面我们用google对特定站点进行一次测试。www.xxxx.com是全国著名大学之一，一次偶然的机会我决定对其站点进行一次测试(文中所涉及该学校的信息均已经过处理，请勿对号入座:).　　首先用google先看这个站点的一些基本情况(一些细节部分就略去了):site:xxxx.com
　　从返回的信息中，找到几个该校的几个系院的域名：
http://a1.xxxx.comhttp://a2.xxxx.comhttp://a3.xxxx.comhttp://a4.xxxx.com
　　顺便ping了一下，应该是在不同的服务器.(想想我们学校就那一台可怜的web服务器，大学就是有钱，汗一个)。学校一般都会有不少好的资料，先看看有什么好东西没:site:xxxx.com filetype:doc
　　得到N个不错的doc。先找找网站的管理后台地址：site:xxxx.com intext:管理site:xxxx.com inurl:loginsite:xxxx.com intitle:管理
　　超过获得2个管理后台地址：http://a2.xxxx.com/sys/admin_login.asphttp://a3.xxxx.com:88/_admin/login_in.asp
　　还算不错，看看服务器上跑的是什么程序：site:a2.xxxx.com filetype:aspsite:a2.xxxx.com filetype:phpsite:a2.xxxx.com filetype:aspxsite:a3.xxxx.com filetype:aspsite:.............
 
a2服务器用的应该是IIS，上面用的是asp的整站程序，还有一个php的论坛　　a3服务器也是IIS，aspx+asp。web程序都应该是自己开发的。有论坛那就看看能不能遇见什么公共的FTP帐号什么的：site:a2.xxxx.com intext:ftp://*:* 

　　没找到什么有价值的东西。再看看有没有上传一类的漏洞：site:a2.xxxx.com inurl:filesite:a3.xxxx.com inurl:load
　　在a2上发现一个上传文件的页面：http://a2.xxxx.com/sys/uploadfile.asp
　　用IE看了一下，没权限访问。试试注射，site:a2.xxxx.com filetype:asp
　　得到N个asp页面的地址，体力活就让软件做吧，这套程序明显没有对注射做什么防范，dbowner权限，虽然不高但已足矣，back a shell我不太喜欢，而且看起来数据库的个头就不小，直接把web管理员的密码暴出来再说，MD5加密过。一般学校的站点的密码都比较有规律，通常都是域名+电话一类的变形，用google搞定吧。
site:xxxx.com //得到N个二级域名site:xxxx.com intext:*@xxxx.com //得到N个邮件地址，还有邮箱的主人的名字什么的site:xxxx.com intext:电话 //N个电话
　　把什么的信息做个字典吧，挂上慢慢跑。过了一段时间就跑出4个帐号，2个是学生会的，1个管理员，还有一个可能是老师的帐号。登陆上去：name：网站管理员 pass：a2xxxx7619 //说了吧，就是域名+4个数字
　　要再怎么提权那就不属于本文讨论访问了，呵呵，到此为止。
　　关于google hacking的防范
　　以前我们站的晓风·残月写过一篇躲避google的文章，原理就是通过在站点根目录下建立一个robots.txt以避免网络机器人获得一些敏感的信息，具体大家看原文章：http://www.4ngel.net/article/26.htm
　　不过这种方法我个人不推荐，有点此地无银三百两的味道。简单一点的方法就是上google把自己站点的一些信息删除掉，访问这个URL：http://www.google.com/remove.html
　　前几天看见又有人讨论用程序来欺骗robot的方法，我觉得可以试试，代码如下：




&lt;?if (strstr($_SERVER['HTTP_USER_AGENT'], "Googlebot")){　　header("HTTP/1.1 301");　　header("Location: http://www.google.com");}?&gt;
　　后记
　　这段时间在国外的一些google hack的研究站点看了看，其实也都差不多是一些基本语法的灵活运用，或者配合某个脚本漏洞，主要还是靠个人的灵活思维。国外对于google hack方面的防范也并不是很多，所以大家还是点到为止，不要去搞破坏拉，呵呵。对于一些在win上跑 apache的网管们应该多注意一下这方面，一个intitle:index of就差不多都出来了：）





转移自: (http://blog.sina.com.cn/s/blog_542a3955010001jw.html)[http://blog.sina.com.cn/s/blog_542a3955010001jw.html]