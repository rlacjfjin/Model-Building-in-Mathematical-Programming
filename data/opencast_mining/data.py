profit = {
    '1': 0,
    '2': 0,
    '3': 0,
    '4': -1500,
    '5': 0,
    '6': 1000,
    '7': 0,
    '8': -1500,
    '9': -1000,
    '10': -1000,
    '11': -1500,
    '12': -2000,
    '13': -1500,
    '14': -1500,
    '15': -2000,
    '16': -2500,
    '17': 2000,
    '18': 2000,
    '19': -2000,
    '20': 0,
    '21': 0,
    '22': -4000,
    '23': -2000,
    '24': -2000,
    '25': -5000,
    '26': 16000,
    '27': 4000,
    '28': 2000,
    '29': 0,
    '30': 2000
}
blocks = list(profit.keys())

value = {
    ('30', '26'): 1,
    ('30', '27'): 1,
    ('30', '28'): 1,
    ('30', '29'): 1,
    ('29', '21'): 1,
    ('29', '22'): 1,
    ('29', '24'): 1,
    ('29', '25'): 1,
    ('28', '20'): 1,
    ('28', '21'): 1,
    ('28', '23'): 1,
    ('28', '24'): 1,
    ('27', '18'): 1,
    ('27', '19'): 1,
    ('27', '21'): 1,
    ('27', '22'): 1,
    ('26', '17'): 1,
    ('26', '18'): 1,
    ('26', '20'): 1,
    ('26', '21'): 1,
    ('25', '11'): 1,
    ('25', '12'): 1,
    ('25', '15'): 1,
    ('25', '16'): 1,
    ('24', '10'): 1,
    ('24', '11'): 1,
    ('24', '14'): 1,
    ('24', '15'): 1,
    ('23', '9'): 1,
    ('23', '10'): 1,
    ('23', '13'): 1,
    ('23', '14'): 1,
    ('22', '7'): 1,
    ('22', '8'): 1,
    ('22', '11'): 1,
    ('22', '12'): 1,
    ('21', '6'): 1,
    ('21', '7'): 1,
    ('21', '10'): 1,
    ('21', '11'): 1,
    ('20', '5'): 1,
    ('20', '6'): 1,
    ('20', '9'): 1,
    ('20', '10'): 1,
    ('19', '3'): 1,
    ('19', '4'): 1,
    ('19', '7'): 1,
    ('19', '8'): 1,
    ('18', '2'): 1,
    ('18', '3'): 1,
    ('18', '6'): 1,
    ('18', '7'): 1,
    ('17', '1'): 1,
    ('17', '2'): 1,
    ('17', '5'): 1,
    ('17', '6'): 1
}
arcs = value.keys()

data = dict()
data["blocks"] = blocks
data["arcs"] = arcs
data["profit"] = profit
data["value"] = value
