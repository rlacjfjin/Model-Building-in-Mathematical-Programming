from pyscipopt import Model, quicksum

from data.yield_management.data import data


class YieldManagement:
    def __init__(self, prob_data):
        self.data = prob_data
        self.model = Model()
        self.p1 = dict()
        self.p2 = dict()
        self.p3 = dict()
        self.s1 = dict()
        self.s2 = dict()
        self.s3 = dict()
        self.r1 = dict()
        self.r2 = dict()
        self.r3 = dict()
        self.u = dict()
        self.v = dict()
        self.n = None
        self.opt_prices = dict()

    def preprocessing(self):
        classes = self.data["classes"]
        options = self.data["options"]
        scenarios = self.data["scenarios"]
        prices = dict()
        prices[0] = self.data["price_1"]
        prices[1] = self.data["price_2"]
        prices[2] = self.data["price_3"]
        demands = dict()
        demands[0] = self.data["demand_pred_1"]
        demands[1] = self.data["demand_pred_2"]
        demands[2] = self.data["demand_pred_3"]

        cap = data["cap"]
        cost = data["cost"]
        return classes, options, scenarios, prices, demands, cap, cost

    def create_model(self, period=1):
        assert 1 <= period <= 4
        classes, options, scenarios, prices, demands, cap, cost = self.preprocessing()
        if period > 1:
            for i in scenarios:
                for c in classes:
                    for h in options:
                        demands[0][i, c, h] = 0
                        demands[0][i, c, h] = self.data["demand_actual_1"][c, h] * self.opt_prices[0][c, h]
        if period > 2:
            for j in scenarios:
                for c in classes:
                    for h in options:
                        demands[1][j, c, h] = 0
                        demands[1][j, c, h] = self.data["demand_actual_2"][c, h] * self.opt_prices[1][j, c, h]
        if period > 3:
            opt_p3kch = {}
            for i in scenarios:
                for j in scenarios:
                    for c in classes:
                        for h in options:
                            opt_p3kch[j, c, h] = 0
                            if self.opt_prices[2][i, j, c, h] == 1:
                                opt_p3kch[j, c, h] = self.opt_prices[2][i, j, c, h]
            for k in scenarios:
                for c in classes:
                    for h in options:
                        demands[2][k, c, h] = 0
                        demands[2][k, c, h] = self.data["demand_actual_3"][c, h] * opt_p3kch[k, c, h]

        self.add_variables(classes, options, scenarios, period)
        self.add_objective(classes, options, scenarios, cost)
        self.add_constraints(classes, options, scenarios, prices, demands, cap)
        self.model.hideOutput()
        self.model.optimize()
        self.get_solution(classes, options, scenarios, prices, period)
        if period == 4:
            self.print_result(classes, options, scenarios, prices)
        self.model.freeTransform()

    def add_variables(self, classes, options, scenarios, period):
        self.add_price_variables(classes, options, scenarios, period)
        self.add_sell_variables(classes, options, scenarios)
        self.add_revenue_variables(classes, options, scenarios)
        self.add_capacity_variables(classes, scenarios)

    def add_price_variables(self, classes, options, scenarios, period):
        for c in classes:
            for h in options:
                lb = 0
                if period > 1:
                    lb = self.opt_prices[0][(c, h)]
                self.p1[(c, h)] = self.model.addVar(vtype="B", lb=lb, name="price_1(%s,%s)" % (c, h))
                for i in scenarios:
                    lb = 0
                    if period > 2:
                        lb = self.opt_prices[1][(i, c, h)]
                    self.p2[(i, c, h)] = self.model.addVar(vtype="B", lb=lb, name="price_2(%s,%s,%s)" % (i, c, h))
                    for j in scenarios:
                        lb = 0
                        if period > 3:
                            lb = self.opt_prices[2][(i, j, c, h)]
                        self.p3[(i, j, c, h)] = self.model.addVar(vtype="B", lb=lb,
                                                                  name="price_3(%s,%s,%s,%s)" % (i, j, c, h))

    def add_sell_variables(self, classes, options, scenarios):
        for c in classes:
            for h in options:
                for i in scenarios:
                    self.s1[(i, c, h)] = self.model.addVar(vtype="I", name="sold_1(%s,%s,%s)" % (i, c, h))
                    for j in scenarios:
                        self.s2[(i, j, c, h)] = self.model.addVar(vtype="I", name="sold_2(%s,%s,%s,%s)" % (i, j, c, h))
                        for k in scenarios:
                            self.s3[(i, j, k, c, h)] = self.model.addVar(vtype="I",
                                                                         name="sold_3(%s,%s,%s,%s,%s)" % (
                                                                             i, j, k, c, h))

    def add_revenue_variables(self, classes, options, scenarios):
        for c in classes:
            for h in options:
                for i in scenarios:
                    self.r1[(i, c, h)] = self.model.addVar(vtype="C", name="revenue_1(%s,%s,%s)" % (i, c, h))
                    for j in scenarios:
                        self.r2[(i, j, c, h)] = self.model.addVar(vtype="C",
                                                                  name="revenue_1(%s,%s,%s,%s)" % (i, j, c, h))
                        for k in scenarios:
                            self.r3[(i, j, k, c, h)] = self.model.addVar(vtype="C",
                                                                         name="revenue_1(%s,%s,%s,%s,%s)" % (
                                                                             i, j, k, c, h))

    def add_capacity_variables(self, classes, scenarios):
        for c in classes:
            for i in scenarios:
                for j in scenarios:
                    for k in scenarios:
                        self.u[(i, j, k, c)] = self.model.addVar(vtype="I", name="slack(%s,%s,%s,%s)" % (i, j, k, c))
                        self.v[(i, j, k, c)] = self.model.addVar(vtype="I", name="exceed(%s,%s,%s,%s)" % (i, j, k, c))
        self.n = self.model.addVar(ub=6, vtype="I", name="planes")

    def add_constraints(self, classes, options, scenarios, prices, demands, cap):
        self.add_price_options_constraints(classes, options, scenarios)
        self.add_sales_constraints(classes, options, scenarios, demands)
        self.add_capacity_constraints(classes, options, scenarios, cap)
        self.add_adjustment_constraints(classes, scenarios, cap)
        self.add_not_exceed_estimated_constraints(classes, options, scenarios, prices, demands)

    def add_price_options_constraints(self, classes, options, scenarios):
        for c in classes:
            self.model.addCons(quicksum(self.p1[(c, h)] for h in options) == 1)
            for i in scenarios:
                self.model.addCons(quicksum(self.p2[(i, c, h)] for h in options) == 1)
                for j in scenarios:
                    self.model.addCons(quicksum(self.p3[(i, j, c, h)] for h in options) == 1)

    def add_sales_constraints(self, classes, options, scenarios,
                              demands):  # demand_pred={demand_pred1,demand_pred2,..}
        for c in classes:
            for h in options:
                for i in scenarios:
                    self.model.addCons(self.s1[(i, c, h)] <= demands[0][(i, c, h)] * self.p1[(c, h)])
                    for j in scenarios:
                        self.model.addCons(self.s2[(i, j, c, h)] <= demands[1][(j, c, h)] * self.p2[(i, c, h)])
                        for k in scenarios:
                            self.model.addCons(
                                self.s3[(i, j, k, c, h)] <= demands[2][(k, c, h)] * self.p3[(i, j, c, h)])

    def add_capacity_constraints(self, classes, options, scenarios, cap):
        # cap = self.data["cap"]
        for c in classes:
            for i in scenarios:
                for j in scenarios:
                    for k in scenarios:
                        self.model.addCons(quicksum(self.s1[(i, c, h)] for h in options) +
                                           quicksum(self.s2[(i, j, c, h)] for h in options) +
                                           quicksum(self.s3[(i, j, k, c, h)] for h in options) +
                                           self.u[(i, j, k, c)] - self.v[(i, j, k, c)] - cap[c] * self.n <= 0)

    def add_adjustment_constraints(self, classes, scenarios, cap):
        for i in scenarios:
            for j in scenarios:
                for k in scenarios:
                    self.model.addCons(quicksum(self.u[(i, j, k, c)] for c in classes) ==
                                       quicksum(self.v[(i, j, k, c)] for c in classes))
                    for c in classes:
                        self.model.addCons(self.u[(i, j, k, c)] <= 0.1 * cap[c])
                        self.model.addCons(self.v[(i, j, k, c)] <= 0.1 * cap[c])

    def add_not_exceed_estimated_constraints(self, classes, options, scenarios, prices, demands):
        # If a particular price option is chosen (under certain scenarios), then the sales
        # cannot exceed the estimated demand and the revenue must be the product of the
        # price and sales.
        for c in classes:
            for h in options:
                for i in scenarios:
                    revenue = demands[0][(i, c, h)] * prices[0][(c, h)]
                    self.model.addCons(self.r1[(i, c, h)] <= self.s1[(i, c, h)] * prices[0][(c, h)])
                    self.model.addCons(
                        self.s1[(i, c, h)] * prices[0][(c, h)] - self.r1[(i, c, h)] + self.p1[
                            (c, h)] * revenue <= revenue)
                    for j in scenarios:
                        revenue = demands[1][(j, c, h)] * prices[1][(c, h)]
                        self.model.addCons(self.r2[(i, j, c, h)] <= self.s2[(i, j, c, h)] * prices[1][(c, h)])
                        self.model.addCons(
                            self.s2[(i, j, c, h)] * prices[1][(c, h)] - self.r2[(i, j, c, h)] + self.p2[
                                (i, c, h)] * revenue <= revenue)
                        for k in scenarios:
                            revenue = demands[2][(k, c, h)] * prices[2][(c, h)]
                            self.model.addCons(self.r3[(i, j, k, c, h)] <= self.s3[(i, j, k, c, h)] * prices[2][(c, h)])
                            self.model.addCons(
                                self.s3[(i, j, k, c, h)] * prices[2][(c, h)] - self.r3[(i, j, k, c, h)] + self.p3[
                                    (i, j, c, h)] * revenue <= revenue)

    def add_objective(self, classes, options, scenarios, cost):
        p = self.data["probability"]
        obj_1 = quicksum(p[i] * self.r1[(i, c, h)] for i in scenarios for c in classes for h in options)
        obj_2 = quicksum(p[i] * p[j] * self.r2[(i, j, c, h)] for i in scenarios
                         for j in scenarios for c in classes for h in options)
        obj_3 = quicksum(p[i] * p[j] * p[k] * self.r3[(i, j, k, c, h)] for i in scenarios for j in scenarios
                         for k in scenarios for c in classes for h in options)
        self.model.setObjective(obj_1 + obj_2 + obj_3 - cost * self.n, "maximize")

    def get_solution(self, classes, options, scenarios, prices, period):
        if period == 1:
            print("\n\n\n____________________Week 1 solution___________________________")

            print(f"The expected total profit is: £{round(self.model.getObjVal(), 2): ,}")
            print(f"Number of planes to book: {self.model.getVal(self.n)}")

            print("\n____________________Week 1 prices_______________________________")
            opt_prices_1 = dict()
            for c in classes:
                for h in options:
                    opt_prices_1[(c, h)] = 0
                    val = self.model.getVal(self.p1[c, h])
                    if val > 0.5:
                        opt_prices_1[(c, h)] = round(val)
                        price_ch = opt_prices_1[(c, h)] * prices[0][c, h]
                        print(f"({c},{h}) = £{price_ch: ,}")
            self.opt_prices[0] = opt_prices_1
            # print("\n_____________Week 2 provisional prices____________________________")
            # for i in scenarios:
            #     for c in classes:
            #         for h in options:
            #             val = self.model.getVal(self.p2[i, c, h])
            #             if val > 0.5:
            #                 price_ch = round(val) * prices[1][c, h]
            #                 print(f"({i}, {c}, {h}) = £{price_ch: ,}")

        elif period == 2:
            print("\n\n\n____________________Week 2 solution___________________________")
            print(f"The expected total profit at the beginning of week 2 is: £ {round(self.model.getObjVal(), 2): ,}")
            print(f"Number of planes to book: {self.model.getVal(self.n)}")
            # Week 2 prices
            # optimal values of option prices at week 1
            opt_prices_2 = dict()
            print("\n_____________Week 2 prices____________________________")
            for i in scenarios:
                for c in classes:
                    for h in options:
                        opt_prices_2[(i, c, h)] = 0
                        val = self.model.getVal(self.p2[(i, c, h)])
                        if val > 0.5:
                            opt_prices_2[i, c, h] = round(val)
                            price_ch = opt_prices_2[i, c, h] * prices[1][c, h]
                            if i == 'sce1':
                                print(f"({c},{h}) = £{price_ch: ,}")
            self.opt_prices[1] = opt_prices_2

        # # Week 3 provisional prices
        # print("\n_____________Week 3 provisional prices____________________________")
        # for i in scenarios:
        #     for j in scenarios:
        #         for c in classes:
        #             for h in options:
        #                 val = self.model.getVal(self.p3[i, j, c, h])
        #                 if val > 0.5:
        #                     price_ch = round(val) * prices[2][c, h]
        #                     print(f"({i}, {j}, {c}, {h}) = £{price_ch: ,}")
        elif period == 3:
            print("\n\n\n____________________Week 3 solution___________________________")
            print(f"The expected total profit is: £ {round(self.model.getObjVal(), 2): ,}")
            print(f"Number of planes to book: {self.model.getVal(self.n)}")
            # Week 3  prices
            # optimal values of option prices at week 3
            opt_prices_3 = dict()
            print("\n_____________Week 3 prices____________________________")
            for i in scenarios:
                for j in scenarios:
                    for c in classes:
                        for h in options:
                            val = self.model.getVal(self.p3[i, j, c, h])
                            opt_prices_3[(i, j, c, h)] = 0
                            if val > 0.5:
                                opt_prices_3[(i, j, c, h)] = round(val)
                                price_ch = opt_prices_3[(i, j, c, h)] * prices[2][(c, h)]
                                if i == 'sce1' and j == 'sce1':
                                    print(f"({c}, {h}) = £{price_ch: ,}")
            self.opt_prices[2] = opt_prices_3

    def print_result(self, classes, options, scenarios, prices):
        print("\n\n\n____________________Take off solution___________________________")

        print(f"The actual total profit is: £{round(self.model.getObjVal(), 2): ,}")
        print(f"Number of planes used: {self.model.getVal(self.n)}")
        # Sales week 1
        print("\n___________Week 1 seats sold and revenue__________________________")
        for i in scenarios:
            if i == 'sce1':
                for c in classes:
                    for h in options:
                        val = self.model.getVal(self.s1[i, c, h])
                        if val > 0:
                            tickets = round(val)
                            price = prices[0][c, h] * round(self.model.getVal(self.p1[(c, h)]))
                            revenue = price * tickets
                            print(f"{c} class: {tickets} seats sold at £{price:,}: revenue £{revenue:,}  ")

        # Sales week 2
        print("___________Period 2 seats sold and revenue__________________________")
        for i in scenarios:
            for j in scenarios:
                if i == 'sce1' and j == 'sce1':
                    for c in classes:
                        for h in options:
                            val = self.model.getVal(self.s2[i, j, c, h])
                            if val > 0:
                                tickets = round(val)
                                price = prices[1][c, h] * round(self.model.getVal(self.p2[(i, c, h)]))
                                revenue = price * tickets
                                print(f"{c} class: {tickets} seats sold at £{price:,}: revenue £{revenue:,}  ")
        # Sales week 3
        print("___________Period 3 seats sold and revenue__________________________")
        for i in scenarios:
            for j in scenarios:
                for k in scenarios:
                    if i == 'sce1' and j == 'sce1' and k == 'sce1':
                        for c in classes:
                            for h in options:
                                val = self.model.getVal(self.s3[i, j, k, c, h])
                                if val > 0:
                                    tickets = round(val)
                                    price = prices[2][c, h] * round(self.model.getVal(self.p3[(i, j, c, h)]))
                                    revenue = price * tickets
                                    print(f"{c} class: {tickets} seats sold at £{price:,}: revenue £{revenue:,}  ")


if __name__ == '__main__':
    yield_data = data
    prob = YieldManagement(yield_data)
    prob.create_model()
    prob.create_model(period=2)
    prob.create_model(period=3)
    prob.create_model(period=4)
