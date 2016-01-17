from tabulate import tabulate

import StringIO
import sys

class Serializer:
  def __init__(self, world):
    self.world = world

  def explain(self):
    routes = []
    for i in range(len(self.world.citiesNames)):
      if (self.world.x[0, i].X > 0.5) & (i != 0):
        routes.append(self.printTour('FACTORY -> ', i, self.world.distances[0][i]))
    print tabulate(routes, headers = ['Dist', 'Route'])

  def printTour(self, route, start, distance):
    route = route + self.world.citiesNames[start] + ' -> '
    for i in range(len(self.world.citiesNames)):
      if (self.world.x[start, i].X > 0.5) & (start != i):
        if (i == 0):
          totalDistance = distance + self.world.distances[start][i]
          return [str(totalDistance) + ' km', route + 'FACTORY']
        self.printTour(route, i, distance)







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
