### Power generation

#### 问题描述

发电机有三种不同类型，每种类型有不同的特性(如功率输出、每兆瓦时成本、启动成本等)；

设备可以开启或关闭，启动成本与从关闭到开启的转换相关；

当设备打开时，功率输出可以落在指定的最小值和最大值之间的任何位置；

一天分为5个时间段，每个时间段都有一个预期的总电力需求；

预计需求如下：

| Time Period | Demand (megawatts) |
| --- | --- |
| 12 pm to 6 am | 15000 |
| 6 am to 9 am | 30000 |
| 9 am to 3 pm | 25000 |
| 3 pm to 6 pm | 40000 |
| 6 pm to 12 pm | 27000 |

发电机分为三种类型，每种类型的最小和最大输出如下（当它们打开时）：

| Type | Number available | Minimum output (MW) | Maximum output (MW) |
| --- | --- | --- | --- |
| 0 | 12 |  850 | 2000 |
| 1 | 10 | 1250 | 1750 |
| 2 | 5 | 1500 | 4000 |

使用成本如下：

| Type | Cost per hour (when on) | Cost per MWh above minimum | Startup cost |
| --- | --- | --- | --- |
| 0 | $\$1000$ | $\$2.00$ | $\$2000$ |
| 1 | $\$2600$ | $\$1.30$ | $\$1000$ |
| 2 | $\$3000$ | $\$3.00$ | $\$500$ |

发电机必须满足预测需求，同时也必须有足够的储备能力，以应对实际需求超过预测需求的情况；

对于此模型，所选发电机组必须能够产生多达 115% 的预测需求；

给出发电机的使用方案；



####  解决方案

##### 定义集合

| 集合                   | 含义           |
| ---------------------- | :------------- |
| $t \in \text{Types}$   | 发电机种类集合 |
| $p \in \text{Periods}$ | 时间段集合     |

##### 参数

| 符号                                     | 含义                         |
| ---------------------------------------- | ---------------------------- |
| $\text{period_hours}_p \in \mathbb{N}^+$ | 每个时间段的时间             |
| $\text{generators}_t \in \mathbb{N}^+$   | 每一种发电机的数量           |
| $\text{demand}_p \in \mathbb{R}^+$       | 时间段的需求电力             |
| $\text{start0} \in \mathbb{N}^+$         | 时间段开始时可用的发动机数量 |
| $\text{min_output}_t \in \mathbb{R}^+$   | 发动机的最小输出             |
| $\text{max_output}_t \in \mathbb{R}^+$   | 发动机的最大输出             |
| $\text{base_cost}_t \in \mathbb{R}^+$    | 发动机基本运行成本           |
| $\text{per_mw_cost}_t \in \mathbb{R}^+$: | 额外的成本                   |
| $\text{startup_cost}_t \in \mathbb{R}^+$ | 启动成本                     |

##### 定义变量

| 变量                                   | 含义                       |
| -------------------------------------- | -------------------------- |
| $\text{ngen}_{t,p} \in \mathbb{N}^+$   | 使用的发动机数量           |
| $\text{output}_{t,p} \in \mathbb{R}^+$ | 总输出电力                 |
| $\text{nstart}_{t,p} \in \mathbb{N}^+$ | 时间段开始阶段的发电机数量 |

##### 目标函数

$$
\begin{equation}
\text{Minimize} \quad Z_{on} + Z_{extra} + Z_{startup}
\end{equation}
$$

$$
\begin{equation}
Z_{on} = \sum_{(t,p) \in \text{Types} \times \text{Periods}}{\text{base_cost}_t*\text{ngen}_{t,p}}
\end{equation}
$$

$$
\begin{equation}
Z_{extra} = \sum_{(t,p) \in \text{Types} \times \text{Periods}}{\text{per_mw_cost}_t*(\text{output}_{t,p} - \text{min_load}_t})
\end{equation}
$$

$$
\begin{equation}
Z_{startup} = \sum_{(t,p) \in \text{Types} \times \text{Periods}}{\text{startup_cost}_t*\text{nstart}_{t,p}}
\end{equation}
$$




##### 约束条件

1. **Available generators**
   $$
   \begin{equation}
   \text{ngen}_{t,p} \leq \text{generators}_{t} \quad \forall (t,p) \in \text{Types} \times \text{Periods}
   \end{equation}
   $$

2. **Demand**
   $$
   \begin{equation}
   \sum_{t \in \text{Types}}{\text{output}_{t,p}} \geq \text{demand}_p \quad \forall p \in \text{Periods}
   \end{equation}
   $$

3. **Min/max generation**
   $$
   \begin{equation}
   \text{output}_{t,p} \geq \text{min_output}_t*\text{ngen}_{t,p} \quad \forall (t,p) \in \text{Types} \times \text{Periods}
   \end{equation}
   $$

   $$
   \begin{equation}
   \text{output}_{t,p} \leq \text{max_output}_t*\text{ngen}_{t,p} \quad \forall (t,p) \in \text{Types} \times \text{Periods}
   \end{equation}
   $$

   

