from pyscipopt import Model, quicksum

from data.mining.data import data
import pandas as pd
import numpy as np

class Mining:
    def __init__(self, data):
        self.data = data
        self.model = Model()
        self.blend = dict()
        self.extract = dict()
        self.working = dict()
        self.available = dict()

    def preprocessing(self):
        pass

    def create_model(self):
        years = self.data["years"]
        mines = self.data["mines"]
        self.add_variables(years, mines)
        self.add_constraints(years, mines)
        self.add_objective(years, mines)
        self.model.optimize()
        self.print_results(years,mines)

    def add_variables(self, years, mines):
        for year in years:
            self.blend[year] = self.model.addVar()
            for mine in mines:
                self.extract[year, mine] = self.model.addVar()
                self.working[year, mine] = self.model.addVar(vtype="B")
                self.available[year, mine] = self.model.addVar(vtype="B")

    def add_constraints(self, years, mines):
        self.add_operating_mines_constraints(years, mines)
        self.add_quality_constraints(years, mines)
        self.add_mass_conservation_constraints(years, mines)
        self.add_capacity_constraints(years, mines)
        self.add_open_to_operate_constraints(years, mines)
        self.add_shut_down_constraints(years, mines)

    def add_operating_mines_constraints(self, years, mines):
        max_mines = self.data["max_mines"]
        for year in years:
            self.model.addCons(quicksum(self.working[year, mine] for mine in mines)
                               <= max_mines)

    def add_quality_constraints(self, years, mines):
        quality = self.data["quality"]
        target = self.data["target"]
        for year in years:
            self.model.addCons(quicksum(quality[mine] * self.extract[year, mine] for mine in mines)
                               == target[year] * self.blend[year])

    def add_mass_conservation_constraints(self, years, mines):
        for year in years:
            self.model.addCons(quicksum(self.extract[year, mine] for mine in mines)
                               == self.blend[year])

    def add_capacity_constraints(self, years, mines):
        capacity = self.data["capacity"]
        for year in years:
            for mine in mines:
                self.model.addCons(self.extract[year, mine] <= capacity[mine] * self.working[year, mine])

    def add_open_to_operate_constraints(self, years, mines):
        for year in years:
            for mine in mines:
                self.model.addCons(self.working[year, mine] <= self.available[year, mine])

    def add_shut_down_constraints(self, years, mines):
        for year in years:
            for mine in mines:
                if year < years[-1]:
                    self.model.addCons(self.available[year + 1, mine] <= self.available[year, mine])

    def add_objective(self, years, mines):
        price = self.data["price"]
        time_discount = self.data["time_discount"]
        royalties = self.data["royalties"]
        obj = quicksum(self.blend[year] * price * time_discount[year] for year in years) - \
              quicksum(royalties[mine] * time_discount[year] * self.available[year, mine]
                       for year in years for mine in mines)
        self.model.setObjective(obj, "maximize")

    def print_results(self,years,mines):
        rows = years.copy()
        columns = mines.copy()
        extraction = pd.DataFrame(columns=columns, index=rows, data=0.0)
        sales = pd.DataFrame(columns=['Sales'], index=rows, data=0.0)

        for year in years:
            for mine in mines:
                val = self.model.getVal(self.extract[year,mine])
                if val>0:
                    extraction.loc[year, mine] = np.round(val/1e6, 2)
            val = self.model.getVal(self.blend[year])
            if val:
                sales.loc[year, 'Sales'] = np.round(val / 1e6, 2)
        print(extraction)
        print(sales)


if __name__ == '__main__':
    prob_data = data
    prob = Mining(prob_data)
    prob.create_model()
