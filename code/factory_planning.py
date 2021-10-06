from pyscipopt import Model, quicksum
import pandas as pd
import numpy as np

from data.factory_planning.data import data


class FactoryPlanning:
    def __init__(self, data):
        self.data = data
        self.model = Model()
        self.make = dict()
        self.store = dict()
        self.sell = dict()
        self.repair = dict()

    def preprocessing(self):
        months = self.data["months"]
        products = self.data["products"]
        machines = self.data["machines"]
        return months, products, machines

    def create_model(self, is_repair=False):
        months, products, machines = self.preprocessing()
        self.add_variables(months, products, is_repair)
        self.add_constraints(months, products, machines, is_repair)
        self.add_objective(months, products)
        self.model.optimize()
        self.print_results(months, products,is_repair)

    def add_variables(self, months, products, is_repair):
        max_inventory = self.data["max_inventory"]
        max_sales = self.data["max_sales"]
        for month in months:
            for product in products:
                self.make[(month, product)] = self.model.addVar()
                self.store[(month, product)] = self.model.addVar(ub=max_inventory)
                self.sell[(month, product)] = self.model.addVar(ub=max_sales[month, product])
        if is_repair:
            machines = self.data["machines"]
            down_req = self.data["down_req"]
            for month in months:
                for machine in machines:
                    self.repair[(month, machine)] = self.model.addVar(vtype="I",ub=down_req[machine])

    def add_constraints(self, months, products, machines, is_repair):
        self.add_initial_balance_constraints(months, products)
        self.add_balance_constraints(months, products)
        self.add_target_inventory_constraints(months, products)
        self.add_capacity_constraints(months, products, machines, is_repair)
        if is_repair:
            self.add_maintenance_constraints(months, machines)

    def add_initial_balance_constraints(self, months, products):
        for product in products:
            self.model.addCons(self.make[months[0], product] ==
                               self.sell[months[0], product] + self.store[months[0], product])

    def add_balance_constraints(self, months, products):
        for product in products:
            for month in months:
                if month != months[0]:
                    month_i = months[months.index(month) - 1]
                    self.model.addCons(self.store[month_i, product] + self.make[month, product] ==
                                       self.sell[month, product] + self.store[month, product])

    def add_target_inventory_constraints(self, months, products):
        store_target = self.data["store_target"]
        for product in products:
            self.model.addCons(self.store[months[-1], product] == store_target)

    def add_capacity_constraints(self, months, products, machines, is_repair):
        time_req = self.data["time_req"]
        hours_per_month = self.data["hours_per_month"]
        installed = self.data["installed"]
        down = self.data["down"]
        for machine in machines:
            for month in months:
                if is_repair:
                    self.model.addCons(
                        quicksum(self.make[month, product] * time_req[machine][product] for product in time_req[machine])
                        <= hours_per_month * (installed[machine] - self.repair[month, machine]))
                else:
                    self.model.addCons(
                        quicksum(
                            self.make[month, product] * time_req[machine][product] for product in time_req[machine])
                        <= hours_per_month * (installed[machine] - down.get((month, machine), 0)))

    def add_maintenance_constraints(self, months, machines):
        down_req = self.data["down_req"]
        for machine in machines:
            self.model.addCons(quicksum(self.repair[month, machine] for month in months) == down_req[machine])

    def add_objective(self, months, products):
        holding_cost = self.data["holding_cost"]
        profit = self.data["profit"]
        obj = quicksum(profit[product] * self.sell[month, product] - holding_cost * self.store[month, product]
                       for month in months for product in products)
        self.model.setObjective(obj, "maximize")

    def print_results(self, months, products,is_repair):
        rows = months.copy()
        columns = products.copy()
        make_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
        sell_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
        store_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
        for month in months:
            for product in products:
                make_val = self.model.getVal(self.make[month, product])
                sell_val = self.model.getVal(self.sell[month, product])
                store_val = self.model.getVal(self.store[month, product])
                if make_val > 0:
                    make_plan.loc[month, product] = np.round(make_val, 1)
                if sell_val > 0:
                    sell_plan.loc[month, product] = np.round(sell_val, 1)
                if store_val:
                    store_plan.loc[month, product] = np.round(store_val, 1)
        print(make_plan)
        print(sell_plan)
        print(store_plan)
        if is_repair:
            rows = months.copy()
            columns = self.data["machines"].copy()
            repair_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
            for month, machine in self.repair.keys():
                val = self.model.getVal(self.repair[month, machine])
                if abs(val) > 1e-6:
                    repair_plan.loc[month, machine] = val
            print(repair_plan)


if __name__ == '__main__':
    prob_data = data
    prob = FactoryPlanning(prob_data)
    prob.create_model(True)
