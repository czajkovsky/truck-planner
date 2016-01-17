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
        routes.append(self.printTour('FACTORY -> ', i, self.world.distances[0][i]))
    print routes
    print tabulate(routes, headers = ['DIST', 'COST', 'TRUCK', 'ROUTE'])

  def printTour(self, route, start, distance):
    route = route + self.world.cities[start] + ' -> '
    truckId = -1
    for i in range(len(self.world.cities)):
      if (self.world.x[start, i].X > 0.5) & (start != i):
        if (i == 0):
          for ti in range(len(self.world.trucks['names'])):
            if (self.world.t[start, i, ti].X > 0.5):
              truckId = ti
          totalDistance = distance + self.world.distances[start][i]
          return [
            str(totalDistance) + ' km',
            totalDistance * self.world.trucks['rates'][truckId],
            self.world.trucks['names'][truckId],
            route + 'FACTORY',
          ]
        return self.printTour(route, i, distance)







# def printTour(start, visited, distance):
#       sys.stdout.write(self.citiesNames[start] + ' -> ')
#       for i in sites:
#         if (self.x[start, i].X > 0.5) & (start != i):
#           if (i == 0):
#             truckId = -1
#             for ti in trucks:
#               if (self.t[start,i,ti].X > 0.5):
#                 truckId = ti
#             totalDistance = distance + self.distances[start][i]
#             print 'FACTORY, distance:', totalDistance, 'TRUCK:', truckNames[truckId], 'COST:', totalDistance * truckRates[truckId]
#             return
#           printTour(i, visited, distance + self.distances[start][i])

#     for i in sites:
#       if (self.x[0, i].X > 0.5) & (i != 0):
#         sys.stdout.write('FACTORY' + ' -> ')
#         printTour(i, [], self.distances[0][i])
