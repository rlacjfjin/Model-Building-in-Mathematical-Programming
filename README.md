# Model-Building-in-Mathematical-Programming
Model Building in Mathematical Programming Fifth Edition

### 说明

原计划用gurobi来写的，但因版权问题，无法使用gurobi，只能用开源的求解器scip；

花了很长时间，现在回想一看，感觉没啥意义；

### 任务清单(25个)

- [ ] Food manufacture
- [ ] Factory planning
- [ ] Manpower planning
- [ ] Refinery optimization
- [ ] Mining
- [ ] Farm planning
- [ ] Economic planning
- [ ] Decentralisation
- [ ] Curve fitting
- [ ] Logical design
- [ ] Market sharing
- [ ] Opencast mining
- [ ] Tariff rates (power generation)
- [ ] Hydro power
- [x] [Three-dimensional noughts and crosses](三维井字棋盘)
  - 书中第17题
  - 已完成，不是重点

- [ ] Optimizing a constraint
- [x] Distribution(Supply Network Design)

- [x] [Agricultural pricing](Agricultural pricing.md)
  - 书中第21题
  - 双线性目标函数
- [x] [Efficiency Analysis](Efficiency Analysis.md)
  - 书中第22题
- [x] [Milk Collection Problem](Milk Collection Problem.md)
  - 书中第23题

- [x] [Yield management](Yield management.md)
  - 书中第24题----结果与书上的不太一样

- [x] Car rental

  - 书中第25题、26题

  - 写的代码结果跟书上不太一致，后面继续修改

- [x] [Lost baggage distribution](Lost baggage distribution.md)
  - 书中第27题

- [ ] Protein folding
- [ ] Protein comparison



### 已完成列表

1. [Distribution(Supply Network Design)](供应链)
   - 资源配送问题(工厂-仓库-供应商，工厂-供应商)
   - 仓库可以扩张，也可以关闭，也可以新开
   - 相对来说模型简单，整数规划
   - [代码参考](code\distribution.py) 
   
2. [Agricultural pricing](Agricultural pricing.md)
   - 定价策略：确定价格和需求，收益最大化
   - 目标是双线性的，即 单价$\times$ 数量
   - [代码参考](code\agriculture_pricing.py) 
   
3. [Efficiency Analysis](Efficiency Analysis.md)
   - 数据包络分析 (DEA: data envelopment analysis ) 
   - 模型简单，主要是DEA方法的掌握
   
4. [Milk Collection Problem](Milk Collection Problem.md)
   - TSP的扩展：节点集合分每天要访问的节点和隔天要访问的节点
   - 求解难点：子环路约束
   - scip的lazy constraints方法
   
5. [Yield management](Yield management.md)
   - 定价策略：不同价格下的售卖情况不一样
   - 过了一段时间后可以得到真实的需求，按真实的需求不断改进未来的定价策略
   - 收益最大化
   - 双线性目标函数(可线性化，引入辅助变量)
   
6. Car rental

7. [Lost baggage distribution](Lost baggage distribution.md)
   - CVRP的扩展：限制最长行驶时间、最小化车辆使用数
   - 求解难点：子环路约束
   - scip的lazy constraints方法
   
8. [Food manufacture](Food manufacture)
   - 线性规划问题：给出采购和制造方案，实现利益最大化
   - 主要是库存管理：满足初始库存、库存的平衡、目标库存、保证可用量、质量守恒等等
   - 可扩展为0-1整数规划
   - 感觉零售行业比较常见
   
9. [Factory planning](Factory planning)
   - 线性规划问题：给定机器和要生产的产品以及产品的需求，每个机器可以生产的产品数量已知，机器在一定时间使用后需要维护，基于以上限制给出生产计划；
   - 与[Food manufacture](Food manufacture)类似，考虑库存因素
   - 可扩展为：给定维护计划表，0-1整数规划
   
10. [Manpower planning](Manpower planning)

    - 人力资源管理问题
    - 线性规划问题
    - 主要是考虑人员流失成本、转岗成本、招聘成本；

11. [Economic planning](Economic planning)
    - 线性规划问题
    - 根据各行业之间的相互关系，规划未来几年的各行业投入以及产出；
    - 规划时间内的模型是个动态模型，规划时间以后的是静态模型；
    - 值得参考其思路；
12. [Decentralisation](Decentralisation)
    - 公司部门迁移问题；
    - 考虑成本：1. 迁移节约成本  2. 迁移导致的沟通成本； 总成本最小
    - 双线性问题，scip可以处理
- 觉得难点是成本的量化，但是该问题已经给出了成本量化后的结果
  
13. Farm planning

14. Market sharing

15. [Mining](Mining)

    - 从多个矿山中选几个矿山运营；
    - 整数规划；

16. [Opencast mining](Opencast mining)

    - 不知道有什么意义，给定的profit都不知道怎么计算的
    - 单位模矩阵，整数规划变成线性规划；

17. [Power generation](Power generation)

    - 多种发电机选择要用的发电机 ；
    - 整数规划模型；
    - 扩展：添加水力发电厂，不同的约束；

18. Refinery optimization----暂时不做，跟工作没什么关系

19. Protein folding-----暂时不做

20. Protein comparison-----暂时不做

21. Three-dimensional noughts and crosses----已完成，没啥意义

22. Optimising a constraint-----简化约束，暂时觉得没啥意义

23. Curve fitting------没啥意义

24. Logical design-----没啥意义，暂时不做

    

#### 扩展

1. [Cell Tower Coverage](file:///D:/modeling-examples-master/cell_tower_coverage/cell_tower.html)
2. [colgen-cutting_stock](file:///D:/modeling-examples-master/colgen-cutting_stock/colgen-cutting_stock.html)
3. [covid19_facility_location](file:///D:/modeling-examples-master/covid19_facility_location/covid19_facility_location.html)-----选址问题
4. [customer_assignment](file:///D:/modeling-examples-master/customer_assignment/customer_assignment.html)----涉及聚类
5. [facility_location](file:///D:/modeling-examples-master/facility_location/facility_location.html)
6. [introduction_to_modeling](file:///D:/modeling-examples-master/intro_to_modeling/introduction_to_modeling.html)------可看可不看
7. [l0_regression](file:///D:/modeling-examples-master/linear_regression/l0_regression.html)------可看可不看
8. [marketing_campaign_optimization](file:///D:/modeling-examples-master/marketing_campaign_optimization/marketing_campaign_optimization.html)
9. [offshore_wind_farming](file:///D:/modeling-examples-master/offshore_wind_farming/offshore_wind_farming.html)
10. [std_pooling](file:///D:/modeling-examples-master/pooling/std_pooling.html)
11. [portfolio_selection_optimization](file:///D:/modeling-examples-master/portfolio_selection_optimization/portfolio_selection_optimization.html)
12. [technician_routing_scheduling](file:///D:/modeling-examples-master/technician_routing_scheduling/technician_routing_scheduling.html)
14. [workforce_scheduling](file:///D:/modeling-examples-master/workforce/workforce_scheduling.html)
