from cities_importer import CitiesImporter

class Importer:
  def __init__(self):
    self.cities = CitiesImporter('../data/demo/distances.csv', 'FACTORY')
    # self.cities = CitiesImporter('../data/distances.csv', 'DC')

  def process(self):
    citiesData = self.cities.process()
    return {
      'cities': citiesData['cities'],
      'distances': citiesData['distances']
    }
