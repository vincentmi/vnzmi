---
layout:     post
title:      "多语言网站开发 不完全技术分析收录"
date:       2006-03-07 01:24:52
author:     "Vincent"
image:  "img/post-bg-dot.jpg"
catalog: false
tags:
    - 新浪博客
    - 技术文章
---


语言是信息传播的主要障碍。



多语言网站，顾名思义就是能够以多种语言（而不是单种语言）为用户提供信息服务，让使用不同语言的用户都能够从同个网站获得内容相同的信息。




多语言网站实现方案



1，静态：就是为每种语言分别准备一套页面文件，要么通过文件后缀名来区分不同语言，要么通过子目录来区分不同语言。



例
如对于首页文件index_en.htm提供英语界面，index_gb.htm提供简体中文界面，index_big.htm提供繁体中文界面，或者是
en/index.htm提供英语界面，gb/index.htm提供简体中文界面，big/index.htm提供繁体中文界面，一旦用户选择了需要的
语言后，自动跳转到相应的页面，首页以下其他链接也是按照同样方式处理。从维护的角度来看，通过子目录比通过文件后缀名来区分不同语言版本显得要简单明
了。



2，动态：站点内所有页面文件都是动态页面文件（PHP，ASP等）而不是静态页面文件，在需要输出语言文字的地方统一采用语言变量来表示，这些语言变量可以根据用户选择不同的语言赋予不同的值，从而能够实现在不同的语言环境下输出不同的文字。



例如：语言变量ln_name，当用户选择的语言是英语时赋值为“Name”，当用户选择的语言是简体中文时赋值为“姓名”，这样就可以适应不同语言时的输出。



采用静态方式的优点是页面直接输出到客户端，不需要在服务器上运行，占用服务器的资源比较少，系统能够支持的并发连接数较多，缺点是要为每种语言制作一套页面文件，很多内容即使是和语言无关的也要分不同语言来存储，因此占用的存储空间较多。



采
用动态方式和静态方式的优缺点正好相反，它的优点是动态页面文件只有一套，不同语言的文字使用语言变量来存储，和语言无关的内容只存储一份，占用的存储空
间较少，并且扩展新语言比较容易，缺点需要在服务器上运行，然后把结果输入到客户端，占用服务器的资源比较多，系统能够支持的并发连接数较少。




动态数据存贮涉及的一些技术问题



由于现在网站上动态应用日益增多，相当多的网站还会使用文件或者数据库来存储应用信息，因此如果文件或者数据库中存储的内容与语言相关时，还需要特别注意。对于存储在数据库中信息，可以采取以下几种方式支持多语言：



1，在数据库级别支持多语言：为每种语言建立独立的数据库，不同语言的用户操作不同的数据库。



2，在表级别支持多语言：为每种语言建立独立的表，不同语言的用户操作不同的表，但是它们在同一个数据库中。



3，在字段级别支持多语言：在同一个表中为每种语言建立独立的字段，不同语言的用户操作不同的字段，它们在同一个表中。



由于数据库中有大量的信息（如标志，编码，数字等）是用于内部处理使用的，与语言无关的，因此在数据库级别支持多语言会导致空间的极大浪费，在字段级别支持多语言最大的问题是一旦需要支持新的语言，由于需要修改表结构，维护起来非常麻烦，可扩展性不好。



相
比之下，在表级别支持多语言比较好，因为并不是所有的表都需要支持多语言，对于与语言无关的表，不同语言的用户共用一套，那些和语言相关的表根据支持语言
的种类来建立，不同语言的用户存取访问不同的表格。这样使得维护简单，节省了存储空间，即使是扩展起来也比较方便，只要把需要支持多语言的表，多建立一套
即可。



还需要注意的问题是：有些表中某些字段是不同语言版本的表共享的（例如库存量），由于各种语言的表之间的相对独立性，使得数据共享有些困难。解决的方法有两个：



1，不同语言的表的共享字段同步：也就是说，只要修改了其中一个表的共享字段，其他语言表中该字段也作相应改变，实际上当不同语言的用户同时访问时处理还是比较麻烦的，并且扩充新语言时修改工作比较大。



