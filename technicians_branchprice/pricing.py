from gurobipy import Model, GRB, quicksum

def generate_new_patterns(technicians, locations, availability, efficiency, duals):
    new_patterns = []

    for tech in technicians:
        model = Model("pricing")
        model.setParam("OutputFlag", 0)

        y = {loc: model.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"y_{loc}") for loc in locations}
        a_total = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="total_hours")

        model.addConstr(quicksum(y[loc] / efficiency[tech][loc] for loc in locations) == a_total)
        model.addConstr(a_total <= availability[tech])

        revenue = quicksum(duals[loc] * y[loc] for loc in locations)
        model.setObjective(revenue, GRB.MAXIMIZE)
        model.optimize()

        reduced_cost = 1.0 - model.ObjVal
        if reduced_cost < -1e-6:
            pattern = {
                "tech": tech,
                "location": "multi",
                "time": a_total.X,
                "hours": {loc: y[loc].X for loc in locations},
                "availability": availability
            }
            new_patterns.append(pattern)

    return new_patterns
