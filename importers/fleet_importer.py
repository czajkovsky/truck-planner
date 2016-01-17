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

  def process(self):
    truckTypes = []
    with open(self.path, 'rb') as file:
      reader = csv.reader(file, delimiter = ';')
      file.next()
      for row in reader:
        truckTypes.append({
          'name': row[0],
          'count': int(row[1]),
          'capacity': int(row[2]),
          'rate': float(row[3].replace(',', '.')),
          'maxDailyDistance': int(row[6]),
          'maxDeliveryPoints': int(row[8]),
          'lumpSum': float(row[7].replace(',', '.'))
        })

    for type in truckTypes:
      for i in range(type['count']):
        self.trucks['names'].append(type['name'] + '#' + str(i + 1))
        self.trucks['capacities'].append(type['capacity'])
        self.trucks['maxDeliveryPoints'].append(type['maxDeliveryPoints'])
        self.trucks['maxDailyDistance'].append(type['maxDailyDistance'])
        self.trucks['rates'].append(type['rate'])

    return self.trucks
