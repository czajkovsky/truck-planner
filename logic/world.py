from gurobipy import *
import StringIO
import sys

class World:
  def __init__(self, citiesNames, demands, distances):
    self.citiesNames = citiesNames
    self.demands = demands
    self.distances = distances

  def compute(self):
    sites = range(len(self.citiesNames))
    clients = sites[1:]

    truckNames = ['Transit', 'TIR']
    truckCapacities = [10, 20]
    truckRates = [1.0, 2.0]
    trucks = range(len(truckNames))

    capacity = 20

    model = Model('Diesel Fuel Delivery')

    x = {} # communication from i -> j
    t = {} # truck t on route i -> j

    for i in sites:
      for j in sites:
        x[i, j] = model.addVar(vtype = GRB.BINARY)
        for k in trucks:
          print 'x'
          t[i, j, k] = model.addVar(vtype = GRB.BINARY)

    print t

    u = {}
    for i in clients:
      u[i] = model.addVar(lb = self.demands[i - 1], ub = capacity)

    model.update()

    obj = quicksum(
      self.distances[i][j] * x[i,j] * t[i, j, ti] * truckRates[ti] for i in sites for j in sites for ti in trucks if i != j
    )

    print obj;
    model.setObjective(obj)

    for j in clients:
      model.addConstr(quicksum(x[i, j] for i in sites if i != j) == 1)

    for i in clients:
      model.addConstr(quicksum(x[i, j] for j in sites if i != j) == 1)

    for i in sites:
      model.addConstr(quicksum(t[i, j, ti] for j in sites for ti in trucks if i != j) == 1)

    for j in sites:
      model.addConstr(quicksum(t[i, j, ti] for i in sites for ti in trucks if i != j) == 1)

    for i in clients:
      model.addConstr(u[i] <= capacity + (self.demands[i - 1] - capacity) * x[0, i])

    for i in clients:
      for j in clients:
        if i != j:
          model.addConstr(u[i] - u[j] + capacity * x[i, j] <= capacity - self.demands[j - 1])

    model.optimize()

    def printTour(start, visited, distance):
      sys.stdout.write(self.citiesNames[start] + ' -> ')
      for i in sites:
        if (x[start, i].X > 0.5) & (start != i):
          if (i == 0):
            print 'FACTORY, distance:', distance + self.distances[start][i]
            return
          printTour(i, visited, distance + self.distances[start][i])

    for i in sites:
      if (x[0, i].X > 0.5) & (i != 0):
        sys.stdout.write('FACTORY' + ' -> ')
        printTour(i, [], self.distances[0][i])
