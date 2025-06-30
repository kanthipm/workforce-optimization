from gurobipy import Model, GRB

def solve_ilp():
    model = Model("ILP")
    x = model.addVar(lb=0, vtype=GRB.INTEGER, name="x")
    y = model.addVar(lb=0, vtype=GRB.INTEGER, name="y")

    model.setObjective(3*x + 2*y, GRB.MAXIMIZE)
    model.addConstr(2*x + y <= 100, name="c1")
    model.addConstr(x + y <= 80, name="c2")

    model.optimize()

    #can add if model.status == GRB.OPTIMAL to make sure optimal solution was found
    print(f"x = {x.X}, y = {y.X}")
        
if __name__ == "__main__":
    solve_ilp()
