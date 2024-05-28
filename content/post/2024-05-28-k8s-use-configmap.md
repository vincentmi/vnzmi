---
layout:     post
title:      "在k8s中使用configmap保存配置文件"
date:       "2024-05-28 15:13:00"
author:     "Vincent"
image:  "/img/post-bg-engine.jpg"
catalog: true
tags:
    - k8s
    - yaml
---

## 创建configmap

```yaml
# wechatcert.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: wechatcert
  namespace: default
data:
  cert_1_cert: |+
    -----BEGIN CERTIFICATE-----
    MIID8zCCAtugAwIBAgIUcyzP2XJ7nKl3+iDPTWJIzmco9gMwDQYJKoZIhvcNAQEL
    .....
    ngtlczmDIg==
    -----END CERTIFICATE-----
  cert_1_key: |+
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDATL6EMPG73/jh
    ....
    Jh6zPUlTJ+7QFlbt5DdnhKox
    -----END PRIVATE KEY-----
  cert_15_1602411903_cert: |+
    -----BEGIN CERTIFICATE-----
    MIIEMTCCAxmgAwIBAgIUNQhkhxGUolX3wHCUi4hNWVQmuF4wDQYJKoZIhvcNAQEL
    BQAwXjELMAkGA1UEBhMCQ04xEzARBgNVBAoTClRlbnBheS5jb20xHTAbBgNVBAsT
    FFR....
    eZzKlZJBt5JC/5mcdoBlWOgBJnCE
    -----END CERTIFICATE-----
  cert_15_1602411903_key: |+
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC+yTjTdt8ijeGr
    -----END PRIVATE KEY-----
```
#### 创建configMap
```sh
kubectl apply -f wechatcert.yaml
```

## 挂载到POD 

```yaml
# nginx1.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx1
  labels:
    app: nginx1
spec:
  containers:
  - name: nginx1
    image: nginx:alpine
    ports:
    - containerPort: 80
    volumeMounts:
      - name: wechatcert
        mountPath: "/data/cert"
        readOnly: true
  volumes:
  - name: wechatcert
    configMap:
      name: wechatcert
      items:
        - key: cert_1_cert
          path: 1/apiclient_cert.pem
        - key: cert_1_key
          path: 1/apiclient_key.pem
        - key: cert_15_1602411903_cert
          path: 15/1602411903/apiclient_cert.pem
        - key: cert_15_1602411903_key
          path: 15/1602411903/apiclient_key.pem
```

#### 应用到POD

```sh
kubectl apply -f nginx1.yaml
```







