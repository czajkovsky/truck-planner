from cities_importer import CitiesImporter
from demands_importer import DemandsImporter

class Importer:
  def __init__(self):
    self.cities = CitiesImporter('../data/demo/distances.csv', 'FACTORY')
    self.demands = DemandsImporter('../data/demo/orders.csv')
    # self.cities = CitiesImporter('../data/distances.csv', 'DC')

  def process(self):
    citiesData = self.cities.process()
    demandsData = self.demands.process(citiesData['cities'])
    return {
      'cities': citiesData['cities'],
      'distances': citiesData['distances'],
      'demands': demandsData['demands']
    }
