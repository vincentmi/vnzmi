---
layout:     post
title:      "golang协程和channel使用"
date:       "2021-11-04 17:12:00"
author:     "Vincent"
image:  "img/post-bg-golang.jpg"
catalog: true
tags:
    - golang
    - goroutine
    - channel
---

## 简介

协程是golang的一大特色和卖点. *协程(goroutine)* 是轻量级的执行线程,使用```go```关键字到函数或者lamba表达式可以快速启动协程.协程函数的返回值会被抛弃.线程的调度由操作系统来管理，是抢占式调度。而协程不同，协程需要互相配合，主动交出执行权。

## 配置

**GOMAXPROCS** 设置逻辑CPU数量,一般情况下使用CPU核心数量值.使用足够的线程来提高golang的并行执行效率.如果你的业务是IO密集型则可以设置数倍与CPU核心数的值来得到更好的性能.如果Go程序在容器中执行则需要根据情况减少该值得,因为容器中无法使用到宿主机的全部核心.设置更小的值可以避免线程切换的开销.

## 使用channel进行协程通讯

#### 定义通道

```go
ch1 := make(chan string) //定义了一个无缓冲的string通道
ch2 := make(chan string , 4) //定义了一个4个元素的string通道
```

#### 通道操作符

```go
ch1 <- "Chengdu" //向通道写入数据
itemOfCh1 := <- ch1 //从ch1通道读取一条数据
<- ch1 //读取通道的下一个值
var in_only chan<- int //只能接收通道
var out_only <-chan int //只读取的通道
close(ch) //关闭通道
```

#### 通道阻塞

默认情况通道是同步无缓冲的,在接受方未准备好之前发送方是阻塞的.通道中没有数据则接收方也是阻塞的.

```go
package main

import (
	"fmt"
	"time"
)

func f1(in chan int) {
	data := <-in
	fmt.Println(data)
}

func main() {
	out := make(chan int)
	out <- 2
	fmt.Println(v)
	go f1(out)
	time.Sleep(100 * time.Millisecond)
}
```

> 以上程序会panic退出,因为out写入数据并没有接受者,因此main主协程被阻塞了.后面的代码永远不会被执行,因此通道永远不会有数据,产生了死锁.```修改 out:=make(chan int , 1)``` 让通道有一个缓冲则不会死锁.或者在写入前启动读取的协程.或者在另外一个协程来读取都可以解决这个问题.

#### 使用信号量

可以通过信号量来让主协程等待子协程的完成退出执行.

```go
package main

import (
	"fmt"
	"time"
)

func f1(in chan int, done chan int) {
	data := <-in
	fmt.Println(data)
	time.Sleep(10e9)
	done <- 1
}

func main() {
	out := make(chan int)
	done := make(chan int)
	go f1(out, done)
	out <- 2
	<-done
}

```

输出 2 之后10秒后程序才会退出,我们就不需要使用sleep来让主进程执行.

#### 关闭通道

显式的关闭通道,关闭通道表示发送者不会有新的数据发送给接受者了.只有发送者需要关闭通道.

```go
ch := make(chan int )
defer close(ch)

data,ok := <-ch //接收到数据则ok为 true,使用ok可以检测通道是否关闭或者阻塞

```

下面这种情况,读取通道在主进程不会报死锁错误,因为检查到通道关闭后就不进行通道读取跳出循环,因此不会再继读没有写入的通道.所以没有死锁.

```go
package main

import "fmt"

func makeStream(n int) chan bool {
	ch := make(chan bool, n)
	go func() {
		for i := 0; i < n; i++ {
			ch <- true
		}
		close(ch)
	}()
	return ch
}

func main() {
	stream := makeStream(5)

	for {
		v, ok := <-stream
		if !ok {
			break
		}
		fmt.Println(v)
	}
}

```

#### 使用select 切换协程

从不同并发协程获取值可以用```select```关键字来进行轮训.通常和```for```循环一起使用

- 如果都阻塞了等待其中一个可以处理
- 如果多个可以处理随机选择一个.外层有循环则下次再处理剩余的
- 如果没有通道可以处理而有```default```则执行default.否则一直阻塞
- 如果没有case,这select会一直阻塞
- 可以使用break跳出select

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() {
		for i := 0; i < 10; i++ {
			ch1 <- fmt.Sprintf("A%d", i)
		}
	}()

	go func() {
		for i := 0; i < 10; i++ {
			ch2 <- fmt.Sprintf("B%d", i)
		}

	}()

	go func() {
		for {
			select {
			case v := <-ch1:
				fmt.Println(v)
			case v := <-ch2:
				fmt.Println(v)
			}
		}
	}()

	time.Sleep(1e9)
}
```

可以使用这种模式做为服务端来循环处理客户请求

#### 计时器(Ticker)

```go
type Ticker struct {
	C <-chan Time // The channel on which the ticks are delivered.
	r runtimeTimer
}
```

定时器的C变量会根据你创建的定时器时间,在给定时间内向该通道写入时间

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.NewTicker(time.Second)

	go func() {
		for {
			v := <-t.C
			fmt.Println(v)
		}
	}()

	time.Sleep(10e9) // <-time.After(10e9) 使用通道来设置超时
}
```

> 使用 ```time.Tick(duration)```可以直接获取通道,类似```time.NewTicker(1e9).C```
>
> ```time.After(duration)```只发送一次时间.可以使用这个通道来处理超时

## 协程的恢复

协程在遭遇```panic```时安全退出,而不影响其他协程

```go
package main

import (
	"log"
	"time"
)

func doWork() {
	time.Sleep(4e9)
	panic("fk")
}

func main() {

	go func() {
		for {
			log.Printf("another worker")
			time.Sleep(1e9)
		}
	}()

	go func() {

		defer func() {
			if err := recover(); err != nil {
				log.Printf("出问题了 %s", err)
			}
		}()

		doWork()
	}()

	time.Sleep(10e9)
}

```

## 使用锁还是通道

在一种场景下,有多个任务,一个worker处理一项任务.这种场景很适合使用通道和协程来解决问题

```go
package main

type Task struct{}
type Result struct{}

func process(Task *Task) Result {
	return Result{}
}

func main() {

	tasks, results := make(chan Task), make(chan Result)

	workCount := 10

	//创建任务
	go func() {
		for i := 0; i < workCount; i++ {
			tasks <- Task{}
		}
	}()

	//启动worker
	for i := 0; i < workCount; i++ {
		go func() {
			for {
				t := <-tasks
				result := process(&t) //处理数据
				results <- result     //写入结构
			}
		}()
	}

	//消费结果

}

```



- 使用锁的情景：
  - 访问共享数据结构中的缓存信息
  - 保存应用程序上下文和状态信息数据
- 使用通道的情景：
  - 与异步操作的结果进行交互
  - 分发任务
  - 传递数据所有权

