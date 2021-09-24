### Lost baggage distribution

#### 问题描述

一家公司从机场提取丢失或延误的行李；

顾客必须在规定的时间之前交付行李；

给出一个方案，包括：

	1. 使用最少的车辆
	2. 每辆货车应该交付哪些货物
	3. 交付的顺序

货车没有容量限制；

![image-20210924153209113](image\lost_baggage_distribution.jpg)

#### 数学模型

##### 定义集合

| 集合                            | 含义                     |
| ------------------------------- | :----------------------- |
| $\mathcal{L} = \{0,1..(n-1)\} $ | 出发点和客户位置信息集合 |
| $\mathcal{K}$                   | 可用车辆集合             |
| $S_k \in S  $                   | 第$k$的子路径            |

##### 参数

| 符号                          | 含义                  |
| ----------------------------- | --------------------- |
| $time_{i,j} \in \mathbb{R}^+$ | $i$到$j$ 处的行驶时间 |

##### 定义变量

| 变量                       | 含义                             |
| -------------------------- | -------------------------------- |
| $x_{i, j, k} \in \{0, 1\}$ | 第$k$ 辆车从$i$ 到$j$ 是否被访问 |
| $y_{i, k} \in \{0, 1\}$    | 第$k$ 辆车是否访问$i$点          |
| $z_{k} \in \{0,1 \}$       | 第$k$ 辆车是否被使用             |

##### 约束条件

1.  **Van utilization**	
   $$
   \begin{equation}
   y_{i,k} \leq z_{k} \quad \forall i \in L \setminus \{0\}, \; k \in V
   \end{equation}
   $$
   
2. **Travel time**
   $$
   \begin{equation}
   \sum_{i \in L} \sum_{j \in L \setminus \{0\}} t_{i,j} \cdot x_{i,j,k} \leq 120 \quad \forall k \in  V
   \end{equation}
   $$

3. **Visit all customers**
   $$
   \begin{equation}
   \sum_{k \in V}  y_{i,k} = 1 \quad \forall i \in L \setminus \{0\}
   \end{equation}
   $$
   
4. **Depot**
   $$
   \begin{equation}
   \sum_{k \in V}  y_{1,k} \geq \sum_{k \in V} z_k
   \end{equation}
   $$

5. **Arriving at a location**

$$
\begin{equation}
\sum_{i \in L}  x_{i,j,k} =  y_{j,k}  \quad \forall j \in L, \; k \in V
\end{equation}
$$

6. **Leaving a location**
   $$
   \begin{equation}
   \sum_{i \in L}  x_{j,i,k} = y_{j,k}  \quad \forall j \in L, \; k \in V
   \end{equation}
   $$
   
7. **Breaking symmetry**
   $$
   \begin{equation}
   \sum_{i \in L}  y_{i,k} \geq \sum_{i \in L}  y_{i,k+1} \quad \forall k \in  \{0..K-1\}
   \end{equation}
   $$
   
8. **Subtour elimination**
   $$
   \begin{equation}
   \sum_{(i,j) \in S_k}x_{i,j,k} \leq |S_k|-1 \quad \forall  k \in K, \;   S_k \subseteq L
   \end{equation}
   $$
   

##### 目标函数

$$
\begin{equation}
\text{Minimize} \quad \sum_{k = 1}^{K} z_k
\end{equation}
$$

#### 参考代码

 [lost_baggage_distribution.py](code\lost_baggage_distribution.py) 

