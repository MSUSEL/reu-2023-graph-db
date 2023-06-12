from arango import ArangoClient


client = ArangoClient()
db = client.db('BRON', username='root', password='changeme')

TacTac = 'TacticTactic'

graph = db.graph('BRONGraph')

if graph.has_edge_definition(TacTac):
    graph.delete_edge_definition(TacTac)
    db.delete_collection(TacTac)

graph.create_edge_definition(
    edge_collection=TacTac,
    from_vertex_collections=['tactic'],
    to_vertex_collections=['tactic']
)

TT = graph.edge_collection(TacTac)

tactic = db.collection('tactic')

temp = 'tactic/tactic_000'

tac1 = {'_to' : temp+'14', '_from': temp+'13'}
tac2 = {'_to' : temp+'09', '_from': temp+'14'}
tac3 = {'_to' : temp+'06', '_from': temp+'09'}
tac4 = {'_to' : temp+'11', '_from': temp+'06'}
tac5 = {'_to' : temp+'12', '_from': temp+'11'}
tac6 = {'_to' : temp+'04', '_from': temp+'12'}
tac7 = {'_to' : temp+'03', '_from': temp+'04'}
tac8 = {'_to' : temp+'05', '_from': temp+'03'}
tac9 = {'_to' : temp+'10', '_from': temp+'05'}
tac10 = {'_to' : temp+'01', '_from': temp+'10'}
tac11 = {'_to' : temp+'02', '_from': temp+'01'}
tac12 = {'_to' : temp+'07', '_from': temp+'02'}
tac13 = {'_to' : temp+'08', '_from': temp+'07'}

TT.import_bulk([tac1, tac2, tac3, tac4, tac5, tac6, tac7, tac8, tac9, tac10, tac11, tac12, tac13])
