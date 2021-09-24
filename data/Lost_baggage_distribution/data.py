import math
import random

# number of locations, including the depot. The index of the depot is 0
n = 17
locations = [*range(n)]

# number of vans
K = 6
vans = [*range(K)]

# Create n random points
# Depot is located at (0,0) coordinates
random.seed(1)
points = [(0, 0)]
points += [(random.randint(0, 50), random.randint(0, 50)) for i in range(n - 1)]

# Dictionary of Euclidean distance between each pair of points
# Assume a speed of 60 km/hr, which is 1 km/min. Hence travel time = distance
time = {(i, j):
            math.sqrt(sum((points[i][k] - points[j][k]) ** 2 for k in range(2)))
        for i in locations for j in locations if i != j}
data = dict()
data["time"] = time
data["vans"] = vans
data["locations"] = locations
data["positions"] = points
