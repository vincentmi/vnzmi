---
layout:     post
title:      "JavaScript的9个陷阱及评点"
date:       2007-09-21 23:07:04
author:     "Vincent"
header-img:  "img/xinyuan-no7.jpg"
catalog: false
tags:
    - 新浪博客
    - Javascript
---


 
来自 Nine Javascript Gotchas ,
以下是JavaScript容易犯错的九个陷阱。虽然不是什么很高深的技术问题，但注意一下，会使您的编程轻松些，即所谓make
life easier. 笔者对某些陷阱会混杂一些评点。
1.　最后一个逗号

如这段代码，注意最后一个逗号，按语言学角度来说应该是不错的（python的类似数据类型辞典dictionary就允许如此）。IE会报语法错误，但语焉不详，你只能用人眼从几千行代码中扫描。
&lt;script&gt;
  var theObj = {
       
city : "Boston",
       
state : "MA",
  }
&lt;/script&gt;
2.　this的引用会改变
如这段代码：
&lt;input type="button" value="Gotcha!"
id="MyButton" &gt;
&lt;script&gt;
var MyObject = function () {
   
this.alertMessage = "Javascript rules";
   
this.ClickHandler = function() {
       
alert(this.alertMessage );
  }
}();
document.getElementByIdx(”theText”).onclick = 
MyObject.ClickHandler
&lt;/script&gt;
并不如你所愿，答案并不是”JavaScript
rules”。在执行MyObject.ClickHandler时，代码中红色这行，this的引用实际上指向的是document.getElementByIdx("theText")的引用。可以这么解决：
&lt;input type="button" value="Gotcha!"
id="theText" &gt;
&lt;script&gt;
var MyObject = function () {
    var self =
this;
   
this.alertMessage = “Javascript rules”;
    this.OnClick
= function() {
       
alert(self.value);
    }
}();
document.getElementByIdx(”theText”).onclick = 
MyObject.OnClick
&lt;/script&gt;

实质上，这就是JavaScript作用域的问题。如果你看过，你会发现解决方案不止一种。
3.　标识盗贼
在JavaScript中不要使用跟HTML的id一样的变量名。如下代码：
&lt;input type="button"
id="TheButton"&gt;
&lt;script&gt;
    TheButton =
get("TheButton");
&lt;/script&gt;
IE会报对象未定义的错误。我只能说：IE sucks.
4.　字符串只替换第一个匹配
如下代码：
&lt;script&gt;
    var fileName
= "This is a title".replace(" ","_");
&lt;/script&gt;
而实际上，结果是”This_is a title“.
在JavaScript中，String.replace的第一个参数应该是正则表达式。所以，正确的做法是这样：
var fileName = "This is a title".replace(/
/g,"_");
5.　mouseout意味着mousein

事实上，这是由于事件冒泡导致的。IE中有mouseenter和mouseleave，但不是标准的。作者在此建议大家使用库比如YUI来解决问题。
6.　parseInt是基于进制体系的

这个是常识，可是很多人给忽略了parseInt还有第二个参数，用以指明进制。比如，parseInt("09")，如果你认为答案是9，那就错了。因为，在此，字符串以0开头，parseInt以八进制来处理它，在八进制中，09是非法，返回false，布尔值false转化成数值就是0.
因此，正确的做法是parseInt("09", 10).
7.　for...in...会遍历所有的东西
有一段这样的代码：
var arr = [5,10,15]
var total = 1;
for ( var x in arr) {
    total =
total * arr[x];
}
运行得好好的，不是吗？但是有一天它不干了，给我返回的值变成了NaN,
晕。我只不过引入了一个库而已啊。原来是这个库改写了Array的prototype，这样，我们的arr平白无过多出了一个属性（方法），而for...in...会把它给遍历出来。所以这样做才是比较安全的：
for ( var x = 0; x &lt; arr.length; x++)
{
    total =
total * arr[x];
}
其实，这也是污染基本类的prototype会带来危害的一个例证。
8.　事件处理器的陷阱

这其实只会存在使用作为对象属性的事件处理器才会存在的问题。比如window.onclick
=
MyOnClickMethod这样的代码，这会复写掉之前的window.onclick事件，还可能导致IE的内容泄露（sucks
again）。在IE还没有支持DOM
2的事件注册之前，作者建议使用库来解决问题，比如使用YUI:
YAHOO.util.Event.addListener(window, "click",
MyOnClickMethod);
这应该也属于常识问题，但新手可能容易犯错。
9.　Focus Pocus

新建一个input文本元素，然后把焦点挪到它上面，按理说，这样的代码应该很自然：
var newInput =
document.createElement("input");
document.body.appendChild(newInput);
newInput.focus();
newInput.select();
但是IE会报错（sucks again and
again）。理由可能是当你执行fouce()的时候，元素尚未可用。因此，我们可以延迟执行：
var newInput =
document.createElement("input");
newInput.id = "TheNewInput";
document.body.appendChild(newInput);
setTimeout(function(){
//这里我使用闭包改写过，若有兴趣可以对比原文
 document.getElementByIdx('TheNewInput').focus();

 document.getElementByIdx('TheNewInput').select();},
10);

在实践中，JavaScript的陷阱还有很多很多，大多是由于解析器的实现不到位而引起。这些东西一般都不会在教科书中出现，只能靠开发者之间的经验分享。谢天谢地，我们生活在网络时代，很多碰到的问题，一般都可以在Google中找到答案。
本文链接：http://www.blueidea.com/tech/web/2007/4919.asp




