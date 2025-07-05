import json
from technicians_branchprice.master import solve_master
from technicians_branchprice.pricing import generate_new_patterns

def is_integer_solution(model_vars):
    return all(abs(var.X - round(var.X)) < 1e-6 for var in model_vars)

def branch_and_price(patterns, technicians, locations, availability, efficiency, demand, forced={}):
    model, x_vars, duals = solve_master(patterns, demand, integer=False, forced_values=forced)

    if is_integer_solution(x_vars):
        print(f"Objective value: {model.ObjVal}")
        for i, var in enumerate(model.getVars()):
            if var.X > 1e-6:
                print(f"Plan {i}: {patterns[i]['tech']} → hours {patterns[i]['hours']} (used {round(var.X)} times)")
        return model.ObjVal

    new_plans = generate_new_patterns(technicians, locations, availability, efficiency, duals)
    if new_plans:
        patterns.extend(new_plans)
        return branch_and_price(patterns, technicians, locations, availability, efficiency, demand, forced)

    for i, var in enumerate(x_vars):
        if abs(var.X - round(var.X)) > 1e-6:
            print(f"\n🔀 Branching on x[{i}] = {var.X:.2f}")
            # x[i] = 0/1, creates 2 branches
            left_forced = forced.copy()
            left_forced[i] = 0
            left_obj = branch_and_price(patterns.copy(), technicians, locations, availability, efficiency, demand, left_forced)

            right_forced = forced.copy()
            right_forced[i] = 1
            right_obj = branch_and_price(patterns.copy(), technicians, locations, availability, efficiency, demand, right_forced)

            return min(left_obj, right_obj)
        
def column_generation_loop(data_path):
    with open(data_path, "r") as f:
        data = json.load(f)

    technicians = data["technicians"]
    locations = data["locations"]
    demand = data["demand"]
    availability = data["availability"]
    efficiency = data["efficiency"]

    patterns = []
    for tech in technicians:
        for loc in locations:
            hours = 10 * efficiency[tech][loc]
            pattern = {
                "tech": tech,
                "location": loc,
                "time": 10,
                "hours": {l: 0 for l in locations},
                "availability": availability
            }
            pattern["hours"][loc] = hours
            patterns.append(pattern)

    branch_and_price(patterns, technicians, locations, availability, efficiency, demand)

