classes = ['First', 'Business', 'Economy']
options = ['option1', 'option2', 'option3']
scenarios = ['sce1', 'sce2', 'sce3']
price1 = {
    ('First', 'option1'): 1200,
    ('Business', 'option1'): 900,
    ('Economy', 'option1'): 500,
    ('First', 'option2'): 1000,
    ('Business', 'option2'): 800,
    ('Economy', 'option2'): 300,
    ('First', 'option3'): 950,
    ('Business', 'option3'): 600,
    ('Economy', 'option3'): 200,
}
price2 = {
    ('First', 'option1'): 1400,
    ('Business', 'option1'): 1100,
    ('Economy', 'option1'): 700,
    ('First', 'option2'): 1300,
    ('Business', 'option2'): 900,
    ('Economy', 'option2'): 400,
    ('First', 'option3'): 1150,
    ('Business', 'option3'): 750,
    ('Economy', 'option3'): 350,
}
price3 = {
    ('First', 'option1'): 1500,
    ('Business', 'option1'): 820,
    ('Economy', 'option1'): 480,
    ('First', 'option2'): 900,
    ('Business', 'option2'): 800,
    ('Economy', 'option2'): 470,
    ('First', 'option3'): 850,
    ('Business', 'option3'): 500,
    ('Economy', 'option3'): 450,
}
prob = {'sce1': 0.1, 'sce2': 0.7, 'sce3': 0.2}
demand_pred1 = {
    ('sce1', 'First', 'option1'): 10,
    ('sce1', 'Business', 'option1'): 20,
    ('sce1', 'Economy', 'option1'): 45,
    ('sce1', 'First', 'option2'): 15,
    ('sce1', 'Business', 'option2'): 25,
    ('sce1', 'Economy', 'option2'): 55,
    ('sce1', 'First', 'option3'): 20,
    ('sce1', 'Business', 'option3'): 35,
    ('sce1', 'Economy', 'option3'): 60,
    ('sce2', 'First', 'option1'): 20,
    ('sce2', 'Business', 'option1'): 40,
    ('sce2', 'Economy', 'option1'): 50,
    ('sce2', 'First', 'option2'): 25,
    ('sce2', 'Business', 'option2'): 42,
    ('sce2', 'Economy', 'option2'): 52,
    ('sce2', 'First', 'option3'): 35,
    ('sce2', 'Business', 'option3'): 45,
    ('sce2', 'Economy', 'option3'): 63,
    ('sce3', 'First', 'option1'): 45,
    ('sce3', 'Business', 'option1'): 45,
    ('sce3', 'Economy', 'option1'): 55,
    ('sce3', 'First', 'option2'): 50,
    ('sce3', 'Business', 'option2'): 46,
    ('sce3', 'Economy', 'option2'): 56,
    ('sce3', 'First', 'option3'): 60,
    ('sce3', 'Business', 'option3'): 47,
    ('sce3', 'Economy', 'option3'): 64,
}
demand_pred2 = {
    ('sce1', 'First', 'option1'): 20,
    ('sce1', 'Business', 'option1'): 42,
    ('sce1', 'Economy', 'option1'): 50,
    ('sce1', 'First', 'option2'):  25,
    ('sce1', 'Business', 'option2'): 45,
    ('sce1', 'Economy', 'option2'):  52,
    ('sce1', 'First', 'option3'):  35,
    ('sce1', 'Business', 'option3'): 46,
    ('sce1', 'Economy', 'option3'): 60,
    ('sce2', 'First', 'option1'): 10,
    ('sce2', 'Business', 'option1'): 50,
    ('sce2', 'Economy', 'option1'): 60,
    ('sce2', 'First', 'option2'): 40,
    ('sce2', 'Business', 'option2'):  60,
    ('sce2', 'Economy', 'option2'): 65,
    ('sce2', 'First', 'option3'): 50,
    ('sce2', 'Business', 'option3'): 80,
    ('sce2', 'Economy', 'option3'):90,
    ('sce3', 'First', 'option1'): 50,
    ('sce3', 'Business', 'option1'):  20,
    ('sce3', 'Economy', 'option1'): 10,
    ('sce3', 'First', 'option2'):  55,
    ('sce3', 'Business', 'option2'): 30,
    ('sce3', 'Economy', 'option2'): 40,
    ('sce3', 'First', 'option3'): 80,
    ('sce3', 'Business', 'option3'): 50,
    ('sce3', 'Economy', 'option3'):  60,
}
demand_pred3 = {
    ('sce1', 'First', 'option1'): 30,
    ('sce1', 'Business', 'option1'):  40,
    ('sce1', 'Economy', 'option1'): 50,
    ('sce1', 'First', 'option2'):  35,
    ('sce1', 'Business', 'option2'):  50,
    ('sce1', 'Economy', 'option2'):  60,
    ('sce1', 'First', 'option3'):  40,
    ('sce1', 'Business', 'option3'): 55,
    ('sce1', 'Economy', 'option3'):  80,
    ('sce2', 'First', 'option1'):  30,
    ('sce2', 'Business', 'option1'):  10,
    ('sce2', 'Economy', 'option1'):  50,
    ('sce2', 'First', 'option2'): 40,
    ('sce2', 'Business', 'option2'): 40,
    ('sce2', 'Economy', 'option2'):  60,
    ('sce2', 'First', 'option3'):60,
    ('sce2', 'Business', 'option3'): 45,
    ('sce2', 'Economy', 'option3'):  70,
    ('sce3', 'First', 'option1'):  50,
    ('sce3', 'Business', 'option1'):  40,
    ('sce3', 'Economy', 'option1'):  60,
    ('sce3', 'First', 'option2'):  70,
    ('sce3', 'Business', 'option2'):  45,
    ('sce3', 'Economy', 'option2'):  65,
    ('sce3', 'First', 'option3'):  80,
    ('sce3', 'Business', 'option3'):  60,
    ('sce3', 'Economy', 'option3'):  70
}
demand_actual1 = {
    ('First', 'option1'): 25,
    ('Business', 'option1'): 50,
    ('Economy', 'option1'): 50,
    ('First', 'option2'): 30,
    ('Business', 'option2'): 40,
    ('Economy', 'option2'): 53,
    ('First', 'option3'): 40,
    ('Business', 'option3'): 45,
    ('Economy', 'option3'): 65,
}
demand_actual2 = {
    ('First', 'option1'):  22,
    ('Business', 'option1'):45,
    ('Economy', 'option1'): 50,
    ('First', 'option2'): 45,
    ('Business', 'option2'): 55,
    ('Economy', 'option2'):  60,
    ('First', 'option3'): 50,
    ('Business', 'option3'): 75,
    ('Economy', 'option3'): 80,
}
demand_actual3 = {
    ('First', 'option1'):  45,
    ('Business', 'option1'):  20,
    ('Economy', 'option1'): 55,
    ('First', 'option2'): 60,
    ('Business', 'option2'):  40,
    ('Economy', 'option2'):  60,
    ('First', 'option3'):  75,
    ('Business', 'option3'): 50,
    ('Economy', 'option3'): 75
}
cap = {'First': 37, 'Business': 38, 'Economy': 47}
cost = 50000
data = dict()
data["classes"] = classes
data["options"] = options
data["scenarios"] = scenarios
data["price_1"] = price1
data["price_2"] = price2
data["price_3"] = price3
data["probability"] = prob
data["demand_pred_1"] = demand_pred1
data["demand_pred_2"] = demand_pred2
data["demand_pred_3"] = demand_pred3
data["demand_actual_1"] = demand_actual1
data["demand_actual_2"] = demand_actual2
data["demand_actual_3"] = demand_actual3
data["cap"] = cap
data["cost"] = cost
