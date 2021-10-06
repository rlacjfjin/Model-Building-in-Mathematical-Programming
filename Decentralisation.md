### Decentralisation

#### 问题描述

一家公司打算把部门迁移到别的地方；

有好处： 房租便宜、政府补贴、更容易招聘等等，这些事先已经算好了(量化为成本)

有坏处：部门之间的沟通交流，这些也已经量化成成本了

给出每个部门所迁移的地方，以最大限度的减少年度总成本；

现有五个部门：A~E，可迁移的备选地方为：Bristol、Brighton或者留在原来的地方；

迁移带来的好处量化表如下：

|  | A    | B    | C    | D | E |
| --- | --- | --- | --- | --- | --- |
| Bristol  | 10   | 15   | 10   | 20   | 5    |
| Brighton | 10   | 20   | 15   | 15 | 15 |

沟通成本定义为：$C_{ik} D_{jl}$ ，其中$C_{ik}$ 为部门之间的沟通成本，$D_{jl}$ 为城市之间的沟通成本，具体表如下：

![image-20210930112623526](D:\github\Model-Building-in-Mathematical-Programming\image\decentralisation_data.jpg)



####  解决方案

##### 定义集合

| 集合                          | 含义         |
| ----------------------------- | :----------- |
| $d,d2 \in \text{Departments}$ | 部门集合     |
| $c,c2 \in \text{Cities}$      | 备选城市集合 |

##### 参数

| 符号                                                    | 含义               |
| ------------------------------------------------------- | ------------------ |
| $\text{benefit}_{d,c} \in \mathbb{R}^+$                 | 部门迁移带来的收益 |
| $\text{communicationCost}_{d,c,d2,c2} \in \mathbb{R}^+$ | 沟通成本           |

##### 定义变量

| 变量                               | 含义                     |
| ---------------------------------- | ------------------------ |
| $\text{locate}_{d,c} \in \{0,1 \}$ | 部门迁移到城市的决策变量 |

##### 目标函数

$$
\begin{equation}
\text{Maximize} \quad Z = \sum_{d \in \text{Departments}} \sum_{c \in \text{Cities}} \text{benefit}_{d,c}*\text{locate}_{d,c} -
\sum_{d,c,d2,c2 \in dcd2c2} \text{communicationCost}_{d,c,d2,c2}*\text{locate}_{d,c}*\text{locate}_{d2,c2}
\end{equation}
$$



##### 约束条件

1. **Department location**
   $$
   \begin{equation}
   \sum_{c \in \text{Cities}} \text{locate}_{d,c} = 1 \quad \forall d \in \text{Departments}
   \end{equation}
   $$

2. **Departments limit**

$$
\begin{equation}
\sum_{d \in \text{Departments}} \text{locate}_{d,c} \leq 3 \quad \forall c \in \text{Cities}
\end{equation}
$$