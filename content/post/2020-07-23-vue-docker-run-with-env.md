---
layout:     post
title:      "VUE项目读取Docker环境变量"
date:       "2020-07-23 23:15:00"
author:     "Vincent"
image:  "img/bulleye_red.svg"
catalog: true
tags:
    - Docker
    - Vue
    - Dockerfile
---

# 使用场景

前端项目通常编译的时候会配置多个环境的参数,根据环境参数编译不同的文件.无法做到在各个环境使用同一个版本的镜像.使用环境变量可以在创建镜像的时候传递基础参数减少编译确保测试的有效性.

## 方案

通过将环境变量传递到DOM,在VUE项目中读取DOM来进行使用环境变量.

#### 读取环境变量

```js
const BASE_URL = document.querySelector('body').getAttribute('baseurl')

const service = axios.create({
  baseURL: BASE_URL || process.env.VUE_APP_API_BASE_URL, // api base_url
  timeout: 6000 // 请求超时时间
})

```

##  构建镜像

#### 修改启动脚本

```$HOSTNAME``` 是镜像自带的环境变量,当前容器的名称

####  ```start.sh```

```sh
#!/bin/sh
sed -i  "s|<body>|<body baseurl=\"$BASE_URL\" hostname=\"$HOSTNAME\" env=\"$ENV\">|"  /usr/share/nginx/html/index.html
nginx -g "daemon off;"
```

#### ```Dockerfile```

```Dockerfile
FROM nginx:1.19-alpine
LABEL author=vincentmi type=vue project=admin-web
COPY ./dist/  /usr/share/nginx/html/
COPY ./start.sh /app/
ENV ENV=prod BASE_URL=/api/v1
EXPOSE 80
ENTRYPOINT ["/app/start.sh"]


```

#### 构建镜像

```build.sh```

```sh
#!/bin/sh
yarn run build && \
docker build -t admin-web ./
```

##  使用

```sh
docker run --name web -d -p 6001:80 -e BASE_URL=http://admin-svc:9100 admin-web
```

BaseURL已经修改了. 在不同的环境设置不同的参数即可.

![preview](/img/in-post/adminweb.png)

 

