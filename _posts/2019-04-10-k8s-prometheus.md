---
layout:     post
title:      "安装Kubernetes集群(3) Prometheus"
date:       2019-04-10 15:31:00
author:     "Vincent"
header-img:  "img/post-bg-engine.jpg"
catalog: true
tags:
    - kubernetes
    - k8s
    - Prometheus
---

Prometheus 可以原生监控K8s ,节点和它本身.[Prometheus Operator](https://coreos.com/operators/prometheus/docs/latest/) 可以简化Prometheus在K8S 中的安装.使用[Prometheus adapter](https://github.com/directxman12/k8s-prometheus-adapter) 可以使用自定义指标参数. Prometheus 也提供内建的控制台和查询语言来查询数据和可视化.Prometheus也可以做为[Grafana](https://prometheus.io/docs/visualization/grafana/)的数据源.


# 安装Prometheus Operator

相关镜像

quay.io/coreos/prometheus-config-reloader:v0.0.2

quay.io/prometheus/prometheus:v2.2.0-rc.0

## 创建namespace

```sh
kubelet create namespace kube-util
```

## 安装Prometheus Operator

```yaml
#创建角色绑定
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: prometheus-operator
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prometheus-operator
subjects:
- kind: ServiceAccount
  name: prometheus-operator
  namespace: kube-util
---
## 创建集群角色
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: prometheus-operator
rules:
- apiGroups:
  - extensions
  resources:
  - thirdpartyresources
  verbs:
  - "*"
- apiGroups:
  - apiextensions.k8s.io
  resources:
  - customresourcedefinitions
  verbs:
  - "*"
- apiGroups:
  - monitoring.coreos.com
  resources:
  - alertmanagers
  - prometheuses
  - prometheuses/finalizers
  - servicemonitors
  verbs:
  - "*"
- apiGroups:
  - apps
  resources:
  - statefulsets
  verbs: ["*"]
- apiGroups: [""]
  resources:
  - configmaps
  - secrets
  verbs: ["*"]
- apiGroups: [""]
  resources:
  - pods
  verbs: ["list", "delete"]
- apiGroups: [""]
  resources:
  - services
  - endpoints
  verbs: ["get", "create", "update"]
- apiGroups: [""]
  resources:
  - nodes
  verbs: ["list", "watch"]
- apiGroups: [""]
  resources:
  - namespaces
  verbs: ["list"]
---
##创建账户
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prometheus-operator
---
## 创建部署脚本
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    k8s-app: prometheus-operator
  name: prometheus-operator
spec:
  replicas: 1
  template:
    metadata:
      labels:
        k8s-app: prometheus-operator
    spec:
      containers:
      - args:
        - --kubelet-service=kube-system/kubelet
        - --config-reloader-image=quay.io/coreos/configmap-reload:v0.0.1
        image: quay.io/coreos/prometheus-operator:v0.17.0
        name: prometheus-operator
        ports:
        - containerPort: 8080
          name: http
        resources:
          limits:
            cpu: 200m
            memory: 100Mi
          requests:
            cpu: 100m
            memory: 50Mi
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
      serviceAccountName: prometheus-operator
```

>
>注意namespace 账户所在的namespace要与安装的空间一致.


# 为应用添加Prometheus支持

Prometheus资源包含一个```serviceMonitorSelector```字段,定义了```ServiceMonitor```应用到哪些服务中.


### 先创建一个部署脚本,启动3个实例

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: example-app
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: example-app
    spec:
      containers:
      - name: example-app
        image: fabxc/instrumented_app
        ports:
        - name: web
          containerPort: 8080
```

### 定义服务


```yaml
kind: Service
apiVersion: v1
metadata:
  name: example-app
  labels:
    app: example-app
spec:
  selector:
    app: example-app
  ports:
  - name: web
    port: 8080
```

### 创建ServiceMonitor对象
ServiceMonitor 使用一个标签选择器来选择要监控的服务.

```yaml
piVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: example-app
  labels:
    team: frontend
spec:
  selector:
    matchLabels:
      app: example-app
  endpoints:
  - port: web
```

### 创建Prometheus对象

```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
spec:
  serviceMonitorSelector:
    matchLabels:
      team: frontend
  resources:
    requests:
      memory: 400Mi
```

### 将Prometheus端口暴露出来

```yaml
apiVersion: v1
kind: Service
metadata:
  name: prometheus
spec:
  type: NodePort
  ports:
  - name: web
    nodePort: 30900
    port: 9090
    protocol: TCP
    targetPort: web
  selector:
    prometheus: prometheus
```

也可以用ingress

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: mon-ingress
spec:
  rules:
  - host: mon.local.vnzmi.com
    http:
      paths:
      - backend:
          serviceName: prometheus
          servicePort: 9090
```