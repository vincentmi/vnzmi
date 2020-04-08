---
layout:     post
title:      "Lets Encrypt 申请免费SSL证书"
date:       "2020-04-08 21:48:00"
author:     "Vincent"
header-img:  "img/home-bg-highway.jpg"
catalog: true
tags:
    - SSL
    - Nginx
    - Feign
    - type
---


## 申请SSL 

```shell
docker run -it --rm  -v /Users/vincentmi/cert:/etc/letsencrypt  certbot/certbot  certonly --manual  --preferred-challenges dns
```

#### 路径
SSL保存路径为 ```/Users/vincentmi/cert/live/philo.in```

#### NGINX  配置

```nginx
server {
        listen 443 ssl http2;
        server_name *.dev.philo.in;
        ssl_certificate /Users/vincentmi/cert/live/philo.in/fullchain.pem;
        ssl_certificate_key /Users/vincentmi/cert/live/philo.in/privkey.pem;
}
```

## 更新SSL

```
docker run -it --rm  -v /Users/vincentmi/cert:/etc/letsencrypt  certbot/certbot  renew
```







 

