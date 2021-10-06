from pyscipopt import Model, quicksum
import pandas as pd
import numpy as np
from data.food_manufacture.data import data


class FoodManufacture:
    def __init__(self, data):
        self.data = data
        self.model = Model()
        self.produce = dict()
        self.buy = dict()
        self.consume = dict()
        self.store = dict()
        self.use = dict()

    def preprocessing(self):
        pass

    def create_model(self, is_extend=False):
        months = self.data["months"]
        oils = self.data["oils"]
        self.add_variables(months, oils, is_extend)
        self.add_objective(months, oils)
        self.add_constraints(months, oils,is_extend)
        self.model.optimize()
        self.print_result(months, oils)

    def add_variables(self, months, oils, is_extend):
        self.add_produced_quantity_variables(months)
        self.add_bought_quantity_variables(months, oils)
        self.add_consume_quantity_variables(months, oils)
        self.add_store_quantity_variables(months, oils)
        if is_extend:
            self.add_use_variables(months, oils)

    def add_produced_quantity_variables(self, months):
        for month in months:
            self.produce[month] = self.model.addVar()

    def add_bought_quantity_variables(self, months, oils):
        for month in months:
            for oil in oils:
                self.buy[(month, oil)] = self.model.addVar()

    def add_consume_quantity_variables(self, months, oils):
        for month in months:
            for oil in oils:
                self.consume[(month, oil)] = self.model.addVar()

    def add_store_quantity_variables(self, months, oils):
        for month in months:
            for oil in oils:
                self.store[(month, oil)] = self.model.addVar()

    def add_use_variables(self, months, oils):
        for month in months:
            for oil in oils:
                self.use[(month, oil)] = self.model.addVar(vtype="B")

    def add_constraints(self, months, oils,is_extend):
        self.add_initial_balance_constraints(months, oils)
        self.add_balance_constraints(months, oils)
        self.add_target_inventory_constraints(months, oils)
        self.add_capacity_constraints(months, oils)
        self.add_hardness_constraints(months, oils)
        self.add_mass_constraints(months,oils)
        if is_extend:
            self.add_consumption_range_constraints(months,oils)

    def add_initial_balance_constraints(self, months, oils):
        init_store = self.data["init_store"]
        for oil in oils:
            self.model.addCons(init_store + self.buy[months[0], oil] ==
                               self.consume[months[0], oil] + self.store[months[0], oil])

    def add_balance_constraints(self, months, oils):
        for oil in oils:
            for month in months:
                if month != month[0]:
                    self.model.addCons(self.store[months[months.index(month) - 1], oil] + self.buy[month, oil]
                                       == self.consume[month, oil] + self.store[month, oil])

    def add_target_inventory_constraints(self, months, oils):
        target_store = self.data["target_store"]
        for oil in oils:
            self.model.addCons(self.store[months[-1], oil] == target_store)

    def add_capacity_constraints(self, months, oils):
        veg_cap = self.data["veg_cap"]
        oil_cap = self.data["oil_cap"]
        for month in months:
            self.model.addCons(quicksum(self.consume[month, oil] for oil in oils if "VEG" in oil)
                               <= veg_cap)
            self.model.addCons(quicksum(self.consume[month, oil] for oil in oils if "OIL" in oil)
                               <= oil_cap)

    def add_hardness_constraints(self, months, oils):
        hardness = self.data["hardness"]
        min_hardness = self.data["min_hardness"]
        max_hardness = self.data["max_hardness"]
        for month in months:
            self.model.addCons(quicksum(hardness[oil] * self.consume[month, oil] for oil in oils)
                               >= min_hardness * self.produce[month])
            self.model.addCons(quicksum(hardness[oil] * self.consume[month, oil] for oil in oils)
                               <= max_hardness * self.produce[month])

    def add_mass_constraints(self, months,oils):
        for month in months:
            self.model.addCons(quicksum(self.consume[month,oil] for oil in oils) == self.produce[month])

    def add_consumption_range_constraints(self,months,oils):
        min_consume = self.data["min_consume"]
        veg_cap = self.data["veg_cap"]
        oil_cap = self.data["oil_cap"]
        max_ingredients = self.data["max_ingredients"]
        for month in months:
            for oil in oils:
                self.model.addCons(min_consume*self.use[month,oil] <= self.consume[month,oil])
                if "VEG" in oil:
                    self.model.addCons(self.consume[month, oil] <= veg_cap*self.use[month,oil])
                else:
                    self.model.addCons(self.consume[month, oil] <= oil_cap*self.use[month,oil])

        for month in months:
            self.model.addCons(quicksum(self.use[month,oil] for oil in oils) <= max_ingredients)
            self.model.addCons(self.use[month,"VEG1"] <= self.use[month,"OIL3"])
            self.model.addCons(self.use[month,"VEG2"] <= self.use[month,"OIL3"])

    def add_objective(self, months, oils):
        price = self.data["price"]
        cost = self.data["cost"]
        holding_cost = self.data["holding_cost"]
        obj_1 = quicksum(price * self.produce[month] for month in months)
        obj_2 = quicksum(cost[(month, oil)] * self.buy[(month, oil)] for month in months for oil in oils)
        obj_3 = quicksum(holding_cost * self.store[(month, oil)] for month in months for oil in oils)
        self.model.setObjective(obj_1 - obj_2 - obj_3,"maximize")

    def print_result(self,months,oils):
        rows = months.copy()
        columns = oils.copy()
        purchase_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

        for month, oil in self.buy.keys():
            val = self.model.getVal(self.buy[month,oil])
            if abs(val) > 1e-6:
                purchase_plan.loc[month, oil] = np.round(val, 1)
        print(purchase_plan)

        reqs = pd.DataFrame(columns=columns, index=rows, data=0.0)
        for month, oil in self.consume.keys():
            val = self.model.getVal(self.consume[(month,oil)])
            if abs(val) > 1e-6:
                reqs.loc[month, oil] = np.round(val, 1)
        print(reqs)
        store_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

        for month, oil in self.store.keys():
            val = self.model.getVal(self.store[(month,oil)])
            if abs(val) > 1e-6:
                store_plan.loc[month, oil] = np.round(val, 1)
        print(store_plan)


if __name__ == '__main__':
    prob_data = data
    prob = FoodManufacture(prob_data)
    prob.create_model(True)