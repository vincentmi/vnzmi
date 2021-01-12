---
layout:     post
title:      "Coursera - Machine learning 学习笔记(3)  - 支持向量机"
date:       "2021-01-05 22:08:00"
author:     "Vincent"
header-img:  "img/post-ml.png"
catalog: true
tags:
    - Machine Learning
    - Andrew NG
    - Math
---

课程地址: [ https://www.coursera.org/learn/machine-learning/home/welcome]( https://www.coursera.org/learn/machine-learning/home/welcome)

作业 [Vincent code exercise](https://github.com/vincentmi/machine-learning-exercise)


# 第七周 支持向量机(SVM)

### 模型

$
\min \limits_{\theta} C \sum \limits_{i=1}^{m} \left[ y^{(i)}cost_1(\theta^Tx^{(i)}) + (1-y^{(i)}cost_0(\theta^Tx^{(i)})) \right] + \frac{1}{2}\sum \limits_{i=1}^n\theta_j^2
$

- y = 1 阳性, 则 $\theta^Tx \geq 1 $
-  y = 0 阴性, 则 $\theta^Tx \leq -1 $


### 核函数

- 高斯函数

$
f_1=simmilarity(x,l^{(1)}) = \exp \left( - \frac{\Vert x-l^{(1)}\Vert ^2}{2\sigma^2} \right)
$

如果 $x\approx l^{(1)}$ 这$f_1 \approx 1$ 
如果$x$与$l^{(1)}$很远这 $f_1 \approx 0 $ 
$sigma^2$ 越大则函数曲线越平滑

使用核函数当$\theta^Tf \gt 0 $ 则预测为 $y=1$

### SVM参数

#### $C(=\frac{1}{\lambda})$

- 设置大的$C$值,这相当于小的$\lambda$值,会得到低偏差,高方差,存在过拟合风险
- 设置大的$C$值,这相当于大的$\lambda$值,会得到高偏差,低方差,存在欠拟合风险 

### $\sigma^2$ 
 
 - 取值大,$f_i$的变化更为平滑,高偏差,低方差.过拟合
 - 取值大,$f_i$的变化更为陡峭,低偏差,高方差.欠拟合

### 应用

- 常用的SVM库,使用 ```liblinear```,```libsvm```来计算 $\theta$
- 需要指定参数```C```,选择核函数,使用高斯核函数则需要选择$\sigma^2$
- 不使用核函数则为线性核函数.$\theta^Tx \gt 0 $ 则预测为 $y=1$
- **使用高斯核函数的时候要进行特征缩放**
- 对分类使用库提供的函数或者使用 one-vs-all的方式
- 选择逻辑回归还是SVM的建议(n 特征数量 m 训练集大小)
    -  如果n相对m非常大,n>m,例如,n=10000,而m=10,100或者1000,此时使用逻辑回归
    -  如果n很小
        - m中等,使用SVM和高斯核函数.比如 n在1-1000内,m在10到1W
        - m巨大,创建或者添加更多特征,然后使用逻辑回归或者使用无核的SVM,例如:n在1-1000而m在5W+
- 使用设置好的神经网络通常也行,但是训练会慢很多,而且会有局部最低值问题.

   
