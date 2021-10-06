### Opencast mining

#### 问题描述

现有200$\times$200方形地块内进行露天采矿；

土壤的滑移角使得开挖边的坡度不可能超过 45 度；

考虑到滑移角的限制，该公司决定将此问题视为提取矩形块的问题之一;

每一个矩形块为50$\times$50$\times$25，挖的时候只能依次从上往下挖；

如下图表示4层的挖掘图，如17在1，2，5，6下面；

![image-20211006135923760](D:\github\Model-Building-in-Mathematical-Programming\image\opencast_mining.jpg)

已经获得了不同深度不同地点矿石价值的估计；

每个区块开采矿石的利润都已估算出来;

![image-20211006140154540](D:\github\Model-Building-in-Mathematical-Programming\image\opencast_mining_data.jpg)

目标是找到使总利润最大化的矿石开采计划； 

####  解决方案

##### 定义集合

| 集合                 | 含义       |
| -------------------- | :--------- |
| $b\in \text{Blocks}$ | 矩形块集合 |

##### 参数

| 符号                                     | 含义                     |
| ---------------------------------------- | ------------------------ |
| $\text{profit}_{b} \in \mathbb{R}^+$     | 从矩形块中采矿的收益     |
| $(b,b2) \in Arcs = Blocks \times Blocks$ | 表示不同矩形块的关联规则 |

##### 定义变量

| 变量                             | 含义         |
| -------------------------------- | ------------ |
| $\text{extract}_{b} \in \{0,1\}$ | 矩形块的选中 |

##### 目标函数

$$
\begin{equation}
\text{Maximize} \quad \sum_{b \in Blocks} \text{profit}_{b}*\text{extract}_{b}
\end{equation}
$$



##### 约束条件

1. **Extraction**
   $$
   \begin{equation}
   \text{extract}_{b2} \geq \text{extract}_{b} \quad \forall (b,b2) \in \text{Arcs}
   \end{equation}
   $$
   