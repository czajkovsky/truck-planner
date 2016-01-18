from importers.importer import Importer
from logic.world import World
from logic.serializer import Serializer
import time

def calculateFleet(fleet, inheritedFleet):
  for i in range(len(fleet['names'])):
    fleet['count'][i] += inheritedFleet[i]
  return fleet

SIMPLE_MODE = True
BATCHES_SIZE = 6

importer = Importer('test', '-2013-02-01', 'DC', SIMPLE_MODE, BATCHES_SIZE)
data = importer.process()
serializer = Serializer()
batchesToRetry = []

start = time.time()

for i in range(len(data['cities'])):
  print 'BATCH #' + str(i + 1) + ' out of ' + str(len(data['cities']))
  if i > 0:
    if result != -1:
      fleet = calculateFleet(data['fleets'][i], serializer.trucksLeft(world))
      fleet = data['fleets'][i]
  else:
    fleet = data['fleets'][i]

  serializer.listFleet(data['fleets'][i])
  serializer.listCities(data['cities'][i], data['demands'][i])

  world = World(data['cities'][i], data['demands'][i], data['distances'][i], fleet)
  result = world.compute(SIMPLE_MODE)
  if result == -1:
    batchesToRetry.append(i)
  else:
    serializer.add(world)

for i in batchesToRetry:
  print 'RETRY BATCH #' + str(i + 1) + ' out of ' + str(len(batchesToRetry))

  fleet = calculateFleet(data['fleets'][i], serializer.trucksLeft(world))
  serializer.listFleet(data['fleets'][i])
  serializer.listCities(data['cities'][i], data['demands'][i])

  world = World(data['cities'][i], data['demands'][i], data['distances'][i], fleet)
  result = world.compute(SIMPLE_MODE)

  if result == -1:
    'PRINT UNABLE TO SOLVE IT :(('
  else:
    serializer.add(world)

serializer.explain()

print 'FINISHED after {0:.02f}s (BATCH SIZE: {1})'.format(time.time() - start, BATCHES_SIZE)
