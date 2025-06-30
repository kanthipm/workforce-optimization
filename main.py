from models.cutting_stock.solver import column_generation_loop

if __name__ == "__main__":
    column_generation_loop("data/rolls.json")
