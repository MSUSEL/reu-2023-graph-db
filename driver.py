from arango import ArangoClient
import json, get_json_from_db, insert_control_data, insert_tech_ctrl_edge, insert_tactic_path

# access to the arango database
client = ArangoClient()
db = client.db('BRON', username = 'root', password = 'changeme')

# open the json file
with open("nist800-53-r5-mappings2.json", 'r') as file:
    data = json.load(file)

    # execute functions in other src files
    print("Inserting TechniqueCapac edge collection...")
    get_json_from_db.get_tech_capac(db)
    print("Inserting Control Collection...")
    insert_control_data.insert(db, data)
    print("Inserting TechniqueControl edge collection...")
    insert_tech_ctrl_edge.create_edge(db, data)
    print("Inserting TacticTactic Collection...")
    insert_tactic_path.create_edge(db)
    print("Finished Inserting")
