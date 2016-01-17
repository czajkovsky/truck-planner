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
    truckRates = [1.1, 2.0]
    truckLimits = [4, 2]
    trucks = range(len(truckNames))

    vehicleNames = ['Transit#1', 'Transit#2', 'Transit#3', 'Transit#4', 'TIR#1', 'TIR#2']
    vehicleMaxDeliveryPoints = [20, 20, 20, 20, 3, 3]
    vehicleCapacities = [10, 10, 10, 10, 20, 20]
    vehicleRates = [1.1, 1.1, 1.1, 1.1, 2.0, 2.0]
    vehicles = range(len(vehicleNames))

    capacity = 20

    model = Model('Diesel Fuel Delivery')

    x = {} # communication from i -> j
    # t = {} # truck ti on route i -> j t[i, j, ti]
    v = {} # vehicle v on route i->j v[t,j,ti]

    for i in sites:
      for j in sites:
        x[i, j] = model.addVar(vtype = GRB.BINARY)
        # for ti in trucks:
        #   t[i, j, ti] = model.addVar(vtype = GRB.BINARY)
        for vi in vehicles:
          v[i, j, vi] = model.addVar(vtype = GRB.BINARY)

    u = {}
    for i in clients:
      u[i] = model.addVar(lb = self.demands[i - 1], ub = capacity)

    model.update()

    obj = quicksum(
      self.distances[i][j] * x[i,j] * v[i, j, vi] * vehicleRates[vi] for i in sites for j in sites for vi in vehicles if i != j
    )

    model.setObjective(obj)

    for j in clients:
      model.addConstr(quicksum(x[i, j] for i in sites if i != j) == 1)

    for i in clients:
      model.addConstr(quicksum(x[i, j] for j in sites if i != j) == 1)

    for i in sites:
      for j in sites:
        # model.addConstr(quicksum(t[i, j, ti] for ti in trucks if i != j) == x[i,j])
        model.addConstr(quicksum(v[i, j, vi] for vi in vehicles if i != j) == x[i,j])

    for i in clients:
      c = quicksum(v[j, i, vi] * vehicleCapacities[vi] for vi in vehicles for j in sites if i != j)
      model.addConstr(u[i] <= c + (self.demands[i - 1] - c) * x[0, i])

    for i in clients:
      c = quicksum(v[k, i, vi] * vehicleCapacities[vi] for vi in vehicles for k in sites if i != k)
      for j in clients:
        if i != j:
          model.addConstr(u[i] - u[j] + c * x[i, j] <= c - self.demands[j - 1])

    for i in clients:
      for routeIn in sites:
        for routeOut in sites:
          if (i != routeIn) & (i != routeOut):
            # for ti in trucks:
            #   model.addConstr(t[i,routeOut,ti] * x[routeIn,i] == t[routeIn,i,ti] * x[i,routeOut])
            for vi in vehicles:
              model.addConstr(v[i,routeOut,vi] * x[routeIn,i] == v[routeIn,i,vi] * x[i,routeOut])

    # for ti in trucks:
    #   model.addConstr(quicksum(t[0, i, ti] for i in clients) <= truckLimits[ti])

    for vi in vehicles:
      model.addConstr(quicksum(v[0, i, vi] for i in clients) <= 1)


    for vi in vehicles:
      model.addConstr(quicksum(v[i, j, vi] for i in clients for j in clients if j != i) <= vehicleMaxDeliveryPoints[vi])

    model.optimize()

    for i in sites:
      for j in sites:
        if i != j:
          for vi in vehicles:
            if v[i, j, vi].X > 0.5:
              print self.citiesNames[i], '->', self.citiesNames[j], ':', vehicleNames[vi]

    def printTour(start, visited, distance):
      sys.stdout.write(self.citiesNames[start] + ' -> ')
      for i in sites:
        if (x[start, i].X > 0.5) & (start != i):
          if (i == 0):
            vehicleId = -1
            for vi in vehicles:
              if (v[start,i,vi].X > 0.5):
                vehicleId = vi
            totalDistance = distance + self.distances[start][i]
            print 'FACTORY, distance:', totalDistance, 'TRUCK:', vehicleNames[vehicleId], 'COST:', totalDistance * vehicleRates[vehicleId]
            return
          printTour(i, visited, distance + self.distances[start][i])

    for i in sites:
      if (x[0, i].X > 0.5) & (i != 0):
        sys.stdout.write('FACTORY' + ' -> ')
        printTour(i, [], self.distances[0][i])
