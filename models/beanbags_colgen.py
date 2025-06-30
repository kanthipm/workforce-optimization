from gurobipy import Model, GRB, quicksum

volume_cap = 100
weight_cap = 50

volumes = [30, 20, 40, 25, 15, 10]
weights = [10, 15, 20, 10, 8, 5]
n = len(volumes)

patterns = []
for i in range(n):
    pattern = [0] * n
    pattern[i] = 1
    patterns.append(pattern)

def solve_master(patterns):
    model = Model("master")
    model.setParam("OutputFlag", 0)
    x = [model.addVar(obj=1.0, name=f"x_{i}") for i in range(len(patterns))]

    constraints = []
    for i in range(n):
        constr = model.addConstr(
            quicksum(patterns[p][i] * x[p] for p in range(len(patterns))) >= 1,
            name=f"demand_{i}"
        )
        constraints.append(constr)

    model.optimize()
    duals = [con.Pi for con in constraints]
    return model, x, duals

def solve_pricing(duals):
    model = Model("pricing")
    model.setParam("OutputFlag", 0)
    y = [model.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name=f"y_{i}") for i in range(n)]

    model.addConstr(quicksum(volumes[i] * y[i] for i in range(n)) <= volume_cap)
    model.addConstr(quicksum(weights[i] * y[i] for i in range(n)) <= weight_cap)

    model.setObjective(quicksum(duals[i] * y[i] for i in range(n)), GRB.MAXIMIZE)
    model.optimize()

    reduced_cost = 1.0 - model.ObjVal
    if reduced_cost < -1e-6:
        return [int(y[i].X) for i in range(n)]
    else:
        return None

while True:
    master_model, x_vars, duals = solve_master(patterns)
    new_pattern = solve_pricing(duals)

    if new_pattern is None:
        break

    patterns.append(new_pattern)

print(f"\nOptimal number of bins used: {master_model.ObjVal}")
for i, var in enumerate(master_model.getVars()):
    if var.X > 1e-6:
        print(f"Use pattern {patterns[i]} → {round(var.X)} times")
