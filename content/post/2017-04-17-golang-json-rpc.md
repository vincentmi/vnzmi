---
layout:     post
title:      "Golang net/rpc 开发jsonrpc服务"
date:       2017-04-17 16:01:00
author:     "Vincent"
image:  "img/post-bg-golang.jpg"
catalog: true
tags:
    - golang
    - rpc
---

## RPC

RPC作为微服务框架下的各个模块的通讯协议进行系统内部各个服务之间的沟通。随着业务量的增大和系统的复杂度增加，可能还需要使用系统总线对各个消息进行路由、异步调用以及流量控制。Go提供了```net/rpc```包来实现对RPC的支持,通过启动一个服务器，注册一个对象暴露他的公共方法来允许远程调用， 一个服务器可以注册多个不数据类型的对象（服务），但是将一个数据类型注册成不同服务会产生一个错误。默认使用```GRPC```协议来进行数据编码。也可以通过实现```ServiceCodec```来自己控制消息的编码和解码。

## Go RPC服务
Go中可以注册为服务的对象需要满足以下几个条件

- 方法是类型是公共的，可以在包外使用
- 方法是公共的，可以在包外进行调用
- 方法有两个参数，都是公共类型或者Go内建的类型
- 第二个参数是一个指针
- 方法的返回类型是```error```

方法的定义类似这种

```go
func (t *T) MethodName(argType T1, replyType *T2) error
```

第一个参数是调用者发过来的参数，第二个调用结果返回的值的指针。返回非```nil```的字符串会被客户端以错误信息接收

## Golang net/rpc 服务端

Golang RPC方法需要满足以下条件
-

```go
package main

import (
	"staff_account/account"
	"net/rpc"
	"staff_account/db"
	"log"
	"net/rpc/jsonrpc"
	"net"
)

func checkErr(err error){
	if err != nil {
		log.Fatalf("RPC-SVR-FAIL: %v",err)
	}
}

func main() {

	db.GetInstance().SetDSN("root:root@tcp(192.168.33.10:3306)/staff_account?charset=utf8")

	//log.Print(db.GetInstance().Row("SELECT * FROM staff"  ))

	account := new(account.Account)
	s := rpc.NewServer()
	err := s.Register(account)
	checkErr(err)

	s.HandleHTTP(rpc.DefaultRPCPath ,rpc.DefaultDebugPath)

	port := ":9400"

	net ,err :=  net.Listen("tcp" ,port)
	log.Printf("RPC Listening  at :%v ",port)

	for {
		conn, err := net.Accept()
		checkErr(err)
		log.Printf("RPC-ACCEPT: %v "  , conn.RemoteAddr() )
		go s.ServeCodec(jsonrpc.NewServerCodec(conn))
	}
	/*
	checkErr(err)
	//db.GetInstance().SetDSN("postgres://root@192.168.1.62:26257/staff_account?sslmode=disable")
	err = http.Serve(net ,nil)
	checkErr(err)*/
}
````


待续







