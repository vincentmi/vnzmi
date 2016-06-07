---
layout:     post
title:      "PHP 文件写性能比较"
date:       2016-02-17 21:30:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - OP
    - iTerm
---
## 安装lrzsz 支持

使用brew安装

```
brew install lrzsz
```

如果brew下载可能会被墙。如果可以手动进行下载。可以这样处理
<!--more-->
查看brew的缓存路径

```
VincentdeMacBook-Air:bin vincentmi$ brew --cache
/Library/Caches/Homebrew
```

然后将你下载好的文件拷贝到这个目录。再执行一次安装，brew则不会再去下载了。


### 创建命令处理脚本

大神门写好了zmodem的脚本，放到指定位置即可

***/usr/local/bin/iterm2-send-zmodem.sh***

内容如下

```

#!/bin/bash
# Author: Matt Mastracci (matthew@mastracci.com)
# AppleScript from http://stackoverflow.com/questions/4309087/cancel-button-on-osascript-in-a-bash-script
# licensed under cc-wiki with attribution required
# Remainder of script public domain

FILE=`osascript -e 'tell application "iTerm" to activate' -e 'tell application "iTerm" to set thefile to choose file with prompt "Choose a file to send"' -e "do shell script (\"echo \"&(quoted form of POSIX path of thefile as Unicode text)&\"\")"`
if [[ $FILE = "" ]]; then
  echo Cancelled.
  # Send ZModem cancel
  echo -e \\x18\\x18\\x18\\x18\\x18
  echo \# Cancelled transfer
  echo
else
  echo $FILE
  /usr/local/bin/sz "$FILE"
  echo \# Received $FILE
  echo
fi
```

***/usr/local/bin/iterm2-recv-zmodem.sh***

内容如下

```

#!/bin/bash
# Author: Matt Mastracci (matthew@mastracci.com)
# AppleScript from http://stackoverflow.com/questions/4309087/cancel-button-on-osascript-in-a-bash-script
# licensed under cc-wiki with attribution required 
# Remainder of script public domain

FILE=`osascript -e 'tell application "iTerm" to activate' -e 'tell application "iTerm" to set thefile to choose folder with prompt "Choose a folder to place received files in"' -e "do shell script (\"echo \"&(quoted form of POSIX path of thefile as Unicode text)&\"\")"`
if [[ $FILE = "" ]]; then
  echo Cancelled.
  # Send ZModem cancel
  echo -e \\x18\\x18\\x18\\x18\\x18
  echo \# Cancelled transfer
  echo
else
  echo $FILE
  cd "$FILE"
  /usr/local/bin/rz
  echo \# Received $FILE
  echo
fi

```


###修改item2的配置

打开 主菜单 -> Profiles ->Open Profies -> Default ->Edit Profles
选择 Default 
点击 Advanced 选项卡
选择 Triggers -> Edit

增加2个触发器

```
Regular expression: \*\*B0100 
Action: Run Silent Coprocess 
Parameters: /usr/local/bin/iterm2-send-zmodem.sh


Regular expression: \*\*B00000000000000 
Action: Run Silent Coprocess 
Parameters: /usr/local/bin/iterm2-recv-zmodem.sh
```






