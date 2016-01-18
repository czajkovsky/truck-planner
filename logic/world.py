from gurobipy import *
from tabulate import tabulate

import StringIO
import sys

class World:
  def __init__(self, cities, demands, distances, fleet):
    # WORLD DEFINITION
    self.cities = cities
    self.demands = demands
    self.distances = distances
    self.trucks = fleet

    # DECISION VARIABLES
    # x[i,j] : route (i->j) is used
    # t[i,j,ti] : truck ti is used on route (i->j)
    # u[i] : palettes for client i
    self.x = {}
    self.t = {}
    self.u = {}

    # MODEL
    self.model = Model('Palette Delivery system')

  def compute(self, simpleMode):
    sites = range(len(self.cities))
    clients = sites[1:]
    trucksRg = range(len(self.trucks['names']))


    allCapacities = []
    demandsCp = list(self.demands)
    for ti in trucksRg:
      for i in range(self.trucks['count'][ti]):
        allCapacities.append(self.trucks['capacities'][ti])
    allCapacities.sort(reverse = True)
    demandsCp.sort(reverse = True)

    if (len(allCapacities) > len(demandsCp)):
      for i in range(len(demandsCp)):
        if demandsCp[i] > allCapacities[i]:
          return -1;

    maxCapacity = max(self.demands)

    for i in sites:
      for j in sites:
        self.x[i, j] = self.model.addVar(vtype = GRB.BINARY)
        for ti in trucksRg:
          self.t[i, j, ti] = self.model.addVar(vtype = GRB.BINARY)

    for i in clients:
      self.u[i] = self.model.addVar(lb = self.demands[i - 1], ub = maxCapacity, vtype = GRB.INTEGER)

    self.model.update()

    # OBJECTIVE
    obj = quicksum(
      self.distances[i][j] * self.x[i,j] * self.t[i, j, ti] * self.trucks['rates'][ti]
      for i in sites
      for j in sites
      for ti in trucksRg
      if i != j
    )
    self.model.setObjective(obj)

    # CONSTRAINT #1 & #2
    # There is only one incoming and one outgoing route per client
    for j in clients:
      self.model.addConstr(quicksum(self.x[i, j] for i in sites if i != j) == 1)

    for i in clients:
      self.model.addConstr(quicksum(self.x[i, j] for j in sites if i != j) == 1)

    # CONSTRAINT #3
    # Each existing route has truck assigned
    for i in sites:
      for j in sites:
        self.model.addConstr(quicksum(self.t[i, j, ti] for ti in trucksRg if i != j) == self.x[i,j])

    # CONSTRAINT #4 & #5
    # Palettes per client don't exceed truck capacity
    for i in clients:
      capacity = quicksum(
        self.t[j, i, ti] * self.trucks['capacities'][ti]
        for ti in trucksRg
        for j in sites
        if i != j
      )
      self.model.addConstr(self.u[i] <= capacity + (self.demands[i - 1] - capacity) * self.x[0, i])

    for i in clients:
      capacity = quicksum(
        self.t[k, i, ti] * self.trucks['capacities'][ti]
        for ti in trucksRg
        for k in sites
        if i != k
      )
      for j in clients:
        if i != j:
          self.model.addConstr(self.u[i] - self.u[j] + capacity * self.x[i, j] <= capacity - self.demands[j - 1])

    # CONSTRAINT #6
    # Incomming truck equals outgoing truck
    for i in clients:
      for routeIn in sites:
        for routeOut in sites:
          if (i != routeIn) & (i != routeOut):
            for ti in trucksRg:
              self.model.addConstr(self.t[i,routeOut,ti] * self.x[routeIn,i] == self.t[routeIn,i,ti] * self.x[i,routeOut])

    if simpleMode:
      # CONSTRAINT #7
      # Don't use more trucks that you have
      for ti in trucksRg:
        self.model.addConstr(quicksum(self.t[0, i, ti] for i in clients) <= self.trucks['count'][ti])

    else:
      # CONSTRAINT #8
      # Each truck can leave factory only once
      for ti in trucksRg:
        self.model.addConstr(quicksum(self.t[0, i, ti] for i in clients) <= 1)

      # CONSTRAINT #9 & #10
      # Don't exceed maximum daily distance and maxiumum delivery points
      for ti in trucksRg:
        distance = quicksum(
          self.t[i, j, ti] * self.x[i,j] * self.distances[i][j]
          for i in sites
          for j in sites
          if j != i
        )

        deliveryPoints = quicksum(
          self.t[i, j, ti]
          for i in clients
          for j in clients
          if j != i
        )

      self.model.addConstr(distance <= self.trucks['maxDailyDistance'][ti])
      self.model.addConstr(deliveryPoints <= self.trucks['maxDeliveryPoints'][ti])

    self.model.setParam(GRB.Param.TimeLimit, 1200.0)
    self.model.optimize()
