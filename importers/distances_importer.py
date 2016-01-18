import csv
import os

class DistancesImporter:
  def __init__(self, path):
    self.path = os.path.join(os.path.dirname(__file__), path)

  def process(self, cities):
    self.distances = [[-1 for x in range(len(cities))] for x in range(len(cities))]
    self.assignDistances(cities)
    return self.distances

  def assignDistances(self, cities):
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        try:
          fromIndexes = []
          toIndexes = []
          for i in range(len(cities)):
            if cities[i].startswith(row[0]):
              fromIndexes.append(i)
            if cities[i].startswith(row[1]):
              toIndexes.append(i)

          if (len(toIndexes) > 0) & (len(fromIndexes) > 0):
            for i in fromIndexes:
              for j in fromIndexes:
                self.distances[i][j] = 0.0

            for i in toIndexes:
              for j in toIndexes:
                self.distances[i][j] = 0.0

            for fromInd in fromIndexes:
              for toInd in toIndexes:
                self.distances[fromInd][toInd] = float(row[2].replace(',', '.'))

        except (ValueError,IndexError):
          None
