from pyscipopt import Model, quicksum
import pandas as pd
from data.agricultural_pricing.data import data


class AgriculturePricing:
    def __init__(self, prob_data):
        self.data = prob_data
        self.model = Model()

    def preprocessing(self):
        pass

    def create_model(self):
        dairy = self.data["dairy"]
        q, p = self.add_variables(dairy)
        self.add_constraints(q, p, dairy)
        self.add_objective(q, p, dairy)
        self.model.optimize()
        # Output Report
        price_demand = pd.DataFrame(columns=["Products", "Price", "Demand"])
        for d in dairy:
            p_val = self.model.getVal(p[d])
            q_val = self.model.getVal(q[d])
            price_demand = price_demand.append({"Products": d, "Price": '${:,.2f}'.format(round(1000 * p_val)),
                                                "Demand": '{:,.2f}'.format(round(1e6 * q_val))}, ignore_index=True)
        price_demand.index = [''] * len(price_demand)
        print(price_demand)

    def add_variables(self, dairy):
        q = dict()  # quantity
        p = dict()  # price
        for i in dairy:
            q[i] = self.model.addVar(name="q(%s)" % i)
            p[i] = self.model.addVar(name="p(%s)" % i)
        return q, p

    def add_constraints(self, q, p, dairy):
        components = self.data["components"]
        qtyper = self.data["qtyper"]
        capacity = self.data["capacity"]
        consumption = self.data["consumption"]
        price = self.data["price"]
        elasticity = self.data["elasticity"]
        elasticity12 = self.data["elasticity12"]
        elasticity21 = self.data["elasticity21"]
        priceIndex = self.data["priceIndex"]
        self.add_capacity_constraints(q, dairy, components, qtyper, capacity)
        self.add_price_index_constraints(p, dairy, consumption, priceIndex)
        self.add_elasticity_constraints(q, p, consumption, price, elasticity, elasticity12, elasticity21)

    def add_capacity_constraints(self, q, dairy, components, qtyper, capacity):
        for c in components:
            self.model.addCons(quicksum(qtyper[c, d] * q[d] for d in dairy) <= capacity[c])

    def add_price_index_constraints(self, p, dairy, consumption, priceIndex):
        self.model.addCons(quicksum(consumption[d] * p[d] for d in dairy) <= priceIndex)

    def add_elasticity_constraints(self, q, p, consumption, price, elasticity, elasticity12, elasticity21):
        self.model.addCons((q["milk"] - consumption['milk']) / consumption['milk'] ==
                           -elasticity['milk'] * (p['milk'] - price['milk']) / price['milk'])
        self.model.addCons((q['butter'] - consumption['butter']) / consumption['butter'] ==
                           -elasticity['butter'] * (p['butter'] - price['butter']) / price['butter'])
        self.model.addCons((q['cheese1'] - consumption['cheese1']) / consumption['cheese1'] ==
                           -elasticity['cheese1'] * (p['cheese1'] - price['cheese1']) / price['cheese1']
                           + elasticity12 * (p['cheese2'] - price['cheese2']) / price['cheese2']
                           )
        self.model.addCons((q['cheese2'] - consumption['cheese2']) / consumption['cheese2'] ==
                           -elasticity['cheese2'] * (p['cheese2'] - price['cheese2']) / price['cheese2']
                           + elasticity21 * (p['cheese1'] - price['cheese1']) / price['cheese1']
                           )

    def add_objective(self, q, p, dairy):
        # bilinear objective function
        obj = dict()
        for d in dairy:
            obj[d] = self.model.addVar()
            self.model.addCons(obj[d] == q[d] * p[d])
        self.model.setObjective(quicksum(obj[d] for d in dairy), "maximize")


if __name__ == '__main__':
    agriculture_data = data
    prob = AgriculturePricing(agriculture_data)
    prob.create_model()
