from gurobipy import Model, GRB, quicksum

#solves the lp using current plans
def solve_master(patterns, demand):
    model = Model("master")
    model.setParam("OutputFlag", 0)

    x = [model.addVar(obj=1.0, name=f"x_{i}") for i in range(len(patterns))]

    constraints = {}
    for loc in demand:
        constraints[loc] = model.addConstr(
            #total hours > demand
            quicksum(patterns[p]["hours"].get(loc, 0) * x[p] for p in range(len(patterns))) >= demand[loc],
            name=f"demand_{loc}"
        )

    tech_set = set(pattern["tech"] for pattern in patterns)
    for tech in tech_set:
        model.addConstr(
            #total time spent by tech <= availability
            quicksum(patterns[p]["time"] * x[p] for p in range(len(patterns)) if patterns[p]["tech"] == tech) <= patterns[0]["availability"][tech],
            name=f"avail_{tech}"
        )

    model.optimize()
    #extracts dual values from location constraints to use in pricing
    duals = {loc: constraints[loc].Pi for loc in constraints}
    return model, x, duals
