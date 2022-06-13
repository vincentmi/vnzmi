---
layout:     post
title:      "播放器"
date:       2006-01-14 12:44:42
author:     "Vincent"
header-img:  "img/post-bg-dot.jpg"
catalog: false
tags:
    - 新浪博客
    - 技术文章
---



匹配

```<tr....>....</tr>``` 标签 

```/<tr(>|\s[^>]{0,}>).{0,}?<\/tr>/```
 
 

不知这播放器相关参数说明能否帮上你的忙(默认0为否,-1或1为是) 


```xml

<object classid="clsid:22D6F312-B0F6-11D0-94AB-0080C74C7E95" id="MediaPlayer1" width="286" height="225"> 
    <param name="AudioStream" value="-1"> 
    <param name="AutoSize" value="-1"> <!--是否自动调整播放大小--> <param name="AutoStart" value="-1"> <!--是否自动播放--> 
    <param name="AnimationAtStart" value="-1"> 
    <param name="AllowScan" value="-1"> 
    <param name="AllowChangeDisplaySize" value="-1"> 
    <param name="AutoRewind" value="0"> 
    <param name="Balance" value="0"> <!--左右声道平衡,最左-9640,最右9640--> 
    <param name="BaseURL" value> 
    <param name="BufferingTime" value="15"> <!--缓冲时间--> 
    <param name="CaptioningID" value> 
    <param name="ClickToPlay" value="-1"> 
    <param name="CursorType" value="0"> 
    <param name="CurrentPosition" value="0"> <!--当前播放进度 -1 表示不变,0表示开头 单位是秒,比如10表示从第10秒处开始播放,值必须是-1.0或大于等于0--> 
    <param name="CurrentMarker" value="0"> 
    <param name="DefaultFrame" value> 
    <param name="DisplayBackColor" value="0"> 
    <param name="DisplayForeColor" value="16777215"> 
    <param name="DisplayMode" value="0"> 
    <param name="DisplaySize" value="0"> <!--视频1-50%, 0-100%, 2-200%,3-全屏 其它的值作0处理,小数则采用四舍五入然后按前的处理--> 
    <param name="Enabled" value="-1"> 
    <param name="EnableContextMenu" value="-1"> <!-是否用右键弹出菜单控制--> <param name="EnablePositionControls" value="-1"> 
    <param name="EnableFullScreenControls" value="-1"> 
    <param name="EnableTracker" value="-1"> <!--是否允许拉动播放进度条到任意地方播放--> 
    <param name="Filename" value="http://01.wma" valuetype="ref"> 
    <!--播放的文件地址--> 
    <param name="InvokeURLs" value="-1"> 
    <param name="Language" value="-1"> 
    <param name="Mute" value="0"> <!--是否静音--> 
    <param name="PlayCount" value="10"> <!--重复播放次数,0为始终重复--> <param name="PreviewMode" value="-1"> 
    <param name="Rate" value="1"> <!--播放速率控制,1为正常,允许小数--> <param name="SAMIStyle" value> <!--SAMI样式--> 
    <param name="SAMILang" value> <!--SAMI语言--> 
    <param name="SAMIFilename" value> <!--字幕ID--> 
    <param name="SelectionStart" value="-1"> 
    <param name="SelectionEnd" value="-1"> 
    <param name="SendOpenStateChangeEvents" value="-1"> 
    <param name="SendWarningEvents" value="-1"> 
    <param name="SendErrorEvents" value="-1"> 
    <param name="SendKeyboardEvents" value="0"> 
    <param name="SendMouseClickEvents" value="0"> 
    <param name="SendMouseMoveEvents" value="0"> 
    <param name="SendPlayStateChangeEvents" value="-1"> 
    <param name="ShowCaptioning" value="0"> <!--是否显示字幕,为一块黑色,下面会有一大块黑色,一般不显示--> 
    <param name="ShowControls" value="-1"> <!--是否显示控制,比如播放,停止,暂停--> 
    <param name="ShowAudioControls" value="-1"> <!--是否显示音量控制--> 
    <param name="ShowDisplay" value="0"> <!--显示节目信息,比如版权等--> 
    <param name="ShowGotoBar" value="0"> <!--是否启用上下文菜单--> 
    <param name="ShowPositionControls" value="-1"> <!--是否显示往前往后及列表,如果显示一般也都是灰色不可控制--> 
    <param name="ShowStatusBar" value="-1"> <!--当前播放信息,显示是否正在播放,及总播放时间和当前播放到的时间--> 
    <param name="ShowTracker" value="-1"> <!--是否显示当前播放跟踪条,即当前的播放进度条--> 
    <param name="TransparentAtStart" value="-1"> 
    <param name="VideoBorderWidth" value="0"> <!--显示部的宽部,如果小于视频宽,则最小为视频宽,或者加大到指定值,并自动加大高度.此改变只改变四周的黑框大小,不改变视频大小--> 
    <param name="VideoBorderColor" value="0"> <!--显示黑色框的颜色, 为RGB值,比如ffff00为黄色--> 
    <param name="VideoBorder3D" value="0"> 
    <param name="Volume" value="0"> <!--音量大小,负值表示是当前音量的减值,值自动会取绝对值,最大为0,最小为-9640--> 
    <param name="WindowlessVideo" value="0"> <!--如果是0可以允许全屏,否则只能在窗口中查看--> 
</object> 
```

