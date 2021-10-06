from pyscipopt import Model, quicksum

from data.power_generation import data
import pandas as pd

class PowerGeneration:
    def __init__(self, data):
        self.data = data
        self.model = Model()
        self.ngen = dict()
        self.nstart = dict()
        self.output = dict()
        self.hydro = dict()
        self.hydrostart = dict()
        self.pumping = dict()
        self.height = dict()

    def create_model(self, is_hydro=False):
        self.add_variables(is_hydro)
        self.add_constraints(is_hydro)
        self.add_objective(is_hydro)
        self.model.optimize()
        self.print_results(is_hydro)

    def add_variables(self, is_hydro):
        for t in range(self.data.ntypes):
            for p in range(self.data.nperiods):
                self.ngen[t, p] = self.model.addVar(vtype="I")
                self.nstart[t, p] = self.model.addVar(vtype="I")
                self.output[t, p] = self.model.addVar(vtype="C")
        if is_hydro:
            for h in range(self.data.hydrounits):
                for p in range(self.data.nperiods):
                    self.hydro[h, p] = self.model.addVar(vtype="B")
                    self.hydrostart[h, p] = self.model.addVar(vtype="B")
            for p in range(self.data.nperiods):
                self.pumping[p] = self.model.addVar(vtype="C")
                self.height[p] = self.model.addVar(vtype="C")

    def add_constraints(self, is_hydro):
        self.add_generator_count_costraints()
        self.add_demand_constraints(is_hydro)
        self.add_min_max_generation_constraints()
        self.add_reserve_constraints(is_hydro)
        self.add_startup_constraints(is_hydro)
        if is_hydro:
            self.add_reservoir_height_constraints()

    def add_generator_count_costraints(self):
        for t in range(self.data.ntypes):
            for p in range(self.data.nperiods):
                self.model.addCons(self.ngen[t, p] <= self.data.generators[t])

    def add_demand_constraints(self, is_hydro):
        for p in range(self.data.nperiods):
            if is_hydro:
                self.model.addCons(quicksum(self.output[t, p] for t in range(self.data.ntypes)) +
                                   quicksum(
                                       self.hydro[h, p] * self.data.hydro_load[h] for h in range(self.data.hydrounits))
                                   >= self.data.demand[p] + self.pumping[p])
            else:
                self.model.addCons(quicksum(self.output[t, p] for t in range(self.data.ntypes)) >=
                                   self.data.demand[p])

    def add_min_max_generation_constraints(self):
        for t in range(self.data.ntypes):
            for p in range(self.data.nperiods):
                self.model.addCons(self.output[t, p] >= self.data.min_load[t] * self.ngen[t, p])
                self.model.addCons(self.output[t, p] <= self.data.max_load[t] * self.ngen[t, p])

    def add_reserve_constraints(self, is_hydro):
        delta = 0
        if is_hydro:
            delta = sum(self.data.hydro_load)
        for p in range(self.data.nperiods):
            self.model.addCons(quicksum(self.data.max_load[t] * self.ngen[t, p] for t in range(self.data.ntypes))
                               >= 1.15 * self.data.demand[p] - delta)

    def add_startup_constraints(self, is_hydro):
        for t in range(self.data.ntypes):
            for p in range(self.data.nperiods):
                if p == 0:
                    self.model.addCons(self.ngen[t, p] <= self.data.maxstart0 + self.nstart[t, p])
                else:
                    self.model.addCons(self.ngen[t, p] <= self.ngen[t, p - 1] + self.nstart[t, p])
        if is_hydro:
            for h in range(self.data.hydrounits):
                for p in range(self.data.nperiods):
                    if p == 0:
                        self.model.addCons(self.hydro[h, p] <= self.hydrostart[h, p])
                    else:
                        self.model.addCons(self.hydro[h, p] <= self.hydrostart[h, p - 1] +
                                           self.hydrostart[h, p])

    def add_reservoir_height_constraints(self):
        for p in range(self.data.nperiods):
            if p == 0:
                p_1 = self.data.nperiods - 1
            else:
                p_1 = p - 1
            self.model.addCons(self.height[p] == self.height[p_1] + self.data.period_hours[p] * self.pumping[p] / 3000
                               - quicksum(self.data.hydro_height_reduction[h] * self.data.period_hours[p] *
                                          self.hydro[h, p] for h in range(self.data.hydrounits)))

    def add_objective(self, is_hydro):
        active = quicksum(self.data.base_cost[t] * self.data.period_hours[p] * self.ngen[t, p]
                          for t in range(self.data.ntypes) for p in range(self.data.nperiods))
        per_mw = quicksum(self.data.per_mw_cost[t] * self.data.period_hours[p] *
                          (self.output[t, p] - self.data.min_load[t] * self.ngen[t, p])
                          for t in range(self.data.ntypes) for p in range(self.data.nperiods))
        startup = quicksum(self.data.startup_cost[t] * self.nstart[t, p]
                           for t in range(self.data.ntypes) for p in range(self.data.nperiods))
        hydro_active, hydro_startup = 0, 0
        if is_hydro:
            hydro_active += quicksum(self.data.hydro_cost[h] * self.data.period_hours[p] * self.hydro[h, p]
                                     for h in range(self.data.hydrounits) for p in range(self.data.nperiods))
            hydro_startup += quicksum(self.data.hydro_startup_cost[h] * self.hydrostart[h, p]
                                      for h in range(self.data.hydrounits) for p in range(self.data.nperiods))

        self.model.setObjective(active + per_mw + startup + hydro_startup + hydro_active)


    def print_results(self,is_hydro):
        ntypes = self.data.ntypes
        nperiods = self.data.nperiods

        rows = ["Thermal" + str(t) for t in range(ntypes)]
        units = pd.DataFrame(columns=range(nperiods), index=rows, data=0.0)
        startups = pd.DataFrame(columns=range(nperiods), index=rows, data=0.0)

        for t in range(ntypes):
            for p in range(nperiods):
                units.loc["Thermal" + str(t), p] = self.model.getVal(self.ngen[t, p])
                startups.loc["Type" + str(t), p] = self.model.getVal(self.nstart[t, p])
        print(units)
        print(startups)
        if is_hydro:
            rows = ["HydroA", "HydroB"]
            hydrotable = pd.DataFrame(columns=range(nperiods), index=rows, data=0.0)
            pumptable = pd.DataFrame(columns=range(nperiods), index=["Pumping"], data=0.0)

            for p in range(nperiods):
                hydrotable.loc["HydroA", p] = int(self.model.getVal(self.hydro[0, p]))
                hydrotable.loc["HydroB", p] = int(self.model.getVal(self.hydro[1, p]))
                pumptable.loc["Pumping", p] = self.model.getVal(self.pumping[p])
            print(hydrotable)
            print(pumptable)

if __name__ == '__main__':
    prob = PowerGeneration(data)
    prob.create_model(False)
