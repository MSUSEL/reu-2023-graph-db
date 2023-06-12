from arango import ArangoClient
import json

client = ArangoClient()

# access to the BRON database
db = client.db('BRON', username = 'root', password = 'changeme')

#collection = ''

# name of the 
TECH_CONT = 'TechniqueControl'

with open("nist800-53-r5-mappings2.json", 'r') as file:
    data = json.load(file)


    graph = db.graph('BRONGraph')

    if graph.has_edge_definition(TECH_CONT):
        graph.delete_edge_definition(TECH_CONT)
        db.delete_collection(TECH_CONT)
    
    graph.create_edge_definition(
                edge_collection = TECH_CONT,
                from_vertex_collections = ['technique'],
                to_vertex_collections = ['control'])

    TC = graph.edge_collection(TECH_CONT)

    control = db.collection('control')
    technique = db.collection('technique')

    tech_base = ''
    cont_base = ''
    tech_id = ''
    control_id = ''

    for obj in data:

        tech_key = 'Technique_ID'
        if tech_key in obj:
            name = obj[tech_key]

        cont_key = 'Control_ID'
        if cont_key in obj:
            Somekey = obj[cont_key]

        for tech in technique:
            if tech['original_id'] == tech_base:
                tech_id = tech['_id']
        
        for cont in control:
            if cont['_key'] == cont_base:
                control_id = cont['_id']

        edge_data = {'_from': tech_id, '_to': control_id}
        TC.insert(edge_data)
