from tabulate import tabulate

import StringIO
import sys

class Serializer:
  def __init__(self, world):
    self.world = world

  def explain(self):
    routes = []
    for i in range(len(self.world.cities)):
      if (self.world.x[0, i].X > 0.5) & (i != 0):
        routes.append(self.printTour('FACTORY -> ', i, self.world.distances[0][i], 0))
    print tabulate(routes, headers = ['DIST', 'COST', 'TRUCK', 'PALETTES', 'ROUTE'])

  def printTour(self, route, start, distance, demand):
    route = route + self.world.cities[start] + ' -> '
    demand += self.world.demands[start - 1]
    truckId = -1
    for i in range(len(self.world.cities)):
      if (self.world.x[start, i].X > 0.5) & (start != i):
        totalDistance = distance + self.world.distances[start][i]
        if (i == 0):
          for ti in range(len(self.world.trucks['names'])):
            if (self.world.t[start, i, ti].X > 0.5):
              truckId = ti
          return [
            str(totalDistance) + ' km',
            totalDistance * self.world.trucks['rates'][truckId],
            self.world.trucks['names'][truckId],
            demand,
            route + 'FACTORY'
          ]
        return self.printTour(route, i, totalDistance, demand)
