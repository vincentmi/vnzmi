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


# 第四周 神经网络-模型

### 4.1 模型

##### 4.1.1 基本元素
- 激活函数(activation function) , $g(z)$ , $a_i^{(j)}$第$j$层的第$i$个神经元
- 偏置神经元(bias unit)
- 权重(Weight)
- 输入层 Input Layer
- 结果层 Output Layer
- 隐藏层 Hidden Layer
- $a_i^{(j)}$ 表示在$j$层的第$i$ 个单元
- $\Theta^j$ 权重矩阵控制$j$到$j+1$层各个神经元的权重,如果$j$层有$S_j$个神经元,$j+1$层有$S_{j+1}$个神经元,那么$\Theta^{(j)}$是$S_{j+1} \times S_j +1 $ 矩阵.

##### 4.1.2 计算公式
$
[x_1  x_2 x_3] \rightarrow [a_1^2 a_2^2 a_3^2 .... ] \rightarrow h_\theta(x)
$

计算
$
\begin{aligned} a_1^{(2)} = g(\Theta_{10}^{(1)}x_0 + \Theta_{11}^{(1)}x_1 + \Theta_{12}^{(1)}x_2 + \Theta_{13}^{(1)}x_3) \newline a_2^{(2)} = g(\Theta_{20}^{(1)}x_0 + \Theta_{21}^{(1)}x_1 + \Theta_{22}^{(1)}x_2 + \Theta_{23}^{(1)}x_3) \newline a_3^{(2)} = g(\Theta_{30}^{(1)}x_0 + \Theta_{31}^{(1)}x_1 + \Theta_{32}^{(1)}x_2 + \Theta_{33}^{(1)}x_3) \newline h_\Theta(x) = a_1^{(3)} = g(\Theta_{10}^{(2)}a_0^{(2)} + \Theta_{11}^{(2)}a_1^{(2)} + \Theta_{12}^{(2)}a_2^{(2)} + \Theta_{13}^{(2)}a_3^{(2)}) \newline \end{aligned}
$

向量化:

$
z^{(j+1)} = \Theta^{(j)}a^{(j)}
$

$a^{(j)} = g(z^{(j)})$
$h_{\Theta}(x) =a^{(j+1)} =  g(z^{(j+1)})$

预测结果为向量:

$
y^{(i)} = \begin{bmatrix} 
h_{\Theta}(x)_1 \\\
h_{\Theta}(x)_2 \\\
....
\end{bmatrix}
$

>
>Octive Matlab Tips: 
> ```[m,n] = max(A,[],2)```可以查找矩阵每行的最大值的位置.
>

# 第五周 神经网络-训练

通过正向传播算法和反向传播算法来进行神经网络的训练

### 5.1 代价函数$j$

来看看这个复杂到爆的代价函数.

$L$ 网络的总层数

$s_l$ 低$l$层的单元数量,不包含偏置单元

$K$ 输出单元数量,即要分出的类别的数量

$
J(\Theta) = - \frac{1}{m} \sum_{i=1}^m \sum_{k=1}^K \left[y^{(i)}_k \log ((h_\Theta (x^{(i)}))_k) + (1 - y^{(i)}_k)\log (1 - (h_\Theta(x^{(i)}))_k)\right] + \frac{\lambda}{2m}\sum_{l=1}^{L-1} \sum_{i=1}^{s_l} \sum_{j=1}^{s_{l+1}} ( \Theta_{j,i}^{(l)})^2
$

### 5.2 反向传播算法

#### 5.2.1 初始化

我们的训练集 为 $\{(x^{(1)},y^{(1)})\ ... \ (x^{(m)},y^{(m)}\}$
将权重矩阵$\Delta^l$初始化为0矩阵.

#### 5.2.2 计算正向传播 
>
> 注意计算每一层的时候 都要加上一个 $a_0^{(l)} = 0$.
>

对于训练样本 $t = 0 ... m $
设置 $a^{(1)} = x^{(t)}$  
计算正向传播每层的 $a{(l)}$的值,$l = 2,3,4 \ ...\ L$

需要提供 $J(\Theta)$ 和他的偏导数$\frac{\partial}{\partial\Theta^{(l)}_{i,j}}J(\Theta)$ 来运行梯度下降或其他高级算法

$
z^{(l)} = \Theta^{(l-1)}a^{(l-1)} \\\
a^{(l)} = g(z^{(l)}) \\\
a^{(L)} = h_{\Theta}(x) = g(z^L)
$

#### 5.2.3 使用$y^t$计算$\delta^L = a^L - y^{(t)}$

最后一层.使用样本的正确结果减去通过神经元激活函数算出的值获取我们计算的总偏差.
通过公式我们可以反向推算出上一层的偏差.一次推倒第一层.

#### 5.2.4 计算上一层的偏差值 $\delta^{(L-1)},\delta ^{(L-2)},\ ... \ \delta ^2$

每个权重都是下一层的误差乘激活函数的
偏导数$\delta_j^{(l)}=\frac{\partial}{\partial z_j^{(l)}}cost(t)$,对数据进行一些微调. 

另外不用计算第一层.


$
\delta^{(l-1)} = (\Theta^{(l-1)})^T\delta^{(l)} \cdot g'(z^{(l-1)})
$

将偏导数带入:

$\delta^{(l)} = ((\Theta^{(l)})^T\delta^{(l+1)}) \cdot a^{(l)} \cdot (1-a^{(l)})$

#### 5.2.5 更新权重矩阵

公式:

$\Delta^{(l)}_{i,j} := \Delta^{(l)}_{i,j} + a_j^{l}\delta^{l+1}_{i,j}$

对应的向量公式:

$\Delta^{(l)} := \Delta^{(l)} + \delta^{(i+1)}(a^{(l)})^T$

然后计算新的$\Delta$矩阵

$j\ne0 $时
$
D^{(l)}_{ij} := \frac{1}{m}(\Delta_{i,j}^{(l)} + \lambda\Theta_{i,j}^{(l)})
$

$j=0 $时去掉正规化相关内容

$
D^{(l)}_{ij} := \frac{1}{m}\Delta_{i,j}^{(l)}
$




# 第六周 

     













 



