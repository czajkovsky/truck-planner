from gurobipy import *
import StringIO
import sys

class World:
  def __init__(self):
    siteNames = ["FACTORY", "A", "B", "C", "D", "E"]
    sites = range(len(siteNames))
    clients = sites[1:]
    demand = [3000, 1200, 1600, 1400, 1000]

    dist = [
      [0,   30,  90,  50,  90 , 100],
      [30,  0,   60,  80,  120, 130],
      [90,  60,  0,   140, 180, 190],
      [50,  80,  140, 0,   40 , 50 ],
      [90,  120, 180, 40,  0  , 50 ],
      [100, 130, 190, 50,  50 , 0  ],
    ]

    capacity = 4500

    model = Model('Diesel Fuel Delivery')

    x = {}
    for i in sites:
      for j in sites:
        x[i,j] = model.addVar(vtype = GRB.BINARY)

    u = {}
    for i in clients:
      u[i] = model.addVar(lb = demand[i - 1], ub = capacity) # OK

    model.update()

    obj = quicksum(dist[i][j] * x[i,j] for i in sites for j in sites if i != j)
    model.setObjective(obj)

    for j in clients:
      model.addConstr(quicksum(x[i, j] for i in sites if i != j) == 1)

    for i in clients:
      model.addConstr(quicksum(x[i, j] for j in sites if i != j) == 1)

    for i in clients:
      model.addConstr(u[i] <= capacity + (demand[i - 1] - capacity) * x[0, i])

    for i in clients:
      for j in clients:
        if i != j:
          model.addConstr(u[i] - u[j] + capacity * x[i, j] <= capacity - demand[j - 1])

    model.optimize()

    def printTour(start, visited, distance):
      sys.stdout.write(siteNames[start] + ' -> ')
      for i in sites:
        if (x[start, i].X > 0.5) & (start != i):
          if (i == 0):
            print 'FACTORY, distance:', distance + dist[start][i]
            return
          printTour(i, visited, distance + dist[start][i])

    for i in sites:
      if (x[0, i].X > 0.5) & (i != 0):
        sys.stdout.write('FACTORY' + ' -> ')
        printTour(i, [], dist[0][i])
