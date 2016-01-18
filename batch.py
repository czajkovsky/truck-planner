from importers.importer import Importer
from logic.world import World
from logic.serializer import Serializer
import time


SIMPLE_MODE = True
BATCHES_SIZE = 5

start = time.time()

timers = {
  'start': start,
  'import': 0,
  'compute': 0
}

# importer = Importer('demo', '', 'FACTORY', SIMPLE_MODE, BATCHES_SIZE)
# importer = Importer('main', '-2013-02-01', 'DC', SIMPLE_MODE)
importer = Importer('batch', '-2013-02-01', 'DC', SIMPLE_MODE, BATCHES_SIZE)
data = importer.process()

print data['cities'][0]
print data['fleets'][0]

serializer = Serializer()

for i in range(len(data['cities'])):
  print 'BATCH #' + str(i + 1)
  world = World(data['cities'][i], data['demands'][i], data['distances'][i], data['fleets'][i])
  world.compute(SIMPLE_MODE)
  serializer.add(world)

serializer.explain()
