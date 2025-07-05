#technicians_colgen/technician_branchprice
from technicians_branchprice.solver import column_generation_loop

if __name__ == "__main__":
    column_generation_loop("data/technicians.json")
