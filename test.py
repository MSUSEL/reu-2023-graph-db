from arango import ArangoClient

# access to the arango database
client = ArangoClient()
db = client.db('BRON', username = 'root', password = 'changeme')

query = 'for item in cve '\
        + 'filter item.original_id == \'CVE-2019-15243\' or item.original_id == \'CVE-2020-3177\' '\
        + 'for e, v, p in 1..5 inbound item CweCve, CapecCwe, TechniqueCapec '\
        + 'filter LENGTH(p.edges) > 2 '\
        + 'return distinct LAST(p.vertices)._id'

cursor = db.aql.execute(query)

tech_list = []

for tech in cursor:
    tech_ctrl = db.collection('TechniqueControl')
    ctrl_list = []
    for data in tech_ctrl:
        if data['_from'] == tech:
            ctrl_list.append(data['_to'])

    # temp testing
    if 'control/SC-7' not in ctrl_list:
        print(tech)
    #print(ctrl_list)
    # rint(d)
    # list.append(d)

# print(list)