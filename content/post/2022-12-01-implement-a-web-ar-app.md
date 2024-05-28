---
layout:     post
title:      "开发一个基于WEB的AR应用"
date:       "2022-12-01 10:00:00"
author:     "Vincent"
image:  "/img/3d.png"
catalog: true
tags:
    - AR.js
    - Aframe
    - WebRTC
    - Js
---

##  AR.js

AR.js 是用于 Web 增强现实的轻量级库，具有图像跟踪、基于位置的 AR 和标记跟踪等功能。

github 地址 : https://github.com/AR-js-org/AR.js
文档:  https://ar-js-org.github.io/AR.js-Docs/

## 基于位置的AR

### gps-camera 组件

场景中允许一个该对象,将该对象绑定到 ```camera``` 实体.用于捕捉设备的运动和摄像机进行关联,处理旋转 位置等变化.

```html
<a-camera gps-camera rotation-reader></a-camera>
```

> ```rotation-reader``` 用于处理旋转事件.参考AFrame文档  https://aframe.io/docs/0.9.0/components/camera.html#reading-position-or-rotation-of-the-camera


### gps-entity-place 组件

场景中允许多个该组件.该组件定义定义了实体的GPS位置,当设备指向物体时显示该实体,如果比较远则显示的比较小,太远了则会隐藏该组件.

```html
<a-box material="color: yellow" gps-entity-place="latitude: <your-latitude>; longitude: <your-longitude>"/>
```

> 使用Aframe的```position```属性可以指定该实体的高度信息,单位米.
> ```<a-box material="color: yellow" gps-entity-place="latitude: <your-latitude>; longitude: <your-longitude>" position="0 30 0"/>```

##### 添加自定义属性

```js
const distanceMsg = document.querySelector('[gps-entity-place]').getAttribute('distanceMsg');
console.log(distanceMsg);   // "890 meters"
```















