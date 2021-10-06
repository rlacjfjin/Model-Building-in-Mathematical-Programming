from pyscipopt.scip import Model, quicksum

from data.opencast_mining.data import data
import pandas as pd


class OpencastMining:
    def __init__(self, data):
        self.data = data
        self.model = Model()

    def create_model(self):
        profit = self.data["profit"]
        blocks = self.data["blocks"]
        arcs = self.data["arcs"]
        extract = dict()
        print(blocks)
        for b in blocks:
            extract[b] = self.model.addVar(ub=1, vtype="C")
        for b, b2 in arcs:
            self.model.addCons(extract[b] <= extract[b2])
        obj = quicksum(profit[b] * extract[b] for b in blocks)
        self.model.setObjective(obj, "maximize")
        self.model.optimize()
        count = 0
        extraction_plan = pd.DataFrame(columns=["Block", "Profit/Loss"])
        for b in blocks:
            if self.model.getVal(extract[b]):
                count += 1
                extraction_plan = extraction_plan.append(
                    {"Block": b, "Profit/Loss": '${:,.2f}'.format(profit[b] * round(self.model.getVal(extract[b])))},
                    ignore_index=True)
        extraction_plan.index = [''] * count
        print(extraction_plan)


if __name__ == '__main__':
    prob = OpencastMining(data)
    prob.create_model()
