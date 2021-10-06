### Food manufacture

#### 问题描述

A food is manufactured by reﬁning raw oils and blending them together.

##### 数据

1. raw oils categories

   |      Category      |           Oil           |
   | :----------------: | :---------------------: |
   |   Vegetable oils   |     VEG 1 <br>VEG 2     |
   | Non-vegetable oils | OIL 1<br>OIL 2<br>OIL 3 |

2. raw oils prices

   | Month    | VEG 1 | VEG 2 | OIL 1 | OIL 2 | OIL 3 |
   | -------- | ----- | ----- | ----- | ----- | ----- |
   | January  | 110   | 120   | 130   | 110   | 115   |
   | February | 130   | 130   | 110   | 90    | 115   |
   | March    | 110   | 140   | 130   | 100   | 95    |
   | April    | 120   | 110   | 120   | 120   | 125   |
   | May      | 100   | 120   | 150   | 110   | 105   |
   | June     | 90    | 100   | 140   | 80    | 135   |



##### 限制条件

1. 最终产品的售价为 $150/t

2. 植物油和非植物油需要不同的生产线进行精炼

3. 每个月可精炼的油量是有限的；植物油<=200 t/month, 非植物油 <=250 t/month

4. 精炼过程中可视为无损失，精炼成本可忽视不计

5. 原油可存储用于后续的生产，存储成本为5$/t/month; 最终产品不可存储，精炼油也不能存储；

6. 生产产品有技术性难度指标(3～6); 假设混合生产中技术性难度指标有线性相关性；

   | Oils  | Hardness |
   | ----- | -------- |
   | VEG 1 | 8.8      |
   | VEG 2 | 6.1      |
   | OIL 1 | 2.0      |
   | OIL2  | 4.2      |
   | OIL 3 | 5.0      |

7. 期初库存：每种原由有500t； 要求这些库存也将在 6 月底存在；

可扩展约束：

 	1. 制造食物的时候，不得超过使用三种油
 	2. 一种油在一个月内一旦被使用，至少要用20t
 	3. 若 VEG 1或VEG 2在一个月内被使用，则OIL 3也必须被使用

##### 目标

- 应该采取什么样的采购和制造方案，实现利润最大化？

#### 解决方案

##### 定义集合

| 集合                                          | 含义         |
| --------------------------------------------- | :----------- |
| $t \in \text{Months}$                         | 月份集合     |
| $V=\{\text{VEG1},\text{VEG2}\}$               | 食用油集合   |
| $N=\{\text{OIL1},\text{OIL2},\text{OIL3}\}  $ | 非食用油集合 |
| $o \in \text{Oils} = V \cup N$                | 油的集合     |

##### 参数

| 符号                                   | 含义                   |
| -------------------------------------- | ---------------------- |
| $\text{price} \in \mathbb{R}^+$        | 最终的售卖价格         |
| $\text{init_store} \in \mathbb{R}^+$   | 初始库存               |
| $\text{target_store} \in \mathbb{R}^+$ | 目标库存               |
| $\text{holding_cost} \in \mathbb{R}^+$ | 每个月的维持成本       |
| $\text{veg_cap} \in \mathbb{R}^+$      | 精炼植物油的装机容量   |
| $\text{oil_cap} \in \mathbb{R}^+$      | 精炼非植物油的装机容量 |
| $\text{min_hardness} \in \mathbb{R}^+$ | 最终产品允许的最低硬度 |
| $\text{max_hardness} \in \mathbb{R}^+$ | 最终产品允许的最大硬度 |
| $\text{hardness}_o \in \mathbb{R}^+$   | 产品的硬度             |
| $\text{cost}_{t,o} \in \mathbb{R}^+$   | 预估的购买价格         |

##### 定义变量

| 变量                                    | 含义     |
| --------------------------------------- | -------- |
| $\text{produce}_t \in \mathbb{R}^+$     | 生产的量 |
| $\text{buy}_{t,o} \in \mathbb{R}^+$     | 购买的量 |
| $\text{consume}_{t,o} \in \mathbb{R}^+$ | 使用的量 |
| $\text{store}_{t,o} \in \mathbb{R}^+$   | 存储的量 |

##### 约束条件

