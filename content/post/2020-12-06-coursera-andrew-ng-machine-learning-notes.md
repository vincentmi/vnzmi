---
layout:     post
title:      "Coursera - Machine learning 学习笔记(1) - 线性回归和分类器"
date:       "2020-12-06 23:04:00"
author:     "Vincent"
image:  "img/post-ml.png"
katex:  true
catalog: true
tags:
    - Machine Learning
    - Andrew NG
    - Math
---

课程地址: [ https://www.coursera.org/learn/machine-learning/home/welcome]( https://www.coursera.org/learn/machine-learning/home/welcome)

作业 [Vincent code exercise](https://github.com/vincentmi/machine-learning-exercise)

# 第一周 简介和一元线性回归

### 1.1 机器学习定义(Tom Mitchell)
 **E**  :  经验, 指训练样本  
 **T** : 目标任务,一类机器学习解决的问题  
 **P** : 衡量目标任务T的性能  
 
 > 举例: 关于垃圾邮件的机器学习 
 > T: 将邮件标记为垃圾或者非垃圾 
 > E: 查看当前邮箱中邮件的是否垃圾的标签 
 > P: 标记垃圾邮件的准确率 
 
### 1.2 机器学习分类
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
  
### 1.3 模型描述
$x^{(i)} $ 表示第i 个训练样本,的输入参数
$y^{(i)}$ 表示第i个训练样本的输出参数
$m$  训练集样本数量,样本的行数
$h$ (Hypothesis) 假设函数,预测结果的函数
$j$  代价函数,描述假设函数与训练样本输出值的差异

### 1.4 一元线性回归
**预测函数** 

$h_\theta(x) = \theta_0 + \theta_1x$ 

**代价函数** 

$J(\theta_0,\theta_1)=\frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x^{(i)})-y^{(i)})^2$

**目标**

$min_{\theta0,\theta1}(j)$ 获得最小代价

**参数更新**

$\theta_j=\theta_j - \alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1)$

带入函数求导之后:

$\theta_j=\theta_j - \alpha\frac{1}{m} \sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x^{(i)}$

使用临时变量.不要使用被更新的$\theta$值带入更新公式

## 第二周 多元线性回归

###  2.1 公式
**样本** 

$x=[x_0 \ x_1\ x_2\ x_3\ ... \ x_n]$

$x_0 = 1 $

**参数**

$\theta=\begin{bmatrix}
\theta_0 \\\  
\theta_1 \\\  
\theta_2 \\\
... \\\
\theta_n \\\
\end{bmatrix}
$

$y=\begin{bmatrix}
y_0 \\\  
y_1 \\\  
y_2 \\\
... \\\
y_n \\\
\end{bmatrix}
$


$X=\begin{bmatrix}
1 & x^{(1)}_1 & x^{(1)}_2 & x^{(1)}_3&...x^{(1)}_n \\\
1 & x^{(2)}_1 & x^{(2)}_2 & x^{(2)}_3 &...x^{(2)}_n\\\
...\\\
1 & x^{(m)}_1 & x^{(m)}_2 & x^{(m)}_3 &...x^{(m)}_n\\\
\end{bmatrix}
$

**预测函数** 

$h_\theta(x) = \theta_0x_0 + \theta_1x_1 ... \theta_nx_n=\theta^Tx$ 

转换为向量:

$h_\theta(x) = X\theta$ 

**代价函数** 

$J(\theta)=\frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x^{(i)})-y^{(i)})^2$

**目标**

$min_{\theta0,\theta1 ... \theta_n}(j)$ 获得最小代价

```matlab
J = 1/(2*m) * sum((X*theta - y).^2);
```

**参数更新**

$\theta_j=\theta_j - \alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1 ... \theta_n) = \theta_j - \alpha\frac{\partial}{\partial\theta_j}J(\theta)$

带入函数求导之后:

$\theta_j=\theta_j - \alpha\frac{1}{m} \sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x_j^{(i)}$

转换为向量
$\theta = \theta -  \frac{\alpha}{m} X^T(X\theta - y)$

```matlab
theta = theta - (alpha/m) * (X'*(X*theta -y))
```

### 2.2 特征缩放

- 将特征值限制在近似范围,降低梯度下降的步数.进行特征缩放后轮廓图将会更规则提高梯度下降的效率.
- 将特征值缩放到 $-1 \le x_i \le 1$
- 均值归一 常用公式 $x_i=\frac{x_i-avg(x)}{max(x)-min(x)}$

```matlab
%  均值归一
% x-均值/标准差
function xi= normalization(x)
avg=sum(x)/length(x);
s=max(x) - min(x);
xi=(x - avg)/s;
```

