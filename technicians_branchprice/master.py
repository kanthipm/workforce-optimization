from gurobipy import Model, GRB, quicksum

def solve_master(patterns, demand, integer=False, forced_values=None):
    model = Model("master")
    model.setParam("OutputFlag", 0)

    x = []

    # modified to optionally use integer variables, and apply foced values from branching

    for i in range(len(patterns)):
        var_type = GRB.INTEGER if integer else GRB.CONTINUOUS
        x_var = model.addVar(vtype=var_type, obj=1.0, name=f"x_{i}")
        x.append(x_var)

    if forced_values:
        for idx, val in forced_values.items():
            model.addConstr(x[idx] == val, name=f"branch_fix_{idx}")

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
    if not integer:
        duals = {loc: constraints[loc].Pi for loc in constraints}
    else:
        duals = None  # No duals in integer mode

    return model, x, duals
