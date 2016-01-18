from tabulate import tabulate

import StringIO
import sys

class Serializer:
  def __init__(self):
    self.worlds = []

  def explain(self):
    routes = []
    for wi in range(len(self.worlds)):
      for i in range(len(self.worlds[wi].cities)):
        if (self.worlds[wi].x[0, i].X > 0.5) & (i != 0):
          routes.append(self.printTour(wi + 1, self.worlds[wi], 'FACTORY -> ', i, self.worlds[wi].distances[0][i], 0))
    print tabulate(routes, headers = ['BATCH', 'DIST', 'COST', 'TRUCK', 'PALETTES', 'ROUTE'])
    totalCost = 0
    totalPalettes = 0
    for route in routes:
      totalCost += route[2]
      totalPalettes += route[4]
    print '\n\n===========\n* Total cost:\n    {0}'.format(totalCost)
    print '* Palettes delivered:\n    {0}'.format(totalPalettes)

  def printTour(self, wid, world, route, start, distance, demand):
    route = route + world.cities[start] + ' -> '
    demand += world.demands[start - 1]
    truckId = -1
    for i in range(len(world.cities)):
      if (world.x[start, i].X > 0.5) & (start != i):
        totalDistance = distance + world.distances[start][i]
        if (i == 0):
          for ti in range(len(world.trucks['names'])):
            if (world.t[start, i, ti].X > 0.5):
              truckId = ti
          return [
            wid,
            str(totalDistance) + ' km',
            totalDistance * world.trucks['rates'][truckId],
            world.trucks['names'][truckId],
            demand,
            route + 'FACTORY'
          ]
        return self.printTour(wid, world, route, i, totalDistance, demand)

  def add(self, world):
    self.worlds.append(world)

  def trucksLeft(self, world):
    trucks = [0] * len(world.trucks['names'])
    for ti in range(len(world.trucks['names'])):
      trucks[ti] = world.trucks['count'][ti]
    for i in range(len(world.cities)):
      if (world.x[0, i].X > 0.5) & (i != 0):
        for ti in range(len(world.trucks['names'])):
          if (world.t[0, i, ti].X > 0.5):
            trucks[ti] -= 1
    return trucks

  def listCities(self, cities, demands):
    print "PROCESSING {0} CITIES".format(len(cities))
    citiesList = []
    for i in range(len(cities)):
      citiesList.append([
        cities[i],
        demands[i - 1]
      ])
    print tabulate(citiesList, headers = ['NAME', 'DEMAND'])
    print ''

  def listFleet(self, fleet):
    trucks = []
    for i in range(len(fleet['names'])):
      trucks.append([
        fleet['names'][i],
        fleet['count'][i],
        fleet['capacities'][i]
      ])
    print tabulate(trucks, headers = ['NAME', 'COUNT', 'CAPACITY'])
    print ''
