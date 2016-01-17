import csv
import os

class DistancesImporter:
  def __init__(self, path):
    self.path = os.path.join(os.path.dirname(__file__), path)

  def process(self, cities):
    self.distances = [[-1 for x in range(len(cities))] for x in range(len(cities))]
    self.assignDistances(cities)
    for i in range(len(cities)):
      self.distances[i][i] = 0.0
    return self.distances

  def assignDistances(self, cities):
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        try:
          self.distances[cities.index(row[0])][cities.index(row[1])] = float(row[2].replace(',', '.'))
        except (ValueError,IndexError):
          None
