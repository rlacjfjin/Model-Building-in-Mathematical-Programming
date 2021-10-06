### Economic Planning

#### 问题描述

假设考虑以下三个行业：

1. Coal(煤炭)
2. Steel(钢铁)
3. Transport(运输)

这些行业互相影响，如，燃烧生产钢铁的高炉需要煤炭，提取煤炭的机械需要钢铁等，即某一行业的输入变成另一行业的输出；

其量化关系如下：

| input (t) / <br /> output (t+1) | Coal | Steel | Transport |
| --- | --- | --- | --- |
| Coal | 0.1 | 0.5 | 0.4 |
| Steel | 0.1 | 0.1 | 0.2 |
| Transport | 0.2 | 0.1 | 0.2 |
| Labor | 0.6 | 0.3 | 0.2 |
|**Total**  | **1** | **1** | **1**|

说明：获得1单位的Coal需要投入0.1Coal + 0.1 Steel + 0.2 Transport + 0.6 Labor

投入生产能力，导致其他行业的生产能力的增加(永久性)，如下表：

| input (t) / <br /> output (t+2) | Coal | Steel | Transport |
| --- | --- | --- | --- |
| Coal | 0.1 | 0.7 | 0.9 |
| Steel | 0.1 | 0.1 | 0.2 |
| Transport | 0.2 | 0.1 | 0.2 |
| Labor | 0.4 | 0.2 | 0.1 |

库存信息如下表:

| Present | Stocks | Productive Capacity |
| --- | --- | --- |
| Coal | 150 | 300 |
| Steel | 80 | 350 |
| Transport | 100 | 280 |

要求规划方案，使得在规划范围内最大化总人力利用率，即就业，同时满足每年的消费需求；



#### 解决方案

##### 定义集合

| 集合                        | 含义               |
| --------------------------- | :----------------- |
| $i,j \in \text{Industries}$ | 行业集合           |
| $ t \in \text{Years}$       | 需要规划的时间集合 |

##### 参数

| 符号                                          | 含义                             |
| --------------------------------------------- | -------------------------------- |
| $\text{demand}_{j} \in \mathbb{R}^+$          | 需求                             |
| $\text{initial_stock}_{j} \in \mathbb{R}^+$   | 初始库存                         |
| $\text{in_out_prod}_{i,j} \in \mathbb{R}^+$   | 投入的产品量                     |
| $\text{in_out_cap}_{i,j} \in \mathbb{R}^+$    | 当年的投入使未来生产能力增加的量 |
| $\text{industry_cap}_{j} \in \mathbb{R}^+$    | 生产能力                         |
| $\text{labor_extra_cap}_{j} \in \mathbb{R}^+$ | 永久增加产能的劳动力需求         |
| $\text{labor_prod}_{j} \in \mathbb{R}^+$      | 劳动力需求                       |

##### 定义变量

| 变量                                       | 含义     |
| ------------------------------------------ | -------- |
| $\text{production}_{j,t} \in \mathbb{R}^+$ | 生产量   |
| $\text{stock}_{j,t} \in \mathbb{R}^+$      | 库存     |
| $\text{extra_cap}_{j,t} \in \mathbb{R}^+$  | 额外产能 |

假设考虑的规划时间以后，有：

	1. 需求在规划时间以后保持不变
 	2. 库存水平在规划时间以后保持不变
 	3. 规划时间以后无法增加产能

即：规划时间以后是一个静态模型，生产量如下：
$$
\begin{equation}
x_{i} = \text{demand}_{i} + \sum_{j \in \text{Industries} } \text{in_out_prod}_{i,j} * x_{j}
\end{equation}
$$
上式给出了规划时间以后的产品生产量的下界，然后下一年的生产量有如下限制：
$$

\text{production}_{j,t} \geq x_{j} \quad \forall j \in \text{Industries}, \; t=6. \\

\text{extra_cap}_{j,t} = 0 \quad \forall j \in \text{Industries}, \; t=6.
$$

##### 约束条件

1. **Balance equation**
   $$
   \begin{equation}
   \text{initial_stock}_{i} = \sum_{j \in \text{Industries} } \text{in_out_prod}_{i,j}*\text{production}_{j,2}+\text{demand}_{i} + \sum_{j \in \text{Industries} } \text{in_out_cap}_{i,j}*\text{extra_cap}_{j,3} +
   \text{stock}_{i,1}
   \end{equation}
   $$
   
   $$
   \begin{equation}
   \text{production}_{j,t} + \text{stock}_{i,t-1} =
   \sum_{j \in \text{Industries} } \text{in_out_prod}_{i,j}*\text{production}_{j,t+1} + \text{demand}_{i} +
   \sum_{j \in \text{Industries} } \text{in_out_cap}_{i,j}*\text{extra_cap}_{j,t+2} 
   + \text{stock}_{i,t} \quad \forall t \in H_{2,4}
   \end{equation}
   $$

$$
\begin{equation}
\text{production}_{j,5} + \text{stock}_{i,4} =
\sum_{j \in \text{Industries} } \text{in_out_prod}_{i,j}*\text{production}_{j,6}  +
\text{demand}_{i} + \text{stock}_{i,5}
\end{equation}
$$

2. **End of horizon constraints**

$$
\text{production}_{j,t} \geq x_{j} \quad \forall j \in \text{Industries}, \; t=6 
$$

$$
\text{extra_cap}_{j,t} = 0 \quad \forall j \in \text{Industries}, \; t=6
$$

3. **Productive capacity constraints**
   $$
   \begin{equation}
   \text{production}_{j,t} \leq \text{base_cap}_{j} + \sum_{\tau \leq t} \text{extra_cap}_{j,\tau} \quad \forall t \in \text{Horizon}
   \end{equation}
   $$

##### 目标函数

$$
\begin{equation}
\text{Maximize} \quad Z =
\sum_{t \in \text{fiveYears} } \sum_{j \in \text{Industries} } \text{labor_prod}_{j}*\text{production}_{j,t} +
\sum_{t \in \text{fiveYears} } \sum_{j \in \text{Industries} } \text{labor_extra_cap}_{j}*\text{extra_cap}_{j,t}
\end{equation}
$$

