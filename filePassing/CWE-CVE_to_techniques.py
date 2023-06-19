import json
import os.path
import sys

from arango import ArangoClient

# access to the arango database
client = ArangoClient()
db = client.db('BRON', username='root', password='changeme')


def read_cve(data, controls):
    for obj in data:
        for key, value in obj.items():
            query = 'for item in cve ' \
                    + 'filter item.original_id == @value ' \
                    + 'for e, v, p in 1..5 inbound item CweCve, CapecCwe, TechniqueCapec ' \
                    + 'filter LENGTH(p.edges) > 2 ' \
                    + 'return distinct LAST(p.vertices)._id'
            bind_vars = {'value': value}
            cursor = db.aql.execute(query, bind_vars=bind_vars)

            tech_list = []

            for tech in cursor:
                tech_ctrl = db.collection('TechniqueControl')
                ctrl_list = []
                for data in tech_ctrl:
                    if data['_from'] == tech:
                        ctrl_list.append(data['_to'])

                # temp testing
                in_list = False
                for item in controls:
                    for ctrl_key, ctrl_value in item.items():
                        control = 'control/' + str(ctrl_value)
                        if control in ctrl_list:
                            in_list = True
                            break
                if not in_list:
                    print(tech)


def read_cwe(data, controls):
    for obj in data:
        for key, value in obj.items():
            query = 'for item in cwe ' \
                    + 'filter item.original_id == @value ' \
                    + 'for e, v, p in 1..4 inbound item CapecCwe, TechniqueCapec ' \
                    + 'filter LENGTH(p.edges) > 1 ' \
                    + 'return distinct LAST(p.vertices)._id'
            bind_vars = {'value': value}
            cursor = db.aql.execute(query, bind_vars=bind_vars)

            tech_list = []

            for tech in cursor:
                tech_ctrl = db.collection('TechniqueControl')
                ctrl_list = []
                for data in tech_ctrl:
                    if data['_from'] == tech:
                        ctrl_list.append(data['_to'])

                # temp testing
                in_list = False
                for item in controls:
                    for ctrl_key, ctrl_value in item.items():
                        control = 'control/' + str(ctrl_value)
                        if control in ctrl_list:
                            in_list = True
                            break
                if not in_list:
                    print(tech)


def main():
    try:
        a_file = str(sys.argv[1])
        if not os.path.isfile(a_file):
            print('Error: File Not Found')
            exit(1)

        b_file = str(sys.argv[2])
        if not os.path.isfile(a_file):
            print('Error: File Not Found')
            exit(1)

        with open(a_file, 'r') as file:
            controls = open(b_file, 'r')
            controls = json.load(controls)
            data = json.load(file)
            for item in data:
                if 'cve' in item:  # TODO: Change to check the right side of the data??
                    read_cve(data, controls)
                    break
                elif 'cwe' in item:
                    read_cwe(data, controls)
                    break
                else:
                    print('hello')
                    break
    except IndexError:
        print("Must have command argument")


main()
