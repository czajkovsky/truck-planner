from importers.importer import Importer
from logic.world import World

importer = Importer('demo')
data = importer.process()
world = World(data['cities'],  data['demands'], data['distances'])
world.compute()
