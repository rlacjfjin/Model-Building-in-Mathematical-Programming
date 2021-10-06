
supply = dict({'Liverpool': 150000,
               'Brighton': 200000})

through = dict({'Newcastle': 70000,
                'Birmingham': 50000,
                'London': 100000,
                'Exeter': 40000,
                'Bristol': 30000,
                'Northampton': 25000})
# through = dict({'Newcastle': 70000,
#                 'Birmingham': 50000,
#                 'London': 100000,
#                 'Exeter': 40000})

opencost = dict({'Newcastle': 10000,
                 'Birmingham': 0,
                 'London': 0,
                 'Exeter': 5000,
                 'Bristol': 12000,
                 'Northampton': 4000})

demand = dict({'C1': 50000,
               'C2': 10000,
               'C3': 40000,
               'C4': 35000,
               'C5': 60000,
               'C6': 20000})

cost = dict({
    ('Liverpool', 'Newcastle'): 0.5,
    ('Liverpool', 'Birmingham'): 0.5,
    ('Liverpool', 'London'): 1.0,
    ('Liverpool', 'Exeter'): 0.2,
    ('Liverpool', 'Bristol'): 0.6,
    ('Liverpool', 'Northampton'): 0.4,
    ('Liverpool', 'C1'): 1.0,
    ('Liverpool', 'C3'): 1.5,
    ('Liverpool', 'C4'): 2.0,
    ('Liverpool', 'C6'): 1.0,
    ('Brighton', 'Birmingham'): 0.3,
    ('Brighton', 'London'): 0.5,
    ('Brighton', 'Exeter'): 0.2,
    ('Brighton', 'Bristol'): 0.4,
    ('Brighton', 'Northampton'): 0.3,
    ('Brighton', 'C1'): 2.0,
    ('Newcastle', 'C2'): 1.5,
    ('Newcastle', 'C3'): 0.5,
    ('Newcastle', 'C5'): 1.5,
    ('Newcastle', 'C6'): 1.0,
    ('Birmingham', 'C1'): 1.0,
    ('Birmingham', 'C2'): 0.5,
    ('Birmingham', 'C3'): 0.5,
    ('Birmingham', 'C4'): 1.0,
    ('Birmingham', 'C5'): 0.5,
    ('London', 'C2'): 1.5,
    ('London', 'C3'): 2.0,
    ('London', 'C5'): 0.5,
    ('London', 'C6'): 1.5,
    ('Exeter', 'C3'): 0.2,
    ('Exeter', 'C4'): 1.5,
    ('Exeter', 'C5'): 0.5,
    ('Exeter', 'C6'): 1.5,
    ('Bristol', 'C1'): 1.2,
    ('Bristol', 'C2'): 0.6,
    ('Bristol', 'C3'): 0.5,
    ('Bristol', 'C5'): 0.3,
    ('Bristol', 'C6'): 0.8,
    ('Northampton', 'C2'): 0.4,
    ('Northampton', 'C4'): 0.5,
    ('Northampton', 'C5'): 0.6,
    ('Northampton', 'C6'): 0.9
})

# cost = {
#     ('Liverpool', 'Newcastle'): 0.5,
#     ('Liverpool', 'Birmingham'): 0.5,
#     ('Liverpool', 'London'): 1.0,
#     ('Liverpool', 'Exeter'): 0.2,
#     ('Liverpool', 'C1'): 1.0,
#     ('Liverpool', 'C3'): 1.5,
#     ('Liverpool', 'C4'): 2.0,
#     ('Liverpool', 'C6'): 1.0,
#     ('Brighton', 'Birmingham'): 0.3,
#     ('Brighton', 'London'): 0.5,
#     ('Brighton', 'Exeter'): 0.2,
#     ('Brighton', 'C1'): 2.0,
#     ('Newcastle', 'C2'): 1.5,
#     ('Newcastle', 'C3'): 0.5,
#     ('Newcastle', 'C5'): 1.5,
#     ('Newcastle', 'C6'): 1.0,
#     ('Birmingham', 'C1'): 1.0,
#     ('Birmingham', 'C2'): 0.5,
#     ('Birmingham', 'C3'): 0.5,
#     ('Birmingham', 'C4'): 1.0,
#     ('Birmingham', 'C5'): 0.5,
#     ('London', 'C2'): 1.5,
#     ('London', 'C3'): 2.0,
#     ('London', 'C5'): 0.5,
#     ('London', 'C6'): 1.5,
#     ('Exeter', 'C3'): 0.2,
#     ('Exeter', 'C4'): 1.5,
#     ('Exeter', 'C5'): 0.5,
#     ('Exeter', 'C6'): 1.5
# }

data = dict()
data["supply"] = supply
data["through"] = through
data["opencost"] = opencost
data["demand"] = demand
data["cost"] = cost