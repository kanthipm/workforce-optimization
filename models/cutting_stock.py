from gurobipy import Model, GRB, quicksum

roll_length = 10
sizes = [3, 4]
demand = [5, 3]
n_items = len(sizes)

patterns = []
for i in range(n_items):
    pattern = [0] * n_items
    pattern[i] = roll_length // sizes[i]
    patterns.append(pattern)

def solve_master(patterns):
    model = Model("master")
    model.setParam("OutputFlag", 0)
    x = [model.addVar(obj=1.0, name=f"x_{i}") for i in range(len(patterns))]
    constraints = []
    for j in range(n_items):
        constr = model.addConstr(
            quicksum(patterns[i][j] * x[i] for i in range(len(patterns))) >= demand[j],
            name=f"demand_{j}"
        )
        constraints.append(constr)
    model.optimize()
    duals = [c.Pi for c in constraints]
    return model, x, duals

def solve_pricing(duals):
    model = Model("pricing")
    model.setParam("OutputFlag", 0)
    y = [model.addVar(vtype=GRB.INTEGER, lb=0, name=f"y_{j}") for j in range(n_items)]
    model.addConstr(quicksum(sizes[j] * y[j] for j in range(n_items)) <= roll_length)
    model.setObjective(quicksum(duals[j] * y[j] for j in range(n_items)), GRB.MAXIMIZE)
    model.optimize()
    reduced_cost = 1.0 - model.ObjVal
    if reduced_cost < -1e-6:
        return [int(y[j].X) for j in range(n_items)]
    else:
        return None

while True:
    master_model, x_vars, duals = solve_master(patterns)
    new_pattern = solve_pricing(duals)
    if new_pattern is None:
        break
    patterns.append(new_pattern)

master_model.write("final_master.lp")
print(f"Optimal number of rolls used: {master_model.ObjVal}")
for i, var in enumerate(master_model.getVars()):
    if var.X > 1e-6:
        print(f"Use pattern {patterns[i]} → {var.X} times")
