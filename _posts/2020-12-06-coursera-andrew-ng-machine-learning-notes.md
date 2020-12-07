---
layout:     post
title:      "Coursera - Machine learning 学习笔记"
date:       "2020-12-06 23:04:00"
author:     "Vincent"
header-img:  "img/post-ml.png"
catalog: true
tags:
    - Machine Learning
    - Andrew NG
    - Math
---

课程地址: [ https://www.coursera.org/learn/machine-learning/home/welcome]( https://www.coursera.org/learn/machine-learning/home/welcome)

# 第一周 简介

### 1. 机器学习定义(Tom Mitchell)
 **E**  :  经验, 指训练样本
 **T** : 目标任务,一类机器学习解决的问题.
 **P** : 衡量目标任务T的性能
 
 > 举例: 关于垃圾邮件的机器学习
 > T: 将邮件标记为垃圾或者非垃圾
 > E: 查看当前邮箱中邮件的是否垃圾的标签
 > P: 标记垃圾邮件的准确率
 
### 2. 机器学习分类
- 监督学习 (Supervised Learning)
    - 回归问题 regression , 例如: 根据房屋面积和价格的数据样本预测给定面积的房价的问题,price =fx(area) 房价是关于面积的函数.
        - 根据给出的正确值 预测连续的输出值 
    - 分类问题 classification, 例如: 根据肿瘤大小预测肿瘤是良性还是恶性
        - 根据输入的值,预测所属分类 
- 非监督学习
    - 没有明确目标的训练方式,例如:对新闻进行分类 
        - 举例:降噪函数 ``` [W,s,v] = svd((repmat(sum(x.*x,1),size(x,1),1).*x)*x') ``` (懵逼)
- 其他
    - 强化学习 Reinforcement Learning  根据反馈进行调整
    - Recommender system 
  
### 3 模型描述
$x^{(i)} $ 表示第i 个训练样本,的输入参数
$y^{(i)}$ 表示第i个训练样本的输出参数
$m$  训练集样本数量,样本的行数
$h$ (Hypothesis) 假设函数,预测结果的函数
$j$  代价函数,描述假设函数与训练样本输出值的差异

### 4 一元线性回归
**预测函数** 

$h_\theta(x) = \theta_0 + \theta_1x$ 

**代价函数** 

$J(\theta_0,\theta_1)=\frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x^{(i)}-y^{(i)}))^2$

**目标**

$min_{\theta0,\theta1}(j)$ 获得最小代价

**参数更新**

$\theta_j=\theta_j - \alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1)$

带入函数求导之后:

$\theta_j=\theta_j - \alpha\frac{1}{m} \sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x^{(i)}$

使用临时变量.不要使用被更新的$\theta$值带入更新公式

## 第二周 多元线性回归
**样本** 

$x=[x_1\ x_2\ x_3\ ... \ x_n]$

**参数**

$\theta=[\theta_0 \  \theta_1 \  \theta_2 ... \theta_n]$

**预测函数** 

$h_\theta(x) = \theta_0 + \theta_1x_1 ... \theta_nx_n$ 

**代价函数** 

$J(\theta_0,\theta_1)=\frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x^{(i)}-y^{(i)}))^2$

**目标**

$min_{\theta0,\theta1}(j)$ 获得最小代价

**参数更新**

$\theta_j=\theta_j - \alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1)$

带入函数求导之后:

$\theta_j=\theta_j - \alpha\frac{1}{m} \sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x^{(i)}$

使用临时变量.不要使用被更新的$\theta$值带入更新公式




$
X=\begin{bmatrix} 
x_1^1 & x_1^2 & x_1^3 \\\
x_1^2& x_2^2 & x_2^3 \\\
x_1^3& x_3^2 & x_3^3 \\\
\end{bmatrix} 
$
 



