from gurobipy import Model, GRB

def is_feasible(K):
    model = Model("FeasibilityCheck")
    model.setParam("OutputFlag", 0)  
    x = model.addVar(vtype=GRB.INTEGER, lb=0)
    y = model.addVar(vtype=GRB.INTEGER, lb=0)

    model.addConstr(2 * x +  y <= 100)
    model.addConstr(x + y <= K)

    model.optimize()
    return model.status == GRB.OPTIMAL

def solve_bsb():
    low, high = 0, 100
    best_K = -1

    while low <= high:
        mid = (low + high) // 2
        if is_feasible(mid):
            best_K = mid
            low = mid + 1
        else:
            high = mid - 1

    print(f"Maximum feasible K = {best_K}")

if __name__ == "__main__":
    solve_bsb()
