#### 问题描述

- 因公司内部的组织架构调整，需要做人力规划；
- 预计未来三年内的人力需求；
- 为了满足未来的人力需求，从以下几个方面入手
  1. Recruitment 招聘
     - 每年的招聘人员需求
  2. Retraining 重新培训(内部转岗)
     - 非熟练工->半熟练工，附带成本
     - 半熟练工->熟练工，附带成本
     - 降级->部分员工主动离职(公司无额外成本)，导致人力流失的成本
  3. Redundancy 冗余人力
     - 裁员的成本
     - 雇佣比规划更多员工的人力成本
  4. Short-time working 短期工
     - 短期员工的计划人员数以及成本
     - 短期员工的生产效率是全职员工的50%

- 存在人力流失的成本；
- 近期无招聘人员，现有员工均已就业满一年；

#### 优化方向

1. 减少冗余人力，即裁员人数最小化
2. 最小化用人成本

#### 解决方案

##### 定义符号

| 符号                                                         | 描述                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| $\mathcal{T}=\{1,2,3...\}$                                   | 预计人员规划的时间集合                                       |
| $\mathcal{S}=\{s_1,s_2,s_3,...\}$                            | 技能熟练度分类集合                                           |
| $\text{demand}_{t,s}$        $t\in\mathcal{T}, s\in\mathcal{S}$ | 在$t$年技能类型为$s$的员工需求                               |
| $\text{rookie_attrition} \in [0,1] \subset \mathbb{R}^+$     | Percentage of workers who leave within the first year of service |
| $\text{veteran_attrition} \in [0,1] \subset \mathbb{R}^+$:   | Percentage of workers who leave after the first year of service |
| $\text{demoted_attrition} \in [0,1] \subset \mathbb{R}^+$:   | Percentage of workers who leave the company after a demotion. |
|                                                              |                                                              |
| $\text{max_retrained}_{s,s'}$        $s\in\mathcal{S}, s'\in\mathcal{S}$ | 从技能$s$ 到$s'$ 转岗允许的上限;(跳级以及不转岗时为0)        |
| $\text{max_overmanning}$                                     | 每年的超员员工允许的上限                                     |

##### 定义变量

|                             变量                             |                   含义                   |
| :----------------------------------------------------------: | :--------------------------------------: |
| $\text{employed}_{t,s}$           $t\in\mathcal{T}, s\in\mathcal{S}$ |  在$t$年技能类型为$s$的**实际员工**人数  |
| $\text{recruited}_{t,s}$           $t\in\mathcal{T}, s\in\mathcal{S}$ |  在$t$年技能类型为$s$的**招聘员工**人数  |
| $\text{retrained}_{t,s,s'}$       $t\in\mathcal{T}, s,s'\in\mathcal{S}$ | 在$t$年从技能类型$s$转为$s'$ 的员工人数  |
| $\text{redundant}_{t,s}$         $t\in\mathcal{T}, s\in\mathcal{S}$ | 在$t$年技能类型为$s$的**被解雇员工**人数 |
| $\text{shorttime}_{t,s}$           $t\in\mathcal{T}, s\in\mathcal{S}$ |  在$t$年技能类型为$s$的**短期员工**人数  |
| $\text{overmanning}_{t,s}$           $t\in\mathcal{T}, s\in\mathcal{S}$ |  在$t$年技能类型为$s$的**超员员工**人数  |

##### 约束条件

1. 平衡性约束balance

   实际可用员工人数为前一年的员工数+招聘员工数+转岗员工数-解雇员工数
   $$
   \text{employed}_{t,s} =  (1-\text{veteran_attrition}_s)*\text{employed}_{t-1,s} + (1-\text{rookie_attrition}_s)*\text{recruited}_{t,s}+\sum_{s' \in \mathcal{S} | s' < s}{\{(1-\text{veteran_attrition})*\text{retrained}_{t,s',s} - \text{retrained}_{t,s,s'}\}} + \sum_{s' \in \mathcal{S} | s' > s}{\{(1-\text{demotion_attrition})*\text{retrained}_{t,s',s} - \text{retrained}_{t,s,s'}\}} - \text{redundant}_{t,s} \quad t\in\mathcal{T},s\in\mathcal{S}
   $$

2. 满足人力需求demand
   $$
   \text{demand}_{t,s} = \text{employed}_{t,s} - \text{overmanning}_{t,s} - \text{shorttime}_{t,s} * \text{prod_rate}, \quad  t\in\mathcal{T}, s\in\mathcal{S}
   $$

3. 训练转岗约束

   1. 转岗人员数的上限
      $$
      0\leq \text{retrained}_{t,s,s'}\leq \text{max_retrained}_{s,s'}    \quad   t\in\mathcal{T}, s,s'\in\mathcal{S}
      $$

   2. 不能跳级转岗，即跳级情况下$\text{retrained}_{t,s,s'}=0$

4. 超员员工人数有上限 bound 
   $$
   \sum_{s \in \mathcal{S}}{\text{overmanning}_{t,s}} \leq \text{max_overmanning} \quad \forall t \in \mathcal{T}
   $$

##### 目标函数

1. 极小化冗余人力
   $$
   \text{Minimize} \quad Z = \sum_{t \in \mathcal{T}}\sum_{s \in \mathcal{S}}{\text{redundant}_{t,s}}
   $$
   

2. 极小化用人成本: 转岗训练成本+短期员工成本+解雇员工成本+超员员工成本
   $$
   \text{Minimize} \quad W = \sum_{t \in\mathcal{T}}\sum_{s \in\mathcal{S}}\sum_{s' \in\mathcal{S}}{\{\text{ret_cost}_{s}*\text{retrained}_{t,s,s'}}\} + \sum_{t \in\mathcal{T}}\sum_{s \in\mathcal{S}}{\{\text{sh_cost}*\text{shorttime}_{t,s} + \text{red_cost}_s*\text{redundant}_{t,s} + \text{ove_cost}_s*\text{overmanning}_{t,s}\}}
   $$
   



