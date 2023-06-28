# imports
import networkx as nx
from pyvis import network as net
import webbrowser
import os


# method to create web browser graph
def make_graph(db, cursor):
    # setting up the graph
    tac_tac = db.collection('TacticTactic')
    graph = nx.Graph()
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
    for tt in tac_tac:
        if tt['_from'] in tactech_from_list and tt['_to'] in tactech_from_list:
            graph.add_edge(tt['_from'], tt['_to'])

    show_prioritize(graph)

    # translates networkx graph into PyViz graph
    g.from_nx(graph)
    g.show('graph.html')
    # open the custom PyViz graph in the default web browser
    webbrowser.open('file://' + os.path.abspath(os.getcwd()) + '/graph.html')


# method to sort the individual priority lists
def sort_list(a_list):
    return sorted(a_list, key=lambda tup: tup[1], reverse=False)  # lambda arguments : expression


def show_prioritize(graph):
    # priority of tactic
    high = []
    mid = []
    low = []
    # iterate over every node in the graph
    for node in graph.__iter__():
        # if its a tactic node
        if 'tactic' in node:
            # start the edge type counters
            cnt_tac = 0
            cnt_tech = 0
            for neighbor in graph.neighbors(node):
                if 'technique' in neighbor:
                    # add a technique edge
                    cnt_tech += 1
                else:
                    # add a tactic edge
                    cnt_tac += 1
            # sort the nodes into high, mid, and low priority based on tactic to tactic connectivity
            match cnt_tac:
                case 0:
                    low.append((node, cnt_tech))
                case 1:
                    mid.append((node, cnt_tech))
                case _:
                    high.append((node, cnt_tech))
    # sort the individual lists
    low = sort_list(low)
    mid = sort_list(mid)
    high = sort_list(high)

    # determine the highest priority node and change color to red
    #print('Low:', low, "\nMid:", mid, "\nHigh:", high)
    if high.__len__() > 0 and graph.has_node(high[0][0]):
        graph.add_node(high[0][0], color='red')
    elif mid.__len__() > 0 and graph.has_node(mid[0][0]):
        graph.add_node(mid[0][0], color='red')
    elif low.__len__() > 0 and graph.has_node(low[0][0]):
        graph.add_node(low[0][0], color='red')
    else:
        pass
