---
layout:     post
title:      "使用Flutter构建跨平台的手机APP"
date:       2018-03-28 11:20:00
author:     "Vincent"
header-img:  "img/post-bg-app.jpg"
catalog: true
tags:
    - IOS
    - Android
    - Flutter
    - Google
    
---

## 简介

![Flutter](/img/in_post/flutter.png)

Flutter是Google使用Dart语言开发的开源移动应用开发框架，, 可同时快速的在Android和iOS平台运行,性能无限接近原生。 目前还是Beta版本.Flutter可以理解为一种类似ReactiveNative的框架.但是自己实现了底层的控件绘制.因此性能会有一些优势.提供IOS和安卓原生风格的组件.更多的组件可以从组件库中查看.

官网 [https://flutter.io](https://flutter.io)   
GitHub [https://github.com/flutter/flutter](https://github.com/flutter/flutter)    
组件库: [https://flutter.io/widgets/](https://flutter.io/widgets/)

## 安装

- 先拉版本库

```sh
git clone -b beta https://github.com/flutter/flutter.git
```

使用中国镜像进行安装 .

```sh
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
git clone -b dev https://github.com/flutter/flutter.git
```
将路径加入PATH,```export PATH="$PWD/flutter/bin:$PATH"```
执行```flutter-doctor```  进行安装,会安装一些包和工具.

```sh
$ flutter doctor
Building flutter tool...
Downloading Material fonts...                                4.6s
Downloading package sky_engine...                            4.1s
Downloading common tools...                                 15.1s
Downloading darwin-x64 tools...                             13.1s
Downloading android-arm-profile/darwin-x64 tools...         13.7s
Downloading android-arm-release/darwin-x64 tools...         12.9s
Downloading android-arm64-profile/darwin-x64 tools...        5.3s
Downloading android-arm64-release/darwin-x64 tools...       11.5s
Downloading android-x86 tools...                             8.4s
Downloading android-x64 tools...                            29.1s
Downloading android-arm tools...                            10.4s
Downloading android-arm-profile tools...                    14.7s
Downloading android-arm-release tools...                     3.7s
Downloading android-arm64 tools...                          13.3s
Downloading android-arm64-profile tools...                  18.7s
Downloading android-arm64-release tools...                   9.2s
Downloading ios tools...                                    15.6s
Downloading ios-profile tools...                             6.2s
Downloading ios-release tools...                            15.7s
Downloading Gradle Wrapper...                                3.0s
Doctor summary (to see all details, run flutter doctor -v):
[✓] Flutter (Channel beta, v0.2.3, on Mac OS X 10.13.3 17D102, locale zh-Hans-CN)
[✗] Android toolchain - develop for Android devices
    ✗ Unable to locate Android SDK.
      Install Android Studio from: https://developer.android.com/studio/index.html
      On first launch it will assist you in installing the Android SDK components.
      (or visit https://flutter.io/setup/#android-setup for detailed instructions).
      If Android SDK has been installed to a custom location, set $ANDROID_HOME to that location.
[!] iOS toolchain - develop for iOS devices (Xcode 9.2)
    ✗ Your Mac needs to enabled for developer mode before using Xcode for the first time.
      Run 'sudo DevToolsSecurity -enable' to enable developer mode.
    ✗ libimobiledevice and ideviceinstaller are not installed. To install, run:
        brew install --HEAD libimobiledevice
        brew install ideviceinstaller
    ✗ ios-deploy not installed. To install:
        brew install ios-deploy
    ✗ CocoaPods not installed.
        CocoaPods is used to retrieve the iOS platform side's plugin code that responds to your plugin usage on the Dart side.
        Without resolving iOS dependencies with CocoaPods, plugins will not work on iOS.
        For more info, see https://flutter.io/platform-plugins
      To install:
        brew install cocoapods
        pod setup
[✗] Android Studio (not installed)
[!] Connected devices
    ! No devices available
```

doctor程序或检查Android Studio 和 Xcode 和相关的SDK 模拟器的安装情况.根据情况 自行完成安装即可.

- 安装Android Studio插件,进入菜单```Preferences>Plugins ```
安装 ```Flutter``` 和 ```Dart``` ,之后重启AS.









