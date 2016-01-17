from clients_importer import ClientsImporter
from demands_importer import DemandsImporter
from distances_importer import DistancesImporter
from fleet_importer import FleetImporter

class Importer:
  def __init__(self, model, ordersVersion):
    path = ' ' + model + '/'
    self.clientsImp = ClientsImporter("../data/{0}/{1}.csv".format(model, 'distances'), 'FACTORY')
    self.demandsImp = DemandsImporter("../data/{0}/{1}{2}.csv".format(model, 'orders', ordersVersion))
    self.distancesImp = DistancesImporter("../data/{0}/{1}.csv".format(model, 'distances'))
    self.fleetImp = FleetImporter("../data/{0}/{1}.csv".format(model, 'fleet'))

  def process(self):
    cities = ['FACTORY']
    demands = []
    clients = self.clientsImp.process()
    allDemands = self.demandsImp.process(clients)

    for i in range(len(clients)):
      if allDemands[i] > 0:
        cities.append(clients[i])
        demands.append(allDemands[i])

    return {
      'cities': cities,
      'distances': self.distancesImp.process(cities),
      'demands': demands,
      'fleet': self.fleetImp.process()
    }
