# 0 Type;
# 1 Avialable count;
# 2 Capacity;
# 3 Price for 1km;
# 4 Maks daily distance;
# 5 Max delivery points;

import csv
import os

class FleetImporter:
  def __init__(self, path):
    self.path = os.path.join(os.path.dirname(__file__), path)
    self.trucks = {
      'names': [],
      'maxDeliveryPoints': [],
      'maxDailyDistance': [],
      'capacities': [],
      'rates': [],
    }

  def process(self, count):
    truckTypes = []
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        truckTypes.append({
          'name': row[0],
          'count': int(row[1]) / count,
          'capacity': int(row[2]),
          'rate': float(row[3].replace(',', '.')),
          'maxDailyDistance': int(row[4]),
          'maxDeliveryPoints': int(row[5])
        })

    for type in truckTypes:
      for i in range(type['count']):
        self.trucks['names'].append(type['name'] + '#' + str(i + 1))
        self.trucks['capacities'].append(type['capacity'])
        self.trucks['maxDeliveryPoints'].append(type['maxDeliveryPoints'])
        self.trucks['maxDailyDistance'].append(type['maxDailyDistance'])
        self.trucks['rates'].append(type['rate'])

    return self.trucks
