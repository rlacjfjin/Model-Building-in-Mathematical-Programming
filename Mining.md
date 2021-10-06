### Mining

#### 问题描述

一家矿业公司需要为某个拥有 4 个矿山的区域制定一个五年的运营计划；

最多能拥有3个矿山，且即使当前阶段不运营，只要未来有可能要运营，公司还是需要继续支付使用费用，否则认为是永久放弃使用权；

每年需要支付的费用如下：

| <i></i> | Royalties |
| --- | --- |
| Mine 1 | $\$5 Million$ |
| Mine 2 | $\$4 Million$ |
| Mine 3 | $\$4 Million$ |
| Mine 4 | $\$5 Million$ |

每个矿山可采取的矿石的上限如下表：

| <i></i> | Max Production |
| --- | --- |
| Mine 1 | $2.0\times10^6$ Tons |
| Mine 2 | $2.5\times10^6$ Tons |
| Mine 3 | $1.3\times10^6$ Tons |
| Mine 4 | $3.0\times10^6$ Tons |

每个矿山能采取的矿石品质是不同的，如下表：

| <i></i> | Ore Quality |
| --- | --- |
| Mine 1 | 1.0 |
| Mine 2 | 0.7 |
| Mine 3 | 1.5 |
| Mine 4 | 0.5 |

每年有年度目标，如下表：

| <i></i> | Quality Target |
| --- | --- |
| Year 1 | 0.9 |
| Year 2 | 0.8 |
| Year 3 | 1.2 |
| Year 4 | 0.6 |
| Year 5 | 1.0 |

最终的可售卖矿石售价为 10 美元/吨。 未来年度的收入和成本按每年 10% 的比率贴现；

每年应该运营哪些矿山，每个矿山应该开采多少矿石？

####  解决方案

##### 定义集合

| 集合                 | 含义         |
| -------------------- | :----------- |
| $t \in \text{Years}$ | 计划年度集合 |
| $m \in \text{Mines}$ | 可用矿山集合 |

##### 参数

| 符号                                                    | 含义                     |
| ------------------------------------------------------- | ------------------------ |
| $\text{price} \in \mathbb{R}^+$                         | 售卖价                   |
| $\text{max_mines} \in \mathbb{N}$                       | 最大可用矿山数量         |
| $\text{royalties}_m \in \mathbb{R}^+$                   | 维持矿山的成本           |
| $\text{capacity}_m \in \mathbb{R}^+$                    | 矿山中最大可采取矿石数量 |
| $\text{quality}_m \in \mathbb{R}^+$                     | 矿石采取的质量           |
| $\text{target} \in \mathbb{R}^+$                        | 每年的质量目标           |
| $\text{time_discount}_t \in [0,1] \subset \mathbb{R}^+$ | 收入和成本的贴现的比例   |

##### 定义变量

| 变量                                    | 含义               |
| --------------------------------------- | ------------------ |
| $\text{blend}_t \in \mathbb{R}^+$       | 可售卖的矿石数量   |
| $\text{extract}_{t,m} \in \mathbb{R}^+$ | 采取的矿石数量     |
| $\text{working}_{t,m} \in \{0,1\}$      | 需要运营的矿山     |
| $\text{available}_{t,m} \in \{0,1\}$    | 需要持续持有的矿山 |

##### 目标函数

$$
\begin{equation}
\text{Maximize} \quad Z = \sum_{t \in \text{Years}}\sum_{m \in \text{Mines}}{\text{time_discount}_t*(\text{price}*\text{blend}_t-\text{royalties}_m*\text{extract}_{t,m})}
\tag{0}
\end{equation}
$$



##### 约束条件

1. **Operating Mines**
   $$
   \begin{equation}
   \sum_{m \in \text{Mines}}{\text{working}_{t,m}} \leq \text{max_mines} \quad \forall t \in \text{Years}
   \tag{1}
   \end{equation}
   $$

2. **Quality**

   $$
   \begin{equation}
   \sum_{m \in \text{Mines}}{\text{quality}_m*\text{extract}_{t,m}} = \text{target}_t*\text{blended}_t \quad \forall t \in \text{Years}
   \tag{2}
   \end{equation}
   $$

3. **Mass Conservation**
   $$
   \begin{equation}
   \sum_{m \in \text{Mines}}{\text{extract}_{t,m}} = \text{blend}_t \quad \forall t \in \text{Years}
   \tag{3}
   \end{equation}
   $$

4. **Mine Capacity**
   $$
   \begin{equation}
   \sum_{m \in \text{Mines}}{\text{extract}_{t,m}} \leq \text{capacity}_m*\text{working}_{t,m} \quad \forall t \in \text{Years}
   \tag{4}
   \end{equation}
   $$

5. **Open to Operate**
   $$
   \begin{equation}
   \text{working}_{t,m} \leq \text{available}_{t,m} \quad \forall (t,m) \in \text{Years} \times \text{Mines}
   \tag{5}
   \end{equation}
   $$
   

6. **Shut Down**
   $$
   \begin{equation}
   \text{available}_{t+1,m} \leq \text{available}_{t,m} \quad \forall (t < 5,m) \in \text{Years} \times \text{Mines}
   \tag{6}
   \end{equation}
   $$
   