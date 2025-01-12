#  max x + 2 y
#  subject to
#        x + y <= 4
#        x <= 2
#        y <= 3
#        x, y >= 0

import gurobipy as gp
from gurobipy import GRB

try:
    # Create a new model
    m = gp.Model("Exemplo")

    # Create variables
    x = m.addVar(vtype=GRB.CONTINUOUS, name="x")
    y = m.addVar(vtype=GRB.CONTINUOUS, name="y")

    # Set objective
    m.setObjective(x + 2*y, GRB.MAXIMIZE)

    # Add constraint: x + y <= 4
    m.addConstr(x + y <= 4, "c0")

    # Add constraint: x <= 2
    m.addConstr(x <= 2, "c1")

    # Add constraint: y <= 3
    m.addConstr(y <= 3, "c2")

    # Optimize model
    m.optimize()

    for v in m.getVars():
        print(f"{v.VarName} {v.X:g}")

    print(f"Obj: {m.ObjVal:g}")

except gp.GurobiError as e:
    print(f"Error code {e.errno}: {e}")

except AttributeError:
    print("Encountered an attribute error")
