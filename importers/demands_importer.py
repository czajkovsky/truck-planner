import csv
import os

class DemandsImporter:
  def __init__(self, path):
    self.path = os.path.join(os.path.dirname(__file__), path)

  def process(self, cities):
    MAX_CAPACITY = 33 # to-do remove harcoded value

    self.demands = [0 for x in range(len(cities))]
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        try:
          self.demands[cities.index(row[0])] += int(row[1])
        except (ValueError,IndexError):
          None
      for i in range(len(self.demands)):
        if self.demands[i] > MAX_CAPACITY:
          count = self.demands[i] / MAX_CAPACITY
          originalName = cities[i]
          cities[i] = originalName + '#0'
          self.demands[i] = self.demands[i] % MAX_CAPACITY
          for j in range(count):
            name = originalName + '#' + str(j + 1)
            cities.append(name)
            self.demands.append(MAX_CAPACITY)

    return {
      'demands': self.demands,
      'cities': cities
    }
