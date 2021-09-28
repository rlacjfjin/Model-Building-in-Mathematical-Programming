dairy = ['milk', 'butter', 'cheese1', 'cheese2']
components = ['fat', 'dryMatter']

qtyper = {
    ('fat', 'milk'): 0.04,
    ('fat', 'butter'): 0.8,
    ('fat', 'cheese1'): 0.35,
    ('fat', 'cheese2'): 0.25,
    ('dryMatter', 'milk'): 0.09,
    ('dryMatter', 'butter'): 0.02,
    ('dryMatter', 'cheese1'): 0.3,
    ('dryMatter', 'cheese2'): 0.4
}

capacity = {
    'fat': 600,
    'dryMatter': 750
}
consumption = {
    'milk': 4.82,
    'butter': 0.32,
    'cheese1': 0.21,
    'cheese2': 0.07,
}
price = {
    'milk': 0.297,
    'butter': 0.72,
    'cheese1': 1.05,
    'cheese2': 0.815,
}
elasticity = {
    'milk': 0.4,
    'butter': 2.7,
    'cheese1': 1.1,
    'cheese2': 0.4
}

elasticity12 = 0.1
elasticity21 = 0.4

priceIndex = 1.939

data = dict()
data["dairy"] = dairy
data["components"] = components
data["qtyper"] = qtyper
data["capacity"] = capacity
data["consumption"] = consumption
data["price"] = price
data["elasticity"] = elasticity
data["elasticity12"] = elasticity12
data["elasticity21"] = elasticity21
data["priceIndex"] = priceIndex
