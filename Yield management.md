### Yield management

#### 问题描述

航空公司出售飞往特定目的地的机票，航班将在三周后起飞；

最多可用六架飞机来安排航班，每架飞机的租金为50000英镑，有：

	1. 37个头等舱座位 
	2. 38个商务舱座位 
	3. 47 个经济舱座位

其中，任何类别的10%的座位数可以转移到相邻的类别；

对每个座位定价，随着时间变化可以更新价格，但一旦购买了就不能退票；

为了方便管理，每个类别有三个可选的价格，不需要为每个类别选择相同的选项；

如下表：

![image-20210927165739723](D:\github\Model-Building-in-Mathematical-Programming\image\yield_manage_price.jpg)

每个阶段的需求是不确定的，但会受价格的影响；

预先对价格和需求的概率分布进行了预测，如下表：

![image-20210927170003515](D:\github\Model-Building-in-Mathematical-Programming\image\yield_manage_pred.jpg)

需求的预测如下表：

![yield_manage_forecastDemand](D:\github\Model-Building-in-Mathematical-Programming\image\yield_manage_forecastDemand.PNG)

决定：

	1. 当前阶段的价格
	2. 每个类别能预售多少张票
	3. 要租的飞机数
	4. 未来的价格
	5. 未来能够售卖的机票

来实现收益最大化；应给出所有可能发生的组合情况下的收益分析；

过了一段时间过后，能拿到实际的需求，如下表：

![image-20210927170954875](D:\github\Model-Building-in-Mathematical-Programming\image\yield_manage_actualDemand.jpg)

根据实际的需求，重新给出未来的收益最大化方案；

#### 解决方案

**符号说明**

| 集合                         | 含义           |
| ---------------------------- | -------------- |
| $i,j,k \in \text{Scenarios}$ | 不同场景集合   |
| $h \in \text{Options}$       | 可选价格的集合 |
| $c \in \text{Class}$         | 座位等级集合   |

**参数表(给定的数据)**

| 符号说明                                        | 含义                                                         |
| ----------------------------------------------- | ------------------------------------------------------------ |
| $\text{price1}_{c,h} \in \mathbb{R}^+$          | option $h$ , class $c$ , week 1 对应的价格                   |
| $\text{price2}_{i,c,h} \in \mathbb{R}^+$        | 第一周scenario $i$ 下的 option $h$ , class $c$ , week 2 对应的价格 |
| $\text{price3}_{i,j,c,h} \in \mathbb{R}^+$      | 第一周scenario $i$, 第二周scenario $j$ 下的 option $h$  class $c$ week 3 对应的价格 |
| $\text{forecast1}_{i,c,h} \in \mathbb{R}^+$     | class $c$  option $h$ scenario $i$  week 1需求预测           |
| $\text{forecast2}_{i,j,c,h} \in \mathbb{R}^+$   | 第一周的scenario $i$, 第二周的scenario $j$ , class $c$ option $h$ week 2 需求预测 |
| $\text{forecast3}_{i,j,k,c,h} \in \mathbb{R}^+$ | 第一周的scenario $i$, 第二周的scenario $j$, 第三周的scenario $k$, class $c$ option $h$ week 3 需求预测 |
| $\text{prob}_i \in [0,1]$                       | scenario $i$ 发生的概率                                      |
| $\text{cap}_c \in \mathbb{N}$                   | 每台飞机的 class $c$ 的座位数                                |
| $\text{cost} \in \mathbb{R}^+$                  | 租用每台飞机的成本                                           |

**决策变量定义**

| 变量                              | 含义                                                         |
| --------------------------------- | ------------------------------------------------------------ |
| $p1_{c,h} \in \{0, 1\}$           | week 1 class $c$, option $h$ 是否被选择                      |
| $p2_{i,c,h} \in \{0, 1\}$         | 第一周的scenario $i$ , week 2 class $c$, option $h$ 是否被选择 |
| $p3_{i,j,c,h} \in \{0, 1\}$       | 第一周scenario $i$, 第二周scenario $j$ ,week 3,class $c$, option $h$ 是否被选择 |
| $s1_{i,c,h} \in \mathbb{R}^+$     | week 1 class $c$  option $h$ scenario $i$ 对应的售卖票数     |
| $s2_{i,j,c,h} \in \mathbb{R}^+$   | week 2 class $c$  option $h$  scenario $i$  week 1,  scenario $j$  week 2 对应的售卖票数 |
| $s3_{i,j,k,c,h} \in \mathbb{R}^+$ | week 3 class $c$  option $h$  scenario $i$  week 1,  scenario $j$  week 2 scenario $k$ week 3 对应的售卖票数 |
| $r1_{i,c,h} \in \mathbb{R}^+$     | week 1 class $c$  option $h$ scenario $i$ 收益               |
| $r2_{i,j,c,h} \in \mathbb{R}^+$   | week 2 class $c$  option $h$  scenario $i$  week 1,  scenario $j$  week 2 收益 |
| $r3_{i,j,k,c,h} \in \mathbb{R}^+$ | week 3 class $c$  option $h$  scenario $i$  week 1,  scenario $j$  week 2 scenario $k$ week 3 收益 |
| $u_{ijkc}$                        | 连续几周的scenario分别为$i,j,k$ 下的class $c$ 松弛量         |
| $v_{ijkc}$                        | 连续几周的scenario分别为$i,j,k$ 下的class $c$ 剩余量         |
| $n$                               | 租飞机的数量                                                 |

