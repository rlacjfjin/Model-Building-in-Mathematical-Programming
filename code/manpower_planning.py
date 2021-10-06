from pyscipopt import Model, quicksum

from data.manpower_planning.data import data
import pandas as pd
import numpy as np


class ManpowerPlanning:
    def __init__(self, data):
        self.data = data
        self.model = Model()
        self.hire = dict()
        self.part_time = dict()
        self.workforce = dict()
        self.layoff = dict()
        self.excess = dict()
        self.train = dict()

    def create_model(self):
        years = self.data["years"]
        skills = self.data["skills"]
        self.add_variables(years, skills)
        self.add_constraints(years, skills)
        # self.add_objective(years, skills)
        self.add_cost_objective(years,skills)
        self.model.optimize()
        self.print_results(years, skills)

    def add_variables(self, years, skills):
        max_hiring = self.data["max_hiring"]
        max_parttime = self.data["max_parttime"]
        for year in years:
            for skill in skills:
                self.hire[year, skill] = self.model.addVar(name=f"Hire_{year}_{skill}", ub=max_hiring[year, skill])
                self.part_time[year, skill] = self.model.addVar(name=f"Part_time_{year}_{skill}", ub=max_parttime)
                self.workforce[year, skill] = self.model.addVar(name=f"Available_{year}_{skill}")
                self.layoff[year, skill] = self.model.addVar(name=f"Layoff_{year}_{skill}")
                self.excess[year, skill] = self.model.addVar(name=f"Overmanned_{year}_{skill}")
                for other_skill in skills:
                    self.train[year, skill, other_skill] = self.model.addVar(
                        name=f"Train_{year}_{skill}_{other_skill}")

    def add_constraints(self, years, skills):
        self.add_balance_constraints(years, skills)
        self.add_skill_constraints(years)
        self.add_overmanning_constraints(years, skills)
        self.add_demand_constraints(years, skills)

    def add_balance_constraints(self, years, skills):
        veteran_attrition = self.data["veteran_attrition"]
        curr_workforce = self.data["curr_workforce"]
        rookie_attrition = self.data["rookie_attrition"]
        demoted_attrition = self.data["demoted_attrition"]
        for year in years:
            for skill in skills:
                if year == 1:
                    pre_employed = curr_workforce[skill]
                else:
                    pre_employed = self.workforce[year - 1, skill]
                pre_employed = (1 - veteran_attrition[skill]) * pre_employed
                cur_recruited = (1 - rookie_attrition[skill]) * self.hire[year, skill]
                cur_retrained = quicksum(
                    (1 - veteran_attrition[skill]) * self.train[year, skill1, skill] -
                    self.train[year, skill, skill1] for skill1 in skills if skill1 < skill)
                cur_retrained += quicksum(
                    (1 - demoted_attrition) * self.train[year, skill1, skill] -
                    self.train[year, skill, skill1] for skill1 in skills if skill1 > skill)
                cur_redundant = self.layoff[year, skill]
                self.model.addCons(self.workforce[year, skill] ==
                                   pre_employed + cur_recruited + cur_retrained - cur_redundant)

    def add_skill_constraints(self, years):
        max_train_unskilled = self.data["max_train_unskilled"]
        max_train_semiskilled = self.data["max_train_semiskilled"]
        for year in years:
            # Unskilled_training
            self.model.addCons(self.train[year, "s1", "s2"] <= max_train_unskilled)
            self.model.addCons(self.train[year, "s1", "s3"] == 0)
            # Semiskilled training
            self.model.addCons(self.train[year, "s2", "s3"] <=
                               max_train_semiskilled * self.workforce[year, "s3"])

    def add_overmanning_constraints(self, years, skills):
        max_overmanning = self.data["max_overmanning"]
        for year in years:
            self.model.addCons(quicksum(self.excess[year, skill] for skill in skills)
                               <= max_overmanning)

    def add_demand_constraints(self, years, skills):
        parttime_cap = self.data["parttime_cap"]
        demand = self.data["demand"]
        for year in years:
            for skill in skills:
                self.model.addCons(self.workforce[year, skill] == demand[year, skill] +
                                   self.excess[year, skill] + parttime_cap * self.part_time[year, skill])

    def add_objective(self, years, skills):
        obj = quicksum(self.layoff[year, skill] for year in years for skill in skills)
        self.model.setObjective(obj, "minimize")

    def add_cost_objective(self,years,skills):
        training_cost = self.data["training_cost"]
        layoff_cost = self.data["layoff_cost"]
        parttime_cost = self.data["parttime_cost"]
        overmanning_cost = self.data["overmanning_cost"]
        obj2 = quicksum(
            (training_cost[level] * self.train[year, level, skills[skills.index(level) + 1]] if level < 's3' else 0)
            + layoff_cost[level] * self.layoff[year, level]
            + parttime_cost[level] * self.part_time[year, level]
            + overmanning_cost[level] * self.excess[year, level] for year in years for level in skills)
        self.model.setObjective(obj2)

    def print_results(self, years, skills):
        rows = years.copy()
        columns = skills.copy()
        hire_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
        layoff_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
        parttime_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
        excess_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

        for year, skill in self.hire.keys():
            val = self.model.getVal(self.hire[year, skill])
            if val > 0:
                hire_plan.loc[year, skill] = np.round(val, 1)
            val = self.model.getVal(self.layoff[year, skill])
            if val > 0:
                layoff_plan.loc[year, skill] = np.round(val, 1)
            val = self.model.getVal(self.part_time[year, skill])
            if val > 0:
                parttime_plan.loc[year, skill] = np.round(val, 1)
            val = self.model.getVal(self.excess[year, skill])
            if val > 0:
                excess_plan.loc[year, skill] = np.round(val, 1)

        columns = ['{0} to {1}'.format(level1, level2) for level1 in skills for level2 in skills if level1 != level2]
        train_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

        for year, level1, level2 in self.train.keys():
            col = '{0} to {1}'.format(level1, level2)
            val = self.model.getVal(self.train[year, level1, level2])
            if val > 0:
                train_plan.loc[year, col] = np.round(val, 1)
        print(hire_plan)
        print(train_plan)
        print(layoff_plan)
        print(parttime_plan)
        print(excess_plan)


if __name__ == '__main__':
    prob_data = data
    prob = ManpowerPlanning(prob_data)
    prob.create_model()
