### Efficiency Analysis

#### 问题描述

一家汽车制造商想要评估不同车库的效率，这些车库获得了销售其汽车的特许经营权；

评估的方法：数据包络分析 (DEA: data envelopment analysis ) 

每个车库有可量化的输入：

1. 员工
2. 陈列方式
3. 不同经济类别的流域人口
4. 不同品牌的年度需求

每个车库有可量化的输出：

1. 不同品牌的汽车销量
2. 年度利润

DEA的核心假设是：输入和输出是正相关的，即：扩大输入，得到的回报也更多；

评估效率的高和低：对于一个车库来说，如果不存在其他车库组合的等量输入，而得到的回报不低与该车库等方案，则认为该车库是效率高的；

数据如下:

![image-20210924161555216](D:\github\Model-Building-in-Mathematical-Programming\image\DEA_1.jpg)

![image-20210924161623318](D:\github\Model-Building-in-Mathematical-Programming\image\DEA_2.jpg)



#### 数学模型

##### 定义集合

| 集合                   | 含义                                              |
| ---------------------- | :------------------------------------------------ |
| $j,k \in \text{DMUS}$  | $\text{DMU}$ 的下标集合，$k$ 代表目标$\text{DMU}$ |
| $i \in \text{Inputs}$  | 输入集合                                          |
| $r \in \text{Outputs}$ | 输出集合                                          |

##### 参数

| 符号                        | 含义                                       |
| --------------------------- | ------------------------------------------ |
| $\text{invalue}_{i,j} > 0$  | Value of input $i$ for $\text{DMU}$  $j$   |
| $\text{outvalue}_{r,j} > 0$ | Value of output $r$ for  $\text{DMU}$  $j$ |

##### 定义变量

| 变量           | 含义                  |
| -------------- | --------------------- |
| $u_{r} \geq 0$ | Weight of output $r$. |
| $v_{i} \geq 0$ | Weight of input $i$.  |

**目标函数**：最大化目标DMU( decision making units, 决策单位 )的效率
$$
\text{Maximize} \quad E_k = \sum_{r \in \text{Outputs}} \text{outvalue}_{r,k}*u_{r} \tag{LP0}
$$
**约束条件**

1. Efficiency ratio
   $$
   \begin{equation} \sum_{r \in \text{Outputs}} \text{outvalue}_{r,j}*u_{r} - \sum_{i \in \text{Inputs}} \text{invalue}_{i,k}*v_{i} \leq 0 \quad \forall j \in \text{DMUS} \tag{LP1} \end{equation}
   $$

2. Normalization
   $$
   \begin{equation} \sum_{i \in \text{Inputs}} \text{invalue}_{i,k}*v_{i} = 1 \tag{LP2} \end{equation}
   $$

注：

- DMU的效率高的定义：$E_{k}^{*} = 1$



#### 参考代码

 [efficiency_analysis.py](code\efficiency_analysis.py) 