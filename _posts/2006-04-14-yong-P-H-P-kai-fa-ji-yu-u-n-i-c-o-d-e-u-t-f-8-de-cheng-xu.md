---
layout:     post
title:      "用PHP开发基于unicode(utf-8)的程序"
date:       2006-04-14 17:32:05
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: true
tags:
    - 新浪博客
    - 技术文章
---


Author:朱辉(ice)phpx.com ID: ice日期:2005-3-19 11:20因朋友(teacherli)的再三要求, 所以我终于定下心来, 写一篇关于这方面的文章.让大家轻松的从本地编码的程序过度到unicode程序.Unicode又被称之为"万国码",就是说他支持很多特性.最有意思的就是, 可以在同一个页中显示不同国家的文字.好了, 打字幸苦, 废话少说!我们预设开发平台为:FreeBSD5.3+Apache2+Mysql4.1.7+PHP5.03服务器的配置我就少说,(有需要的请搜索这方面的文章.) 直接进入正题.PHP开发程序可以用EmEditor 4X. 这个可以轻松的把文档从不同的编码转换到utf-8,我用editplus的新版本, 在保存文件的时候, 也可以保存成utf-8编码格式的文件.注意:如果你的文件中只有english的话,你的文件将还是普通文件, 但这个不会影响你的程序运行, 这个就是utf-8编码的特点. 因为utf-8文件中, 有这个特性, 详细的可以去http://www.unicode.org上看看. 我一开始的时候, 国内几乎没有关于utf-8的文章可以参考, 所以, 很多东西都是在http://www.unicode.org和http://www.w3c.org上了解到的. 首先, 我们要建立一个Mysql表, 如果在mysql3.23.x下, 普通的建立就可以了. 但在mysql4.x下,我们要做一些特殊的设置.如:CREATE TABLE `ice_member` (`id` int(8) unsigned NOT NULL auto_increment,`name` varchar(255) NOT NULL default ’0’,`photo` varchar(50) NOT NULL default ’0’,`level` tinyint(1) unsigned NOT NULL default ’0’,`status` tinyint(1) unsigned NOT NULL default ’0’,`addtime` varchar(16) NOT NULL default ’’,`edittime` varchar(16) NOT NULL default ’’,UNIQUE KEY `id` (`id`),KEY `name` (`name`),KEY `level` (`level`),KEY `status` (`status`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;有没有注意到? 最后有一段 ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;ENGINE是说表的类型是MyISAM,一般都用MyISAM表,如果有特殊的, 也可以用InnoDB,我这里不说InnoDB了, 有需要清参考InnoDB的资料.DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;这个就是设定这个表是utf-8格式, 校对是utf8普通模式.我的理解是这样的.这个是数据表的建立完成. 其次是php了. php文件中, 你要把文件save成utf-8, 如果显示有乱码的话, 就要在文件的头文件中,强制文件为utf-8, 具体内容如下:&lt;?header("Content-type: text/html; charset=utf-8");//your content.....?&gt;OK, 这个显示文件内容就搞定, 下一步就是用php连接和处理内容一到数据中了. 很多人一开始的时候都打算用utf-8,就是因为这一步处理不了而想放弃使用utf-8了, 我的好朋友(teacherli)就是一个典型例子. 好了, 我们来处理这个难题.&lt;?$db=mysql_content(xxx);$db=mysql_select_db(xxxx);//重点来了, 在utf-8下, 如果服务器是自己的,就在服务器上设置, 如果不是, 就要在//每次连接数据库的时候,就加多这么一个查询.$db-&gt;query("SET CHARACTER_SET_CLIENT = utf8,CHARACTER_SET_CONNECTION = utf8,CHARACTER_SET_DATABASE = utf8,CHARACTER_SET_RESULTS = utf8,CHARACTER_SET_SERVER = utf8,COLLATION_CONNECTION = utf8_general_ci,COLLATION_DATABASE = utf8_general_ci,COLLATION_SERVER = utf8_general_ci,AUTOCOMMIT=1");?&gt;这里的设置, 看就明白了, 如果不明白, 我也没有法子. 只有最后一个我说明一下:AUTOCOMMIT=1, 这个是处理mysql4x的事务的. mysql4支持事务, 很多朋友说, mysql4Insert 数据的时候好慢, 就是因为事务搞的. 事务是很有用的, 如果不知道怎么用,就把事务的处理交给AUTOCOMMIT=1处理了吧.好了, 现在就可以用utf-8开发程序了.再补充一点, 如果用模板, 也要保存成utf-8编码的文件, 还有, 要在html文件的CHARSET中设置文档的编码是utf-8哦, 不然会有乱码出现. 如有不太明白的, 可以发email给我.(datafile#163.com)或QQ我<img>259079)以后我还会尽量发多一点关于php处理utf-8的文章和多一些的代码, 希望有人支持. 





转移自: (http://blog.sina.com.cn/s/blog_542a3955010002lp.html)[http://blog.sina.com.cn/s/blog_542a3955010002lp.html]