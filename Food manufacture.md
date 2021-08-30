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

### Sets and Indices

t∈Months={Jan,Feb,Mar,Apr,May,Jun}t∈Months={Jan,Feb,Mar,Apr,May,Jun}: Set of months.

V={VEG1,VEG2}V={VEG1,VEG2}: Set of vegetable oils.

N={OIL1,OIL2,OIL3}N={OIL1,OIL2,OIL3}: Set of non-vegetable oils.

o∈Oils=V∪No∈Oils=V∪N: Set of oils.

