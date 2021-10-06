from pyscipopt import Model, quicksum
import pandas as pd

from data.supply.data import data


class Distribution:
    def __init__(self, data):
        self.data = data
        self.model = Model()
        self.q = dict()
        self.open = dict()
        self.expand = None

    def preprocessing(self):
        supply = self.data["supply"]
        demand = self.data["demand"]
        through = self.data["through"]
        cost = self.data["cost"]
        arcs = cost.keys()
        depots = through.keys()
        customers = demand.keys()
        factories = supply.keys()
        return depots, factories, customers, arcs, supply, demand, through, cost

    def create_model(self, is_changed=False):
        depots, factories, customers, arcs, supply, demand, through, cost = self.preprocessing()
        self.add_variables(arcs, is_changed)
        self.add_constraints(depots, factories, customers, arcs, supply, demand, through, is_changed)
        self.add_objective(arcs, cost, is_changed)
        self.model.optimize()
        self.print_result(arcs,is_changed)

    def add_variables(self, arcs, is_changed):
        self.add_quantity_variables(arcs)
        if is_changed:
            open_depots = ["Birmingham", "London"]
            depots = self.data["through"].keys()
            self.add_open_variables(depots, open_depots)
            self.add_expand_variables()

    def add_quantity_variables(self, arcs):
        for arc in arcs:
            self.q[arc] = self.model.addVar()

    def add_open_variables(self, depots, open_depots):
        for depot in depots:
            lb = 0
            if depot in open_depots:
                lb = 1
            self.open[depot] = self.model.addVar(vtype="B", lb=lb)

    def add_expand_variables(self):
        self.expand = self.model.addVar(vtype="B")

    def add_constraints(self, depots, factories, customers, arcs, supply, demand, through, is_changed):
        self.add_capacity_constraints(factories, arcs, supply)
        self.add_demand_constraints(customers, arcs, demand)
        self.add_flow_conservation_constraints(depots, arcs)
        if is_changed:
            depot_list = ["Birmingham"]
            self.add_depot_throughput_with_select_constraints(depots, depot_list, arcs, through)
            self.add_depot_count(depots)
        else:
            self.add_depot_throughput_constraints(depots, arcs, through)

    def add_capacity_constraints(self, factories, arcs, supply):
        for factory in factories:
            self.model.addCons(quicksum(self.q[arc] for arc in arcs if factory == arc[0]) <= supply[factory])

    def add_demand_constraints(self, customers, arcs, demand):
        for customer in customers:
            self.model.addCons(quicksum(self.q[arc] for arc in arcs if customer == arc[1]) == demand[customer])

    def add_flow_conservation_constraints(self, depots, arcs):
        for depot in depots:
            self.model.addCons(quicksum(self.q[arc] for arc in arcs if depot == arc[0]) ==
                               quicksum(self.q[arc] for arc in arcs if depot == arc[1]))

    def add_depot_throughput_constraints(self, depots, arcs, through):
        for depot in depots:
            self.model.addCons(quicksum(self.q[arc] for arc in arcs if depot == arc[1]) <= through[depot])

    def add_depot_throughput_with_select_constraints(self, depots, depot_list, arcs, through):
        for depot in depots:
            if depot not in depot_list:
                self.model.addCons(quicksum(self.q[arc] for arc in arcs if depot == arc[0])
                                   <= through[depot] * self.open[depot])
            else:
                self.model.addCons(quicksum(self.q[arc] for arc in arcs if depot == arc[1])
                                   <= through[depot] + self.expand * 20000)

    def add_depot_count(self, depots):
        self.model.addCons(quicksum(self.open[depot] for depot in depots) <= 4)

    def add_objective(self, arcs, cost, is_changed):
        obj = quicksum(self.q[arc] * cost[arc] for arc in arcs)
        if is_changed:
            opencost = self.data["opencost"]
            depots = self.data["through"].keys()
            obj += quicksum(self.open[depot] * opencost[depot] for depot in depots)
            obj += self.expand * 3000
            obj -= (opencost['Newcastle'] + opencost['Exeter'])
        self.model.setObjective(obj)

    def print_result(self, arcs,is_changed ):
        if is_changed:
            depots = self.data["through"].keys()
            print('List of open depots:', [d for d in depots if self.model.getVal(self.open[d]) > 0.5])
            if self.model.getVal(self.expand) > 0.5:
                print('Expand Birmingham')
        product_flow = pd.DataFrame(columns=["From", "To", "Flow"])
        for arc in arcs:
            val = self.model.getVal(self.q[arc])
            if val > 1e-6:
                product_flow = product_flow.append({"From": arc[0], "To": arc[1], "Flow": val},
                                                   ignore_index=True)
        product_flow.index = [''] * len(product_flow)
        print(product_flow)


if __name__ == '__main__':
    prob_data = data
    prob = Distribution(prob_data)
    prob.create_model(is_changed=True)
