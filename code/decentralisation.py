from pyscipopt import Model, quicksum
import pandas as pd

from data.decentralisation.data import data


class Decentralisation:
    def __init__(self, data):
        self.data = data
        self.model = Model()
        self.locate = dict()

    def create_model(self):
        Departments = self.data["Departments"]
        Cities = self.data["Cities"]
        self.add_variables(Departments, Cities)
        self.add_constraints(Departments, Cities)
        self.add_objective(Departments, Cities)
        self.model.optimize()
        self.print_results(Departments,Cities)

    def add_variables(self, Departments, Cities):
        for d in Departments:
            for c in Cities:
                self.locate[d, c] = self.model.addVar(vtype="B")

    def add_constraints(self, Departments, Cities):
        self.add_department_location_constraints(Departments, Cities)
        self.add_departments_limit_constraints(Departments, Cities)

    def add_department_location_constraints(self, Departments, Cities):
        for d in Departments:
            self.model.addCons(quicksum(self.locate[d, c] for c in Cities) == 1)

    def add_departments_limit_constraints(self, Departments, Cities):
        for c in Cities:
            self.model.addCons(quicksum(self.locate[d, c] for d in Departments) <= 3)

    def add_objective(self, Departments, Cities):
        benefit = self.data["benefit"]
        communicationCost = self.data["communicationCost"]
        obj_1 = quicksum(benefit[d, c] * self.locate[d, c] for d in Departments for c in Cities)
        aux_variables = dict()
        for d, c, d2, c2 in communicationCost.keys():
            aux_variables[d, c, d2, c2] = self.model.addVar()
            self.model.addCons(aux_variables[d, c, d2, c2] == self.locate[d, c] * self.locate[d2, c2])
        obj_2 = quicksum(communicationCost[d, c, d2, c2] * aux_variables[d, c, d2, c2]
                         for d, c, d2, c2 in communicationCost.keys())
        self.model.setObjective(obj_1 - obj_2, "maximize")

    def print_results(self, Departments, Cities):
        relocation_plan = pd.DataFrame(columns=["Department", "City"])
        benefit = self.data["benefit"]
        count = 0
        total_benefit = 0
        for c in Cities:
            for d in Departments:
                val = self.model.getVal(self.locate[d, c])
                if val > 0.5:
                    count += 1
                    relocation_plan = relocation_plan.append({"Department": d, "City": c}, ignore_index=True)
                    total_benefit += 1000 * benefit[d, c]
        relocation_plan.index = [''] * count
        print(relocation_plan)
        print("\n\n_________________________________________________________________________________")
        print(f"Financial report")
        print("_________________________________________________________________________________")
        dollars_benefit = '${:,.2f}'.format(total_benefit)
        print(f"The yearly total benefit is {dollars_benefit} dollars")
        communicationCost = self.data["communicationCost"]
        total_communication_cost = 0
        for d, c, d2, c2 in communicationCost.keys():
            val = self.model.getVal(self.locate[d,c]) * self.model.getVal(self.locate[d2,c2])
            if val > 0.5:
                total_communication_cost += 1000 * communicationCost[d, c, d2, c2]
        dollars_communication_cost = '${:,.2f}'.format(total_communication_cost)
        print(f"The yearly total communication cost is {dollars_communication_cost} dollars")
        total_gross_margin = total_benefit - total_communication_cost
        dollars_gross_margin = '${:,.2f}'.format(total_gross_margin)
        print(f"The yearly total gross margin is {dollars_gross_margin} dollars")


if __name__ == '__main__':
    prob_data = data
    prob = Decentralisation(prob_data)
    prob.create_model()
