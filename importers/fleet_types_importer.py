# 0 Type;
# 1 Avialable count;
# 2 Capacity;
# 3 Price for 1km;
# 4 Maks daily distance;
# 5 Max delivery points;

import csv
import os

class FleetTypesImporter:
  def __init__(self, path):
    self.path = os.path.join(os.path.dirname(__file__), path)

  def process(self, count):
    self.trucks = {
      'names': [],
      'count': [],
      'maxDeliveryPoints': [],
      'maxDailyDistances': [],
      'capacities': [],
      'rates': [],
    }
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        self.trucks['names'].append(row[0]),
        self.trucks['count'].append(int(row[1]) / count),
        self.trucks['capacities'].append(int(row[2]))
        self.trucks['rates'].append(float(row[3].replace(',', '.')))
        self.trucks['maxDailyDistances'].append(int(row[4]))
        self.trucks['maxDeliveryPoints'].append(int(row[5]))
    return self.trucks
