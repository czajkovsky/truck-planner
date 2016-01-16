from cities_importer import CitiesImporter
from demands_importer import DemandsImporter

class Importer:
  def __init__(self, model):
    path = ' ' + model + '/'
    self.cities = CitiesImporter("../data/{0}/{1}.csv".format(model, 'distances'), 'FACTORY')
    self.demands = DemandsImporter("../data/{0}/{1}.csv".format(model, 'orders'))

  def process(self):
    citiesData = self.cities.process()
    demandsData = self.demands.process(citiesData['cities'][1:])
    return {
      'cities': citiesData['cities'],
      'distances': citiesData['distances'],
      'demands': demandsData['demands']
    }