上面的这个播放器是老式的那种,新式播放器是在MediaPlayer9.0以后出现的,也就是说只有装了9.0或9.0以上的播放器才能正常使用的. -------------------------------------------------------------------------------- 下面是新式播放器代码,相对以前的来说要简单很多: 


```xml
    <object id="player" height="64" width="260" classid="CLSID:6BF52A52-394A-11d3-B153-00C04F79FAA6"> 
    <param NAME="AutoStart" VALUE="-1"> <!--是否自动播放--> 
    <param NAME="Balance" VALUE="0"> <!--调整左右声道平衡,同上面旧播放器代码--> 
    <param name="enabled" value="-1"> <!--播放器是否可人为控制--> 
    <param NAME="EnableContextMenu" VALUE="-1"> <!--是否启用上下文菜单--> 
    <param NAME="url" VALUE="http://1.wma"> <!--播放的文件地址--> <param NAME="PlayCount" VALUE="1"> <!--播放次数控制,为整数--> 
    <param name="rate" value="1"> <!--播放速率控制,1为正常,允许小数,1.0-2.0--> 
    <param name="currentPosition" value="0"> <!--控件设置:当前位置--> 
    <param name="currentMarker" value="0"> <!--控件设置:当前标记--> 
    <param name="defaultFrame" value=""> <!--显示默认框架--> 
    <param name="invokeURLs" value="0"> <!--脚本命令设置:是否调用URL--> <param name="baseURL" value=""> <!--脚本命令设置:被调用的URL--> <param name="stretchToFit" value="0"> <!--是否按比例伸展--> 
    <param name="volume" value="50"> <!--默认声音大小0%-100%,50则为50%--> <param name="mute" value="0"> <!--是否静音--> 
    <param name="uiMode" value="mini"> <!--播放器显示模式:Full显示全部;mini最简化;None不显示播放控制,只显示视频窗口;invisible全部不显示--> 
    <param name="windowlessVideo" value="0"> <!--如果是0可以允许全屏,否则只能在窗口中查看--> 
    <param name="fullScreen" value="0"> <!--开始播放是否自动全屏--> 
    <param name="enableErrorDialogs" value="-1"> <!--是否启用错误提示报告--> 
    <param name="SAMIStyle" value> <!--SAMI样式--> 
    <param name="SAMILang" value> <!--SAMI语言--> 
    <param name="SAMIFilename" value> <!--字幕ID--> 
</object>
```



