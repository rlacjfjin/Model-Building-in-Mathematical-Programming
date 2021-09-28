### Agricultural pricing

#### 问题描述

现要对牛奶、黄油、奶酪定价；

可由Fat和Dry matter获取，可用的量为分别为 600,000吨/年 和 750,000/年；

产品的百分比组成如下表：

| Composition | Fat (%) | Dry matter (%) |
| --- | --- | --- |
| Milk | 4 | 9 |
| Butter | 80 | 2 |
| Cheese 1 | 35 | 30 |
| Cheese 2 | 25 | 40 |

去年产品的需求和价格如下表：

| Dairy <br /> products | Milk | Butter | Cheese 1 | Cheese 2 |
| --- | --- | --- | --- | --- |
| Demand (1000 tons) | 4.82 | 0.32 |  0.21 | 0.07 |
| Price (dollars/ton) | 297 | 720 | 1050 | 815 |

弹性系数和交叉弹性系数见下表： 

| Milk | Butter | Cheese 1 | Cheese 2 | Cheese 1 to  <br /> Cheese 2 |  Cheese 2 to  <br /> Cheese 1 |
| --- | --- | --- | --- | --- |  --- |
| 0.4 | 2.7 | 1.1 |  0.4 | 0.1 |  0.4 |

要求物价指数不能高于去年；去年的物价指数为1.939；

确定每个产品的价格，使得收益最大化；



#### 数学模型

- 定义集合

  - $\mathcal{D} $ 每日产品集合
  - $\mathcal{C}$  产品的组成(component)集合

- 参数

  1. 每年可用的component吨数 $S_{c} \in \mathbb{R}^+$

  2. 产品中component的百分比 $T_{c,d} \in [0,1]$

  3. 去年产品的消费 $Q_{d} \in \mathbb{R}^+$

  4. 去年产品的价格$P_{d} \in \mathbb{R}^+$

  5. 去年产品消费价格弹性指数 $E_{d} \in \mathbb{R}^+$ 以及交叉弹性指数$e_{d_1,d_2} \in \mathbb{R}^+$

  6. 反应去年总消费成本的物价指数 $PI \in \mathbb{R}^+$

     

$$
\begin{alignat*}{2}
\text{Maximize} & \quad \sum_{d \in \mathcal{D}}{q_d * p_d} \\
\mbox{s.t.}\quad
&\sum_{d \in \mathcal{D}}{T_{c,d}* q_{d} } \leq S_{c} \quad \forall c \in \mathcal{C}\tag{1} \\
&\sum_{d \in \mathcal{D}}{Q_{d}* p_{d} } \leq PI \tag{2}\\
&\frac{q_{d} - Q_{d}}{Q_{d}} = -E_{d}*\frac{p_{d} - P_{d}}{P_{d}}+e_{d_i,d_j}∗\frac{p_{d_i}−P_{d_i}}{P_{d_i}}  \quad \forall d \in \mathcal{D},d_i,d_j \in \mathcal{\bar{D}} \tag{3}\\
\end{alignat*} \\
$$

- 模型说明

  - 决策变量$q_d$ ----需求
  - 决策变量$p_d$ ----价格
  - 约束(1) ---- 供应量的限制
  - 约束(2) ---- 新价格必须确保不会增加去年消费的总费用
  - 约束(3) ---- 需求与价格的关系通过弹性指数来关联(假设有线性关系)

