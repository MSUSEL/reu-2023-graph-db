# imports 
from arango import ArangoClient
import networkx as nx
from pyvis import network as net
import webbrowser
import os

# method to create web browser graph
def make_graph(db, cursor):
    # setting up the graph
    TacTac = db.collection('TacticTactic')
    graph = nx.DiGraph()
    g = net.Network(height='100vh', width='100%', notebook=True)

    # list for easy checking later
    tactech_from_list = []

    # takes the ._from ._to edge from the cursor query
    for item in cursor:
        key, value = item.items()
        # adding nodes and edge into networkx graph
        graph.add_nodes_from([key[1], value[1]])
        graph.add_edge(key[1], value[1])
        # adding tactic into list for easy checking
        tactech_from_list.append(key[1])

    # this is checking the BRON database for tactic to tactic 
    # paths that need to be placed into the networkx graph
    for tt in TacTac:
        if tt['_from'] in tactech_from_list and tt['_to'] in tactech_from_list:
            graph.add_edge(tt['_from'], tt['_to'])

    # translates networkx graph into PyViz graph
    g.from_nx(graph)
    # this is a list of sliders that can interact with the graph, adds things like wind and gravity
    #g.show_buttons(filter_=['physics'])
    g.show('custom.html')
    # open the custom PyViz graph in the default web browser
    webbrowser.open('file://' + os.path.abspath(os.getcwd()) + '/custom.html')
