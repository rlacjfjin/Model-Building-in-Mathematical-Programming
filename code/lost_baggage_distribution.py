from itertools import combinations
import matplotlib.pyplot as plt
import networkx
from pyscipopt import Model, Eventhdlr, Conshdlr, quicksum, SCIP_RESULT, SCIP_EVENTTYPE
import math

from data.Lost_baggage_distribution.data import data


def find_next(route, node):
    for i, j in enumerate(route):
        if node == j[0]:
            return j[1]


class SEC(Conshdlr):
    def createCons(self, name, variables, prob_data):
        model = self.model
        cons = model.createCons(self, name)
        cons.data = {'vars': variables, "data": prob_data}
        return cons

    def find_subtours(self, cons, solution=None):
        vans = cons.data["data"]["vans"]
        time = cons.data["data"]["time"]
        for k in vans:
            edges = []
            x = cons.data['vars']
            for i, j in time.keys():
                if self.model.getSolVal(solution, x[(i, j, k)]) > 0.5:
                    edges.append((i, j))

            G = networkx.Graph()
            G.add_edges_from(edges)
            components = list(networkx.connected_components(G))
            if len(components) > 1:
                return components
        return []

    def conscheck(self, constraints, solution, check_integrality,
                  check_lp_rows, print_reason, completely, **results):
        for cons in constraints:
            if self.find_subtours(cons, solution):
                return {"result": SCIP_RESULT.INFEASIBLE}
        return {"result": SCIP_RESULT.FEASIBLE}

    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        consadded = False
        for cons in constraints:
            subtours = self.find_subtours(cons)
            if subtours:
                x = cons.data['vars']
                time = cons.data["data"]["time"]
                for k in cons.data["data"]["vans"]:
                    for S in subtours:
                        self.model.addCons(
                            quicksum(x[(i, j, k)] for i in S for j in S if (i, j) in time.keys()) <= len(S) - 1)
                        consadded = True
        if consadded:
            return {"result": SCIP_RESULT.CONSADDED}
        return {"result": SCIP_RESULT.FEASIBLE}

    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        pass


