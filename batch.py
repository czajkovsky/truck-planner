from importers.importer import Importer
from logic.world import World
from logic.serializer import Serializer
import time

def calculateFleet(fleet, inheritedFleet):
  for i in range(len(fleet['names'])):
    fleet['count'][i] += inheritedFleet[i]
  return fleet

SIMPLE_MODE = True
BATCHES_SIZE = 5

start = time.time()

timers = {
  'start': start,
  'import': 0,
  'compute': 0
}

# importer = Importer('demo', '', 'FACTORY', SIMPLE_MODE, BATCHES_SIZE)
# importer = Importer('main', '-2013-02-01', 'DC', SIMPLE_MODE, BATCHES_SIZE)
importer = Importer('batch', '-debug', 'DC', SIMPLE_MODE, BATCHES_SIZE)
data = importer.process()

serializer = Serializer()

for i in range(len(data['cities'])):
  print 'BATCH #' + str(i + 1)
  if i > 0:
    fleet = calculateFleet(data['fleets'][i], serializer.trucksLeft(world))
    fleet = data['fleets'][i]
  else:
    fleet = data['fleets'][i]

  serializer.listFleet(data['fleets'][i])
  serializer.listCities(data['cities'][i])

  world = World(data['cities'][i], data['demands'][i], data['distances'][i], fleet)
  world.compute(SIMPLE_MODE)
  serializer.add(world)

serializer.explain()
