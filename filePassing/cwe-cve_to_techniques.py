import json
import os.path
import sys
import tech_tac_graph
from arango import ArangoClient

# access to the arango database
client = ArangoClient()
db = client.db('BRON', username='root', password='changeme')

# reads cve in the json file and find the technique of them
def read_cve(data, controls):
    # stores cve(s) in the file
    cve_list = []

    # temp
    print('Reading CVEs in the input file...')

    # gets all the cve in the specified json file
    for obj in data:
        for cve_value in obj.values():
            cve_list.append(cve_value) # adds each cve to the list

    # finds the techniques that can result to the cve in the cve_list
    query = 'for item in cve ' \
        + 'filter item.original_id in @cve_list ' \
        + 'for e, v, p in 1..5 inbound item CweCve, CapecCwe, TechniqueCapec ' \
        + 'filter LENGTH(p.edges) > 2 ' \
        + 'return distinct LAST(p.vertices)._id'
    
    # specify that @cve_list in the query is cve_list
    bind = {'cve_list': cve_list}

    # execute the query
    cursor = db.aql.execute(query, bind_vars=bind)
    find_tech_not_ctrl(controls, cursor)

    
# reads cwe in the json file and find the technique of them
def read_cwe(data, controls):
    # stores cwe(s) in the file
    cwe_list = []

    # temp
    print('Reading CWEs in the input file...')

    # gets all the cwe in the specified json file
    for obj in data:
        for cwe_value in obj.values():
            cwe_list.append(cwe_value) # adds each cwe to the list

    # finds the techniques that can result to the cwe in the cve_list
    query = 'for item in cwe ' \
            + 'filter item.original_id in @cwe_list ' \
            + 'for e, v, p in 1..4 inbound item CapecCwe, TechniqueCapec ' \
            + 'filter LENGTH(p.edges) > 1 ' \
            + 'return distinct LAST(p.vertices)._id'
    
    # specify that @cwe_list in the query is cwe_list
    bind = {'cwe_list': cwe_list}

    # execute the query
    cursor = db.aql.execute(query, bind_vars=bind)
    find_tech_not_ctrl(controls, cursor)


# find techniques that do not have the controls specified by user
def find_tech_not_ctrl(controls, cursor_tech):
    # stores techniques that do not have specified controls
    tech_list = []

    # temp
    print('Finding Technique that does not have specify control...')

    # compare the techniques and controls
    for tech in cursor_tech:
        tech_ctrl = db.collection('TechniqueControl')
        ctrl_list = [] # stores control that map to the specific technique
        for data in tech_ctrl:
            if data['_from'] == tech:
                ctrl_list.append(data['_to'])

        # indicates whether control is in the list
        in_list = False
        for a_ctrl in controls:
            for  ctrl_value in a_ctrl.values():
                control = 'control/' + str(ctrl_value)
                if control in ctrl_list:
                    in_list = True
                    break
        if not in_list:
            tech_list.append(tech)

    # finds the paths between the techniques we got and tactics
    query = 'for item in @tech_list ' \
        + 'for e, v, p in 1..2 inbound ' \
        + 'item TacticTechnique ' \
        + 'return { From: v._from, To: v._to }'
    
    # specifing that @tech_list in the query is tech_list that we declared
    bind_vars = {'tech_list': tech_list}
    cursor_tac_tec = db.aql.execute(query, bind_vars=bind_vars)

    # calls function to make a graph
    tech_tac_graph.make_graph(db, cursor_tac_tec)


def main():
    try:
        # checks the cve/cwe json file that specified in command line is valid
        in_file = str(sys.argv[1])
        if not os.path.isfile(in_file):
            print('Error: File Not Found')
            exit(1) # exits the system

        # checks the control json file that specified in command line is valid
        ctrl_file = str(sys.argv[2])
        if not os.path.isfile(ctrl_file):
            print('Error: File Not Found')
            exit(1) # exits the system

        # opens the above files
        with open(in_file, 'r') as file:
            controls = open(ctrl_file, 'r')
            controls = json.load(controls)
            data = json.load(file)
            # checks the input file contains either, cve, cwe, or other data
            for item in data:
                if 'cve' in item:  # NOTE: temp, can do other way to check the item in file
                    read_cve(data, controls)
                    break
                elif 'cwe' in item: # NOTE: temp, can do other way to check the item in file
                    read_cwe(data, controls)
                    break
                else:
                    print('Invalid (not \'cve\'/\'cwe\') item detected from the input json file')
                    break
    except IndexError:
        print("Usage: python3 [file_name] [cve/cwe.json] [controls.json]")

if __name__ == '__main__':
    main()
