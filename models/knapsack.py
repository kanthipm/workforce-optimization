from gurobipy import Model, GRB

def solve_knapsack():
    items = ['a', 'b', 'c', 'd']
    values = {'a': 60, 'b': 100, 'c': 120, 'd': 80}
    weights = {'a': 10, 'b': 20, 'c': 30, 'd': 25}
    capacity = 50

    model = Model("Knapsack")
    x = {i: model.addVar(vtype=GRB.BINARY, name=f"x_{i}") for i in items}
    model.setObjective(sum(values[i] * x[i] for i in items), GRB.MAXIMIZE)
    model.addConstr(sum(weights[i] * x[i] for i in items) <= capacity, name="capacity")
    model.optimize()

    print("Selected items:", [i for i in items if x[i].X == 1])
    print("Total value:", model.ObjVal)
    
if __name__ == "__main__":
    solve_knapsack()