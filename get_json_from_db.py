# import ArangoClient for use
from arango import ArangoClient

# setting guest database and local database
guest = ArangoClient(hosts='http://bron.alfa.csail.mit.edu:8529')
client = ArangoClient()

# opening guest database and local database
guest_db = guest.db('BRON', username='guest', password='guest')
db = client.db('BRON', username='root', password='changeme')

# opening guest db document for transfer
guest_collection = guest_db.collection('TechniqueCapec')

# open local graph for edge placement
graph = db.graph('BRONGraph')

# if the collection does not exist in local, create it
# (should by default)
if not db.has_collection('TechniqueCapec'):
    db.create_collection('TechniqueCapec')

# wipe the local collection clean
TC = db.collection('TechniqueCapec')
TC.truncate()

# grab all documents in guest collection
documents = guest_collection.all()

# place all edges into the local database
for document in documents:
    TC.insert(document)
