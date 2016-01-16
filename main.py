from importers.importer import Importer
from logic.world import World

importer = Importer()
data = importer.process()
world = World(data['cities'],  data['demands'], data['distances'])
world.compute()
