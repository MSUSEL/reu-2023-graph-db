# from arango import ArangoClient

# # access to the arango database
# client = ArangoClient()
# db = client.db('BRON', username = 'root', password = 'changeme')

if db.has_graph('gb'):
    db.delete_graph('gb')

# gb = db.create_graph('gb')

tt = gb.create_edge_definition(
    edge_collection = 'TacticTechnique_user',
    from_vertex_collections = ['tactic'],
    to_vertex_collections = ['technique']
)

# tat = gb.create_edge_definition(
#     edge_collection = ''
# )

str = 'hello/goodbye'
if 'good' in str:
    print('Yes')
else:
    print('No')
# query = 'let iterable = ( '\
#     + 'for item in cve '\
#     + 'filter item.original_id in [\'CVE-2019-15243\', \'CVE-2020-3177\', \'CVE-2020-1472\'] '\
#     + 'for e, v, p in 1..5 inbound '\
#     + 'item CweCve, CapecCwe, TechniqueCapec '\
#     + 'filter length(p.edges) > 2 '\
#     + 'return distinct Last(p.vertices)) '\
#     + 'for item in iterable '\
#     + 'return item._id'
#     # + 'for e, v, p in 1..2 inbound '\
#     # + 'item TacticTactic, TacticTechnique '\
#     # + 'return p'

# cursor = db.aql.execute(query)

# for c in cursor:
#     # if c != 
#     print(c)

# g.insert_edge(collection='TacticTechnique', edge={'_from': 'tactic/tactic_00002', '_to': 'technique/technique_00183'})
# print(g.edge_definitions())