import pyscipopt as scip
import pandas as pd


class CarRental:
    def __init__(self, PD=0.1, CO=15, DF=10):
        # 参数
        self.D = dict()
        self.P = dict()
        self.C = dict()
        self.Q, self.R, self.RCA, self.RCB, self.CS = dict(), dict(), dict(), dict(), dict()
        self.PD = PD
        self.CO = CO
        self.DF = DF
        self.model = scip.Model()
        self.load_data()

    def load_data(self):
        demand_df = pd.read_excel("..\\data\\car_rental\\demands.xlsx", index_col=0)
        capacity_df = pd.read_excel("..\\data\\car_rental\\repair_capacity.xlsx", index_col=0)
        rent_to_return_df = pd.read_excel("..\\data\\car_rental\\rent_to_return.xlsx", index_col=0)
        transfers_df = pd.read_excel("..\\data\\car_rental\\transfers.xlsx", index_col=0)
        other_cost_df = pd.read_excel("..\\data\\car_rental\\other_costs.xlsx", index_col=0)
        self.preprocessing(demand_df, capacity_df, rent_to_return_df, transfers_df, other_cost_df)

    def preprocessing(self, demand, capacity, rent, trans, others):
        self.depots = list(capacity.index)
        self.repair_depots = list(capacity[capacity["capacity"] > 0].index)
        self.non_repair_depots = list(capacity[capacity["capacity"] <= 0].index)
        self.days = list(demand.index)
        self.rentDays = list(others.index)
        print(others)
        print(self.rentDays)
        for d in self.depots:
            for t in self.days:
                self.D[(d, t)] = demand.loc[t, d]
            for d1 in self.depots:
                self.P[(d, d1)] = rent.loc[d, d1]
                self.C[(d, d1)] = trans.loc[d, d1]
        for k in self.rentDays:
            self.Q[k] = others.loc[k, "Q"]
            self.RCA[k] = others.loc[k, "RCA"]
            self.RCB[k] = others.loc[k, "RCB"]
            self.CS[k] = others.loc[k, "CS"]
        for d in self.depots:
            self.R[d] = capacity.loc[d, "capacity"]

    def add_auxiliary_variables(self):
        self.nu = dict()  # 一天开始时不受损车辆数
        self.nd = dict()  # 一天开始时受损车辆数
        self.eu = dict()  # 一天结束时不受损车辆数
        self.ed = dict()  # 一天结束时受损车辆数
        self.tr = dict()  # 已经租出去的车辆数
        self.rp = dict()  # 需要维修的车辆数
        for d in self.depots:
            for day in self.days:
                self.nu[(d, day)] = self.model.addVar(name="num_ud_cars(%s,%s)" % (d, day))
                self.nd[(d, day)] = self.model.addVar(name="num_d_cars(%s,%s)" % (d, day))
                self.eu[(d, day)] = self.model.addVar(name="end_inv_ud(%s,%s)" % (d, day))
                self.ed[(d, day)] = self.model.addVar(name="end_inv_d(%s,%s)" % (d, day))
                self.tr[(d, day)] = self.model.addVar(name="num_h_cars(%s,%s)" % (d, day),
                                                      ub=self.D[(d, day)])
                self.rp[(d, day)] = self.model.addVar(name="repair_num_cars(%s,%s)" % (d, day),
                                                      ub=self.R[d])
        self.tu = dict()  # 不受损车辆的挑拨数量
        self.td = dict()  # 受损车辆的调拨数量
        for d_i in self.depots:
            for d_j in self.depots:
                for day in self.days:
                    self.tu[(d_i, d_j, day)] = self.model.addVar(name="trans_ud(%s,%s,%s)" % (d_i, d_j, day))
                    self.td[(d_i, d_j, day)] = self.model.addVar(name="trans_d(%s,%s,%s)" % (d_i, d_j, day))

    def add_variables(self):
        self.n = self.model.addVar(name="num_cars")
        self.add_auxiliary_variables()

    def add_undamaged_into_depots(self):
        # repair depots case
        for d in self.repair_depots:
            for day in self.days:
                self.model.addCons(scip.quicksum((1 - self.PD) * self.P[d1, d] * self.Q[k] * self.tr[d1, (day - k) % 6]
                                                 for d1 in self.depots for k in self.rentDays)
                                   + scip.quicksum(self.tu[(d1, d, (day - 1) % 6)] for d1 in self.depots)
                                   + self.rp[(d, (day - 1) % 6)] + self.eu[(d, (day - 1) % 6)] == self.nu[(d, day)])
        # non-repair depots case
        for d in self.non_repair_depots:
            for day in self.days:
                self.model.addCons(scip.quicksum((1 - self.PD) * self.P[d1, d] * self.Q[k] * self.tr[d1, (day - k) % 6]
                                                 for d1 in self.depots for k in self.rentDays)
                                   + scip.quicksum(self.tu[(d1, d, (day - 1) % 6)] for d1 in self.depots)
                                   + self.eu[(d, (day - 1) % 6)] == self.nu[(d, day)])

    def add_damaged_into_depots(self):
        # repair depots case
        for d in self.repair_depots:
            for day in self.days:
                self.model.addCons(scip.quicksum(self.PD * self.P[d1, d] * self.Q[k] * self.tr[d1, (day - k) % 6]
                                                 for d1 in self.depots for k in self.rentDays)
                                   + scip.quicksum(
                    self.td[d1, d, (day - 1) % 6] for d1 in self.depots for dd in self.depots if (dd == d))
                                   + self.ed[(d, (day - 1) % 6)] == self.nd[(d, day)])
        for d in self.non_repair_depots:
            for day in self.days:
                self.model.addCons(scip.quicksum(self.PD * self.P[d1, d] * self.Q[k] * self.tr[d1, (day - k) % 6]
                                                 for d1 in self.depots for k in self.rentDays)
                                   + self.ed[(d, (day - 1) % 6)] == self.nd[(d, day)])

    def add_undamaged_output_depots(self):
        # repair depot case
        for d in self.repair_depots:
            for day in self.days:
                self.model.addCons(self.tr[d, day] + scip.quicksum(self.tu[(d, d1, day)] for d1 in self.depots)
                                   + self.eu[(d, day)] == self.nu[(d, day)])
        # non-repair deopt case
        for d in self.non_repair_depots:
            for day in self.days:
                self.model.addCons(self.tr[d, day] + scip.quicksum(self.tu[(d, d1, day)] for d1 in self.depots)
                                   + self.eu[(d, day)] == self.nu[(d, day)])

    def add_damaged_output_depots(self):
        # repair depot case
        for d in self.repair_depots:
            for day in self.days:
                self.model.addCons(
                    self.rp[(d, day)] + scip.quicksum(self.td[(d, d1, day)] for d1 in self.non_repair_depots)
                    + self.ed[(d, day)] == self.nd[(d, day)])
        # non-repair depot case
        for d in self.non_repair_depots:
            for day in self.days:
                self.model.addCons(scip.quicksum(self.td[(d, d1, day)] for d1 in self.repair_depots)
                                   + self.ed[(d, day)] == self.nd[(d, day)])

    def add_total_num_constraints(self):
        self.model.addCons(scip.quicksum(0.25 * self.tr[(d, 0)] +
                                         0.45 * self.tr[(d, 1)] +
                                         self.nu[(d, 2)] + self.nd[(d, 2)] for d in self.depots) == self.n)

    def add_constraints(self):
        self.add_undamaged_into_depots()
        self.add_damaged_into_depots()
        self.add_undamaged_output_depots()
        self.add_damaged_output_depots()
        self.add_total_num_constraints()

    def add_objective(self):
        obj_1 = scip.quicksum(self.P[(i, i)] * self.Q[k] * (self.RCA[k] - self.CS[k] + self.DF) * self.tr[(i, t)]
                              for i in self.depots for t in self.days for k in self.rentDays)
        obj_2 = scip.quicksum(self.P[(i, j)] * self.Q[k] * (self.RCB[k] - self.CS[k] + self.DF) * self.tr[(i, t)]
                              for i in self.depots for j in self.depots for k in self.rentDays for t in self.days)
        obj_3 = scip.quicksum(self.C[(i, j)] * (self.tu[(i, j, t)] + self.td[(i, j, t)]) for i in self.depots
                              for j in self.depots for t in self.days)
        obj = obj_1 + obj_2 - obj_3 - self.CO * self.n
        self.model.setObjective(obj, "maximize")

    def create_model(self):
        self.add_variables()
        self.add_constraints()
        self.add_objective()

    def solve_and_analysis(self):
        self.model.optimize()
        # Output report

        # Total number of cars owned
        print(f"The optimal number of cars to be owned is: {round(self.model.getVal(self.n))}.")

        # Optimal profit
        print(f"The optimal profit is: {'${:,.2f}'.format(round(self.model.getObjVal(), 2))}.")


if __name__ == '__main__':
    ex = CarRental()
    ex.create_model()
    ex.solve_and_analysis()
