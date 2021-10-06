from itertools import product

inout_prod = {
    ('coal', 'coal'): 0.1,
    ('coal', 'steel'): 0.5,
    ('coal', 'transport'): 0.4,
    ('steel', 'coal'): 0.1,
    ('steel', 'steel'): 0.1,
    ('steel', 'transport'): 0.2,
    ('transport', 'coal'): 0.2,
    ('transport', 'steel'): 0.1,
    ('transport', 'transport'): 0.2
}
labor_prod = dict({'coal': 0.6,
                   'steel': 0.3,
                   'transport': 0.2})
inout_cap = {
    ('coal', 'coal'): 0.1,
    ('coal', 'steel'): 0.7,
    ('coal', 'transport'): 0.9,
    ('steel', 'coal'): 0.1,
    ('steel', 'steel'): 0.1,
    ('steel', 'transport'): 0.2,
    ('transport', 'coal'): 0.2,
    ('transport', 'steel'): 0.1,
    ('transport', 'transport'): 0.2
}
labor_extra_cap = dict({'coal': 0.4,
                        'steel': 0.2,
                        'transport': 0.1})
industries = {'coal','steel','transport'}
stock0 = {
    'coal': 250,
    'steel': 180,
    'transport': 200,
}
capacity0 = {
    'coal':  300,
    'steel':350,
    'transport':280,
}
demand = {
    'coal': 60,
    'steel': 60,
    'transport': 30,
}
horizon = [1, 2, 3, 4, 5, 6]

data = dict()
data["inout_prod"] = inout_prod
data["labor_prod"] = labor_prod
data["inout_cap"] = inout_cap
data["labor_extra_cap"] = labor_extra_cap
data["industries"] = industries
data["stock0"] = stock0
data["capacity0"] = capacity0
data["demand"] = demand
data["horizon"] = horizon
