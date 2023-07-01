---
layout:     post
title:      "WebRTC技术简介-RTCPeerConnection"
date:       2018-11-14 15:31:00
author:     "Vincent"
image:  "img/post-bg-webrtc.jpg"
catalog: true
tags:
    - webrtc
    - js
---

##  第一个WebRPC应用

WebRPC 需要做以下的几件事:

- 获取音频,视频或者其他数据
- 获取网络信息比如IP地址,端口,并与其他的WebRTC客户端进行交换,穿过NAT合防火墙进行连接.
- 处理信号以便发起请求报告错误或者关闭会话
- 交换客户端支持的媒体信息,比如分辨率,解码器
- 传输音频视频流或者数据

为了获得流数据的 WebRTC实现了以下API

- ```MediaStream``` 获取数据流,比如从用户的摄像头或者麦克风
- ```RPCPeerConnection``` 音频或者视频的调用,具有加密和带宽管理
- ```RTCDataChannel``` 点到点的通用数据传输.

#### MediaStream(即:getUserMedia)

MediaStream用来表示同步的媒体流,例如:从摄像头和麦克风获取的输入包含了视频合音频流.(MediaStreamTrack和```<track>```元素是完全不同的,不要混淆)

为了更好的理解 ```MediaStream``` 你可以打开DEMO , [webrtc.github.io/samples/src/content/getusermedia/gum.](webrtc.github.io/samples/src/content/getusermedia/gum.).在JS控制台检查 ```stream```变量.

每一个```MediaStram```对象都有一个输入,可能是由```getUserMedia()```生成的```MediaStream```,也有一个输出,输出可能是一个```video```对象或者一个```RTCPeerConnection```.

每个```MediaStream```都有一个标签,比如 ```Xk7EuLhsuHKbnjLWkW4yYGNJJ8ONsgwHBvLQ``` (通过 ```stream.id```可以获取).```getAudioTracks()```和```getVideoTracks()```方法会返回一个 ```MediaStreamTrack```数组.

刚才的示例中 ```stream.getAudioTracks()```返回了一个空数组,因为我们没有获取音频.如果连接了摄像头 ```stream.getVideoTracks()``` 会返回包含一个 ```MediaStreamTrack```元素的数组.```MediaStreamTrack```的 ```kind```属性 (值 ```video```或者```audio```)来标识媒体的类型.以及一个```label```  , (比如 ```FaceTime HD Camera (05ac:8514)```) 来对一个或者多个的音视频频道进行描述.当前例子我们只有个视频频道没有音频频道.但是我们想象出现多个频道的情况,比如: 使用前置摄像头,后置摄像头以及麦克风和屏幕分享应用.

```MediaStream```可以通过设置 ```srcObject```属性来绑定到```video```.

>
> ```MediaStramTrack```会激活摄像头,如果不用了要使用 ```track.stop()```来进行关闭.
>

```getUserMedia```也可以作为 ```Web Audio API```的输入节点.

```js
navigator.mediaDevices.getUserMedia({audio: true}, (stream) => {
  // Create an AudioNode from the stream
  const mediaStreamSource =
    audioContext.createMediaStreamSource(stream);
  mediaStreamSource.connect(filterNode);
  filterNode.connect(gainNode);
  // connect the gain node to the destination (i.e. play the sound)
  gainNode.connect(audioContext.destination);
});
```

基于Chromium的应用程序合扩展可以将```audioCapture```和```videoCapture``` 权限加入到manifest文件,这样就只会在安装的时候要求用户授权.使用的时候就不用再点击进行授权了.

#### Constraints 约束

