from pyscipopt import Model, quicksum
import pandas as pd

from data.economic_planning.data import data


class EconomicPlanning:
    def __init__(self, data):
        self.data = data
        self.model = Model()
        self.production = dict()
        self.stock = dict()
        self.extra_cap = dict()

    def preprocessing(self):
        industries = self.data["industries"]
        inout_prod = self.data["inout_prod"]
        demand = self.data["demand"]
        static = Model()
        static_prod = dict()
        for i in industries:
            static_prod[i] = static.addVar()
        for i in industries:
            static.addCons(static_prod[i] - quicksum(inout_prod[i, j] * static_prod[j] for j in industries)
                           == demand[i])
        static.setObjective(0)
        static.optimize()
        print("\n\n_________________________________________________________________________________")
        print(f"The production of goods by industry for the static model of the economy is:")
        print("_________________________________________________________________________________")
        static_solution = dict()
        for i in industries:
            val = static.getVal(static_prod[i])
            static_solution[i] = val
            if val > 0:
                dollars_static_prod = '${:,.2f}'.format(val)
                print(f"Generate {dollars_static_prod} million dollars of {i} ")
        return static_solution

    def create_model(self):
        industries = self.data["industries"]
        horizon = self.data["horizon"]
        static_solution = self.preprocessing()
        self.add_variables(industries, horizon)
        self.add_constraints(industries, horizon, static_solution)
        self.add_objective(industries, horizon)
        self.model.optimize()
        self.print_results(industries, horizon)

    def add_variables(self, industries, horizon):
        # capacity0 = self.data["capacity0"]
        for i in industries:
            for h in horizon:
                # ub = capacity0[i]
                # if h == 1:
                #     ub = 0
                self.production[i, h] = self.model.addVar()
                if h == 1:
                    self.model.chgVarUb(self.production[i, h], 0)
                # else:
                #     self.model.chgVarUb(self.production[i,h],ub)

                self.extra_cap[i, h] = self.model.addVar()
                self.stock[i, h] = self.model.addVar()
                if h < 3:
                    self.model.chgVarUb(self.extra_cap[i, h], 0)
                if h == 6:
                    self.model.chgVarUb(self.extra_cap[i, h], 0)

    def add_constraints(self, industries, horizon, static_prod):
        self.add_balance_constraints(industries, horizon)
        self.add_horizon_constraints(industries, static_prod)
        self.add_capacity_constraints(industries, horizon)

    def add_balance_constraints(self, industries, horizon):
        stock0 = self.data["stock0"]
        inout_prod = self.data["inout_prod"]
        inout_cap = self.data["inout_cap"]
        demand = self.data["demand"]
        for i in industries:
            for h in horizon:
                if h == 1:
                    self.model.addCons(
                        stock0[i] == quicksum(inout_prod[i, j] * self.production[j, 2] for j in industries)
                        + quicksum(inout_cap[i, j] * self.extra_cap[j, 3] for j in industries)
                        + self.stock[i, 1] + demand[i])
                elif h == 5:
                    self.model.addCons(self.production[i, 5] + self.stock[i, 4] ==
                                       quicksum(inout_prod[i, j] * self.production[j, 6] for j in industries)
                                       + demand[i] + self.stock[i, 5])
                elif h in [2, 3, 4]:
                    self.model.addCons(self.production[i, h] + self.stock[i, h - 1] ==
                                       quicksum(inout_prod[i, j] * self.production[j, h + 1] for j in industries)
                                       + quicksum(inout_cap[i, j] * self.extra_cap[j, h + 2] for j in industries)
                                       + demand[i] + self.stock[i, h])

    def add_horizon_constraints(self, industries, static_prod):
        for j in industries:
            self.model.addCons(self.production[j, 6] >= static_prod[j])

    def add_capacity_constraints(self, industries, horizon):
        capacity0 = self.data["capacity0"]
        for i in industries:
            for h in horizon:
                self.model.addCons(self.production[i, h] - quicksum(self.extra_cap[i, t] for t in horizon if t <= h)
                                   <= capacity0[i])

    def add_objective(self, industries, horizon):
        fiveYears = horizon[:5]
        labor_prod = self.data["labor_prod"]
        labor_extra_cap = self.data["labor_extra_cap"]
        obj_1 = quicksum(labor_prod[j] * self.production[j, t] for j in industries for t in fiveYears)
        obj_2 = quicksum(labor_extra_cap[j] * self.extra_cap[j, t] for j in industries for t in fiveYears)
        self.model.setObjective(obj_1 + obj_2, "maximize")

    def print_results(self, industries, horizon):
        print("_______________________________________________________________________________________________")
        print(f"The production of goods by industry and year for the dynamic Leontief model of the economy is:")
        print("_______________________________________________________________________________________________")
        fiveYears = horizon[:5]
        capacity0 = self.data["capacity0"]
        goods = {}
        totalCap = {}
        inv = {}
        for i in industries:
            production_list = []
            amount = capacity0[i]
            extra_cap_list = []
            inv_list = []
            for t in fiveYears:
                amount += self.model.getVal(self.extra_cap[i, t])
                val = self.model.getVal(self.production[i, t])
                production_list.append('${:,.2f}'.format(val))
                extra_cap_list.append(round(amount))
                inv_list.append('${:,.2f}'.format(self.model.getVal(self.stock[i, t])))
            inv[i] = inv_list
            goods[i] = production_list
            totalCap[i] = extra_cap_list
        goods_production = pd.DataFrame(goods, index=["Year1", "Year2", "Year3", "Year4", "Year5"])
        extra_capacity = pd.DataFrame(totalCap, index=["Year1", "Year2", "Year3", "Year4", "Year5"])
        stock_level = pd.DataFrame(inv, index=["Year1", "Year2", "Year3", "Year4", "Year5"])
        print(goods_production)
        print("_______________________________________________________________________________________________")
        print(f"The productive capacity by industry and year for the dynamic Leontief model of the economy is:")
        print("_______________________________________________________________________________________________")
        print(extra_capacity)
        print("____________________________________________________________________________________")
        print(f"Stock level by industry at the end of year for the dynamic Leontif model of the economy is:")
        print("____________________________________________________________________________________")
        print(stock_level)


if __name__ == '__main__':
    prob_data = data
    prob = EconomicPlanning(prob_data)
    prob.create_model()
