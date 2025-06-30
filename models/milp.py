from gurobipy import Model, GRB

def solve_milp():
    model = Model("MILP")

    x = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="x")
    y = model.addVar(lb=0, vtype=GRB.INTEGER, name="y")
    z = model.addVar(vtype=GRB.BINARY, name="z")

    model.setObjective(2*x + 3*y + 5*z, GRB.MAXIMIZE)

    model.addConstr(x + 2*y + z <= 20)
    model.addConstr(x - y >= 0)

    model.optimize()

    print(f"x = {x.X}, y = {y.X}, z = {z.X}")
    print(f"Objective value = {model.ObjVal}")
    

if __name__ == "__main__":
    solve_milp()
