requirements = [0, 5, 4, 3, 6, 7, 3, 4, 6, 5, 4, 7, 3, 4, 5, 6, 8, 5, 7, 6, 6]
positions = {
    0: (0, 0),
    1: (-3, 3),
    2: (1, 11),
    3: (4, 7),
    4: (-5, 9),
    5: (-5, -2),
    6: (-4, -7),
    7: (6, 0),
    8: (3, -6),
    9: (-1, -3),
    10: (0, -6),
    11: (6, 4),
    12: (2, 5),
    13: (-2, 8),
    14: (6, 10),
    15: (1, 8),
    16: (-3, 1),
    17: (-6, 5),
    18: (2, 9),
    19: (-6, -5),
    20: (5, -4)
}
everyDay = [*range(0, 10)]
otherDay = [*range(10, 21)]
dayType = [1, 2]
tankerCap = 80

data = dict()
data["positions"] = positions
data["requirements"] = requirements
data["everyDay"] = everyDay
data["otherDay"] = otherDay
data["dayType"] = dayType
data["tankerCap"] = tankerCap
