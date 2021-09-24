import math

import networkx
from pyscipopt import Model, Heur, Eventhdlr, Conshdlr, quicksum, SCIP_RESULT, SCIP_EVENTTYPE, SCIP_HEURTIMING
import matplotlib.pyplot as plt


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def read_instance(name):
    x = {}
    y = {}
    xy = {}
    with open(name) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            sp = line.split()
            if len(sp) > 0 and sp[0].isnumeric():
                assert len(sp) == 3
                assert is_number(sp[1]) and is_number(sp[2])
                x[cnt] = float(sp[1])
                y[cnt] = float(sp[2])

                # dictionary from node to its coordinates: we use this for plotting the graph
                xy[cnt] = (x[cnt], y[cnt])
                cnt += 1
            line = fp.readline()
    return x, y, xy


def distance(x1, y1, x2, y2):
    """distance: euclidean distance between (x1,y1) and (x2,y2)"""
    return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)


def compute_distance_matrix(x, y):
    n = len(x)
    V = range(1, n)
    c = {}
    for i in V:
        for j in V:
            if j > i:
                c[i, j] = distance(x[i], y[i], x[j], y[j])
    return c


# lazy constraints??
class SEC(Conshdlr):
    # method for creating a constraint of this constraint handler type
    def createCons(self, name, variables):
        model = self.model
        cons = model.createCons(self, name)

        # data relevant for the constraint; in this case we only need to know which
        # variables cannot form a subtour
        cons.data = {}
        cons.data['vars'] = variables
        return cons

    # find subtours in the graph induced by the edges {i,j} for which x[i,j] is positive
    # at the given solution; when solution is None, the LP solution is used
    def find_subtours(self, cons, solution=None):
        edges = []
        x = cons.data['vars']

        for (i, j) in x:
            if self.model.getSolVal(solution, x[i, j]) > 0.5:
                edges.append((i, j))

        G = networkx.Graph()
        G.add_edges_from(edges)
        components = list(networkx.connected_components(G))

        if len(components) == 1:
            return []
        else:
            return components

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

                # add subtour elimination constraint for each subtour
                for S in subtours:
                    self.model.addCons(quicksum(x[i, j] for i in S for j in S if j > i) <= len(S) - 1)
                    consadded = True

        if consadded:
            return {"result": SCIP_RESULT.CONSADDED}
        else:
            return {"result": SCIP_RESULT.FEASIBLE}

    # this is rather technical and not relevant for the exercise. to learn more see
    # https://scipopt.org/doc/html/CONS.php#CONS_FUNDAMENTALCALLBACKS
    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        pass


# 添加启发式
class TwoOpt(Heur):

    def __init__(self, costs, vars_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}
        self.data['costs'] = costs
        self.data['vars'] = vars_dict
        self.data['primalbound'] = 0.0

    # given an edge = (a, b), returns edge in model, i.e. (a,b) if a < b or (b,a) if b > a
    def real_edge(self, edge):
        assert edge[0] != edge[1]
        return tuple(sorted(edge))

    def heurexec(self, heurtiming, nodeinfeasible):

        # only run if we have a new solution
        primalbound = self.model.getPrimalbound()
        # print("calling 2opt primalbound and stored primal = ", primalbound, self.data['primalbound'])
        if self.model.isInfinity(primalbound) or primalbound == self.data['primalbound']:
            return {"result": SCIP_RESULT.DIDNOTRUN}

        self.data['primalbound'] = primalbound

        x = self.data['vars']
        c = self.data['costs']
        sol = self.model.getBestSol()

        # Build directed edges in the path represented by solution:
        # To compute the path, we store for each node the pair of nodes that it is connected to.
        # Then just traverse the nodes.
        adj = {}
        for (i, j) in x:
            if self.model.getSolVal(sol, x[i, j]) > 0.5:  # variable is binary so > 0.5 --> is 1
                if i in adj:
                    adj[i].append(j)
                else:
                    adj[i] = [j]
                if j in adj:
                    adj[j].append(i)
                else:
                    adj[j] = [i]

        # if there are not enough nodes do nothing
        if len(adj) < 4:
            return {"result": SCIP_RESULT.DIDNOTRUN}

        # compute path
        print("computing path: adjacency list", adj)
        edges = []
        prev_node = None
        curr_node = 1
        while True:
            next_node = adj[curr_node][0]
            if next_node == prev_node:
                next_node = adj[curr_node][1]
            edges.append((curr_node, next_node))
            prev_node = curr_node
            curr_node = next_node
            if curr_node == 1:
                break

        # loop over non-adjacent edges
        print("optimal path is ", edges)

        for edge1 in edges:
            for edge2 in edges:
                # skip adjacent edges
                if edge1[0] in edge2 or edge1[1] in edge2:
                    continue
                e1 = tuple(sorted(edge1))  # in our data structures edges are (i,j) with i < j
                e2 = tuple(sorted(edge2))
                newe1 = tuple(sorted((edge1[0], edge2[0])))
                newe2 = tuple(sorted((edge1[1], edge2[1])))

                # if the uncrossing gives a better solution
                if (c[newe1] + c[newe2] < c[e1] + c[e2]
                        and x[e1].getUbGlobal() >= 0.5 and x[e2].getUbGlobal() >= 0.5
                        and x[newe1].getLbGlobal() <= 0.5 and x[newe2].getLbGlobal() <= 0.5):
                    # create new sol
                    newsol = self.model.createSol(self)
                    # copy values from old sol
                    for e in edges:
                        newsol[x[tuple(sorted(e))]] = 1.0
                    # swap edge in sol
                    newsol[x[e1]] = 0.0
                    newsol[x[e2]] = 0.0
                    newsol[x[newe1]] = 1.0
                    newsol[x[newe2]] = 1.0

                    # add sol
                    stored = self.model.addSol(newsol)
                    assert (stored == True)
                    return {"result": SCIP_RESULT.FOUNDSOL}

        return {"result": SCIP_RESULT.DIDNOTFIND}


