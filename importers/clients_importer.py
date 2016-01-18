import csv
import os

class ClientsImporter:
  def __init__(self, path, factoryKey):
    self.path = os.path.join(os.path.dirname(__file__), path)
    self.factoryKey = factoryKey

  def process(self):
    citiesSet = set()
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        if row[0] != self.factoryKey:
          citiesSet.add(row[0])
    return list(citiesSet)
