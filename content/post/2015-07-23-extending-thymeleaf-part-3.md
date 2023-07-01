---
layout:     post
title:      "扩展Thymeleaf 3 - 模板模式"
date:       2015-07-24 10:33:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - Spring
    - Thymeleaf
---

[http://vincentmi.gitbooks.io/extendingthymeleaf/content/][http://vincentmi.gitbooks.io/extendingthymeleaf/content/]


模板模式或许是Thymeleaf最强大的扩展点，模板模式实际上定义了什么可以被认为是一个“模板”。创建定制化的模板模式允许我们处理不同于默认的XML,XHTML,HTML5的文档格式。


<!--more-->


模板模式由他们的处理程序进行定义。处理程序需要实现接口
```org.thymeleaf.templatemode.ITemplateModeHandler```:


```java
     public interface ITemplateModeHandler {

             public String getTemplateModeName();

             public ITemplateParser getTemplateParser();

             public ITemplateWriter getTemplateWriter();

     }
```

每个模板模式的处理程序定义了Thymeleaf在处理指定模式的模板时需要的所有东西：一个解析器（接口ITemplateParser）,可以将模板转换为DOM树。一个Writer（接口ITemplateWriter）用于处理完成后转换DOM树到期望的结果格式。

Thymeleaf提供一些基本的模板模式，定义在```org.thymeleaf.templatemode.StandardTemplateModeHandlers```类中，他们被注册到每个模板引擎实例中。他们的名字如下：

**XML**: 解析时无需验证的XML.  
**VALIDXML**: 解析时需要验证的XML.   
**XHTML:**解析时不需要验证的XHTML 1.0 或者 1.1 模板.  
**VALIDXHTML** 解析时需要验证的XHTML 1.0 或者 1.1 模板.    
**HTML5** 良好的XML文档结构的HTML5模板.  
**LEGACYHTML5**结构不是那么规则的HTML5模板，因此需要一些预处理步骤，比如标签的补全、语法纠正等等   

为了解析这些模式，Thymeleaf在``` org.thymeleaf.templateparser ```包中提供了一组解析器的实现。这些验证和无需验证的解析器都可以使用SAX和DOM技术。这里也有一个nekoHTML(比较乱的HTML)解析器，用来解析不规范的XML文档（比如标签未闭合）。

默认的，所有标准模式都使用SAX解析，除LEGACYHTML5使用了nekoHTML解析器。

对于Writer提供了2个ITemplateWriter的实现，一个用来生成XHTML一个生成HTML5，另外一个用来生成XML.这几个类都保存在 org.thymeleaf.templatewriter 包中。



