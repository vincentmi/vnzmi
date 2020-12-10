---
layout:     post
title:      "Coursera - Machine learning 学习笔记(2) - 神经网络"
date:       "2020-12-10 23:04:00"
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


# 第四周 神经网络描述

#### 4.1 模型
$$
[x_1  x_2 x_3] \rightarrow [a_1^2 a_2^2 a_3^2] \rightarrow h_\theta(x)
$$

计算
$$
\begin{align*} a_1^{(2)} = g(\Theta_{10}^{(1)}x_0 + \Theta_{11}^{(1)}x_1 + \Theta_{12}^{(1)}x_2 + \Theta_{13}^{(1)}x_3) \newline a_2^{(2)} = g(\Theta_{20}^{(1)}x_0 + \Theta_{21}^{(1)}x_1 + \Theta_{22}^{(1)}x_2 + \Theta_{23}^{(1)}x_3) \newline a_3^{(2)} = g(\Theta_{30}^{(1)}x_0 + \Theta_{31}^{(1)}x_1 + \Theta_{32}^{(1)}x_2 + \Theta_{33}^{(1)}x_3) \newline h_\Theta(x) = a_1^{(3)} = g(\Theta_{10}^{(2)}a_0^{(2)} + \Theta_{11}^{(2)}a_1^{(2)} + \Theta_{12}^{(2)}a_2^{(2)} + \Theta_{13}^{(2)}a_3^{(2)}) \newline \end{align*}
$$

- activation function , $g(z)$
- 输入层 Input Layer
- 结果层 Output Layer
- 隐藏层 Hidden Layer
- $a_i^{(j)}$ 表示在$j$层的第$i$ 个单元
- $\Theta^j$ 权重矩阵,如果$j$层有$S_j$个神经元,$j+1$层有$S_{j+1}$个神经元,那么$\Theta^{(j)}$是$S_{j+1} \times S_j +1 $ 矩阵.

# 第五周 学习神经网络

# 第六周 

     













 



