from arango import ArangoClient
import json

# access to the arango database
client = ArangoClient()
db = client.db('BRON', username = 'root', password = 'changeme')

# open the json file
with open("nist800-53-r5-mappings2.json", 'r') as file:
    data = json.load(file)

    # execute files
    exec(open('get_json_from_db.py').read())
    print("Successfully inserted TechniqueCapac edge collection.")
    print("Inserting Control collection...")
    exec(open('insert_control_data.py').read())
    print("Inserting TechniqueControl edge collection...")
    exec(open('create_tech_ctrl_edge.py').read())
    print("Inserting TacticTactic collection...")
    exec(open('insert_tactic_path.py').read())
    print("End")