### 2.3 学习速率$\alpha$
- 太小会导致收敛过慢
- 太大J函数不会在每次迭代进行减少.无法收敛
- 尝试 0.001,0.01,0.1,1,0.03等
- 绘制成本迭代图形观察收敛情况 ( x=迭代次数,y=j函数的值)
- 自动收敛测试,成本减少少于 $10^{-3}$则可以认为函数收敛收敛
    - 无法收敛尝试调低学习速率$\alpha$    

### 2.4 多项式回归
多项式回归更好的拟合数据
- 根据数据可以选择合适的多项式回归 $h(\theta)=\theta_0+\theta_1x+\theta_1x^2$
- 根据数据可以选择合适的多项式回归 $h(\theta)=\theta_0+\theta_1x+\theta_1\sqrt{x}$

### 2.5 正规方程
求$J$函数的偏导数,并置为0,即曲线斜率为0的点.即可算出对应的$\theta$值. (补微积分:()

- 优点
    - 一次即可算出最优解
    - 不需要进行特征缩放
    - 不需要选择学习速率
    - 适合线性回归
- 缺点
    - 如果$n$非常大,效率会急剧降低
    - 如果特征类型大于10000建议尝试梯度下降算法
    - 不太适合比较复杂的学习算法
- 矩阵不可逆的情况,
    - 删除一些有线性相关的特征量.
    - 删除重复特征

设计矩阵$X$ 为 $\mathbb{R}^{m\times(n+1)}$
$
X=\begin{bmatrix} 
1 & x_1^{(1)} & x_2^{(1)} & x_3^{(1)} \\\
1 &  x_1^{(2)}& x_2^{(2)} & x_3^{(2)} \\\
1 &  x_1^{(3)}& x_2^{(3)} & x_3^{(3)} \\\
\end{bmatrix} 
$

y为 $\mathbb{R}^{m}$

$\theta=(T^TX)^{-1}X^Ty$

```matlab
pinv(X'*X)*X'*y
%X' X的转置 X'=transpose(X)
```
### 2.6 Octave 使用

这部分比较简单,部分函数

- ```disp```打印变量
- ```pinv``` 求逆矩阵,一定会返回
- ```inv```求逆矩阵,奇异矩阵会报错
- ```transpose``` 转置 ,和 ```A'```效果一样
- ```eye(m)```生成单元矩阵
- ```ones(m,n)```生成均为1 的矩阵或者向量
- ```zeros(m,n)```生成均为0的矩阵或向量
- ```rand(m,n)```生成随机矩阵
- ```A(:,1) ``` 取列向量
- ```A(2,:) ``` 取一行
- ```plot(x,y)``` 绘制平面图
- ```surf(x,y,z)```绘制表面图
- ```contour (x,y,z)```绘制轮廓图
- ```whos```查看当前定义变量
- ```who```查看当前定义的变量名
- ```mean```求平均值
- ```std```求标准差

循环语句 

```matlab
for i=1:10,
    v(i)=2^i;
end;
```


条件判断 

```matlab
>> if v(1) == 1,
>    disp('the value is one');
>  elseif v(1) == 2,
>    disp('the value is two');
>  else
>    disp('the value is not one or two');
>  end;
```
### 2.7 数学知识补充

#### 2.7.1 求导数

导数的计算在曲线某个点的斜率

例如 : 求 $f(x)=x^2$的导数 $f'(x)$

$
f'(x)= \frac{f(x+\delta) - f(x)}{\delta} \\\
f'(x)= \frac{(x+\delta)^2 - x^2}{\delta} \\\
f'(x)= \frac{x^2+\delta^2 + 2x\delta- x^2}{\delta} \\\
f'(x)= \frac{\delta^2 + 2x\delta}{\delta} \\\
f'(x)= 2x \\\
$

#### 2.7.2 导数法则

|  函数 | 导数 | - | 法则 |  函数 |  导数 |  
|---|---|---|---|---|---| 
|  $c$(常数)| $0$ | | 乘以常数| $cf$|$cf'$| 
|  $x$ (直线)| $1 $|| 幂次方法则| $x^n$|$nx^{n-1}$| 
| $ax$| $a$ || 加法法则| $f+g$|$f'+g'$| 
|$x^2$(平方)|	$2x$|| 减法法则| $f-g$|$f'-g'$| 
|$\sqrt{x}$(平方根)|  $\frac{1}{2}x^{\frac{-1}{2}}$||积法则| $fg$|$fg'+f'g$| 
|$\sqrt[n]{x}$ |  $\frac{1}{n}x^{-\frac{1-n}{n}}$||积法则| $fg$|$fg'+f'g$| 
|$e^x$(指数)|	$e^x$|| 商法则| $\frac{f}{g}$|$\frac{f'g-g'f}{g^2}$| 
|$a^x$|	$\ln(a)a^x$||倒数法则| $\frac{1}{f}$| $\frac{-f'}{f^2}$| 
|$\ln(x)$(对数)| $\frac{1}{x}$ | 
|$\log_a(x)$| $\frac{1}{x\ln(a)}$||链式法则（为 "复合函数"）|$f^{\circ}g$|$(f'^{\circ}g)g'$| 
| $\sin(x)(三角)$|$\cos(x)$||链式法则|$f(g(x))$|$ f'(g(x))g'(x)$| 
| $\cos(x)	$| $−\sin(x)$||链式法则|  |$\frac{dy}{dx}=\frac{dy}{du}\frac{du}{dx}$  | 
| $\tan(x)$|$sec{2(x)}$| 
| $\sin^{-1}(x)$|	$\frac{1}{\sqrt{1-x^2}}$| 
| $\cos^{-1}(x)$|	$\frac{-1}{\sqrt{1-x^2}}$| 
| $\tan^{-1}(x)$|	$\frac{1}{\sqrt{1+x^2}}$| 

参考 [导数表](https://baike.baidu.com/item/%E5%AF%BC%E6%95%B0%E8%A1%A8)
#### 2.7.3 矩阵乘法 
$
A=\begin{bmatrix}
a_{1,1} &  a_{1,2} &  a_{1,3}\\\
a_{2,1} &  a_{2,2} &  a_{2,3}\\\
\end{bmatrix}
$  
 
$
B=\begin{bmatrix}
b_{1,1} &  b_{1,2}  \\\
b_{2,1} &  b_{2,2} \\\
b_{3,1} &  b_{3,2} \\\
\end{bmatrix} 
$ 
 
$
C = AB = \begin{bmatrix}
a_{1,1}b_{1,1}+a_{1,2}b_{2,1} + a_{1,3}b_{3,1} & a_{1,1}b_{1,2}+a_{1,2}b_{2,2} + a_{1,3}b_{3,2} \\\
a_{2,1}b_{1,1}+a_{2,2}b_{2,1} + a_{2,3}b_{3,1} & a_{2,1}b_{1,2}+a_{2,2}b_{2,2} + a_{2,3}b_{3,2} \\\
\end{bmatrix} 
$ 
 
- 当矩阵A的列数（column）等于矩阵B的行数（row）时，A与B可以相乘。
- 矩阵C的行数等于矩阵A的行数，C的列数等于B的列数。
- 乘积C的第m行第n列的元素等于矩阵A的第m行的元素与矩阵B的第n列对应元素乘积之和。

> **用A的行去乘B的列.**

#第三周 逻辑回归

### 3.1 二元分类

- h函数$ h(\theta)=\theta^Tx$
- 逻辑函数$g$(sigmoid function) ; $g(z) = \frac{1}{1+e^{-z}}$
- 将$g$应用到预测函数 $h(\theta) = \frac{1}{1+e^{-\theta^Tx}}$
- 决策边界
    - $\theta^Tx > 0 => y=1$ 
    - 非线性决策边界 $h(\theta)=g(\theta_0 + \theta_1x_1 + \theta_2x_2+\theta_3x_1^2+\theta_4x_2^2$) 当$\theta=[-1 \  0 \ 0 \ 1\ 1]$则是个圆.
    - 根据数据集选择合适的假设函数
    - 通过多项式获取更复杂的决策边界
- 代价函数,将y=1和y=0两种情况合并为一个方程$Cost(h(\theta(x),y)) = -y\log( {h_{\theta}(x)} ) - (1-y)\log(1-h_{\theta}(x))$

### 3.2 预测函数

$ h(\theta)=g(\theta^Tx)$
$z=\theta^Tx$
$g(z) = \frac{1}{1+e^{-z}}$
$h(\theta) = \frac{1}{1+e^{-\theta^Tx}}$

### 3.3 代价函数
$j(\theta)=-\frac{1}{m} \sum_{i=1}^m[y^{(i)}\log(h_\theta(x^{(i)}))+(1-y^{(i)})\log(1-h_\theta(x^{(i)}))]$

转换为向量
$h=g(X\theta)$
$j(\theta) =\frac{1}{m}  (-y^T\log(h) - (1-y)^T\log(1-h))$
 
### 3.4 梯度下降公式

$
\theta_j := \theta_j - \frac{\alpha}{m} \sum_{i=1}^m[(h_\theta(x^{(i)}) - y^{(i)})x^{(i)}_j]
$

转换为向量:
$\theta := \theta - \frac{\alpha}{m}X^T(g(X\theta)-\vec y)$

### 3.5 多元分类
- 创建多个分类器并进行拟合

### 3.6 过度拟合
-  underfit (high bais) 高偏差
- overfit 过度拟合
    - 出现的问题
        - J代价函数趋近于0
        - 无法正确对新的数据进行好的预测 
    - 解决
        - 减少特征数量
            - 手动删除
            - 使用算法选择
        - 正规化  
            - 减小$\theta$
            - 当有很多稍微有点用的特性时效果很好

### 3.7 正规化

用来解决过度拟合(overfitting)问题.引入$\lambda$来降低$\theta$的影响.

> 
> **特别注意: 在代价函数和梯度下降函数中,正规化都需要排除$\theta_0$**
> 

#### 3.7.1 正规化线性回归

- 代价函数
    正规化的$j$ 函数后面加入,正规化参数 $\lambda \sum_{j=1}^n\theta_j^2$
    
    $J(\theta)=\frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x^{(i)})-y^{(i)})^2 + \lambda \sum_{j=1}^n\theta_j^2 $

-  梯度下降函数

    **正规化不处理$\theta_0$**
    
    $
    \theta_0=
    \theta_0 - \alpha [\frac{1}{m}\sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x_0^{(i)}
    $
    
    
    **当前$j \gt 0$ 时**
    
    $
    \theta_j=
    \theta_j - \alpha [\frac{1}{m}\sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x_j^{(i)}
    +\frac{ \lambda}{m}\theta_j]  $
    进行
    $
    \theta_j= \theta_j(1-\alpha\frac{\lambda}{m} )- \alpha \frac{1}{m}\sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x_j^{(i)})
    $

- 正规方程解法

$$
\begin{aligned}
L_{n+1\times n+1}=\begin{bmatrix}
0 \\\
\ & 1 \\\
\ & & 1 \\\
...\\\
\ & & & & 1 \\\
\end{bmatrix} \\\
\theta =(X^TX + \lambda\cdot L)^{-1}X^Ty
\end{aligned}
$$

**如果$m<n$** $X^TX$ 不可逆.但是加上$ \lambda\cdot L$ 则是可逆的.大佬已经证明了.

#### 3.7.2 正规化逻辑回归

##### - 代价函数

$j(\theta)=-\frac{1}{m} \sum_{i=1}^m[y^{(i)}\log(h_\theta(x^{(i)}))+(1-y^{(i)})\log(1-h_\theta(x^{(i)}))] + \frac{\lambda}{2m} \sum_{i=1}^n\theta_j^2$

向量化:

$ z =g(X\theta)$


$J(\theta) = \frac{1}{m}( -y^T \log(z) - (1-y)^T \log(1-z) + \frac{\lambda}{2m}(\theta^T \theta)$

**第二个公式$\theta_0=0$**



##### - 梯度下降函数

$\theta= \theta_j(1-\alpha\frac{\lambda}{m} )- \alpha \frac{1}{m}\sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x_j^{(i)})
$

向量化:

$
\theta=\frac{1}{m} X^T(z-y) + \frac{\lambda}{m} \cdot \theta
$

第二个公式$θ_0$=0,用于移除$\theta_0$的影响

#### 3.7.3 使用内建优化函数```fminunc```

创建用于优化的函数返回,代价值和$\theta$的微分值,```function [J, grad] = costFunction(theta, X, y)```. 内部会选择算法
算出最优化的$\theta$值

$
\theta =\frac{1}{m}\sum_{i=1}^m(h_{\theta}(x^{(i)}) - y^{(i)}) \cdot x_j^{(i)}
$

```matlab

%代价函数
J=(1/m) * ( -y' * log(z) - (1-y)' * log(1-z) ) + (lambda/(2*m)) * (theta_0' * theta_0);

%梯度函数
grad = 1/m * X'*(z - y) +  (lambda / m) .* theta_0;

%  Set options for fminunc
options = optimset('GradObj', 'on', 'MaxIter', 400);
% Run fminunc to obtain the optimal theta
% This function will return theta and the cost [theta, cost] = ...
fminunc(@(t)(costFunction(t, X, y)), initial theta, options);
```

#### 3.7.4 选择合适的$\lambda$

- 如果$\lambda$设置过大无法拟合数据,因为对于$\theta$的调整对整体的影响力有限.
- 如果$\lambda$设置过小则会过拟合,没有起作用
- 可以通过对训练集进行预测查看准确率来选择合适的值













 



