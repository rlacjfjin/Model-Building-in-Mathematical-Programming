### Milk Collection Problem

#### 问题描述

牛奶加工厂从多个农场收集牛奶，搬运到仓库进行加工；

工厂有一辆罐车，有装载容量；

农场有大小区分，小工厂每隔一天收集一次，大工厂每天都要收集；

推荐一个罐车装载牛奶的路线，满足：

	1. 访问所有大工厂
	2. 访问部分小工厂
	3. 考虑容量限制
	4. 每隔几天，必须再次访问大工厂，访问前一次未访问过的小工厂



<img src="D:\github\Model-Building-in-Mathematical-Programming\image\milk_collection.png" alt="image-20210827161126821" style="zoom:67%;" />



![image-20210924153519326](image\milk_collection_prob.jpg)

#### 数学模型

##### 定义集合

| 集合                                                         | 含义                              |
| ------------------------------------------------------------ | :-------------------------------- |
| $\mathcal{F}$                                                | 加工厂和农场集合，加工厂的下表为0 |
| $\mathcal{everyDay}$                                         | 每天需要访问的农场集合            |
| $\mathcal{otherDay}$                                         | K每隔一天访问的农场集合           |
| $\mathcal{K}$                                                | 要计划的天数                      |
| $\text{Edges}= \{(i,j) \in \mathcal{F} \times\mathcal{F} \}$ | 可达的路径集合                    |
| $S_k \in S  $                                                | 第$k$的子路径                     |

##### 参数

| 符号     | 含义                  |
| -------- | --------------------- |
| $d_{ij}$ | $i$到$j$ 处的运输成本 |
| $C$      | 货车的容量            |
| $R_i$    | 每个农场可提供的奶量  |

##### 定义变量

| 变量                       | 含义                                  |
| -------------------------- | ------------------------------------- |
| $x_{i, j, k} \in \{0, 1\}$ | 第$k$ 天农场$i$ 到$j$ 是否被访问      |
| $y_{i, k} \in \{0, 1\}$    | 隔天访问的农场$i$ 在第$k$天是否被访问 |

##### 约束条件

1.  **Symmetry Constraints**
   $$
   \begin{equation}
   x_{i, j, k} = x_{j, i, k} \quad \forall k \in dayType, \; (i, j) \in Edges
   \tag{1}
   \end{equation}
   $$
   
2. **Entering and leaving an every day farm**
   $$
   \begin{equation}
   \sum_{j: (i,j) \in \text{Edges}} x_{i,j,k} = 2 \quad \forall  i \in everyDay, \; k \in dayType 
   \tag{2}
   \end{equation}
   $$

3.  **Entering and leaving an every other day farm**
   $$
   \begin{equation}
   \sum_{j: (i,j) \in \text{Edges}} x_{i,j,k}  = 2 \cdot y_{i, k} \quad \forall  i \in otherDay, \; k \in dayType 
   \tag{3}
   \end{equation}
   $$
   
4. **Tanker capacity**
   $$
   \begin{equation}
   \sum_{i \in \text{otherDay}} R_{i} \cdot y_{i,k} \leq C -\sum_{i \in everyDay} R_{i} \quad \forall  k \in K 
   \tag{4}
   \end{equation}
   $$
   
5. **Farms visited**
   $$
   \begin{equation}
   y_{i,1} + y_{i,2}  = 1 \quad \forall  i \in \text{otherDay}
   \tag{5}
   \end{equation}
   $$
   
6. **Subtour elimination**
   $$
   \begin{equation}
   \sum_{(i,j) \in S_k}x_{i,j,k} \leq |S_k|-1 \quad \forall  k \in K, \;   S_k \in S
   \tag{6}
   \end{equation}
   $$
   

##### 目标函数

$$
\begin{equation}
\text{Min} \quad Z = \sum_{k \in K} \sum_{(i,j) \in \text{Edges}}  d_{i,j} \cdot x_{i,j,k}
\tag{0}
\end{equation}
$$



#### 参考代码

 [milk_collection.py](code\milk_collection.py) 