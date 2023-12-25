---
layout:     post
title:      "使用OpenCV（1）基础"
date:       "2023-12-08 17:15:00"
author:     "Vincent"
image:  "/img/post-bg-python.png"
catalog: true
tags:
    - opentcv
    - python
---

# 安装

```sh
 pip install opencv-python
 ```

# 验证安装

通过使用opencv 打开一个图片来验证安装是否成功。

```py
import cv2 as cv
img = cv.imread("./bird.png")
cv.imshow("Display window", img)
k = cv.waitKey(0) 
```
运行后会打开文件，点击任何键退出窗口。

# 图形基础

## 数据结构```mat```

低版本的OpenCV使用来自于C语言的 ```IplImage``` 结构体来存储图形资料，该结构的问题在于需要手动进行内容管理，OpenCV2.0引入了一个新的数据结构```Mat```来进行图形的存储。用户不用再手动进行内存分配和回收。已经存在的```mat```对象重用。

```mat```是一个包含两部分数据的类：矩阵头（包含诸如矩阵大小、用于存储的方法、存储矩阵的地址等信息）和指向包含象素矩阵的指针。 矩阵头大小是恒定的，但是矩阵本身的大小可能因图像而异，并且通常会大几个数量级。

## 读取图片 

```cv.imread("./bird.png")```读取图片到```mat```数据结构。

```img = cv.imread("./bird.png",IMREAD_UNCHANGED)```的第二个参数

- IMREAD_COLOR 加载成BGR格式，默认选项
- IMREAD_UNCHANGED 载入原始图片，如果有ALPHA通道则加载ALPHA通道
- IMREAD_GRAYSCALE 加载灰度图

> OpenCV 支持图像格式 Windows 位图 (bmp)、便携式图像格式（pbm、pgm、ppm）和 Sun 光栅（sr、ras）。 在插件的帮助下（如果您自己构建库，则需要指定使用它们，但在我们默认提供的软件包中）您还可以加载图像格式，例如 JPEG（jpeg、jpg、jpe）、JPEG 2000（jp2 - 在 CMake 中的代号为 Jasper）、TIFF 文件（tiff、tif）和可移植网络图形（png）。 此外，OpenEXR 也是一种可能性。

## 保存图片 

```py
 cv.imwrite("sample.png", img)
 ```
将图片写入到文件中。

 ## 捕捉摄像头视频流

 ```py
import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("无法获取摄像头")
    exit()
while True:
    # 一帧一帧读取图片
    ret, frame = cap.read()
    # 读取成功进行展示
    if not ret:
        print("无法读取帧 (可能流结束了?). 退出 ...")
        break
    # 帧处理代码
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # 展示帧内容
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
# 完成后释放摄像头
cap.release()
cv.destroyAllWindows()
 ```

 你也可以对摄像头进行设置，通过 ```cap.get(propId)``` 检查特性，[特性列表见此](https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d)，然后通过```cap.set(propId, value)```设置。 例如：使用 ```cap.get(cv.CAP_PROP_FRAME_WIDTH)```或者视频宽度，然后修改 ```ret = cap.set(cv.CAP_PROP_FRAME_WIDTH,320)```

## 播放视频

```py
import numpy as np
import cv2 as cv
cap = cv.VideoCapture("video.avi")
...
```

和获取摄像头的代码一样只是将 ```cv.VideoCapture```内容改成视频文件保存的位置即可。

## 保存视频

保存视频需要创建```VideoWriter(file,FourCC,fps,frame_resolution)```对象。指定保存的文件位置，编码器，帧率，分辨率参数进行保存。```isColor```标识用于指定是否转换成黑白画面。