**数学模型**

- 约束条件

  1. **Price option**: Exactly one price option must be chosen in each class under each set of scenarios

     
     $$
     \sum_{h \in \text{Options}} p1_{c,h} = 1 \quad \forall c \in \text{Class}
     $$

     $$
     \sum_{h \in \text{Options}} p2_{i,c,h} = 1 \quad \forall c \in \text{Class}, \; i \in \text{Scenarios}
     $$

     $$
     \sum_{h \in \text{Options}} p3_{i,j,c,h} = 1 \quad \forall c \in \text{Class}, \; i,j \in \text{Scenarios}
     $$

     

  2. **Sales**: Numbers sold cannot exceed demand

     
     $$
     s1_{i,c,h} \leq \text{forecast1}_{i,c,h} * p1_{c,h},
     \quad \forall i \in \text{Scenarios}, \; c \in \text{Class}, \; h \in \text{Options}
     $$

     $$
     s2_{i,j,c,h} \leq \text{forecast2}_{j,c,h} * p2_{i,c,h},
     \quad \forall i,j \in \text{Scenarios}, \; c \in \text{Class}, \; h \in \text{Options}
     $$

     $$
     s3_{i,j,k,c,h} \leq \text{forecast3}_{k,c,h} * p3_{i,j,c,h},
     \quad \forall i,j,k \in \text{Scenarios}, \; c \in \text{Class}, \; h \in \text{Options}
     $$

     

  3. Adjustment is possible between classes

     
     $$
     u_{i,j,k,c} \leq 0.1 \text{cap}_c ,\quad \forall i,j,k \in \text{Scenarios},\ c\in \text{Class}\\
     v_{i,j,k,c} \leq 0.1 \text{cap}_c , \quad \forall i,j,k \in \text{Scenarios},\ c\in \text{Class}\\
     \sum_{c} {u_{i,j,k,c}} = \sum_{c}{v_{i,j,k,c}}, \quad \quad \forall i,j,k \in \text{Scenarios}
     $$
     

  4. **Class capacity**

     
     $$
     \sum_{h \in \text{Options}} ({s1_{i,c,h} + s2_{i,j,c,h} + s3_{i,j,k,c,h})} + 
     u_{i,j,k,c} - v_{i,j,k,c} \leq \text{cap}_c * n 
     \quad \forall i,j,k \in \text{Scenarios}, \; c \in \text{Class}
     $$
     ​	

  5. If a particular price option is chosen (under certain scenarios), then the sales cannot exceed the estimated demand and the revenue must be the product of the price and sales
     $$
     r_{1ich} - \text{price1}_{ch}s_{1ich}\leq 0 \\
     r_{2ijch} - \text{price2}_{ch}s_{2ijch}\leq 0 \\
     r_{3ijkch} - \text{price3}_{ch}s_{3ijkch}\leq 0 \\
      \text{price1}_{ch}s_{1ich} - r_{1ich} + \text{price1}_{ch}\text{forecast1}_{i,c,h} p_{1ch} \leq \text{price1}_{ch}\text{forecast1}_{i,c,h} \\
       \text{price2}_{ch}s_{2ijch} - r_{2ijch} + \text{price2}_{ch}\text{forecast2}_{j,c,h} p_{2ich} \leq \text{price2}_{ch}\text{forecast2}_{j,c,h} \\
       \text{price3}_{ch}s_{3ijkch} - r_{3ijkch} + \text{price3}_{ch}\text{forecast3}_{k,c,h} p_{3ijch} \leq \text{price3}_{ch}\text{forecast3}_{k,c,h} \\
     $$
     

     

- 目标函数
  $$
  Profit = \sum\limits_{i,c,h}\text{prob}_i r_{1ich} + \sum\limits_{i,j,c,h}\text{prob}_i\text{prob}_j r_{2ijch} + \sum\limits_{i,j,k,c,h}\text{prob}_i\text{prob}_j\text{prob}_k r_{3ijkch} - cost*n
  $$