1.  **Initial Balance**
   $$
   \begin{equation}
   \text{init_store} + \text{buy}_{Jan,o} = \text{consume}_{Jan,o} + \text{store}_{Jan,o} \quad \forall o \in \text{Oils}
   \tag{1}
   \end{equation}
   $$
   ​	
   $$
   \begin{equation}
   y_{i,k} \leq z_{k} \quad \forall i \in L \setminus \{0\}, \; k \in V
   \end{equation}
   $$

2. **Balance** 
   $$
   \begin{equation}
   \text{store}_{t-1,o} + \text{buy}_{t,o} = \text{consume}_{t,o} + \text{store}_{t,o} \quad \forall (t,o) \in \text{Months} \setminus \{\text{Jan}\} \times \text{Oils}
   \tag{2}
   \end{equation}
   $$
   

3.  **Inventory Target** 

   $$
   \begin{equation}
   \text{store}_{Jun,o} = \text{target_store} \quad \forall o \in \text{Oils}
   \tag{3}
   \end{equation}
   $$

4.  **Refinement Capacity**
    $$
    \begin{equation}
    \sum_{o \in V}\text{consume}_{t,o} \leq \text{veg_cap} \quad \forall t \in \text{Months}
    \tag{4.1}
    \end{equation}
    $$

    $$
    \begin{equation}
    \sum_{o \in N}\text{consume}_{t,o} \leq \text{oil_cap} \quad \forall t \in \text{Months}
    \tag{4.2}
    \end{equation}
    $$

5.  **Hardness**
    $$
    \begin{equation}
    \text{min_hardness}*\text{produce}_t \leq \sum_{o \in \text{Oils}} \text{hardness}_o*\text{consume}_{t,o} \leq \text{max_hardness}*\text{produce}_t \quad \forall t \in \text{Months}
    \tag{5}
    \end{equation}
    $$

6.   **Mass Conservation**

    $$
    \begin{equation}
    \sum_{o \in \text{Oils}}\text{consume}_{t,o} = \text{produce}_t \quad \forall t \in \text{Months}
    \tag{6}
    \end{equation}
    $$
    

##### 目标函数

$$
\begin{equation}
\text{Maximize} \quad Z = \sum_{t \in \text{Months}}\text{price}*\text{produce}_t - \sum_{t \in \text{Months}}\sum_{o \in \text{Oils}}(\text{cost}_{t,o}*\text{consume}_{t,o} + \text{holding_cost}*\text{store}_{t,o})
\tag{0}
\end{equation}
$$

**扩展约束**

1. 定义0-1变量

    $\text{use}_{t,o} \in \{0,1\}$: 1 if oil $o$ is used on month $t$, 0 otherwise. 

2. **Consumption Range**: Oil $o$ can be consumed in month $t$ if we decide to use it in that month, and the Tons consumed should be between 20 and the refinement capacity for its type. 
   $$
   \begin{equation}
   \text{min_consume}*\text{use}_{t,o} \leq \text{consume}_{t,o} \leq \text{veg_cap}*\text{use}_{t,o} \quad \forall (t,o) \in V \times \text{Months}
   \tag{7.1}
   \end{equation}
   $$

   $$
   \begin{equation}
   \text{min_consume}*\text{use}_{t,o} \leq \text{consume}_{t,o} \leq \text{oil_cap}*\text{use}_{t,o} \quad \forall (t,o) \in N \times \text{Months}
   \tag{7.2}
   \end{equation}
   $$

   

3. **Recipe**: The maximum number of oils used in month $t$ must be three.
   $$
   \begin{equation}
   \sum_{o \in \text{Oils}}\text{use}_{t,o} \leq \text{max_ingredients} \quad \forall t \in \text{Months}
   \tag{8}
   \end{equation}
   $$
   

4. **If-then Constraint**: If oils VEG1 or VEG2 are used in month $t$, then OIL3 must be used in that month.
   $$
   \begin{equation}
   \text{use}_{t,\text{VEG1}} \leq \text{use}_{t,\text{OIL3}} \quad \forall t \in \text{Months}
   \tag{9.1}
   \end{equation}
   $$

   $$
   \begin{equation}
   \text{use}_{t,\text{VEG2}} \leq \text{use}_{t,\text{OIL3}} \quad \forall t \in \text{Months}
   \tag{9.2}
   \end{equation}
   $$

   