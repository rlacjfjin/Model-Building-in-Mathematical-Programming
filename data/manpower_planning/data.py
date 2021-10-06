# Parameters

years = [1, 2, 3]
skills = ['s1', 's2', 's3']

curr_workforce = {'s1': 2000, 's2': 1500, 's3': 1000}
demand = {
    (1, 's1'): 1000,
    (1, 's2'): 1400,
    (1, 's3'): 1000,
    (2, 's1'): 500,
    (2, 's2'): 2000,
    (2, 's3'): 1500,
    (3, 's1'): 0,
    (3, 's2'): 2500,
    (3, 's3'): 2000
}
rookie_attrition = {'s1': 0.25, 's2': 0.20, 's3': 0.10}
veteran_attrition = {'s1': 0.10, 's2': 0.05, 's3': 0.05}
demoted_attrition = 0.50
max_hiring = {
    (1, 's1'): 500,
    (1, 's2'): 800,
    (1, 's3'): 500,
    (2, 's1'): 500,
    (2, 's2'): 800,
    (2, 's3'): 500,
    (3, 's1'): 500,
    (3, 's2'): 800,
    (3, 's3'): 500
}
max_overmanning = 150
max_parttime = 50
parttime_cap = 0.50
max_train_unskilled = 200
max_train_semiskilled = 0.25

training_cost = {'s1': 400, 's2': 500}
layoff_cost = {'s1': 200, 's2': 500, 's3': 500}
parttime_cost = {'s1': 500, 's2': 400, 's3': 400}
overmanning_cost = {'s1': 1500, 's2': 2000, 's3': 3000}

data = dict()
data["years"] = years
data["skills"] = skills
data["curr_workforce"] = curr_workforce
data["demand"] = demand
data["max_hiring"] = max_hiring
data["max_overmanning"] = max_overmanning
data["max_parttime"] = max_parttime
data["parttime_cap"] = parttime_cap
data["max_train_unskilled"] = max_train_unskilled
data["max_train_semiskilled"] = max_train_semiskilled
data["rookie_attrition"] = rookie_attrition
data["veteran_attrition"] = veteran_attrition
data["demoted_attrition"] = demoted_attrition
data["training_cost"] = training_cost
data["layoff_cost"] = layoff_cost
data["parttime_cost"] = parttime_cost
data["overmanning_cost"] = overmanning_cost