约束用来设置```getUserMedia()```的分辨率.还支持[更多约束设置](http://dev.w3.org/2011/webrtc/editor/getusermedia.html#the-model-sources-sinks-constraints-and-states),比如 纵横比,前后摄像头,帧率,高度,宽度.以及 ```applyConstraints()```方法.

有一个问题,```getUserMedia```的约束参数会影响共享的资源的配置.比如:一个摄像头在一个页卡中以640X480的分辨率打开,那么他就不能在另外的页卡以更高的分辨率打开.因为他只能以一种模式打开.

设置一个不允许的约束值会抛出一个```DOMException``` 或者 如果设置了一个不支持的分辨率会抛出一个 ```OverconstrainedError```.[查看DEMO](webrtc.github.io/samples/src/content/getusermedia/resolution)

#### 屏幕和页卡捕捉

Chrome 应用可以通过 ```chrome.tabCapture``` 和 ```chrome.desktopCapture``` API  来进行实时的桌面分享. 也可以使用Chrome的实验性API ```chromeMediaSource```约束来获取.注意分享屏幕需要HTTPS连接.


## 2 使用```RTCPeerConnection```建立连接

#### 信号 会话控制,网络和媒体信息

WebRTC使用```RTCPeerConnection```在浏览器之间传输流数据.需要一个机制来进行传输的协调和控制消息的发送,这个过程叫做信号处理.信号处理的方法和协议未包含在WebRTC中.

WebRTC应用的开发者可以选择自己喜欢的消息协议,比如 SIP 或者XMPP,任何适合的双向通行信道.[appr.tc](https://appr.tc/)的示例使用了XHR和Channel API 作为信令机制.[Codelab](https://codelabs.developers.google.com/codelabs/webrtc-web/#0)使用 Node运行的Socket.io 库来做.

信号用于交换以下三类信息:

- 会话控制消息:用来初始化或者关闭通讯和报告错误
- 网络配置:我面向外部世界的IP地址合端口
- 媒体能力:什么样的解码器合分辨率可以被我的浏览器支持和浏览器想要什么样的数据.

在p2p流开始之前我们必须成功通过信号交换这些信息.

例如: 假定Alice想与Bob进行通信.下面是一些代码示例.展示了信号处理的动作.代码架设已经有一些信号处理机制.通过```createSignalingChannel()```方法进行创建.注意在Chrome合Opera中```RTCPeerConnection```已经存在了.

```js
// handles JSON.stringify/parse
const signaling = new SignalingChannel();
const constraints = {audio: true, video: true};
const configuration = {iceServers: [{urls: 'stuns:stun.example.org'}]};
const pc = new RTCPeerConnection(configuration);

// send any ice candidates to the other peer
pc.onicecandidate = ({candidate}) => signaling.send({candidate});

// let the "negotiationneeded" event trigger offer generation
pc.onnegotiationneeded = async () => {
  try {
    await pc.setLocalDescription(await pc.createOffer());
    // send the offer to the other peer
    signaling.send({desc: pc.localDescription});
  } catch (err) {
    console.error(err);
  }
};

// once remote track media arrives, show it in remote video element
pc.ontrack = (event) => {
  // don't set srcObject again if it is already set.
  if (remoteView.srcObject) return;
  remoteView.srcObject = event.streams[0];
};

// call start() to initiate
async function start() {
  try {
    // get local stream, show it in self-view and add it to be sent
    const stream =
      await navigator.mediaDevices.getUserMedia(constraints);
    stream.getTracks().forEach((track) =>
      pc.addTrack(track, stream));
    selfView.srcObject = stream;
  } catch (err) {
    console.error(err);
  }
}

signaling.onmessage = async ({desc, candidate}) => {
  try {
    if (desc) {
      // if we get an offer, we need to reply with an answer
      if (desc.type === 'offer') {
        await pc.setRemoteDescription(desc);
        const stream =
          await navigator.mediaDevices.getUserMedia(constraints);
        stream.getTracks().forEach((track) =>
          pc.addTrack(track, stream));
        await pc.setLocalDescription(await pc.createAnswer());
        signaling.send({desc: pc.localDescription});
      } else if (desc.type === 'answer') {
        await pc.setRemoteDescription(desc);
      } else {
        console.log('Unsupported SDP type.');
      }
    } else if (candidate) {
      await pc.addIceCandidate(candidate);
    }
  } catch (err) {
    console.error(err);
  }
};

```

首先,Alice合Bob交换了网络信息,使用 [ICE框架](https://www.html5rocks.com/en/tutorials/webrtc/basics/#ice)查找网络接和端口.

- Alice使用```onicecandidate```回调,创建了一个```RTCPeerConnection```对象.
- 这个回调会在收到网络候选信息后会被调用
- Alice发送序列号之后的网络候选信息给Bob,通过信号信道, 比如 WebSocket或者其他的
- 当Bob获取到网络候选信息之后,他调用```addIceCandidate```来添加远端的描述.

WebRTC 客户端(比如:Bob Alice) 也需要探明和交换本地以及远端的音频合视频信息.比如分辨力合解码能力.信令通过使用会话描述协议（SDP）交换和应答Offer来进行媒体配置信息的信交换：

- Alice运行```RTCPeerConnection```的```createOffer()```方法,这个方法返回ALice的本地会话描述
- 在回调中Alice使用```setLocalDescription()```然后通过他们的信号信道把会话描述发送给Bob.请注意，在调用setLocalDescription（）之前，RTCPeerConnection不会开始收集候选者：这是在JSEP IETF草案中编写的。
- Bob使用```setRemoteDescription()```将Alice发送给他的描述设置未远端的描述.
- Bob运行```RTCPeerConnection.createAnswer()```方法,传递他从Alice得到的描述信息.这样一个匹配他本地的会话就创建好了. createAnswer（）回调传递给RTCSessionDescription：Bob将其设置为本地描述并将其发送给Alice。
- 当Alice获取到Bob的会话描述信息,他使用```setRemoteDescription```设置为远端的描述信息.
- 完成连接


## Webrtc 调用图

![JESP架构图](/img/in-post/webrtc_process.png)


>
> 如果不使用 ```RTCPeerConnection```了要调用```close()```进行关闭.不然会占用较多资源
>

```RTCSessionDescription``` 对象是符合SDP规格的序列号二进制对象.SDP对象可能类似如下的内容:

```sh
v=0
o=- 3883943731 1 IN IP4 127.0.0.1
s=
t=0 0
a=group:BUNDLE audio video
m=audio 1 RTP/SAVPF 103 104 0 8 106 105 13 126
...
a=ssrc:2223794119 label:H4fjnMzxy3dPIgQ7HxuCTLb4wLLLeRHnFxh810
```

获取和交换网络与媒体信息的过程比较类似.但是两个流程都需要在视频和音频流开始之前
完成.

上面描述的 offer/answer架构被叫做 [JESP](http://tools.ietf.org/html/draft-ietf-rtcweb-jsep-00)  JavaScript Session Establishment Protocol .

![JESP架构图](/img/in-post/jsep.png)

一旦信号处理流程成功,数据可以直接在点到点的在调用和被调用者之间进行传输.如果这样操作失败了则通过一个中介服务器进行传输.流的传输是```RPCPeerConnection```的主要工作. 

#### RTCPeerConnection

```RTCPeerConnection``` 是RPC中处理对端流数据的稳定性和效率的组件. 如下图的架构,可以看到```RTCPeerConnection```在架构中扮演的角色,绿色部分很复杂.

![WebRTC architecture (from webrtc.org)](/img/in-post/webrtc_architecture.png)

从JS的视觉看```RTCPeerConnection``` 讲开发人员从无法复杂性中解脱出来.WebRTC使用编码器和协议做了大量工作使得即使在不可靠的网络下也可以进行实时通讯.

- 丢包隐藏
- 回声消除
- 带宽适应性
- 动态抖动缓冲
- 自动增益控制
- 降噪和抑制
- 图像清理

上面的W3C代码从信令角度展示了WebRTC的简化示例。下面是两个正在运行的WebRTC应用程序的演练：第一个是演示RTCPeerConnection的简单示例;第二个是完全可操作的视频聊天客户端。

#### 不通过服务器的 ```RTCPeerConnection```连接

https://webrtc.github.io/samples/src/content/peerconnection/pc1/ 示例代码演示从单个页面实现一个 ```RTCPeerConnection```连接.

示例中 ```pc1```扮演本地端,```pc2```扮演远端.

##### 调用方

1. 创建一个新的 ```RTCPeerConnection```对象并使用```getUserMedia()```添加流.

```js
pc1 = new RTCPeerConnection(servers);
//..
localStream.getTracks().forEach((track) => {
  pc1.addTrack(track,localStream);
}
```

2. 创建有个 ```offer``` 设置为 ```pc1```的本地描述.作为 ```pc2```的远端描述.这些可以在一段代码里搞定,不用用到信号系统.因为调用和被调用方都在一个页面.

```js
pc1.setLocalDescription(desc).then(()=>{
onSetLocalSuccess(pc1);
} ,
onSetSessionDescriptionError 
);
trace('pc2 setRemoteDescription start')

pc2.setRemoteDescription(desc).then(()=>{
 onSetRemoteSuccess(pc2);
},onSetSessionDescriptionError);
```

##### 被调用方

1. 创建 ```pc2```,当```pc1```有流过来就显示到```video```元素

```js

pc2 = new RTCPeerConnection(servers);
pc2.ontrack = gotRemoteStream;
//...
function gotRemoteStream(e){
  vid2.srcObject = e.stream;
}

```

#### ```RTCPeerConnection```加服务器

在现实世界中,WebRTC需要服务器,虽然很简单,但是也包含以下步骤:

- 用户发现彼此并交换真实世界的信息
- WebRTC 客户端应用交换网络信息
- 端之间交换数据,比如分辨率,视频格式和分辨率
- WebRTC客户端穿透NAT和防火墙

换句话说,WebRTC 需要四类服务器端的功能.

- 用户发现和交流
- 信号处理
- NAT和防火墙穿透
- 当p2p链接失败时的中继服务

```RTCPeerConnection```使用的ICE框架,通过[STUN](http://en.wikipedia.org/wiki/STUN)协议,以及STUN的扩展 [TURN](http://en.wikipedia.org/wiki/Traversal_Using_Relay_NAT) 协议来进行P2P网络的穿透.

[```ICE```](http://en.wikipedia.org/wiki/Interactive_Connectivity_Establishment)是一个连接对等端的框架,比如视频聊天的两个客户端.最初ICE尝试通过UDP直接连接对等端,以尽可能的降低延迟.在这个过程中,STUN服务器的作用是让处于NAT后面的端找出他的公开地址以及端口([了解更多STUN和TURN的内容](https://www.html5rocks.com/en/tutorials/webrtc/infrastructure/))

![Finding connection candidates](/img/in-post/stun.png)

如果UDP连接失败,ICE 尝试TCP,如果直接连接失败.ICE会使用一个TURN的中继服务器进行连接, 通常无法连接的情况是由于NAT穿透和防火墙的原因.换句话说 ICE会首先通过UDP使用STUN直接连接端.如果失败则使用TURN的中继服务.上图展示了这个查找网络地址和端口的过程.


![WebRTC data pathways](/img/in-post/dataPathways.png)

WebRTC大牛Justin Uberti 有个Slide,详细讲解了ICE,STUN和TURN,地址是 [https://www.youtube.com/watch?v=p2HzZkd2A40&t=21m12s](https://www.youtube.com/watch?v=p2HzZkd2A40&t=21m12s) 示例中还包含一个TURN和STUN的实现.

#### 一个简单的视频聊天客户端

体验WebRTC的完整功能,包含信令,防火墙穿透使用STUN服务器等功能,访问 [https://appr.tc/](https://appr.tc/).这个APP使用 [adapter.js](https://github.com/webrtc/adapter)
一个适配层以屏蔽一些差异.访问更多信息 可以查看 [https://webrtc.org/web-apis/interop](https://webrtc.org/web-apis/interop)

代码记录了比较详细的日志.以便让大家通过代码了解更多细节.

如果上面的看不懂可以看 [https://codelabs.developers.google.com/codelabs/webrtc-web/](https://codelabs.developers.google.com/codelabs/webrtc-web/) ,这个教程教大家一步步建立一个完整的视频聊天应用.


### 网络结构

WebRTC 目前实现为只支持单个点到点的通讯.但是也可以被用于更复杂的场景:比如,多个点与点之间直接连接的点到点方式.或者通过一个 多点控制单元(MCU),通过服务器来处理大量的参与者进行选择性的流转发,音视频的混合和录制.

![Multipoint Control Unit topology example](/img/in-post/mcu.png)











