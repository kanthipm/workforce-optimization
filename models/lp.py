from gurobipy import Model, GRB

def solve_lp():
    model = Model("LP")
    x = model.addVar(lb=0, name="x")
    y = model.addVar(lb=0, name="y")

    model.setObjective(3*x + 2*y, GRB.MAXIMIZE)
    model.addConstr(2*x + y <= 100)
    model.addConstr(x + y <= 80)

    model.optimize()

    #can add if model.status == GRB.OPTIMAL to make sure optimal solution was found
    print(f"x = {x.X}, y = {y.X}")

if __name__ == "__main__":
    solve_lp()
