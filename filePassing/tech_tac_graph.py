from arango import ArangoClient
import networkx as nx
#import matplotlib.pyplot as plt
from pyvis import network as net
from IPython.core.display import display, HTML
import webbrowser
import os

# client = ArangoClient()
# db = client.db('BRON', username='root', password='changeme')


def make_graph(db, cursor):
    TacTac = db.collection('TacticTactic')
    graph = nx.DiGraph()
    g = net.Network(height='100vh', width='100%', notebook=True)

    # query = 'let iterable = ( ' \
    #         + 'for item in cve ' \
    #         + 'filter item.original_id in [\'CVE-2019-15243\',\'CVE-2020-3177\',\'CVE-2020-1472\'] ' \
    #         + 'for e, v, p in 1..5 inbound ' \
    #         + 'item CweCve, CapecCwe, TechniqueCapec ' \
    #         + 'filter length(p.edges) > 2 ' \
    #         + 'return distinct Last(p.vertices) ' \
    #         + ') ' \
    #         + 'for item in iterable ' \
    #         + 'for e, v, p in 1..2 inbound ' \
    #         + 'item TacticTechnique ' \
    #         + 'return { From: v._from, To: v._to }'
    
    #cursor = db.aql.execute(query)

    tactech_from_list = []

    for item in cursor:
        key, value = item.items()
        graph.add_nodes_from([key[1], value[1]])
        graph.add_edge(key[1], value[1])
        tactech_from_list.append(key[1])

    for tt in TacTac:
        if tt['_from'] in tactech_from_list and tt['_to'] in tactech_from_list:
            graph.add_edge(tt['_from'], tt['_to'])

    #nx.draw_networkx(graph)
    #plt.show()
    g.from_nx(graph)
    #g.show_buttons(filter_=['physics'])
    g.show('custom.html')
    webbrowser.open('file://' + os.path.abspath(os.getcwd()) + '/custom.html')

# def main():
#     makegraph()

# main()
