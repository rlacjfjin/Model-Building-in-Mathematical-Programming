from pyscipopt import Model, quicksum

from data.DEA.data import data


class DEA:
    def __init__(self, prob_data):
        self.data = prob_data
        self.model = Model()

    def preprocessing(self):
        input = self.data["input"]
        output = self.data["output"]
        dmu = self.data["dmus"]
        invalue = self.data["invalue"]
        outvalue = self.data["outvalue"]
        return input, output, dmu, outvalue, invalue

    def create_model(self, target):
        input, output, dmu, outvalue, invalue = self.preprocessing()
        u = dict()
        v = dict()
        # 添加变量
        for i in input:
            v[i] = self.model.addVar(name="inputWeight(%s)" % i)
        for i in output:
            u[i] = self.model.addVar(name="outputWeight(%s)" % i)
        # 添加约束
        ## Efficiency ratio
        for j in dmu:
            self.model.addCons(quicksum(outvalue[j][r] * u[r] for r in output) -
                               quicksum(invalue[j][i] * v[i] for i in input) <= 0)

        ## normalization
        self.model.addCons(quicksum(invalue[target][i] * v[i] for i in input) == 1)

        # Objective function
        self.model.setObjective(quicksum(outvalue[target][r] * u[r] for r in output), "maximize")
        self.model.optimize()
        # Print results
        print(f"\nThe efficiency of target DMU {target} is {round(self.model.getObjVal(), 3)}")

        print("__________________________________________________________________")
        print(f"The weights for the inputs are:")
        for i in input:
            print(f"For {i}: {round(self.model.getVal(v[i]), 3)} ")

        print("__________________________________________________________________")
        print(f"The weights for the outputs are")
        for r in output:
            print(f"For {r} is: {round(self.model.getVal(u[r]), 3)} ")
        print("__________________________________________________________________\n\n")
        obj = self.model.getObjVal()
        self.model.freeTransform()
        return obj


if __name__ == '__main__':
    dea_data = data
    dmus = dea_data["dmus"]
    prob = DEA(dea_data)
    performance = {}
    for h in dmus:
        performance[h] = prob.create_model(h)
    # Sorting garages in descending efficiency number
    sorted_performance = {k: v for k, v in sorted(performance.items(), key=lambda item: item[1], reverse=True)}

    efficient = []
    inefficient = []

    for h in sorted_performance.keys():
        if sorted_performance[h] >= 0.9999999:
            efficient.append(h)
        if sorted_performance[h] < 0.9999999:
            inefficient.append(h)

    print('____________________________________________')
    print(f"The efficient DMUs are:")
    for eff in efficient:
        print(f"The performance value of DMU {eff} is: {round(performance[eff], 3)}")

    print('____________________________________________')
    print(f"The inefficient DMUs are:")
    for ine in inefficient:
        print(f"The performance value of DMU {ine} is: {round(performance[ine], 3)}")