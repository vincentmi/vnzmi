---
layout:     post
title:      "Golang:错误即值 Errors are values"
subtitle:   "来自Rob Pike的博客翻译"
date:       2016-06-22 14:15:00
author:     "Vincent"
header-img: "img/post-bg-dot.jpg"
catalog: true
tags:
    - RD
    - Golang
---

> 英文原版见此 [https://blog.golang.org/errors-are-values](https://blog.golang.org/errors-are-values)
> 作者 :Rob Pike
> 翻译 :Vincent Mi



## 前言

最近用Go写了一下程序,没有try-catch不太适应。因此翻到了这篇文章.
顺手翻译了过来.可能翻译不太好纯为了自己加深理解.

---

## 正文

如何进行错误处理,这是一个Go程序员之间,特别是一些新的Go程序员,会经常讨论的问题.讨论到最后往往由于以下代码的多次出现而变成了抱怨.

```go
if err != nil {
    return err
}
```

我们最近扫描了我们能找到的开源项目,这段代码只在一页或者两页中出现了一次,是不是比你想象的少很多.然而,必须到处写 ```if err != nuil```的感觉依然存在 , 那一定是哪里出了问题,而且明显问题出在Go自己身上.

不幸的是,这是一个误解,而且很容易纠正.或许一个新的Go程序员想问 "怎么会只有一个错误处理?",那么学习这种模式,保持它.在其它语言中可以使用try-catch或者其他类似机制去处理错误.因此程序员认为,当我需要在其他语言中使用try-catch的时候,我只需要在Go写```if err != nil ```,随着时间的推移Go代码里会出现很多这样的代码片段,结果感觉很笨拙.

不管这个解释是否符合,很显然这些Go程序员忘记了一个关于错误的基本观点:错误也是值.

值可以被编程,因此错误也是值,错误也可以被编程

>Values can be programmed, and since errors are values, errors can be programmed.

当然一个常用的涉及到错误值的语句是测试它是不是```nil``` , 但是也有无数的其他事情可以用错误值来做.使用一些其他事情可以让你更好的编程,可以很大程度排除使用if语句检查错误的固定模式.

这是一个简单的示例,来自[bufio](https://golang.org/pkg/bufio/#pkg-overview) 包的[Scanner](http://golang.org/pkg/bufio/#Scanner)类型.它的 [Scan](http://golang.org/pkg/bufio/#Scanner.Scan)方法执行底层的I/O操作,显然它可能引起一个错误.然而[Scan](http://golang.org/pkg/bufio/#Scanner.Scan)方法并不会暴露错误.他返回一个布尔值,通过在[Scan](http://golang.org/pkg/bufio/#Scanner.Scan)运行之后执行的另一个方法来报告是否发生了错误.调用代码如下:

```go
scanner := bufio.NewScanner(input)
for scanner.Scan() {
    token := scanner.Text()
    // process token
}
if err := scanner.Err(); err != nil {
    // process the error
}
```

当然,也有一个对错误的```nil```检查,但是只出现和执行了一次.```Scan``` 也可以这样定义:

```go 
func (s *Scanner) Scan() (token []byte, error)
```

然后示例代码可能写成这样:

```go 
scanner := bufio.NewScanner(input)
for {
    token, err := scanner.Scan()
    if err != nil {
        return err // or maybe break
    }
    // process token
}
```

代码没有很大不同,但是这里有一个重要的区别.在这段代码中,调用代码必须在每个迭代检查错误.但是在原始的```Scanner```API中.错误处理是从关键API抽象出来的.通过token迭代.使用原始的API客户端代码感觉更加自然:循环直到完成,然后再担心错误.错误处理不会干扰流程控制.

幕后发生了什么. ```Scan``` 一旦发生I/O错误,他记录并返回```False```,另外一个方法 [Err](http://golang.org/pkg/bufio/#Scanner.Err) ,当调用代码请求时报告错误值.虽然这很普通但是和到处写 ```if err != nil ``` 或者让调用代码在每个token后检查错误还是不同的. 这就是使用错误值编程.简单的编程.

无论是什么设计,值得强调的是如何编程来处理错误.这里不是讨论避免检查错误,而是如何在Go中优雅的处理错误.

在我出席2014年秋天东京的GoCon时,出现了错误检查代码的话题.Twitter上一个热情的gopher(@jaxk_)发出了同样的抱怨.他展示了一些类似下面的代码:

```go 
_, err = fd.Write(p0[a:b])
if err != nil {
    return err
}
_, err = fd.Write(p1[c:d])
if err != nil {
    return err
}
_, err = fd.Write(p2[e:f])
if err != nil {
    return err
}
// and so on

``` 
非常重复,实际的代码更长,会有更多重复.所以不太容易只通过一个帮助函数进行重构.在理想情况下使用闭包对错误变量进行包装会有一些帮助.

```go
var err error
write := func(buf []byte) {
    if err != nil {
        return
    }
    _, err = w.Write(buf)
}
write(p0[a:b])
write(p1[c:d])
write(p2[e:f])
// and so on
if err != nil {
    return err
}
```

这种方式有效,但是要求在进行写入操作的每个函数中都必须要有一个闭包函数,比起使用独立的帮助函数显得比较笨拙,因为```err```变量需要通过调用进行维护.

通过借鉴上面```Scan```方法的思路,我们可以让错误处理更清晰,更通用和可复用.在我们的讨论中提到这种方式,但是@jxck_ 不太明白怎么去应用它.因为有点语言障碍,经过长时间的交流,我问他是否可以借用他的笔记本来给他展示一些实际的代码.

我定义了一个叫做 ```errWriter``的类型.如下

```go
 type errWriter struct {
    w   io.Writer
    err error
}
```

定义一个```write```方法.他不需要声明成标准的```Write```函数,另外一个明显的区别是他是小写的.```write```调用w的```Write```方法并记录第一个错误供后面使用.

```go
func (ew *errWriter) write(buf []byte) {
    if ew.err != nil {
        return
    }
    _, ew.err = ew.w.Write(buf)
}
```

一旦发生错误,```write```方法不会进行任何操作只会保存错误值.

基于```errWrite```类型和他的```write```方法.上面的代码可以重构为:

```go
ew := &errWriter{w: fd}
ew.write(p0[a:b])
ew.write(p1[c:d])
ew.write(p2[e:f])
// and so on
if ew.err != nil {
    return ew.err
}
```

和使用闭包相比代码更整洁,并且更容易看到实际的写入代码段.没有杂乱的东西,通过对错误值和接口(interface)编程让代码更好.

在同一个包的一些其他代码片段也可以使用这种方式,甚至直接使用```errWriter```类型.

一旦存在```errWriter```,他就能做更多的事情,特别是用来减少人为的工作.他可以计算字节数,将多个写入内容收集到一个缓冲器中再一起发送.等等

实际上这种模式在标准库中经常出现.[archive/zip](http://golang.org/pkg/archive/zip/)包 和[net/http](http://golang.org/pkg/net/http/)包使用了这种方式.特别是[bufio](http://golang.org/pkg/bufio/)包的
```Write```实际上是一个```errWriter```的实现.

虽然```bufio.Writer.Write```为了实现```io.Writer```接口需要返回一个错误.但是它的行为和我们上面的```errWriter.write```方法类似,使用```Flush```报告错误.所以我们上面的例子可以写成:

```go
b := bufio.NewWriter(fd)
b.Write(p0[a:b])
b.Write(p1[c:d])
b.Write(p2[e:f])
// and so on
if b.Flush() != nil {
    return b.Flush()
}

```

这种方法有一些明显的缺点,至少对某些应用场景是这样. 我们无法知道错误发生时,我们的处理过程完成了多少.通常一个简单的检查已经足够,但是如果这个信息很重要,那么我们有必要进行一个细粒度的检查.

我们看到了避免重复的错误处理代码的一种方式,请记住```errWriter```或者```bufio.Writer'''不是简化错误处理的唯一方法,而且也不是适用与所有情况.关键在于错误就是值,Go语言完全可以处理它们.

使用这个语言去简化你的错误处理.但是记住:无论怎么做,一定要检查你自己的错误!

最后,我与@jxck_的交流的整个过程,包括他录的一个小视频,可以从他的[博客](http://jxck.hatenablog.com/entry/golang-error-handling-lesson-by-rob-pike)找到