# 添加输出
class NewSolEvent(Eventhdlr):
    def __init__(self, vars_dict, prob_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {'vars': vars_dict, 'data': prob_data}

    def eventinit(self):
        self.model.catchEvent(SCIP_EVENTTYPE.BESTSOLFOUND, self)

    def eventexit(self):
        self.model.dropEvent(SCIP_EVENTTYPE.BESTSOLFOUND, self)

    def eventexec(self, event):
        assert event.getType() == SCIP_EVENTTYPE.BESTSOLFOUND
        # get best sol
        time = self.data["data"]["time"]
        vans = self.data["data"]["vans"]
        positions = self.data["data"]["positions"]
        sol = self.model.getBestSol()
        x,t,s = self.data['vars']
        for k in vans:
            edges = []
            for i, j in time.keys():
                if self.model.getSolVal(sol, x[(i, j, k)]) > 0.5:  # variable is binary so > 0.5 --> is 1
                    edges.append((i, j))
            if not edges:
                continue
            # todo: 暂时关闭可视化功能
            # plt.figure(figsize=(10, 6), dpi=100)
            # optgraph = networkx.Graph()
            # optgraph.add_edges_from(edges)
            # networkx.draw(optgraph, node_size=300, pos=positions, with_labels=True, node_color='lightblue')
            # plt.show()

            i = 0
            print(f"Route for van {k}: {i}", end='')
            while True:
                i = find_next(edges, i)
                print(f" -> {i}", end='')
                if i == 0:
                    break
            print(f". Travel time: {round(self.model.getVal(t[k]), 2)} min")

        print(f"Max travel time: {round(self.model.getVal(s), 2)}")


class LostBaggageDistribution:
    def __init__(self, prob_data):
        self.data = prob_data
        self.model = Model()

    def preprocessing(self):
        time = self.data["time"]
        vans = self.data["vans"]
        locations = self.data["locations"]
        return locations, vans, time

    def crete_model(self):
        locations, vans, time = self.preprocessing()
        x, y, z, t, s = self.add_variables(locations, time, vans)
        self.add_constraints(x, y, z, t, s, locations, time, vans)
        self.add_objective(z, s, vans)
        self.model.includeEventhdlr(NewSolEvent([x,t,s], self.data),
                                    "NewSolEvent", "Prints new sol found")
        self.model.optimize()

    def add_variables(self, locations, time, vans):
        x = dict()
        y = dict()
        z = dict()
        t = dict()
        for i, j in time.keys():
            for k in vans:
                x[(i, j, k)] = self.model.addVar(vtype="B", name="x(%s,%s,%s)" % (i, j, k))
        for i in locations:
            for k in vans:
                y[(i, k)] = self.model.addVar(vtype="B", name="y(%s,%s)" % (i, k))

        for k in vans:
            z[k] = self.model.addVar(vtype="B", name="z(%s)" % k)

        for k in vans:
            t[k] = self.model.addVar(vtype="C", ub=120, name="t(%s)" % k)

        s = self.model.addVar(name="s")
        return x, y, z, t, s

    def add_constraints(self, x, y, z, t, s, locations, time, vans):
        self.add_van_utilization_constraints(y, z, locations, vans)
        self.add_travel_time_constraints(x, t, vans, time)
        self.add_visit_all_customers_constraints(y, locations, vans)
        self.add_depot_constraints(y, z, vans)
        self.add_customer_location_constraints(x, y, locations, time)
        self.breaking_symmetry_constraints(y, locations, vans)
        self.max_travel_time_constraints(t, s, vans)
        self.add_sub_tour_elimination(x)

    def add_van_utilization_constraints(self, y, z, locations, vans):
        for i in locations:
            if i > 0:
                for k in vans:
                    self.model.addCons(y[(i, k)] <= z[k])

    def add_travel_time_constraints(self, x, t, vans, time):
        for k in vans:
            self.model.addCons(quicksum(time[i, j] * x[(i, j, k)] for i, j in time.keys() if j > 0) == t[k])

    def add_visit_all_customers_constraints(self, y, locations, vans):
        for i in locations:
            if i > 0:
                self.model.addCons(quicksum(y[(i, k)] for k in vans) == 1)

    def add_depot_constraints(self, y, z, vans):
        self.model.addCons(quicksum(y[(0, k)] for k in vans) >= quicksum(z[k] for k in vans))

    def add_customer_location_constraints(self, x, y, locations, time):
        # arriving
        for j, k in y.keys():
            self.model.addCons(quicksum(x[(i, j, k)] for i in locations if (i, j) in time.keys())
                               == y[(j, k)])
        # leaving
        for j, k in y.keys():
            self.model.addCons(quicksum(x[(j, i, k)] for i in locations if (i, j) in time.keys())
                               == y[(j, k)])

    def breaking_symmetry_constraints(self, y, locations, vans):
        for k in vans:
            if k > 0:
                self.model.addCons(quicksum(y[(i, k - 1)] for i in locations)
                                   >= quicksum(y[(i, k)] for i in locations))

    def max_travel_time_constraints(self, t, s, vans):
        for k in vans:
            self.model.addCons(t[k] <= s)

    def add_sub_tour_elimination(self, x):
        conshdlr = SEC()
        self.model.includeConshdlr(conshdlr, "TSP", "TSP subtour eliminator", chckpriority=-10, enfopriority=-10)
        cons = conshdlr.createCons("no_subtour_cons", x, self.data)
        self.model.addPyCons(cons)

    def add_objective(self, z, s, vans):
        self.model.setObjective(100 * quicksum(z[k] for k in vans) + s)


if __name__ == '__main__':
    prob_data = data
    prob = LostBaggageDistribution(prob_data)
    prob.crete_model()
