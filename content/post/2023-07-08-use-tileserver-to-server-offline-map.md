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

# 1 获取地图数据

## 1.1 从Maptiler下载

下载地址 [https://data.maptiler.com/downloads/planet/](https://data.maptiler.com/downloads/planet/)

![下载](/img/in-post/maptiler_download.png)

直接下载你需要的地图数据，其中各类数据包含数据如下：

- OpenStreetMap ： 包含建筑，道路，自然景观，行政边界
- Contour lines ： 矢量等高线
- hillshading ： 山体阴影
- Satellite ： 卫星地图

另外一些数据  Satellite 2021, Terrain RGB,
Terrain 3D - Cesium quantized mesh, MapTiler Planet Lite, or Landcover 只能下载星球层级的数据.

## 1.2 下载PBF文件进行转换

PBF文件可以从 [https://download.geofabrik.de/asia/china/sichuan.html](https://download.geofabrik.de/asia/china/sichuan.html) 下载。

#### 1.2.1 使用tilemaker 转换pbf文件

> tilemaker会丢失很多属性但是转换比较快。


[tilemaker 官网](https://tilemaker.org/) ,下载地址 [https://github.com/systemed/tilemaker/releases](https://github.com/systemed/tilemaker/releases)

下载后是一个执行文件,使用默认的配置文件和lua脚本进行转换。

```sh
./bin/tilemaker --input ./pbf/sichuan-latest.osm.pbf --output ./mbtiles/sichuan.mbtiles --config ./bin/tilemaker_conf/config-openmaptiles.json --process ./bin/tilemaker_conf/process-openmaptiles.lua
```

执行完成后可用的文件就保存到了 ```./mbtiles/sichuan.mbtiles```

#### 1.2.2 使用openmaptiles转换pbf文件

[openmaptiles](https://openmaptiles.org/)




## 1.3 从天地图下载数据



# 2.启动tileserver-gl服务器


#### 2.1 启动docker镜像

使用docker启动服务

```sh
docker run --rm -it --name tileserver \
--platform linux/amd64 \
-v $(pwd):/data \
 -p 8080:8080 \
 tileserver-gl:z2 \
--mbtiles /data/mbtiles/sichuan.mbtiles
```

> 如果本地无法下载镜像，可以在服务器中使用下面的命令下载镜像
> ```docker pull maptiler/tileserver-gl:latest```
> 导出镜像 ```docker save maptiler/tileserver-gl:latest > tileserver-gl.tar```
> 本地导入 ```docker load < tileserver-gl.tar```

启动后可以访问 ```http://localhost:8080/```看到部署的地图服务,对地图进行浏览

![tileserver-gl](/img/in-post/2024-tileserver-gl.png)

![tileserver-gl](/img/in-post/2024-tileserver-gl-2.png)



# 3.调用瓦片服务

使用 [leafletjs](https://leafletjs.com/) 调用展示地图。

```html

<!DOCTYPE html>
<html lang="zh-CN">
<head>
<title>Sichuan Map</title>
<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <!-- Make sure you put this AFTER Leaflet's CSS -->
     <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="crossorigin=""></script>
</head>

 <body>

    <div id="map"></div>
    <style>#map { height: 400px; }</style>
    <script>
        var map = L.map('map').setView([30.189,102.932], 14);
        L.tileLayer('http://localhost:8080/styles/basic-preview/512/{z}/{x}/{y}.png', {
            maxZoom: 22
        }).addTo(map);
    </script>
 </body>
 </html>
```