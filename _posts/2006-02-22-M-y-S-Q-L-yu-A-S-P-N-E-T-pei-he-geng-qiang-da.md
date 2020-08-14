---
layout:     post
title:      "MySQL与ASP.NET配合更强大"
date:       2006-02-22 09:41:01
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: true
tags:
    - 新浪博客
    - 技术文章
---







　　由于富有竞争力的价格和易于使用，MySQL在市场占有率方面逐步提升。开放源代码社区为了扩展MySQL的使用范围，开发出了.Net框架(.NET Framework)中可以使用的数据库连接器。我们就来学习一下如何在.Net应用程序中使用MySQL。

　　每周三发布的TechRepublic的.NET通讯,包含有网络服务, ASP.NET, ADO.NET, 和 Visual Studio .NET相关的实用技巧与代码实例. 现在就自动订阅!
　　MySQL渐渐的成为了在选择数据库平台时一个切实可行的数据库方案。能够证明这一点的就是许多公司都选择mySQL作为他们的数据库平台，例如 Google、美联社(The Associated Press) 以及美国国家航空宇航局( NASA)。虽然对于一个开放源代码来说，低廉的价格常常被当作主要优点来说服客户，但是对于象Google那样的大规模的组织来说，他们不会放心的把非常有用的信息存放在一个只有价格优势的数据库产品中。MySQL真正的实力远远的超过了他的价格优势，他提供了丰富的来自开放源代码社区和商业化的附加工具。
　　和.NET的数据整合
　　MySQL 社区已经开发出了MySQL的数据接口，他提供了连接数据源和程序代码的基本功能。在Windows平台上，有如下的MySQL连接器:
　　* MySQL Connector/Net 1.0 (之前被称为ByteFX.Data):是一个为MySQL设计的开放源代码.NET数据接口。它是完全用C#来开发的，我们可以在在 MySQL.com网站上找到它。(注意:在本文的例子中，我们都会使用MySQL Connector/Net 1.0这个数据接口来连接数据库，利用Windows安装程序即可轻易安装它，它的代码实例和文档也包含其中。)
　　* MySQLDirect .NET Data Provider: 是一个由 Core Lab 开发的商业数据接口。他的价格由购买的许可证的类型决定，但是我们可以下载它的试用版。
　　如果你使用 Mono，那么在 Mono网站上可以找到PHP连接器的下载。如果你在Windows平台上运行Mono的话，你下载的连接器包含了安装程序。如果不是的话，那就要根据你的操作系统的种类去下载合适的连接器了。
　　使用MySQL数据接口
　　安装好MySQL的数据接口后，你必须在你的代码中引入它才能使用。你可以使用 MySql.Data.MySqlClient这个名空间来连接 MySQL 服务器。在C#中，可以使用using语句来引入MySQL数据接口:
　　using MySql.Data.MySqlClient;
　　另外，你也可以在一个ASP.NET的网页表单(Web Form)中通过使用导入(Import)指令来引入MySQL数据接口:
　　
　　或者，你也可以在你的代码里在使用这个名空间时，写全一个类的完整路径，但是这样的话会比使用Import指令来导入输入更多的字符，浪费更多的字节。指定了名空间后，我们就可以和MySQL数据库进行数据交互了。 MySql.Data.MySqlClient这个名空间提供了许多用于处理MySQL数据的类。下面是这些类的一个样本:
　　* MySqlConnection: 管理和 MySQL 服务器/数据库的连接;
　　* MySqlDataAdapter: 一套用于填充DataSet对象和更新MySQL数据库的命令和连接的集合;
　　* MySqlDataReader: 让你能够从一个 MySQL 数据库读取数据。它是一个单向的数据流;
　　* MySqlCommand: 提供向数据库服务器发送指令的功能;
　　* MySqlException: 当发生问题时提供例外处理。
　　我们会使用其中的一些类去和我们的范例数据库进行数据交互。
　　连接 MySQL 数据库
　　使用MySQL数据库的第一步是要通过MySQLConnection类和数据库建立连接。通过一个连接字串，MySqlConnection 将会被实例化成一个示例。连接字符串将告诉代码到哪里去找MySQL服务器以及其他一些选项。
　　一个连接字串告诉代码使用指定的用户名和密码去连接一个名为MySQLTestServer的MySQL服务器，并进入techrepublic数据库。我在我的测试机上设定了允许匿名登陆(这样的设定有非常大的安全漏洞，所以不建议你在生产服务器上也这么做)，所以在范例中将会使用如下的连接字串:
　　"server=localhost; database=sitepoint;"
　　指定了连接字串后， MySqlConnection 对象的Open方法就被调用并打开连接。连接建立后，你就可以给MySQL数据库发送命令或从数据库获得数据了。
　　ASP.NET和MySQL的组合
　　让我们更深入的讨论一下结合MySqlConnection类和其他的类来生成一个MySQL服务器上的数据库列表。表 B列出了一个使用C#写的ASP.NET的网页表单。它建立了一个连接，接着给服务器下了一个指令(SHOW DATABASES)，然后通过MySqlReader对象把结果显示出来。
　　用 MySqlCommand 对象向MySQL服务器发送 SHOW DATABASES 命令和直接在 MySQL 管理工具中输入这个命令得结果是一样的。唯一的区别是，我们在代码中必须使用另一个对象来获取结果集。MySqlDataReader 对象在获取结果时被实例化(通过 MySqlCommand 类的 ExecuteReader 方法)。MySqlDataReader 对象的 GetString 方法被用于通过ASP.NET的标签控制来显示结果集中的数据。GetString 方法的指针0指定了显示结果集的当前行(在while循环中)的第一列数据。
　　Mono提示
　　如果你使用开放源代码的Mono开发平台，例子中的代码只需要做小小的改动就能正常的运行。MySQL的数据接口在 ByteFX.Data.MySqlClient 这个空间名里，而不是Windows上的MySql.Data.MySqlClient空间名。事实上 MySQL 的数据接口原来是由 ByteFX公司开发的，但是后被MySQL公司收购。所以如果你使用Mono的话，你必须这样声明空间名:
　　using ByteFX.Data.MySqlClient;
　　结语
　　MySQL 和 .NET 的组合提供了一个强大的开发平台。MySQL在开源社区得到了强大的技术支持，.NET也通过 Mono 而被开放源代码社区所接受。这样的组合提供了一个在Windows，及其他语言如UNIX或Linux，环境下高度灵活的开发平台。





转移自: (http://blog.sina.com.cn/s/blog_542a39550100024x.html)[http://blog.sina.com.cn/s/blog_542a39550100024x.html]