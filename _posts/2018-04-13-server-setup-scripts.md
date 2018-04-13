---
layout:     post
title:      "Docker+Consul+Ngxin配置脚本"
date:       2018-04-13 11:20:00
author:     "Vincent"
header-img:  "img/post-bg-engine.jpg"
catalog: true
tags:
    - Consul
    - Docker
    - ops
    - nginx
    
---

## Docker 


```
#!/bin/sh
sudo apt-get remove docker docker-engine docker.io
sudo apt-get update 
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get -y install docker-ce 

apt-cache madison docker-ce
sudo apt-get install docker-ce=<VERSION>
    
```

## NGINX 

```
server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;

        root /usr/share/nginx/html;
        index index.html index.htm;

        # Make site accessible from http://localhost/
        server_name localhost;

        location / {
					proxy_pass  http://127.0.0.1:8009;
			        proxy_redirect     off;
			        proxy_set_header   Host             $host;
			        proxy_set_header   X-Real-IP        $remote_addr;
			        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
			        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
			        proxy_max_temp_file_size 0;
			        proxy_connect_timeout      90;
			        proxy_send_timeout         90;
			        proxy_read_timeout         90;
			        proxy_buffer_size          4k;
			        proxy_buffers              4 32k;
			        proxy_busy_buffers_size    64k;
			        proxy_temp_file_write_size 64k;
        }
        }
        
        
```

## 容器

```sh

#mysql

docker run --name mysql-primary -v /alidata/mysqldb:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=uiQH6zWzXQ  -d mysql:5.7

#registry

sudo docker run   -d   -e ENV_DOCKER_REGISTRY_HOST=registry   -e ENV_DOCKER_REGISTRY_PORT=5000   -p 9080:80   --name drf

# Register
docker run -d -p 5000:5000 --restart always  \
-v /alidata/registry:/var/lib/registry \
 --name registry -e "REGISTRY_AUTH=htpasswd" \
 -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
 -e "REGISTRY_AUTH_HTPASSWD_PATH=/var/lib/registry/auth/passwd" registry:2

#[prtainera
docker run -d -p 8002:9000 \
    --name=portainer \
    -e "SERVICE_NAME=port.vnzmi.com" \
    -e "SERVICE_TAGS=lb-nginx" \
    -v  /var/run/docker.sock:/var/run/docker.sock \
    -v /var/portainer_data:/data \
     portainer/portainer

#registrator
docker run -d \
    --name=registrator \
    --net=host \
    --volume=/var/run/docker.sock:/tmp/docker.sock \
    gliderlabs/registrator:latest \
    -internal=1 -cleanup=1 -ttl=300 -ttl-refresh=60 \
      consul://127.0.0.1:8500

# lb-nginx
docker run -d --name=lb-nginx \
  -e "CONSUL_ADDR=172.18.0.3:8500" \
  -p 8009:80 \
 lb-nginx:latest

# SERVICE
docker run  --name ssq -d -P  \n
  -v /alidata/www/ssq:/var/www \n
  -v /alidata/www/ssq/log:/var/log/nginx \
  -v /alidata/www/ssq/backup:/var/log/backup \
  -e "SERVICE_NAME=ssq_vnzmi_com" \
  -e "SERVICE_TAGS=lb-nginx" \
  -e "SERVICE_CHECK_TCP=true" \
  -e "SERVICE_CHECK_INTERVAL=15s" \
  -e "SERVICE_CHECK_TIMEOUT=3s" \
  vincentmi/php5


```
    









