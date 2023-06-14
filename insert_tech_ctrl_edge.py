# This script creates techniqueControl edgw collection

def create_edge(db, data):
    # constant indicates a name of edge and collection we are going to create
    TECH_CONT = 'TechniqueControl'

    # gets the graph from the database
    graph = db.graph('BRONGraph')

    # delete edge and collection if they exist
    if graph.has_edge_definition(TECH_CONT):
        graph.delete_edge_definition(TECH_CONT)
    if db.has_collection(TECH_CONT):
        db.delete_collection(TECH_CONT)

    # creates an edge in the graph
    graph.create_edge_definition(
                edge_collection = TECH_CONT,
                from_vertex_collections = ['technique'],
                to_vertex_collections = ['control'])

    # gets the edge collection
    tc = graph.edge_collection(TECH_CONT)
    insert_data(db, data, tc)

def insert_data(db, data, tc):
    # gets the collections
    control = db.collection('control')
    technique = db.collection('technique')

    # original id of techinique that will be compared
    tech_base = ''

    # original id of control that will be compared
    ctrl_base = ''

    # original id(s) that will be compared
    tech_id = ''
    control_id = ''

    # loops to get the data in the json file
    for obj in data:

        # gets the technique id
        tech_key = 'Technique_ID'
        if tech_key in obj:
            tech_base = obj[tech_key]

        # gets the control id
        cont_key = 'Control_ID'
        if cont_key in obj:
            ctrl_base = obj[cont_key]

        # gets the id in technique collection that match with the id in the json file
        for tech in technique:
            if tech['original_id'] == tech_base:
                tech_id = tech['_id']

        # gets the id in control collection that match with the id in the json file  
        for ctrl in control:
            if ctrl['_key'] == ctrl_base:
                control_id = ctrl['_id']

        # inserts the edge data
        edge_data = {'_from': tech_id, '_to': control_id}
        tc.insert(edge_data)