4. **Reserve**
   $$
   \begin{equation}
   \sum_{t \in \text{Types}}{\text{max_output}_t*\text{ngen}_{t,p}} \geq 1.15 * \text{demand}_p \quad \forall p \in \text{Periods}
   \end{equation}
   $$

5. **Startup**
   $$
   \begin{equation}
   \text{ngen}_{t,p} \leq \text{ngen}_{t,p-1} + \text{startup}_{t,p} \quad \forall (t,p) \in \text{Types} \times \text{Periods}
   \end{equation}
   $$

#### 扩展

添加水力发电厂；

相应的参数表如下：

| Hydro plant | Output (MW) |
| --- | --- |
| A | 900 |
| B | 1400 |

| Hydro plant | Cost per hour (when on) | Startup cost | Reservoir depth reduction (m/hr) |
| --- | --- | --- | --- |
| A | $\$90$ | $\$1500$ | 0.31 |
| B | $\$150$ | $\$1200$ | 0.47 |



相应的修改原模型：

 1. 添加集合

    $h \in \text{HydroUnits}=\{0,1\}$: Two hydro generators.

	2. 添加参数

    $\text{hydro_load}_h \in \mathbb{R}^+$: Output for hydro generator $h$.

    $\text{hydro_cost}_h \in \mathbb{R}^+$: Cost for operating hydro generator $h$.

    $\text{hydro_startup_cost}_h \in \mathbb{R}^+$: Startup cost for hydro generator $h$.

    $\text{hydro_height_reduction}_h \in \mathbb{R}^+$: Hourly reduction in reservoir height from operating hydro generator $h$.

	3. 添加变量

    $\text{hydro}_{h,p} \in [0,1]$: Indicates whether hydro generators $h$ is on in time period $p$.

    $\text{hydro_start}_{h,p} \in [0,1]$: Indicates whether hydro generator $h$ starts in time period $p$.

    $\text{height}_{p} \in \mathbb{R}^+$: Height of reservoir in time period $p$.

    $\text{pumping}_{p} \in \mathbb{R}^+$: Power used to replenish reservoir in time period $p$.

	4. 目标函数

    原目标函数+$Z_{hydro} + Z_{hydro\_startup}$，其中
    $$
    \begin{equation}
    Z_{hydro} = \sum_{(h,p) \in \text{HydroUnits} \times \text{Periods}}{\text{hydro_cost}_h*\text{hydro}_{h,p}}
    \end{equation}
    $$

    $$
    \begin{equation}
    Z_{hydro\_startup} = \sum_{(h,p) \in \text{HydroUnits} \times \text{Periods}}{\text{hydro_startup_cost}_h*\text{hydro_start}_{h,p}}
    \end{equation}
    $$

	5. 约束条件

    demand约束修改为：
    $$
    \begin{equation}
    \sum_{t \in \text{Types}}{\text{output}_{t,p}} +
    \sum_{h \in \text{HydroUnits}}{\text{hydro_load}_h*\text{hydro}_{h,p}} \geq
    \text{demand}_p + \text{pumping}_p \quad \forall p \in \text{Periods}
    \end{equation}
    $$
    **Reserve**约束修改为：
    $$
    \begin{equation}
    \sum_{t \in \text{Types}}{\text{max_output}_t*\text{ngen}_{t,p}} +
    \sum_{h \in \text{HydroUnits}}{\text{hydro_load}_h} \geq 1.15 * \text{demand}_p \quad \forall p \in \text{Periods}
    \end{equation}
    $$
     添加**Hydro startup**约束：
    $$
    \begin{equation}
    \text{hydro}_{h,p} \leq \text{hydro}_{h,p-1} + \text{hydro_start}_{h,p} \quad \forall (h,p) \in \text{HydroUnits} \times \text{Periods}
    \end{equation}
    $$
    添加**Reservoir height**约束：
    $$
    \begin{equation}
    \text{height}_{p} = \text{height}_{p-1}  + \text{period_hours}_{p}*\text{pumping}_{p}/3000 -
    \sum_{h \in \text{HydroUnits}}{\text{period_hours}_{p}*\text{hydro_height_reduction}_{h}*\text{hydro}_{h,p}} \quad \forall p \in \text{Periods}
    \end{equation}
    $$

    $$
    \begin{equation}
    \text{height}_{pfirst} = \text{height}_{plast}  + \text{period_hours}_{pfirst}*\text{pumping}_{pfirst}/3000 -
    \sum_{h \in \text{HydroUnits}}{\text{period_hours}_{pfirst}*\text{hydro_height_reduction}_{h}*\text{hydro}_{h,pfirst}}
    \end{equation}
    $$

    

