# 0 Type;
# 1 Avialable count;
# 2 Capacity;
# 3 Price for 1km;
# 4 Time lading (min);
# 5 Time unlading (min);
# 6 Maks daily distance;
# 7 Price for distance < 100km (lump sum);
# 8 Max delivery points;
# 9 Cost unlading

import csv
import os

class FleetTypesImporter:
  def __init__(self, path):
    self.path = os.path.join(os.path.dirname(__file__), path)
    self.trucks = {
      'names': [],
      'count': [],
      'maxDeliveryPoints': [],
      'maxDailyDistances': [],
      'capacities': [],
      'rates': [],
    }

  def process(self):
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        self.trucks['names'].append(row[0]),
        self.trucks['count'].append(int(row[1])),
        self.trucks['capacities'].append(int(row[2]))
        self.trucks['rates'].append(float(row[3].replace(',', '.')))
        self.trucks['maxDailyDistances'].append(int(row[6]))
        self.trucks['maxDeliveryPoints'].append(int(row[8]))
    return self.trucks