2，增加一个新的表：把所有语言共享的字段（例如货物编号，产地编码等）全部放在这个表，支持多语言的表只存放与各种语言相关的字段。不同语言的用户在使用数据库时，需要操作两个数据表。

比较而言，第二种方法比较简单，并且效率比较高，维护也比较方便。




应用字符集的选择



一个定位于不同语言国家的企业网站势必需要提供多种语言版本的产品和销售信息来满足其世界各地使用不同语言的客户和合作伙伴，其中包括法语、德语、意大利
语、葡萄牙语、西班牙语、阿拉伯语等等。但有一个问题却极易被网站设计者们所忽略。这就是网站的字符集设置问题。


一般我们使用的是简体中文(GB2312)字符集，而对多语言网站来说，中文字符集却可能会使你辛辛苦苦的努力功亏一篑。原因很简单：就是这个毫不起眼的小小字符集在作怪。 

计算机应用领域中存在着几十种互不相同的字符集，而不同语言客户在浏览不同语言网页时，往往会因为相互间所使用字符集无法兼容而出现乱码情况。我们在浏览国外一些网站时，往往也会出现为了能正常地看到网站上的信息而不得不在各种字符集之间来回切换的情况。 

试
想一下：如果一个网站提供了中，英，法，德等多种语言版本的内容，内容全之又全，设计美仑美奂。我们在中文编码环境下浏览这些非中文版本的页面觉得非常完
美，现在一个法国客户对你的产品发生了兴趣，当他进到法语版面一看—乱码多多，甚至可能整个版面都一塌里糊涂。你的网站再下大工夫又有什么意义呢? 

所
以对提供了多语言版本的网站来说，Unicode字符集应该是最理想的选择。它是一种双字节编码机制的字符集，不管是东方文字还是西方文字，在
Unicode中一律用两个字节来表示，因而至少可以定义65536个不同的字符，几乎可以涵盖世界上目前所有通用的语言的每一种字符。 所以在设计和开
发多语言网站时，一定要注意先把非中文页面的字符集定义为“utf-8”格式。 

这一步非常重要，原因在于若等页面做好之后再更改字符集设置，可说是一件非常非常吃力不讨好的工作，有时候甚至可能需要从头再来，重新输入网站的文字内容。

HTML中的META标签：

&lt;META HTTP-EQUIV=“Content-Type” CONTENT=“text/html; CHARSET=字符集"&gt; 


不写，根据浏览器默认字符集显示charset=gb2312  简体中文 charset=big5 繁体中文  charset=EUC_KR  韩语 charset=Shift_JIS 或 EUC_JP 日语 charset= KOI8-R / Windows-1251 俄语 charset=iso-8859-1  西欧语系（荷兰语,英语,法语,德语,意大利语,挪威语,葡萄牙语,瑞士语.等十八种语言）http://www.microsoft.com/charset=iso-8859-2  中欧语系charset=iso-8859-5 斯拉夫语系（保加利亚语,Byelorussian语,马其顿语,俄语,塞尔维亚语,乌克兰语等）charset=uft-8  unicode多语言



ASP与脚本引擎页码的概念
由于我们传统使用的内码像Big5,GB2312与unicode并不是一一对应,故两者之间的转换要靠codepage(页码)来实现
&lt;%@ Language=VBScript CodePage=xxx%&gt; 


不写，根据服务器端解析引擎默认代码页自动解析并返回浏览器。如果制作的网页脚本与WEB服务端的默认代码页不同，则必须指明代码页：codepage=936 简体中文GBKcodepage=950 繁体中文BIG5codepage=437 美国/加拿大英语codepage=932 日文codepage=949 韩文codepage=866 俄文codepage=65001 unicode UFT-8



建议采用utf8的静态和动态文档。即：


&lt;%@LANGUAGE="VBSCRIPT" CODEPAGE="65001"%&gt;
&lt;meta http-equiv="Content-Type" content="text/html; charset=utf-8" /&gt;



