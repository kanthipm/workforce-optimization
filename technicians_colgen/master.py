from gurobipy import Model, GRB, quicksum

def solve_master(patterns, demand):
    model = Model("master")
    model.setParam("OutputFlag", 0)

    x = [model.addVar(obj=1.0, name=f"x_{i}") for i in range(len(patterns))]

    constraints = {}
    for loc in demand:
        constraints[loc] = model.addConstr(
            quicksum(patterns[p]["hours"].get(loc, 0) * x[p] for p in range(len(patterns))) >= demand[loc],
            name=f"demand_{loc}"
        )

    tech_set = set(pattern["tech"] for pattern in patterns)
    for tech in tech_set:
        model.addConstr(
            quicksum(patterns[p]["time"] * x[p] for p in range(len(patterns)) if patterns[p]["tech"] == tech) <= patterns[0]["availability"][tech],
            name=f"avail_{tech}"
        )

    model.optimize()
    duals = {loc: constraints[loc].Pi for loc in constraints}
    return model, x, duals
