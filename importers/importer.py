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
    batchSizes = []
    citiesBatches = []
    cities = [self.factoryKey]
    demandsBatches = []
    demands = []
    distancesBatches = []
    fleetsBatches = []

    clients = self.clientsImp.process()

    export = self.demandsImp.process(clients)
    allDemands = export['demands']
    clients = export['cities']

    count = 0
    for i in range(len(clients)):
      if allDemands[i] > 0:
        count += 1

    batchSizes = [self.batchSize] * (count / self.batchSize)
    itemsLeft = count % self.batchSize
    if itemsLeft > len(batchSizes):
      batchSizes.append(itemsLeft)
    else:
      for i in range(count % self.batchSize):
        batchSizes[(count / self.batchSize) - i - 1] += 1

    batchCount = 0
    count = 0
    for i in range(len(clients)):
      if allDemands[i] > 0:
        if count + 1 > batchSizes[batchCount]:
          citiesBatches.append(cities)
          demandsBatches.append(demands)
          count = 0
          cities = [self.factoryKey]
          demands = []
          batchCount += 1
        cities.append(clients[i])
        demands.append(allDemands[i])
        count += 1

    citiesBatches.append(cities)
    demandsBatches.append(demands)

    self.batchesCount = len(demandsBatches)

    for i in range(self.batchesCount):
      distancesBatches.append(self.distancesImp.process(citiesBatches[i]))
      fleetsBatches.append(self.fleetImp.process(self.batchesCount))

    return {
      'cities': citiesBatches,
      'distances': distancesBatches,
      'demands': demandsBatches,
      'fleets': fleetsBatches
    }
