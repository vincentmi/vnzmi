---
layout:     post
title:      "WebRTC技术简介-RTCDataChannel"
date:       2018-12-14 15:31:00
author:     "Vincent"
header-img:  "img/post-bg-webrtc.jpg"
catalog: true
tags:
    - webrtc
    - js
---

##  RTCDataChannel

WebRTC可以像音频和视频一样支持实时通讯来传输其他类型的数据.

```RTCDataChannel``` API可以使端到端进行任意数据的交换,保持低延迟和高吞吐量.这里有一些单页DEMO可供参考. [webrtc.github.io/samples/#datachannel ](webrtc.github.io/samples/#datachannel ) 和 [WebRTC codelab ](https://codelabs.developers.google.com/codelabs/webrtc-web/#0) 展示了如何建立一个简单的文件传输应用.

这个API可以应用到很多业务场景:

- 游戏
- 远程控制应用
- 实时文字聊天
- 文件传输
- 去中心化网络

这个API有很多特性扩展	```RTCPeerConnection``` 让他进行强大和灵活的端到端通讯.

- RTCPeerConnection 的会话设置
- 多个同步通道，具有优先级。
- 可靠和不可靠的传输语意
- 内置的安全和拥堵控制
- 和音视频单独或者分开使用

这个语法特意设置的比较像```WebSocket```,包含一个 ```send()```方法和一个  ```message```事件.

```js
const localConnection = new RTCPeerConnection(servers);
const remoteConnection = new RTCPeerConnection(servers);
const sendChannel =
  localConnection.createDataChannel('sendDataChannel');

// ...

remoteConnection.ondatachannel = (event) => {
  receiveChannel = event.channel;
  receiveChannel.onmessage = onReceiveMessage;
  receiveChannel.onopen = onReceiveChannelStateChange;
  receiveChannel.onclose = onReceiveChannelStateChange;
};

function onReceiveMessage(event) {
  document.querySelector("textarea#send").value = event.data;
}

document.querySelector("button#send").onclick = () => {
  var data = document.querySelector("textarea#send").value;
  sendChannel.send(data);
};
```

通讯直接发生在浏览器之间.所以 ```RTCDataChannel```在使用了TURN中继服务来应对网络穿透失败的情况下还可以比 ```WebSocket```更快.

```RTCDataChannel``` 可以在 Chrome,Safari,FireFox,Opera 和 Samsung Internet中使用.[Cube Slam](http://www.cubeslam.com/) 使用这个API来进行游戏状态通讯.
[Sharefest](https://github.com/Peer5/ShareFest)通过该API实现了文件分享.[PeerCDN](https://techcrunch.com/2013/12/17/yahoo-acquires-peercdn/) 使用这个API来做内容分发.

[IETF相关草案](http://tools.ietf.org/html/draft-jesup-rtcweb-data-protocol-00)


## 安全


实时通讯应用或者插件可能有一些被攻击的方式:

- 未经过加密的媒体或者数据可能被网络中的路由器截取
- 应用可能在用户不知情的情况下录制或者分发音频或者视频
- 恶意或者病毒软件可能混进插件里诱导用户安装

WebRTC有一些特性来避免这些问题:
- WebRTC 使用安全协议 [DTLS](http://en.wikipedia.org/wiki/Datagram_Transport_Layer_Security) 和 [SRTP](http://en.wikipedia.org/wiki/Secure_Real-time_Transport_Protocol)
- 所有组件强制进行加密
- WebRTC 不是一个插件.他的组件运行在浏览器的沙箱环境运行,而不是在单独的进程.组件不需单独安装随着浏览器的更新进行更新.
- 摄像头和麦克风的访问必须进行明显的授权,运行时明确的展示给用户.

[了解WebRTC的安全架构](http://www.ietf.org/proceedings/82/slides/rtcweb-13.pdf)

## 开发工具

- 正在进行的WebRTC的统计信息可以在一下地方看到
	- chrome://webrtc-internals
	- opera://webrtc-internals
	- about:webrtc
- 浏览器兼容tips [interop node](http://www.webrtc.org/web-apis/interop)
- [adapter.js](https://github.com/webrtc/adapter) 适配层
- 学习WebRTC信令,[了解](https://appr.tc/)
- [WebRTC框架](http://io13webrtc.appspot.com/#69),[WebRTC服务](http://io13webrtc.appspot.com/#72)


## 终于翻完

WebRTC终于翻译完,但是肯定一堆问题.等我去Codeing做一些应用再来更新.






