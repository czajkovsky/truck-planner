from importers.importer import Importer
from logic.world import World
from logic.serializer import Serializer


SIMPLE_MODE = True
# SIMPLE_MODE = False

# importer = Importer('demo', '', 'FACTORY', SIMPLE_MODE)
# importer = Importer('main', '-2013-02-01', 'DC', SIMPLE_MODE)
importer = Importer('main-small', '-2013-02-01', 'DC', SIMPLE_MODE)

data = importer.process()

world = World(data['cities'], data['demands'], data['distances'], data['fleet'])
world.compute(SIMPLE_MODE)

serializer = Serializer(world)
serializer.explain()
