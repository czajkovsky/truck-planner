from importers.importer import Importer
from logic.world import World
from logic.serializer import Serializer

importer = Importer('demo', '')
# importer = Importer('main', '-2013-02-01')

data = importer.process()

world = World(data['cities'], data['demands'], data['distances'], data['fleet'])
world.compute()

serializer = Serializer(world)
serializer.explain()
