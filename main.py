from importers.importer import Importer
from logic.world import World
from logic.serializer import Serializer
import time


SIMPLE_MODE = True
SIMPLE_MODE = False

start = time.time()

timers = {
  'start': start,
  'import': 0,
  'compute': 0
}

# importer = Importer('demo', '', 'FACTORY', SIMPLE_MODE)
# importer = Importer('main', '-2013-02-01', 'DC', SIMPLE_MODE)
importer = Importer('main-small', '-2013-02-01', 'DC', SIMPLE_MODE)

timers['import'] = time.time() - start
start = time.time()

data = importer.process()

world = World(data['cities'], data['demands'], data['distances'], data['fleet'])
world.compute(SIMPLE_MODE)

timers['compute'] = time.time() - start

serializer = Serializer(world)
serializer.explain()

print 'FINISHED after {0:.02f}s (import: {1:.02f}s, compute: {2:.02f}s)'.format(time.time() - timers['start'], timers['import'], timers['compute'])
