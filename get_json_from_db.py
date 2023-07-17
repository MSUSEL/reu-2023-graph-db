# This script gets data of techniqueCapac edge collection from the BRON guest db

from arango import ArangoClient, DocumentInsertError

def get_tech_capac(db):

    # constant that indicates the collection we're going to use
    TECH_CAP = 'TechniqueCapec'
    
    # setting guest database and local database
    guest = ArangoClient(hosts='http://bron.alfa.csail.mit.edu:8529')

    # opening guest database and local database
    guest_db = guest.db('BRON', username='guest', password='guest')

    # opening guest db document for transfer
    guest_collection = guest_db.collection(TECH_CAP)

    # open local graph for edge placement
    graph = db.graph('BRONGraph')

    # if the edge definition exists remove it
    if graph.has_edge_definition(TECH_CAP):
        graph.delete_edge_definition(TECH_CAP)
    
    # if the collection exists remove it
    if db.has_collection(TECH_CAP):
        db.delete_collection(TECH_CAP)

    # creates new edge definition and collection
    graph.create_edge_definition(
        edge_collection = TECH_CAP,
        from_vertex_collections = ['technique'],
        to_vertex_collections = ['capec'])
    
    # gets the edge collection from the database
    tc = graph.edge_collection(TECH_CAP)

    # grab all documents in guest collection
    documents = guest_collection.all()
    
    # place all edges into the local database
    for document in documents:
        try:
            edge_data = {'_from': document['_from'], '_to': document['_to']}
            tc.insert(edge_data)

        # skip inserting since the capec(attack pattern) in data is  ot in capec collection
        except DocumentInsertError:
            pass
