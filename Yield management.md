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

