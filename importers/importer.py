from clients_importer import ClientsImporter
from demands_importer import DemandsImporter
from distances_importer import DistancesImporter
from fleet_importer import FleetImporter
from fleet_types_importer import FleetTypesImporter

class Importer:
  def __init__(self, model, ordersVersion, factoryKey, simple, batchSize):
    path = ' ' + model + '/'
    self.factoryKey = factoryKey
    self.batchSize = batchSize
    self.clientsImp = ClientsImporter("../data/{0}/{1}.csv".format(model, 'distances'), factoryKey)
    self.demandsImp = DemandsImporter("../data/{0}/{1}{2}.csv".format(model, 'orders', ordersVersion))
    self.distancesImp = DistancesImporter("../data/{0}/{1}.csv".format(model, 'distances'))
    if simple:
      self.fleetImp = FleetTypesImporter("../data/{0}/{1}.csv".format(model, 'fleet'))
    else:
      self.fleetImp = FleetImporter("../data/{0}/{1}.csv".format(model, 'fleet'))

  def process(self):
    citiesBatches = []
    cities = [self.factoryKey]
    demandsBatches = []
    demands = []
    distancesBatches = []
    fleetsBatches = []

    clients = self.clientsImp.process()

    allDemands = self.demandsImp.process(clients)

    count = 0
    for i in range(len(clients)):
      if allDemands[i] > 0:
        if count + 1 > self.batchSize:
          citiesBatches.append(cities)
          demandsBatches.append(demands)
          count = 0
          cities = [self.factoryKey]
          demands = []
        cities.append(clients[i])
        demands.append(allDemands[i])
        count += 1

    if len(demands) > 0:
      citiesBatches.append(cities)
      demandsBatches.append(demands)

    self.batchesCount = len(demandsBatches)

    for i in range(self.batchesCount):
      distancesBatches.append(self.distancesImp.process(citiesBatches[i]))
      fleetsBatches.append(self.fleetImp.process(self.batchesCount))

    print fleetsBatches
    print 'FINISHED IMPORTING: {0} cities'.format(len(cities))

    return {
      'cities': citiesBatches,
      'distances': distancesBatches,
      'demands': demandsBatches,
      'fleets': fleetsBatches
    }
