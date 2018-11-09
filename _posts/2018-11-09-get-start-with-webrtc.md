---
layout:     post
title:      "WebRTC技术简介"
date:       2018-11-09 15:31:00
author:     "Vincent"
header-img:  "img/post-bg-webrtc.jpg"
catalog: true
tags:
    - webrtc
    - js
    
---

## Google I/O 的介绍

https://youtu.be/p2HzZkd2A40


## 1 .通过```getUserMedia()```使用摄像头和麦克风

通过 ```getUserMedia()```我们可以在不使用任何插件的情况下访问到摄像头和麦克风.

#### 特性检查

只需要检查```navigator.mediaDevices.getUserMedia``对象是否存在就可以了

```js
function hasGetUserMedia() {
  return !!(navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia);
}

if (hasGetUserMedia()) {
  // Good to go!
} else {
  alert('getUserMedia() is not supported by your browser');
}
```

#### 访问对象

要使用媒体设备需要申请权限,```getUserMedia()```的参数是一个指定了权限细节的对象,如果需要访问摄像头传递 ```{video : true}```,要使用摄像头和麦克风则传递 ```{video:true,audio:true}```

```html
<video id="video" autoplay></video>

<script>
const constraints = {
  video: true
};
navigator.mediaDevices.getUserMedia(constraints).
  then(function(stream) { 
  	document.querySelector('#video').srcObject = stream
  });
</script>
```

媒体捕捉可以与H5对象``` <video>```和```<audio>```进行连接.注意,我们直接设置了一个 ```MediaStream``` 对象给  ``` video```对象,没有设置 ```src```或者```source```属性.

#### 设置媒体参数

传递给 ```getUserMedia()```的参数还可以设置更多需求和限制给返回的媒体流.例如:你可以除基础的需求外设置额外的参数让返回高清画质.

```js
const hdConstraints = {
  video: {width: {min: 1280}, height: {min: 720}}
};

navigator.mediaDevices.getUserMedia(hdConstraints).
  then((stream) => {video.srcObject = stream});

...

const vgaConstraints = {
  video: {width: {exact: 640}, height: {exact: 480}}
};

navigator.mediaDevices.getUserMedia(vgaConstraints).
  then((stream) => {video.srcObject = stream});
```

如果设置了当前设备不支持的分辨率则会报一个 ```OverconstrainedError```错误.

详情见 [https://w3c.github.io/mediacapture-main/getusermedia.html#idl-def-MediaTrackConstraints](https://w3c.github.io/mediacapture-main/getusermedia.html#idl-def-MediaTrackConstraints)


#### 选择媒体源

```navigator.mediaDevices.enumerateDevices()```可以列举当前设备的可用媒体设备.
代码略长 //_-,但是还是很简单的

```js
const videoElement = document.querySelector('video');
const audioSelect = document.querySelector('select#audioSource');
const videoSelect = document.querySelector('select#videoSource');

navigator.mediaDevices.enumerateDevices()
  .then(gotDevices).then(getStream).catch(handleError);

audioSelect.onchange = getStream;
videoSelect.onchange = getStream;

function gotDevices(deviceInfos) {
  for (let i = 0; i !== deviceInfos.length; ++i) {
    const deviceInfo = deviceInfos[i];
    const option = document.createElement('option');
    option.value = deviceInfo.deviceId;
    if (deviceInfo.kind === 'audioinput') {
      option.text = deviceInfo.label ||
        'microphone ' + (audioSelect.length + 1);
      audioSelect.appendChild(option);
    } else if (deviceInfo.kind === 'videoinput') {
      option.text = deviceInfo.label || 'camera ' +
        (videoSelect.length + 1);
      videoSelect.appendChild(option);
    } else {
      console.log('Found another kind of device: ', deviceInfo);
    }
  }
}

function getStream() {
  if (window.stream) {
    window.stream.getTracks().forEach(function(track) {
      track.stop();
    });
  }

  const constraints = {
    audio: {
      deviceId: {exact: audioSelect.value}
    },
    video: {
      deviceId: {exact: videoSelect.value}
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).
    then(gotStream).catch(handleError);
}

function gotStream(stream) {
  window.stream = stream; // make stream available to console
  videoElement.srcObject = stream;
}

function handleError(error) {
  console.error('Error: ', error);
}
```

#### 安全性

```getUserMedia()```只能被 HTTPS的URL,```localhost``` 和```file://```调用.浏览器每次都会弹出一个申请权限的弹框,用户的选择会被存储起来.可以从浏览器的设置中进行修改.

>
> ```MediaStreamTrack``` 会激活摄像头,摄像头的灯会亮起来,如果你不想用了可以调用
> ```track.stop()```来关闭输入流.
>


#### 获取视频截图

```<canvas>``` API的 ```ctx.drawImage(video, 0, 0)```方法可以把视频帧截取到```<canvas>``` 上.我们通过```getUserMedia()``` 获取视频,之后可以很容易的截取实时视频截图.

```html

<video autoplay></video>
<img src="">
<canvas style="display:none;"></canvas>

<script>
const captureVideoButton =
  document.querySelector('#screenshot .capture-button');
const screenshotButton = document.querySelector('#screenshot-button');
const img = document.querySelector('#screenshot img');
const video = document.querySelector('#screenshot video');

const canvas = document.createElement('canvas');

captureVideoButton.onclick = function() {
  navigator.mediaDevices.getUserMedia(constraints).
    then(handleSuccess).catch(handleError);
};

screenshotButton.onclick = video.onclick = function() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  // Other browsers will fall back to image/png
  img.src = canvas.toDataURL('image/webp');
};

function handleSuccess(stream) {
  screenshotButton.disabled = false;
  video.srcObject = stream;
}
</script>
```

[更复杂的应用](https://www.html5rocks.com/zh/tutorials/getusermedia/intro/)

## 2 使用```RTCPeerConnection```建立连接


## 3 使用 ```RTCDataChannel``` 传递数据









