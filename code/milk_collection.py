from itertools import combinations
import matplotlib.pyplot as plt
import networkx
from pyscipopt import Model, Eventhdlr, Conshdlr, quicksum, SCIP_RESULT, SCIP_EVENTTYPE
import math

from data.milk_collection.data import data


def distance(c1, c2):
    diff = (c1[0] - c2[0], c1[1] - c2[1])
    return math.sqrt(diff[0] * diff[0] + diff[1] * diff[1])


class SEC(Conshdlr):
    def createCons(self, name, variables, data):
        model = self.model
        cons = model.createCons(self, name)
        cons.data = {'vars': variables, "data": data}
        return cons

    def find_subtours(self, cons, solution=None):
        dayType = cons.data["data"]["dayType"]
        farms = [*range(0, len(cons.data["data"]["positions"]))]
        for k in dayType:
            edges = []
            x = cons.data['vars']
            for i in farms:
                for j in farms:
                    if i < j:
                        if self.model.getSolVal(solution, x[(i, j, k)]) > 0.5:
                            edges.append((i, j))

            G = networkx.Graph()
            G.add_edges_from(edges)
            components = list(networkx.connected_components(G))
            if len(components) != 1:
                return components
        return []

    # checks whether solution is feasible
    def conscheck(self, constraints, solution, check_integrality,
                  check_lp_rows, print_reason, completely, **results):

        # check if there is a violated subtour elimination constraint
        for cons in constraints:
            if self.find_subtours(cons, solution):
                return {"result": SCIP_RESULT.INFEASIBLE}

        # no violated constriant found -> feasible
        return {"result": SCIP_RESULT.FEASIBLE}

    # enforces the LP solution: searches for subtours in the solution and adds
    # adds constraints forbidding all the found subtours
    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        consadded = False
        for cons in constraints:
            subtours = self.find_subtours(cons)
            # if there are subtours
            if subtours:
                x = cons.data['vars']
                for k in cons.data["data"]["dayType"]:
                    # add subtour elimination constraint for each subtour
                    for S in subtours:
                        self.model.addCons(quicksum(x[(i, j, k)] for i in S for j in S if j > i) <= len(S) - 1)
                        consadded = True

        if consadded:
            return {"result": SCIP_RESULT.CONSADDED}
        return {"result": SCIP_RESULT.FEASIBLE}

    # this is rather technical and not relevant for the exercise. to learn more see
    # https://scipopt.org/doc/html/CONS.php#CONS_FUNDAMENTALCALLBACKS
    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        pass


