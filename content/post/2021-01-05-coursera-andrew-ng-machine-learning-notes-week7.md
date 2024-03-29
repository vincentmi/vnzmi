---
layout:     post
title:      "Coursera - Machine learning 学习笔记(3)  - 支持向量机异常检测和推荐系统"
date:       "2021-01-05 22:08:00"
author:     "Vincent"
image:  "img/post-ml.png"
katex : true
catalog: true
tags:
    - Machine Learning
    - Andrew NG
    - Math
---

课程地址: [ https://www.coursera.org/learn/machine-learning/home/welcome]( https://www.coursera.org/learn/machine-learning/home/welcome)

作业 [Vincent code exercise](https://github.com/vincentmi/machine-learning-exercise)


# 第七周 支持向量机(SVM)

### 7.1 模型

$
\min \limits_{\theta} C \sum \limits_{i=1}^{m} \left[ y^{(i)}cost_1(\theta^Tx^{(i)}) + (1-y^{(i)}cost_0(\theta^Tx^{(i)})) \right] + \frac{1}{2}\sum \limits_{i=1}^n\theta_j^2
$

- y = 1 阳性, 则 $\theta^Tx \geq 1 $
-  y = 0 阴性, 则 $\theta^Tx \leq -1 $


### 7.2 核函数

- 高斯函数

$
f_1=simmilarity(x,l^{(1)}) = \exp \left( - \frac{\Vert x-l^{(1)}\Vert ^2}{2\sigma^2} \right)
$

如果 $x\approx l^{(1)}$ 这$f_1 \approx 1$ 
如果$x$与$l^{(1)}$很远这 $f_1 \approx 0 $ 
$sigma^2$ 越大则函数曲线越平滑

使用核函数当$\theta^Tf \gt 0 $ 则预测为 $y=1$

### 7.3 SVM参数

#### $C(=\frac{1}{\lambda})$

- 设置大的$C$值,这相当于小的$\lambda$值,会得到低偏差,高方差,存在过拟合风险
- 设置小的$C$值,这相当于大的$\lambda$值,会得到高偏差,低方差,存在欠拟合风险 

### $\sigma^2$ 
 
 - 取值大,$f_i$的变化更为平滑,高偏差,低方差.欠拟合
 - 取值大,$f_i$的变化更为陡峭,低偏差,高方差.过拟合

### 7.4 应用

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

   
# 第八周 无监督学习

### 8.1 聚类算法
- 不用进行数据标记
- 应用实例
    - 客户分类
    - 社交关系分类
    - 计算机集群分类

### 8.2 K均值算法(K Mean)

- 随机选择质心点,
- 循环训练集,计算与质心点的距离对训练集标记所属质心
- 循环质心,计算属于该质心点的的训练集计算新的均值质心点.移动质心
- 继续以上步骤直到质心点收敛不再变化.
- 如果无法找到质心点新的合适的位置.则可以删除该质心点

#### 8.2.1 模型

$c^{(i)}$ 表示 样本$x^{(i)}$当前被分配的聚类
$\mu_k$ 第$k$个聚类的中心点
$\mu_c(i)$ ,表示 样本$x^{(i)}$当前被分配的聚类的中心点


$J(c^{(1)} , ... ,c^{(m)},\mu^{(1)} , ... , \mu^{(k)} ) = \frac{1}{m} \sum_\limits{i=1}^m\Vert x^{(i)} - \mu_c(i)\Vert^2$

$\min_\limits{c^{(1)} , ... ,c^{(m)},\mu^{(1)} , ... , \mu^{(k)} }{J(c^{(1)} , ... ,c^{(m)},\mu^{(1)} , ... , \mu^{(k)} )}$

- 选择初始化聚类中心点: 如果 k < m 随机选择训练样本.
- 选择的初始化中心点会影响聚类最终的结果,通过多次尝试来获取到最小代价函数的聚类
- 如果k在2-10之间通过多次初始化可以得到较好的聚类,当k较大时多次随机对结果影响较小

#### 8.2.2 设置聚类数量

- 肘部原则,使用聚类数量和代价函数值来画图,如果能得到类似手臂的图选择手肘部位.但是能有肘部曲线的状况不太多.
- 更多聚类的数量是基于实际的应用需要来设置.


### 8.3 PCA 算法(主成分分析) 

- 通过降维进行数据可视化
- PCA通过寻找低纬的投影平面来进行降维.

#### 8.3.1 数据预处理

对特征值进行特征缩放和均值归一

$\mu_j = \frac{1}{m} \sum \limits_{i=1}^mx_j^{(i)}$

对每个 $x_j^{(i)}$执行 $x_j - \mu_j$

如果数据有不同数量级还需要除以标准差 $\frac{x_j - \mu_j}{S_j}$

#### 8.3.2 计算协方差矩阵

将数据从 $n$维 降低为 $k$维,计算协方差矩阵

$Sigma = \frac{1}{m} \sum \limits_{i=1}^n(x^{(i)})(x^{(i)})^T$

向量化:
$X= \begin{bmatrix} 
--- (x^{(1)})^T --- \\\
--- (x^{(2)})^T --- \\\
.... \\\
--- (x^{(m)})^T --- \\\
\end{bmatrix}
$

```matlab
Sigma = (1/m) *X'*X;
```

计算特征向量,使用 SVD (奇异值分解)函数

$[U,S,V] = svd(Sigma);$

$U =\left[ \mu^{(1)}  \mu^{(2)} ... \mu^{(n)} \right]\in \mathbb{R}^{nxn}$

取前$k$个向量

```matlab
[U ,S ,V] = svd(Sigma);
U_reduce = U(:,1:k);
z=U_reduce'* x;
```

#### 8.3.3 从压缩数据恢复

$z = U_{reduce}^T x$

恢复数据:

$X_{approx}^{i} = U_{reduce} z^{i}$


#### 8.3.4 选择$k$值

投影均方差(Average,squared,projection,error)  $\frac{1}{m}\sum\limits_{i=1}^m\Vert x^{i} - x_{approx}^{i} \Vert^2$
平均长度 $\frac{1}{m} \sum \limits_{i=1}^{m} \Vert x^{(i)}\Vert ^ 2 $

通常选择能使

$\frac{\frac{1}{m}\sum\limits_{i=1}^m\Vert x^{i} - x_{approx}^{i} \Vert^2}{\frac{1}{m} \sum \limits_{i=1}^{m} \Vert x^{(i)}\Vert ^ 2 }$

更小的 $k$ . 一般 小于 等于 0.01是一个很好的值.也就是99%的数据差异性被保留了.

计算方式:
使用```svd```函数的S矩阵.

$\frac{ \sum \limits_{i=1}^kS_{ii}} {  \sum \limits_{i=1}^nS_{ii} } \geq  0.99 $

#### 8.3.5 使用PCA的建议

- 提高机器学习的执行速度
    - 将输入数据提取出来使用PCA算法计算出 $z^{(1)} z^{(2)} ... z^{(m)}  $ 构建新的训练集
    - 注意映射的矩阵由训练集定义,可以直接使用到CV集和测试集中.
- 数据压缩
    - 减少数据对内存或者磁盘的需求
    - 提高算法速度
- 数据可视化
    - 直接选择$k=2$或者$k=3$因为我们只能对2维和3维进行绘图.
- 错误的应用方式
    - 使用PCA来减少特征值的数量来避免过拟合.不建议这样使用而应该适应正规化的方式来解决这个问题.
    - 不要一开始就使用PCA算法.先使用原始数据进行学习.   


# 第九周  异常检测

### 9.1 异常检测的应用

- 欺诈检测
    - $x^{(i)}$ 是用户的活动特征值
    - 建立模型,从数据计算$p(x)$
    - 当$p(x) < \epsilon $ 则标记为异常用户 
- 制造业产品质量异常检测
- 监控数据中心异常
    - $x^{(i)}$ 获取机器的特征值,比如 $x_1$ 内存用量 $x_2$ 每分钟磁盘访问量 $x_3$ CPU负载量 ,$x_4$ cpu负载/网络流量

### 9.2 高斯分布

$x$是实数,$x$在均值 $\mu$ 和方差 $\sigma^2$下的高斯分布.

$\mu$ 是密度最高的点
$\sigma^2$ 越大则高斯曲线越平滑.密度下降的幅度越慢.

#### 9.2.1 算法

- 选择你认为对异常有指示性的特征量
- 拟合参数 $\mu_1 \mu_2 , ... , \mu_n,\sigma_1^2 , \sigma_2^2,...,\sigma_n^2$
    
    $\mu_j  = \frac{1}{m} \sum\limits_{i=1}^mx_j^{(i)}$
    
    $\sigma^2  = \frac{1}{m} \sum\limits_{i=1}^m (x_j^{(i)} - \mu_j)^2$
    
- 对于新的数据 $x$,计算 $p(x)$

$ p(x) = \prod\limits_{j=1}^n p(x_j;\mu_j,\sigma_j^2) = \prod\limits_{j=1}^n  \frac{1}{\sqrt{2\pi}\sigma_j} \exp( - \frac{(x_j-\mu_j)^2}{2\sigma^2_j})$

>
> $\prod\limits_{(i=1)}^nx_i = x_1 \times x_2 \times x_3 .... \times x_n$ 
>

如果$p(x) < \epsilon $则标记为异常

可以设置 $\epsilon = 0.02 $ 当小于它时则为异常. 

- 训练时建议对训练数据这样划分($y=0$正常$y=1$异常)
    - 将部分正常的训练数据划分到训练集
    - 将部分正常和一半的异常分别划分到测试集和CV集
- 算法评估
    -  在训练集$ \{ x^{(1)},...,x^{(m)} \}$上你和参数
    -  在CV和Test集中计算$p(x)$ 预测 当 $p(x) < \epsilon  \to y = 1 $为异常,$p(x) > \epsilon  \to y = 0$为正常
    -  评估的参数与逻辑回归类似
        - 对预测准确和不准确的数量进行评估
        - 计算准确率和召回率
        - 计算F值
    - 也可以使用CV集来选择$\epsilon$值.

    #### 9.2.2 与监督学习的对比
    
    - 使用异常检测的情况
        - 阳性数据量```y=1```非常少的情况,通常 0-20 个
        - 阴性数据量```y=0```非常大 
        - 异常的种类太多,无法从正常的数据推断异常数据的特征
        - 新的异常和旧的异常差距非常大.
    - 使用监督学习
        - 阴性和阳性的数据量都很大
        - 新的阳性数据的特性和训练集中的样例类似
    - 当数据量发生变化根据情况切换算法 
    
    #### 9.2.3 非高斯分布特征处理
    
    通过对特征值进行一些转换,让它的分布更像高斯分布.
    通过```hist```函数画图观察
    
    常用的方式
    
    -  $\log{(x)}$ 可以将递减方式的参数变成高斯分布
    -  $\log{(x+c)}$
    -  $\sqrt(x)$
    - $x^{\frac{1}{2}}$
    -  $x^{\frac{1}{3}}$

#### 9.2.3 常见问题

- $p(x)$对正常和不正常的数据都比较大
    - 增加额外的可以区分的特征值
    - 例如 对数据中心进行监控 我们可以增加 $x_6 = \frac{CpuLoad^2}{NetworkTraffic}$ 这种新的特性

### 9.3 多变量高斯分布

#### 9.3.1 模型
- 参数 $\mu$ , $\Sigma$

$p(x;\mu,\Sigma) = \frac{1}{(2\pi) \frac{n}{2} \vert \Sigma \vert^{ \frac{1}{2}}}  \exp{ \left(- \frac{1}{2} (x - \mu)^T \Sigma^{-1}(x - \mu)  \right) } $

- 参数拟合 :  对训练集 $\{  x^{(1)}, x^{(2)}, ... x^{(m)}\}$ , x 是n维向量.

$\mu  = \frac{1}{m} \sum\limits_{i=1}^mx^{(i)}$
    
$\Sigma = \frac{1}{m} \sum\limits_{i=1}^m (x^{(i)} - \mu) (x^{(i)} - \mu)^T$

-  对新的数据计算$p(x)$ , $p(x) < \epsilon $则为异常.

#### 9.3.2 与原始模型的比较

- 使用原始模型
    - 通过手动增加新特征值来表达有关联的特征值的关系.
    - 计算开销小一些,可以处理更多的特征值比如 $ n=10000  - 100000$ 
    - 如果训练集数量小也能正常工作
- 多元高斯分布
    - 自动捕捉特征值的关系
    - 计算量大
    - 必须有$m>n$即训练集数量比特征类型多很多,否则$\Sigma$不可逆.通常 $m\geq 10n$
    - 如果特征值存在线性相关也你可逆,比如 $x_1=x_2$或者$x_1=x_2+x_3$,这类关系 

### 9.4 基于内容的推荐系统

主要思想是以内容作为特征量,通过对用户已经评分的内容做为数据集进行线性回归计算 $\Theta$值,对新数据使用该值进行预测.

### 9.5 协同过滤






 
