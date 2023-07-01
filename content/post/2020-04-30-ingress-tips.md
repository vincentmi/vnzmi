---
layout:     post
title:      "Ingress添加权限验证"
date:       "2020-04-30 14:20:00"
author:     "Vincent"
image:  "img/home-bg-highway.jpg"
catalog: true
tags:
    - K8S
    - Nginx
    - Feign
    - type
---


## 生成密码文件

```sh
~  htpasswd -c httpauth admin
New password:
Re-type new password:
Adding password for user admin
```
#### 添加密文

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: httpauth
data:
  auth: admin:$apr1$RjgQNPDx$e9htPYO4fELnCxOb07GIK0
```

#### 配置
对你需要增加权限验证的INgress设置注释

```yaml
    nginx.ingress.kubernetes.io/auth-realm: '"Authentication Required - admin"'
    nginx.ingress.kubernetes.io/auth-secret: httpauth
    nginx.ingress.kubernetes.io/auth-type: basic
```


#### INgress YAML如下

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    field.cattle.io/creatorId: user-ng7cm
    field.cattle.io/ingressState: '{"Y29uc3VsL2xvY2FsL2NvbnN1bC5sb2NhbC5waGlsby5pbi8vaHR0cA==":""}'
    field.cattle.io/publicEndpoints: '[{"addresses":["10.10.0.31"],"port":80,"protocol":"HTTP","serviceName":"local:consul","ingressName":"local:consul","hostname":"consul.local.philo.in","allNodes":true}]'
    nginx.ingress.kubernetes.io/auth-realm: '"Authentication Required - admin"'
    nginx.ingress.kubernetes.io/auth-secret: httpauth
    nginx.ingress.kubernetes.io/auth-type: basic
  creationTimestamp: "2020-04-23T05:52:00Z"
  generation: 2
  labels:
    cattle.io/creator: norman
  name: consul
  namespace: local
  resourceVersion: "1102762"
  selfLink: /apis/extensions/v1beta1/namespaces/local/ingresses/consul
  uid: a55e4299-2552-401b-91a8-a595fd3ff7e3
spec:
  rules:
  - host: consul.local.philo.in
    http:
      paths:
      - backend:
          serviceName: consul
          servicePort: http
status:
  loadBalancer:
    ingress:
    - ip: 10.10.0.31
    - ip: 10.10.0.32
    - ip: 10.10.0.41
    - ip: 10.10.0.42

```








 

