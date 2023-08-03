---
layout:     post
title:      "使用tile-server搭建离线地图服务"
#titleColor: "#000000"
date:       "2023-07-08 09:44:00"
author:     "Vincent"
image:  "/img/home-bg-map.jpg"
catalog: true
tags:
    - tileserver
    - webgis
    - map
---

# 获取地图数据

## 从Maptiler下载

下载地址 [https://data.maptiler.com/downloads/planet/](https://data.maptiler.com/downloads/planet/)

![下载](/img/in-post/maptiler_download.png)

直接下载你需要的地图数据，其中各类数据包含数据如下：

- OpenStreetMap ： 包含建筑，道路，自然景观，行政边界
- Contour lines ： 矢量等高线
- hillshading ： 山体阴影
- Satellite ： 卫星地图

另外一些数据  Satellite 2021, Terrain RGB,
Terrain 3D - Cesium quantized mesh, MapTiler Planet Lite, or Landcover 只能下载星球层级的数据.


## 设置地图风格