# 添加输出
class NewSolEvent(Eventhdlr):

    def __init__(self, vars_dict, coords_nodes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {'vars': vars_dict, 'xy': coords_nodes}

    # we want to be called whenever a new best sol is found
    def eventinit(self):
        self.model.catchEvent(SCIP_EVENTTYPE.BESTSOLFOUND, self)

    # stop listening to event
    def eventexit(self):
        self.model.dropEvent(SCIP_EVENTTYPE.BESTSOLFOUND, self)

    def eventexec(self, event):
        assert event.getType() == SCIP_EVENTTYPE.BESTSOLFOUND
        # get best sol
        sol = self.model.getBestSol()
        # get vars and position of vertices
        x = self.data['vars']
        xy = self.data['xy']

        # plot solution
        # Collect the edges: if the value of x[i,j] is 1, then the edge (i,j) is in the solution
        edges = []
        for (i, j) in x:
            if self.model.getSolVal(sol, x[i, j]) > 0.5:  # variable is binary so > 0.5 --> is 1
                edges.append((i, j))

        # make figure look nicer
        plt.figure(figsize=(10, 6), dpi=100)

        # create empty graph
        optgraph = networkx.Graph()

        # add edges
        optgraph.add_edges_from(edges)

        # draw the nodes, with labels in the position xy (see when we read the instance)
        networkx.draw(optgraph, node_size=300, pos=xy, with_labels=True, node_color='lightblue')

        # show drawing
        plt.show()


class TSP:
    def __init__(self, xcoords, ycoords):
        self.xcoords = xcoords
        self.ycoords = ycoords
        self.cost = compute_distance_matrix(xcoords, ycoords)
        self.model = Model()

    def createVars(self, V):
        x = {}
        for i in V:
            for j in V:
                if j > i:
                    x[i, j] = self.model.addVar(name="x(%s,%s)" % (i, j), vtype='B')
        return x

    def setObjective(self, x):
        self.model.setObjective(quicksum(self.cost[i, j] * x[i, j] for (i, j) in x), "minimize")

    def addComeAndGoConstraints(self, V, x):
        for j in V:
            self.model.addCons(quicksum(x[i, j] for i in V if i < j) + \
                               quicksum(x[j, i] for i in V if i > j) == 2, "ComeAndGo(%s)" % j)

    def addSubtourElimination(self, x):
        # create the constraint handler
        conshdlr = SEC()

        # Add the constraint handler to SCIP. We set check priority < 0 so that only integer feasible solutions
        # are passed to the conscheck callback
        self.model.includeConshdlr(conshdlr, "TSP", "TSP subtour eliminator", chckpriority=-10, enfopriority=-10)

        # create a subtour elimination constraint
        cons = conshdlr.createCons("no_subtour_cons", x)

        # add constraint to SCIP
        self.model.addPyCons(cons)

    def setupModel(self):
        V = range(1, len(self.xcoords))
        x = self.createVars(V)
        self.setObjective(x)
        self.addComeAndGoConstraints(V, x)
        self.addSubtourElimination(x)
        self.model.includeEventhdlr(NewSolEvent(x, xy), "NewSolEvent", "Prints new sol found")
        self.model.includeHeur(TwoOpt(self.cost, x), "2opt", "2 Opt Heuristic", "K",
                               timingmask=SCIP_HEURTIMING.AFTERLPNODE)

        self.model.optimize()


if __name__ == '__main__':
    instance = '../data/tspdata/berlin52.tsp'
    xcoords, ycoords, xy = read_instance(instance)
    tsp = TSP(xcoords, ycoords)
    tsp.setupModel()
