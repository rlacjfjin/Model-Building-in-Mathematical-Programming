
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

oils = ["VEG1", "VEG2", "OIL1", "OIL2", "OIL3"]

cost = {
    ('Jan', 'VEG1'): 110,
    ('Jan', 'VEG2'): 120,
    ('Jan', 'OIL1'): 130,
    ('Jan', 'OIL2'): 110,
    ('Jan', 'OIL3'): 115,
    ('Feb', 'VEG1'): 130,
    ('Feb', 'VEG2'): 130,
    ('Feb', 'OIL1'): 110,
    ('Feb', 'OIL2'): 90,
    ('Feb', 'OIL3'): 115,
    ('Mar', 'VEG1'): 110,
    ('Mar', 'VEG2'): 140,
    ('Mar', 'OIL1'): 130,
    ('Mar', 'OIL2'): 100,
    ('Mar', 'OIL3'): 95,
    ('Apr', 'VEG1'): 120,
    ('Apr', 'VEG2'): 110,
    ('Apr', 'OIL1'): 120,
    ('Apr', 'OIL2'): 120,
    ('Apr', 'OIL3'): 125,
    ('May', 'VEG1'): 100,
    ('May', 'VEG2'): 120,
    ('May', 'OIL1'): 150,
    ('May', 'OIL2'): 110,
    ('May', 'OIL3'): 105,
    ('Jun', 'VEG1'): 90,
    ('Jun', 'VEG2'): 100,
    ('Jun', 'OIL1'): 140,
    ('Jun', 'OIL2'): 80,
    ('Jun', 'OIL3'): 135
}


hardness = {"VEG1": 8.8, "VEG2": 6.1, "OIL1": 2.0, "OIL2": 4.2, "OIL3": 5.0}



data = dict()
data["months"] = months
data["oils"] = oils
data["cost"] = cost
data["hardness"] = hardness
data["price"] = 150
data["init_store"] = 500
data["target_store"] = 500
data["veg_cap"] = 200
data["oil_cap"] = 250

data["min_hardness"] = 3
data["max_hardness"] = 6
data["holding_cost"] = 5
data["max_ingredients"] = 3
data["min_consume"] = 20