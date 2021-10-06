### Factory planning

#### 问题描述

一家工厂在不同机器上生产不同产品，每个产品产生一定的利润，为了使总利润最大化，如何规划工厂的生产计划？

#### 数据

1. 生产表-----生产产品需要的每个过程时间以及利润

|                     | PROD1 | PROD2 | PROD3 | PROD4 | PROD5 | PROD6 | PROD7 |
| ------------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Profit              | 10    | 6     | 8     | 4     | 11    | 9     | 3     |
| Grinding            | 0.5   | 0.7   | -     | -     | 0.3   | 0.2   | 0.5   |
| Vertical Drilling   | 0.1   | 0.2   | -     | 0.3   | -     | 0.6   | -     |
| Horizontal Drilling | 0.2   | -     | 0.8   | -     | -     | -     | 0.6   |
| Boring              | 0.05  | 0.03  | -     | 0.07  | 0.1   | -     | 0.08  |
| Planning            | -     | -     | 0.01  | -     | 0.05  | -     | 0.05  |

2. 停机维护设备表-----无法使用

| Month    | Machine                            |
| -------- | ---------------------------------- |
| January  | One grinder                        |
| February | Two horizontal drills              |
| March    | One borer                          |
| April    | One vertical drill                 |
| May      | One grinder and one vertical drill |
| June     | One horizontal drill               |

3. 销售数量的上限

| Month    | PROD1 | PROD2 | PROD3 | PROD4 | PROD5 | PROD6 | PROD7 |
| -------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| January  | 500   | 1000  | 300   | 300   | 800   | 200   | 100   |
| February | 600   | 500   | 200   | 0     | 400   | 300   | 150   |
| March    | 300   | 600   | 0     | 0     | 500   | 400   | 100   |
| April    | 200   | 300   | 400   | 500   | 200   | 0     | 100   |
| May      | 0     | 100   | 500   | 100   | 1000  | 300   | 0     |
| June     | 500   | 500   | 100   | 300   | 1100  | 500   | 60    |

#### 限制条件

1. 每个月每一类产品可存储100个，但是有存储成本0.50$/unit/month
2. 期初库存为0，但希望6月底对每一类产品有50个存储在仓库里
3. 一周工作6天(一个月24天)，一天两个班次，总共8个小时
4. 不考虑不同过程之间的排序问题

#### 目标

为了使总利润最大化，工厂采取什么措施？



#### 解决方案

##### 定义集合

| 集合                    | 含义     |
| ----------------------- | :------- |
| $t \in \text{Months}$   | 月份集合 |
| $p \in \text{Products}$ | 产品集合 |
| $m \in \text{Machines}$ | 机器集合 |

##### 参数

| 符号                                      | 含义                   |
| ----------------------------------------- | ---------------------- |
| $\text{hours_per_month} \in \mathbb{R}^+$ | 每个月机器可用的时间   |
| $\text{max_inventory} \in \mathbb{N}$     | 每个月可存储的最大库存 |
| $\text{store_target} \in \mathbb{N}$      | 保留的库存数           |
| $\text{holding_cost} \in \mathbb{R}^+$    | 每个月的维持成本       |
| $\text{profit}_p \in \mathbb{R}^+$        | 收入                   |
| $\text{installed}_m \in \mathbb{N}$       | 机器安装的数量         |
| $\text{down}_{t,m} \in \mathbb{N}$        | 维护的机器数量         |
| $\text{time_req}_{m,p} \in \mathbb{R}^+$  | 生产所需要的时间       |
| $\text{max_sales}_{t,p} \in \mathbb{N}$   | 最大可卖的数量         |

##### 定义变量

| 变量                                                         | 含义     |
| ------------------------------------------------------------ | -------- |
| $\text{make}_{t,p} \in \mathbb{R}^+$                         | 生产的量 |
| $\text{store}_{t,p} \in [0, \text{max_inventory}] \subset \mathbb{R}^+$ | 存储的量 |
| $\text{sell}_{t,p} \in [0, \text{max_sales}_{t,p}] \subset \mathbb{R}^+$ | 售卖的量 |

##### 约束条件

1. **Initial Balance:**
   $$
   \begin{equation}
   \text{make}_{\text{Jan},p} = \text{sell}_{\text{Jan},p} + \text{store}_{\text{Jan},p} \quad \forall p \in \text{Products}
   \tag{1}
   \end{equation}
   $$

2. **Balance:** 
   $$
   \begin{equation}
   \text{store}_{t-1,p} + \text{make}_{t,p} = \text{sell}_{t,p} + \text{store}_{t,p} \quad \forall (t,p) \in \text{Months} \setminus \{\text{Jan}\} \times \text{Products}
   \tag{2}
   \end{equation}
   $$

3. **Inventory Target:**
   $$
   \begin{equation}
   \text{store}_{\text{Jun},p} = \text{store_target} \quad \forall p \in \text{Products}
   \tag{3}
   \end{equation}
   $$

4. **Machine Capacity:**
   $$
   \begin{equation}
   \sum_{p \in \text{Products}}\text{time_req}_{m,p}*\text{make}_{t,p} \leq \text{hours_per_month}*(\text{installed}_m - \text{down}_{t,m}) \quad \forall (t,m) \in \text{Months} \times \text{Machines}
   \tag{4}
   \end{equation}
   $$

##### 目标函数

$$
\begin{equation}
\text{Maximize} \quad Z = \sum_{t \in \text{Months}}\sum_{p \in \text{Products}}
(\text{profit}_p*\text{make}_{t,p} - \text{holding_cost}*\text{store}_{t,p})
\tag{0}
\end{equation}
$$



#### 扩展

优化维护计划：

不事先给定维护表，根据特定的维护要求，制定维护计划：

	1. 每台机器必须在六个月中的一个月内停机维护
 	2. grinding machines除外
 	3. 在任何六个月内只有两个需要停机 

参数中，$down$ 改为：
$$
down\_req_m∈\mathbb{N}
$$
变量添加维护的变量：
$$
repair_{t,m}∈\{0,1,…,down\_req_m\}⊂\mathbb{N}
$$
Machine Capacity约束相应的变为：
$$
\begin{equation}
\sum_{p \in \text{Products}}\text{time_req}_{m,p}*\text{make}_{t,p} \leq \text{hours_per_month}*(\text{installed}_m - \text{repair}_{t,m}) \quad \forall (t,m) \in \text{Months} \times \text{Machines}
\tag{4}
\end{equation}
$$
添加维护约束：
$$
\begin{equation}
\sum_{t \in \text{Months}}\text{repair}_{t,m} = \text{down_req}_m \quad \quad m\in  \text{Machines}
\tag{5}
\end{equation}
$$
