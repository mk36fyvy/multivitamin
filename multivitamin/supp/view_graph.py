#!/bin/python3

import sys
import pprint
import networkx as nx
import matplotlib.pyplot as plt

from multivitamin.utils.parser import parse_graph



def create_graph( id, nodes, edges):
    g = nx.Graph()

    g.add_nodes_from(nodes)

    edge_label_dict = {}

    for edge in edges:
        g.add_edge( edge.node1, edge.node2 )
        edge_label_dict[edge.node1, edge.node2] = edge.label

    node_label_dict = {}
    for node in nodes:
        node_label_dict[node] = "{} '{}'".format(node.id, node.label)

    pos = nx.kamada_kawai_layout(g)
    #pos = nx.planar_layout(G) #no edge intersections

    nx.draw_networkx_nodes(g, pos, node_color='#66ffff', cmap=plt.get_cmap('jet'), node_size=500)
    #nx.draw_networkx_nodes(g, pos, node_color='000000', cmap=plt.get_cmap('jet'), node_size=[len(node.id) * 500 for node in nodes])
    nx.draw_networkx_labels(g, pos, labels=node_label_dict, font_size=10, font_weight='bold', font_color='black')
    nx.draw_networkx_edges(g, pos, edge_color='grey')
    #nx.draw_networkx_edge_labels(g, pos, edge_labels=node_label_dict)
    plt.title(id)
    plt.show()


if __name__ == "__main__":

    g = parse_graph(sys.argv[1])
#    print(str(g.id))
    # g = sys.argv[1]
    # print(g)

    create_graph(g.id, g.nodes, g.edges)
