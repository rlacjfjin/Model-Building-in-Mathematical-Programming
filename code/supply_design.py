import pyscipopt as scip
import pandas as pd

from data.supply.data import supply, through, opencost, demand, cost


class SupplyNetwork:
    def __init__(self,
                 factories=None,
                 depots=None,
                 suppliers=None,
                 cities=None,
                 trans_cost=None,
                 supplies=None,
                 demands=None,
                 throughs=None,
                 open_cost=None):
        self.F = factories
        self.D = depots
        self.S = suppliers
        self.C = cities
        self.cost = trans_cost
        self.supply = supplies
        self.demand = demands
        self.through = throughs
        self.open_cost = open_cost
        self.model = scip.Model()

    def preprocessing(self):
        self.F = list(self.supply.keys())
        self.D = list(self.through.keys())
        self.S = list(self.demand.keys())
        self.C = list(self.cost.keys())

    def add_quantity_variables(self, is_select):
        self.q = dict()
        for key in self.C:
            self.q[key] = self.model.addVar(obj=self.cost[key])
        if is_select:
            self.add_open_variables()
            self.add_expand_variables()

    def add_open_variables(self):
        self.open = dict()
        for d in self.D:
            lb = 0
            if d == "Birmingham" or d == "London":
                lb = 1
            self.open[d] = self.model.addVar(obj=self.open_cost[d], vtype="B", lb=lb)

    def add_expand_variables(self):
        self.expand = self.model.addVar(obj=3000, vtype="B")

    def add_supplier_request(self):
        for s in self.S:
            self.model.addCons(scip.quicksum(self.q[(i[0], s)] for i in self.C if s == i[1]) == self.demand[s])

    def add_factory_capacity(self):
        for f in self.F:
            self.model.addCons(scip.quicksum(self.q[(f, i[1])] for i in self.C if f == i[0]) <= self.supply[f])

    def add_depot_through(self):
        for d in self.D:
            self.model.addCons(scip.quicksum(self.q[(i[0], d)] for i in self.C if d == i[1]) <= self.through[d])

    def add_depot_through_is_select(self):
        for d in self.D:
            if d != 'Birmingham':
                self.model.addCons(scip.quicksum(self.q[(d, i[1])] for i in self.C if i[0] == d)
                                   <= self.through[d] * self.open[d])

    def add_depot_expand(self):
        d = 'Birmingham'
        self.model.addCons(scip.quicksum(self.q[(i[0], d)] for i in self.C if i[1] == d)
                           <= self.through[d] + 20000 * self.expand)

    def add_flow_conservation(self):
        for d in self.D:
            self.model.addCons(scip.quicksum(self.q[(d, j[1])] for j in self.C if d == j[0]) ==
                               scip.quicksum(self.q[(i[0], d)] for i in self.C if d == i[1]))

    def add_depot_count(self):
        self.model.addCons(scip.quicksum(self.open[d] for d in self.D) <= 4)

    def add_constraints(self, is_select):
        self.add_supplier_request()
        self.add_factory_capacity()
        self.add_flow_conservation()
        if is_select:
            self.add_depot_count()
            self.add_depot_through_is_select()
            self.add_depot_expand()
        else:
            self.add_depot_through()

    def create_mip_model(self, is_select=False):
        self.preprocessing()
        self.add_quantity_variables(is_select)
        self.add_constraints(is_select)
        if is_select:
            obj = self.model.getObjective()
            obj -= (self.open_cost['Newcastle'] + self.open_cost['Exeter'])
            self.model.setObjective(obj)

    def solve_and_analysis(self, is_select=False):
        self.model.optimize()
        product_flow = pd.DataFrame(columns=["From", "To", "Flow"])
        for c in self.C:
            if self.model.getVal(self.q[c]) > 1e-6:
                product_flow = product_flow.append({"From": c[0], "To": c[1], "Flow": self.model.getVal(self.q[c])},
                                                   ignore_index=True)
        product_flow.index = [''] * len(product_flow)
        print(product_flow)
        if is_select:
            print('List of open depots:', [d for d in self.D if self.model.getVal(self.open[d]) > 0.5])
            if self.model.getVal(self.expand) > 0.5:
                print('Expand Birmingham')


if __name__ == '__main__':
    problem = SupplyNetwork(supplies=supply, demands=demand, throughs=through, trans_cost=cost, open_cost=opencost)
    problem.create_mip_model(False)
    problem.solve_and_analysis(False)
