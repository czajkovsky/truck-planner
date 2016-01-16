import csv
import os

class DemandsImporter:
  def __init__(self, path):
    self.path = os.path.join(os.path.dirname(__file__), path)

  def process(self, cities):
    self.demands = [0 for x in range(len(cities))]
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        self.demands[cities.index(row[0])] = int(row[1])
    return { 'demands': self.demands }