# 添加输出
class NewSolEvent(Eventhdlr):

    def __init__(self, vars_dict, prob_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {'vars': vars_dict, 'data': prob_data}

    # we want to be called whenever a new best sol is found
    def eventinit(self):
        self.model.catchEvent(SCIP_EVENTTYPE.BESTSOLFOUND, self)

    # stop listening to event
    def eventexit(self):
        self.model.dropEvent(SCIP_EVENTTYPE.BESTSOLFOUND, self)

    def eventexec(self, event):
        assert event.getType() == SCIP_EVENTTYPE.BESTSOLFOUND
        # get best sol
        farms = [*range(0, len(self.data["data"]["positions"]))]
        dayType = self.data["data"]["dayType"]
        sol = self.model.getBestSol()
        x = self.data['vars']
        positions = self.data["data"]["positions"]
        for k in dayType:
            edges = []
            for i in farms:
                for j in farms:
                    if j > i:
                        if self.model.getSolVal(sol, x[(i, j, k)]) > 0.5:  # variable is binary so > 0.5 --> is 1
                            edges.append((i, j))
            # make figure look nicer
            plt.figure(figsize=(10, 6), dpi=100)

            # create empty graph
            optgraph = networkx.Graph()

            # add edges
            optgraph.add_edges_from(edges)
            components = list(networkx.connected_components(optgraph))

            print(components)
            # draw the nodes, with labels in the position xy (see when we read the instance)
            networkx.draw(optgraph, node_size=300, pos=positions, with_labels=True, node_color='lightblue')

            # show drawing
            plt.show()


class MilkCollection:
    def __init__(self, prob_data):
        self.data = prob_data
        self.model = Model()

    def preprocessing(self):
        farms = [*range(0, len(self.data["positions"]))]
        dayType = self.data["dayType"]
        everyDay = self.data["everyDay"]
        otherDay = self.data["otherDay"]
        requirements = self.data["requirements"]
        positions = self.data["positions"]
        dist = {(i,j): distance(positions[i], positions[j]) for i,j in combinations(farms, 2)}
        tankerCap = self.data["tankerCap"]
        return farms, dayType, everyDay, otherDay, requirements, tankerCap, dist

    def crete_model(self):
        farms, dayType, everyDay, otherDay, requirements, tankerCap, dist = self.preprocessing()
        x, y = self.add_variables(farms, dayType, otherDay)
        self.add_constraints(x, y, farms, dayType, everyDay, otherDay, tankerCap, requirements)
        self.add_objective(x, farms, dayType, dist)
        self.model.includeEventhdlr(NewSolEvent(x, self.data),
                                    "NewSolEvent", "Prints new sol found")
        self.model.optimize()
        print(f"The optimal distance traveled is: {10 * round(self.model.getObjVal())} miles.")

    def add_variables(self, farms, dayType, otherDay):
        # Edge variables = 1, if farm 'i' is adjacent to farm 'j' on the tour of day type 'k'.
        x = dict()
        for i in farms:
            for j in farms:
                if i < j:
                    for k in dayType:
                        x[(i, j, k)] = self.model.addVar(vtype="B", name="x(%s,%s,%s)" % (i, j, k))
        # Other day variables = 1, if farm 'i' is visited on the tour of day type 'k'.
        y = dict()
        for i in otherDay:
            for k in dayType:
                y[(i, k)] = self.model.addVar(vtype="B", name="y(%s,%s)" % (i, k))
        # Symmetry constraints: copy the object (not a constraint)
        for i, j, k in list(x.keys()):
            x[(j, i, k)] = x[(i, j, k)]
        # Avoid symmetric alternative solutions
        self.model.chgVarLb(y[(otherDay[0], dayType[0])], 1)
        return x, y

    def add_constraints(self, x, y, farms, dayType, everyDay, otherDay, tankerCap, requirements):
        self.add_capacity_constraints(y, dayType, everyDay, otherDay, tankerCap, requirements)
        self.add_visited_constraints(x, y, farms, dayType, everyDay, otherDay)
        self.add_sub_tour_elimination(x)

    def add_capacity_constraints(self, y, dayType, everyDay, otherDay, tankerCap, requirements):
        # Tanker capacity constraint.
        everyDayReq = 0
        for i in everyDay:
            everyDayReq += requirements[i]
        for k in dayType:
            self.model.addCons(quicksum(requirements[i] * y[(i, k)] for i in otherDay) <= tankerCap - everyDayReq)

    def add_visited_constraints(self, x, y, farms, dayType, everyDay, otherDay):
        # Other day farms are visited on day type 1 or 2.
        for i in otherDay:
            self.model.addCons(quicksum(y[(i, k)] for k in dayType) == 1)

        # Every day constraints: two edges incident to an every day farm on tour of day type 'k'.
        for i in everyDay:
            for k in dayType:
                self.model.addCons(quicksum(x[(i, j, k)] for j in farms if j > i) +
                                   quicksum(x[(j, i, k)] for j in farms if j < i) == 2)
        # Other day constraints: two edges incident to an other day farm on tour of day type 'k'.
        for i in otherDay:
            for k in dayType:
                self.model.addCons(quicksum(x[(i, j, k)] for j in farms if j > i) +
                                   quicksum(x[(j, i, k)] for j in farms if j < i) == 2 * y[(i, k)])

    def add_sub_tour_elimination(self, x):
        # create the constraint handler
        conshdlr = SEC()
        # Add the constraint handler to SCIP. We set check priority < 0 so that only integer feasible solutions
        # are passed to the conscheck callback
        self.model.includeConshdlr(conshdlr, "TSP", "TSP subtour eliminator", chckpriority=-10, enfopriority=-10)
        # create a subtour elimination constraint
        cons = conshdlr.createCons("no_subtour_cons", x, self.data)
        # add constraint to SCIP
        self.model.addPyCons(cons)

    def add_objective(self, x, farms, dayType, dist):
        self.model.setObjective(quicksum(dist[i, j] * x[(i, j, k)]
                                         for i in farms
                                         for j in farms
                                         for k in dayType if i < j))


if __name__ == '__main__':
    milk_data = data
    prob = MilkCollection(milk_data)
    prob.crete_model()