import csv
import os

class CitiesImporter:
  def __init__(self, path, factoryKey):
    self.path = os.path.join(os.path.dirname(__file__), path)
    self.factoryKey = factoryKey
    self.cities = [factoryKey]

  def process(self):
    self.cities.extend(self.citiesArray())
    self.distances = [[-1 for x in range(len(self.cities))] for x in range(len(self.cities))]
    self.assignDistances()
    for i in range(len(self.cities)):
      self.distances[i][i] = 0.0
    return { 'cities': self.cities, 'distances': self.distances }

  def citiesArray(self):
    citiesSet = set()
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        if row[0] != self.factoryKey:
          citiesSet.add(row[0])
    return list(citiesSet)

  def assignDistances(self):
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        self.distances[self.cities.index(row[0])][self.cities.index(row[1])] = float(row[2].replace(',', '.'))
