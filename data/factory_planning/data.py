products = ["Prod1", "Prod2", "Prod3", "Prod4", "Prod5", "Prod6", "Prod7"]
machines = ["grinder", "vertDrill", "horiDrill", "borer", "planer"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

profit = {"Prod1": 10, "Prod2": 6, "Prod3": 8, "Prod4": 4, "Prod5": 11, "Prod6": 9, "Prod7": 3}

time_req = {
    "grinder": {"Prod1": 0.5, "Prod2": 0.7, "Prod5": 0.3,
                "Prod6": 0.2, "Prod7": 0.5},
    "vertDrill": {"Prod1": 0.1, "Prod2": 0.2, "Prod4": 0.3,
                  "Prod6": 0.6},
    "horiDrill": {"Prod1": 0.2, "Prod3": 0.8, "Prod7": 0.6},
    "borer": {"Prod1": 0.05, "Prod2": 0.03, "Prod4": 0.07,
              "Prod5": 0.1, "Prod7": 0.08},
    "planer": {"Prod3": 0.01, "Prod5": 0.05, "Prod7": 0.05}
}

# number of machines down
down = {("Jan", "grinder"): 1, ("Feb", "horiDrill"): 2, ("Mar", "borer"): 1,
        ("Apr", "vertDrill"): 1, ("May", "grinder"): 1, ("May", "vertDrill"): 1,
        ("Jun", "planer"): 1, ("Jun", "horiDrill"): 1}
# number of machines that need to be under maintenance
down_req = {"grinder":2, "vertDrill":2, "horiDrill":3, "borer":1, "planer":1}

# number of each machine available
installed = {"grinder": 4, "vertDrill": 2, "horiDrill": 3, "borer": 1, "planer": 1}

# market limitation of sells
max_sales = {
    ("Jan", "Prod1"): 500,
    ("Jan", "Prod2"): 1000,
    ("Jan", "Prod3"): 300,
    ("Jan", "Prod4"): 300,
    ("Jan", "Prod5"): 800,
    ("Jan", "Prod6"): 200,
    ("Jan", "Prod7"): 100,
    ("Feb", "Prod1"): 600,
    ("Feb", "Prod2"): 500,
    ("Feb", "Prod3"): 200,
    ("Feb", "Prod4"): 0,
    ("Feb", "Prod5"): 400,
    ("Feb", "Prod6"): 300,
    ("Feb", "Prod7"): 150,
    ("Mar", "Prod1"): 300,
    ("Mar", "Prod2"): 600,
    ("Mar", "Prod3"): 0,
    ("Mar", "Prod4"): 0,
    ("Mar", "Prod5"): 500,
    ("Mar", "Prod6"): 400,
    ("Mar", "Prod7"): 100,
    ("Apr", "Prod1"): 200,
    ("Apr", "Prod2"): 300,
    ("Apr", "Prod3"): 400,
    ("Apr", "Prod4"): 500,
    ("Apr", "Prod5"): 200,
    ("Apr", "Prod6"): 0,
    ("Apr", "Prod7"): 100,
    ("May", "Prod1"): 0,
    ("May", "Prod2"): 100,
    ("May", "Prod3"): 500,
    ("May", "Prod4"): 100,
    ("May", "Prod5"): 1000,
    ("May", "Prod6"): 300,
    ("May", "Prod7"): 0,
    ("Jun", "Prod1"): 500,
    ("Jun", "Prod2"): 500,
    ("Jun", "Prod3"): 100,
    ("Jun", "Prod4"): 300,
    ("Jun", "Prod5"): 1100,
    ("Jun", "Prod6"): 500,
    ("Jun", "Prod7"): 60,
}

holding_cost = 0.5
max_inventory = 100
store_target = 50
hours_per_month = 2 * 8 * 24

data = dict()
data["products"] = products
data["machines"] = machines
data["months"] = months
data["profit"] = profit
data["time_req"] = time_req
data["down"] = down
data["down_req"] = down_req
data["installed"] = installed
data["max_sales"] = max_sales
data["holding_cost"] = holding_cost
data["max_inventory"] = max_inventory
data["store_target"] = store_target
data["hours_per_month"] = hours_per_month
