
# Parameters

years = [1, 2, 3, 4, 5]
mines = [1, 2, 3, 4]

royalties = {1: 5e6, 2: 4e6, 3: 4e6, 4: 5e6}
capacity = {1: 2e6, 2: 2.5e6, 3: 1.3e6, 4: 3e6}
quality  = {1: 1.0, 2: 0.7, 3: 1.5, 4: 0.5}
target = {1: 0.9, 2: 0.8, 3: 1.2, 4: 0.6, 5: 1.0}
time_discount = {year: (1/(1+1/10.0)) ** (year-1) for year in years}

max_mines = 3
price = 10

data = dict()
data["years"] = years
data["mines"] = mines
data["royalties"] = royalties
data["capacity"] = capacity
data["quality"] = quality
data["target"] = target
data["time_discount"] = time_discount
data["max_mines"] = max_mines
data["price"] = price