FourCC 是由4个字节指定的编码，编码器支持的编码可以从 [fourcc.org](http://fourcc.org)查看. 平台无关，下面在各个操作系统可以正常工作的编码如下：

- Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2. (XVID 建议使用. MJPG 文件较大. X264 可以更好的压缩视频)
- Windows: DIVX 
- MAC : MJPG (.mp4), DIVX (.avi), X264 (.mkv).

FourCC 构建 `cv.VideoWriter_fourcc('M','J','P','G')or cv.VideoWriter_fourcc(*'MJPG')`创建一个 MJPG编码器.

下面代码捕捉摄像头的视频流，对视频内容进行纵向翻转并进行保存。

```py
import cv2
cap = cv2.VideoCapture(0) 
print("{}x{}@{}fps".format(cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT),cap.get(cv2.CAP_PROP_FPS)))
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter("./cap.mkv",fourcc,30.0,(1280,720))
# 读取摄像头中的帧
ret, frame = cap.read()

while cap.isOpened():
    # 读取摄像头中的帧
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv2.flip(frame,0)
    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
```

如果出现保存的视频只有几K无法播放的情况，请检查FPS，分辨率数据是否正确，可以通过
获取摄像机参数打印出当前的分辨率情况，修改配置即可.

```py
print("{}x{}@{}fps".format(cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT),cap.get(cv2.CAP_PROP_FPS)))

```

>
> 编码器可能不支持部分功能遇到无法输出可以关闭 isColor 选项，编码器接受BGR色彩空间
> ```py
> frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
> frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
>```

## 绘制

#### 绘制线段

```py
import numpy as np
import cv2 as cv
# 创建空白图形 创建512x512的零矩阵，用于描述图形的颜色
img = np.zeros((512,512,3), np.uint8)
# 在图形对象绘制 从 0,0 -> 511,511宽度为 5 象素的直线
cv.line(img,(0,0),(511,511),(255,0,0),5)

cv.imshow("draw",img)
k = cv.waitKey(0) 
```

> NumPy是用Python进行科学计算的基础软件包，该包被广泛用于科学计算，机器学习，图形处理中。其中```ndarray```是该包用于保存n维数组的结构。在numpy中可以找到很多Octave和MATlab中对应的函数。
> 相关知识查看 [https://www.numpy.org.cn/user/](https://www.numpy.org.cn/user/)
>

#### 绘制矩形

```py
cv.rectangle(img,(384,0),(510,128),(0,255,0),3)
```
只需指定左上角和右下角的座标即可。

#### 绘制圆形

```py
cv.circle(img,(447,63), 63, (0,0,255), -1)
```

圆形指定圆心和半径即可。

#### 绘制椭圆


要绘制椭圆，我们需要传递几个参数。一个参数是中心位置 （x，y）。下一个参数是轴长度（长轴长度、短轴长度）。角度是椭圆逆时针方向的旋转角度。startAngle 和 endAngle 表示从长轴顺时针方向测量的椭圆弧的起点和终点。即给出值 0 和 360 给出完整的椭圆。有关更多详细信息，请查看[cv.ellipse（）](https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga28b2267d35786f5f890ca167236cbc69) 的文档。以下示例在图像中心绘制一个半椭圆。

```py
cv.ellipse(img,(256,256),(100,50),0,0,180,255,-1)
```

#### 绘制多边形

绘制多边形需要先准备好各个顶点。将这些点转换为形状为 ROWSx1x2 的数组，其中 ROWS 是顶点数，其类型应为 int32。在这里，我们绘制一个具有四个黄色顶点的小多边形。

```py
pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts = pts.reshape((-1,1,2))
cv.polylines(img,[pts],True,(0,255,255))
```

原始顶点数据

$
pts=\begin{bmatrix}
(10,5) (20,30) (70,20) (50,10)
\end{bmatrix}
$

对数组进行```reshape```之后

$
pts=\begin{bmatrix}
(10,5) \\\
(20,30) \\\
(70,20) \\\
(50,10)
\end{bmatrix}
$

> 如果第三个参数为 ```False```，您将得到连接所有点的折线，而不是闭合形状。
```cv.polylines（）``` 可用于绘制多条线。只需创建一个要绘制的所有线条的列表并将其传递给函数即可。所有线条将单独绘制。绘制一组线比为每行调用 ```cv.line（）``` 更好、更快的方法。
#### 绘制文本

```py
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv.LINE_AA)
```

参数可以查看文档，[中文无法正确绘制参考这里](https://zhuanlan.zhihu.com/p/615815756)

## 处理鼠标事件

通过函数 ``` cv.setMouseCallback()```可以设置鼠标事件监听。或者鼠标的当前座标。

要打印opencv 包含的事件 使用如下代码:

```py
import cv2 as cv
events = [i for i in dir(cv) if 'EVENT' in i]
print( events )
 ```

 示例：

 ```py
import numpy as np
import cv2 as cv

# 构建空白图形的象素数组
img = np.zeros((512,512,3), np.uint8)


# 定义鼠标事件回调函数
def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONUP:
        # 检查是鼠标左键点击则在当前座标绘制一个圆形
        cv.circle(img,(x,y),100,(255,0,0),-1)


# 窗口命名
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle) # 设置回调函数
while(1):
    cv.imshow('image',img)
    if cv.waitKey(20) & 0xFF == 27: # 按ESC 退出程序
        break
cv.destroyAllWindows()
```

## 添加滑动调节控件

使用```cv.createTrackbar（） ``` 可以给显示窗口添加调节滑动条。下面示例添加了滑动条来调节图形象素的颜色。使用 ```img[:]```来设置矩阵中所有象素的颜色值。

```py
import numpy as np
import cv2 as cv
def nothing(x):
    pass
# 创建象素矩阵
img = np.zeros((300,512,3), np.uint8)
cv.namedWindow('image')
# create trackbars for color change
cv.createTrackbar('R','image',0,255,nothing)
cv.createTrackbar('G','image',0,255,nothing)
cv.createTrackbar('B','image',0,255,nothing)
# 设置开关滑条
switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'image',0,1,nothing)
while(1):
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    # 获取当前的RGB取值
    r = cv.getTrackbarPos('R','image')
    g = cv.getTrackbarPos('G','image')
    b = cv.getTrackbarPos('B','image')
    s = cv.getTrackbarPos(switch,'image') #获取开关取值
    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]
cv.destroyAllWindows()
```

下一篇学习如何对图片进行各种变换和操作。
