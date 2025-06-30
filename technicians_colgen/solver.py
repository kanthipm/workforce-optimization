import json
from technicians_colgen.master import solve_master
from technicians_colgen.pricing import generate_new_patterns

def column_generation_loop(data_path):
    with open(data_path, "r") as f:
        data = json.load(f)

    technicians = data["technicians"]
    locations = data["locations"]
    demand = data["demand"]
    availability = data["availability"]
    efficiency = data["efficiency"]

    # Start with one-location-only plans
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

    iteration = 0
    while True:
        iteration += 1
        print(f"\nIteration {iteration}")
        model, x, duals = solve_master(patterns, demand)

        new_plans = generate_new_patterns(technicians, locations, availability, efficiency, duals)
        if not new_plans:
            break
        patterns.extend(new_plans)

    print(f"\n Optimal number of assignment plans used: {model.ObjVal}")
    for i, var in enumerate(model.getVars()):
        if var.X > 1e-6:
            print(f"Plan {i}: {patterns[i]['tech']} → hours {patterns[i]['hours']} (used {round(var.X)} times)")
