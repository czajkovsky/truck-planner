from clients_importer import ClientsImporter
from demands_importer import DemandsImporter
from distances_importer import DistancesImporter
from fleet_importer import FleetImporter

class Importer:
  def __init__(self, model, ordersVersion, factoryKey):
    path = ' ' + model + '/'
    self.factoryKey = factoryKey
    self.clientsImp = ClientsImporter("../data/{0}/{1}.csv".format(model, 'distances'), factoryKey)
    self.demandsImp = DemandsImporter("../data/{0}/{1}{2}.csv".format(model, 'orders', ordersVersion))
    self.distancesImp = DistancesImporter("../data/{0}/{1}.csv".format(model, 'distances'))
    self.fleetImp = FleetImporter("../data/{0}/{1}.csv".format(model, 'fleet'))

  def process(self):
    cities = [self.factoryKey]
    demands = []
    clients = self.clientsImp.process()
    allDemands = self.demandsImp.process(clients)

    for i in range(len(clients)):
      if allDemands[i] > 0:
        cities.append(clients[i])
        demands.append(allDemands[i])

    distances = self.distancesImp.process(cities)

    print 'FINISHED IMPORTING: {0} cities'.format(len(cities))

    return {
      'cities': cities,
      'distances': distances,
      'demands': demands,
      'fleet': self.fleetImp.process()
    }
