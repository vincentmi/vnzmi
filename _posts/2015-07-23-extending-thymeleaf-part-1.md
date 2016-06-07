---
layout:     post
title:      "扩展Thymeleaf-1 为什么需要扩展Thymeleaf"
date:       2015-07-23 02:04:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - Spring
    - Thymeleaf
---
gitbook [http://vincentmi.gitbooks.io/extendingthymeleaf/content/][http://vincentmi.gitbooks.io/extendingthymeleaf/content/]


Thymeleaf是一个很容易扩展的库。他的关键在于，大部分面向用户的功能不是直接构建在他的核心中，而是通过打包和组件化到一个称为Dialects(方言)的功能集合中。


<!--more-->


这个库提供2个立即可以使用的方言: 标准方言和Spring方言。但是你可以很容易的创建自己的方言。让我来说说这么做的好处：

## 场景 1: 添加功能到标准方言

话说你的应用程序使用了Spring方言，你需要根据用户的角色（管理员或非管理员）从周一到周五都显示一个红的或蓝色背景的文本警告。但是星期天会一直显示绿色。你可以在你的模版中使用条件表达式计算这个，但是太多表达式会让你的代码有一点不好阅读。

**解决方案：**创建一个新的属性叫做 ```alertclass``` ，并为他创建一个属性处理器(Java代码用于计算正确的CSS样式)，打包到你自己的方言类MyOwnDialect.添加这个方言到你的模版引擎使用th前缀(和Spring方言一致)
。这样你现在就可以使用这个代码 ```th:alertclass="${user.role}"!``` 来输出正确的样式名了。


## 场景2: 视图层组件

又话说你的公司广泛使用Thymeleaf ,你想创建一个常用功能的仓库(tag或者attribute )这样下次你可以在多个应用程序使用而不用拷来拷去。这时候你想要使用类似JSP的taglib的方式创建一个视图层组件。

**解决方案**: 根据功能的关联性创建Thymeleaf方言，根据需要添加到你的应用程序中。注意，如果方言中的Tag或者Attribute使用了本地化和国际化支持。 你可以以处理器的message的方式打包到方言里。而不用你的应用程序想JSP一样去包含一个```messages.properties```文件。


### 场景 3: 创建你自己的模板系统
想象一下你正在创建一个公开网站，允许用户自己设计模板去显示他们的内容。当然你不想你的用户能在模板中坐所有的事情。甚至不允许他们执行标准方言（比如OGNL表达式）。所以你需要你的用户可以添加一些在你控制下的一组功能。（比如显示个人资料图片、博客入口等等）。

**解决方案** 创建一个方言，包含一些你允许你的用户使用的tag和attribute。比如 ```<mysite:profilePhoto />``` 或者 ```<mysite:blogentries fromDate="23/4/2011" /> ```。然后允许你的用户使用这些功能创建模板。让Thymeleaf只执行这些。




