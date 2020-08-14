---
layout:     post
title:      "IE 6 真是个小贱人"
date:       2007-12-13 23:42:28
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: true
tags:
    - 新浪博客
    - Javascript
---


   
今天敲鼓了大半天HTML,firefox让人很省心，ie弄死要装怪。常看论坛啊博客大家恨IE恨的咬牙切齿的。查啊查终于找到原因了,Css控制如下内容
&lt;div style="overflow:hidden"&gt;&lt;div
style="position:relative"&gt;&lt;/div&gt;&lt;/div&gt;这样得2个盒子如果html在
Transitional
和其他严格模式下都会失效。内部盒子超出的部分将不会有任何效果。终于体会到IE这小贱人的无耻，没有谁有IE这么多得BUG。希望IE早点死掉。全天下的网页设计师都在这样咬牙切齿的诅咒着他吧。

ps:就是 这一句 &lt;!DOCTYPE
HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"&gt;
去掉就ok了

 



