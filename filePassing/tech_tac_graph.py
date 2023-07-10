# imports
import networkx as nx
from pyvis import network as net
import webbrowser
import os
import json

# method to create web browser graph
def make_graph(db, cursor):
    #temp
    print('Creating a graph...')

    # setting up the graph
    tac_tac = db.collection('TacticTactic')
    graph = nx.Graph()
    g1 = net.Network(height='100vh', width='100%', notebook=True)
    g2 = net.Network(height='100vh', width='100%', notebook=True)

    # graph that contains only the paths between tactics
    tac_graph = nx.DiGraph()

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
            tac_graph.add_edge(tt['_from'], tt['_to'])

    show_prioritize(graph) # runs algorithm that finds the prioritize paths

    net_flow_graph = make_net_flow_graph(graph, tac_graph)

    # translates networkx graph into PyViz graph
    g1.from_nx(graph)
    g1.force_atlas_2based() # changing the layout of the graph
    g1.show('graph.html')

    # translates network flow graph into PyViz graph
    g2.from_nx(net_flow_graph)
    g2.force_atlas_2based() # changing the layout of the graph
    g2.show('network_flow.html')

    # open the custom PyViz graph in the default web browser
    webbrowser.open('file://' + os.path.abspath(os.getcwd()) + '/graph.html')
    webbrowser.open('file://' + os.path.abspath(os.getcwd()) + '/network_flow.html')


# method to sort the individual priority lists
def sort_list(a_list):
    return sorted(a_list, key=lambda tup: tup[1], reverse=False)  # lambda arguments : expression


# finds priority of tactic
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
    print('Low:', low, "\nMid:", mid, "\nHigh:", high)
    if high.__len__() > 0 and graph.has_node(high[0][0]):
        graph.add_node(high[0][0], color='red')
    elif mid.__len__() > 0 and graph.has_node(mid[0][0]):
        graph.add_node(mid[0][0], color='red')
    elif low.__len__() > 0 and graph.has_node(low[0][0]):
        graph.add_node(low[0][0], color='red')
    else:
        pass


# creates a network flow graph
def make_net_flow_graph(graph, tac_graph):
    net_flow_graph= nx.DiGraph()
    SRC = 'source[s]' # starting point of the graph
    SINK = 'sink[t]' # ending point of the graph

    # prepares unique nodes for the graph
    nodes = [[SRC]] # starting node
    for n in tac_graph.__iter__(): # gets tactic in order of path
        tech = []
        neighbors = graph.neighbors(n)
        for node in neighbors: # loops to get all techniques
            if 'technique' in node:
                tech.append(n.split('/')[-1] + '/' + node.split('/')[-1]) # assigns unique name
        nodes.append(tech)
    nodes.append([SINK]) # ending node

    # adds nodes and edges to the network flow graph
    for i in range(len(nodes)-1):
        for j in range(len(nodes[i])):
            net_flow_graph.add_node(nodes[i][j])

            # checks what capacity to set
            if nodes[i][j] == 'source[s]':
                capa = len(nodes[i+1])
            else:
                capa = len(nodes[i])
            for k in range(len(nodes[i+1])):
                net_flow_graph.add_edge(nodes[i][j], nodes[i+1][k], capacity=capa, title=capa)
    
    return net_flow_graph


# creates a json file that contains all simple paths of network flow graph
def create_simple_paths_json(net_flow_graph, src, sink):
    simple_paths = [] # lists that will hold the json objects
    for path in nx.all_simple_paths(net_flow_graph, src, sink):
        simple_paths.append({'path': path})
    
    # creates and adds the json objects to the file
    with open('net_flow_graph.json', 'w') as out_file:
        json.dump(simple_paths, out_file, indent=2)
