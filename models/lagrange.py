from gurobipy import Model, GRB

def lagrangian_relaxation(lam):
    model = Model("LaGrange")
    model.setParam("OutputFlag", 0)

    x = model.addVar(vtype=GRB.INTEGER, lb=0)
    y = model.addVar(vtype=GRB.INTEGER, lb=0)

    model.addConstr(2*x + y <= 5)
    #relaxing contraint x+y <= 4
    model.setObjective((10 - lam)*x + (6 - lam)*y + 4*lam, GRB.MAXIMIZE)

    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        return model.ObjVal, x.X, y.X
    return None

for lam in range(0, 11):
    result = lagrangian_relaxation(lam)
    if result:
        val, x, y = result
        print(f"λ = {lam}, Obj = {val}, x = {x}, y = {y}")
