import pyscipopt as scip
import matplotlib.pyplot as plt


class ThreeDimTicTacToe:
    def __init__(self, m=14, dim=3):
        self.m = m
        self.dim = dim
        self.model = scip.Model()
        # define variables
        self.delta = dict()
        self.gamma = dict()

    def create_lines(self):
        lines = []
        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.dim):
                    if i == 0:
                        lines.append(((0, j, k), (1, j, k), (2, j, k)))
                    if j == 0:
                        lines.append(((i, 0, k), (i, 1, k), (i, 2, k)))
                    if k == 0:
                        lines.append(((i, j, 0), (i, j, 1), (i, j, 2)))
                    if i == 0 and j == 0:
                        lines.append(((0, 0, k), (1, 1, k), (2, 2, k)))
                    if i == 0 and j == 2:
                        lines.append(((0, 2, k), (1, 1, k), (2, 0, k)))
                    if i == 0 and k == 0:
                        lines.append(((0, j, 0), (1, j, 1), (2, j, 2)))
                    if i == 0 and k == 2:
                        lines.append(((0, j, 2), (1, j, 1), (2, j, 0)))
                    if j == 0 and k == 0:
                        lines.append(((i, 0, 0), (i, 1, 1), (i, 2, 2)))
                    if j == 0 and k == 2:
                        lines.append(((i, 0, 2), (i, 1, 1), (i, 2, 0)))
        lines.append(((0, 0, 0), (1, 1, 1), (2, 2, 2)))
        lines.append(((2, 0, 0), (1, 1, 1), (0, 2, 2)))
        lines.append(((0, 2, 0), (1, 1, 1), (2, 0, 2)))
        lines.append(((0, 0, 2), (1, 1, 1), (2, 2, 0)))
        return lines

    def create_mip_model(self):
        lines = self.create_lines()
        size = range(self.dim)
        # add variables
        for i in size:
            for j in size:
                for k in size:
                    self.delta[(i, j, k)] = self.model.addVar(vtype="B", name="pos(%s,%s,%s)" % (i, j, k))
        for line in lines:
            self.gamma[line] = self.model.addVar(vtype="B")

        # add constraints
        self.model.addCons(scip.quicksum(self.delta[(i, j, k)] for i in size for j in size for k in size) == self.m)
        for line in lines:
            self.model.addCons(self.delta[line[0]] + self.delta[line[1]] + self.delta[line[2]] -
                               self.gamma[line] <= 2)
            self.model.addCons(self.delta[line[0]] + self.delta[line[1]] + self.delta[line[2]] +
                               self.gamma[line] >= 1)
        obj = scip.quicksum(self.gamma[line] for line in lines)
        self.model.setObjective(obj)

    def solve_and_analysis(self):
        self.model.optimize()
        fig, ax = plt.subplots(1, 3, figsize=(10, 5))
        for i in range(3):
            ax[i].grid()
            ax[i].set_xticks(range(4))
            ax[i].set_yticks(range(4))
            ax[i].tick_params(labelleft=False, labelbottom=False)

        for cell in self.delta.keys():
            if self.model.getVal(self.delta[cell]) > 0.5:
                ax[cell[0]].add_patch(plt.Rectangle((cell[1], cell[2]), 1, 1))

        plt.show()


if __name__ == '__main__':
    problem = ThreeDimTicTacToe()
    problem.create_mip_model()
    problem.solve_and_analysis()
