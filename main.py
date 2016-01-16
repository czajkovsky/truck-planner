from importers.importer import Importer
from logic.world import World

# world = World()
importer = Importer()
data = importer.process()
print data['cities']
print data['distances']
print data['demands']
