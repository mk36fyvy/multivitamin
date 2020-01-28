#!/bin/python3

import sys
import networkx as nx
import matplotlib.pyplot as plt
import math

def create_graph( graph_list):
    plot_size = math.ceil(math.sqrt(len(graph_list)))
    for i in range(1,len(graph_list) + 1):
        nodes = graph_list[i-1].nodes
        edges = graph_list[i-1].edges
        G = nx.Graph()
        G.add_nodes_from(nodes)
        edge_label_dict = {}

        for edge in edges:
            G.add_edge( edge.node1, edge.node2 )
            edge_label_dict[edge.node1, edge.node2] = edge.label

        node_label_dict = {}
        for node in nodes:
            node_label_dict[node] = "{} '{}'".format(node.id, node.label)

        pos = nx.kamada_kawai_layout(G)
        plt.subplot(plot_size,plot_size,i)
        nx.draw_networkx_nodes(G, pos, node_color='#66ffff', cmap=plt.get_cmap('jet'), node_size=500)
        nx.draw_networkx_labels(G, pos, labels=node_label_dict, font_size=10, font_weight='bold', font_color='black')
        nx.draw_networkx_edges(G, pos, edge_color='grey')
        plt.title(str(graph_list[i-1].id))
    plt.show()


def create_graphs( graph_list):
    for i in range(1,len(graph_list) + 1):
        nodes = graph_list[i-1].nodes
        edges = graph_list[i-1].edges
        G = nx.Graph()
        G.add_nodes_from(nodes)
        edge_label_dict = {}

        for edge in edges:
            G.add_edge( edge.node1, edge.node2 )
            edge_label_dict[edge.node1, edge.node2] = edge.label

        node_label_dict = {}
        for node in nodes:
            # node_label_dict[node] = "{} '{}'".format(node.id, node.label)
            node_label_dict[node] = "{}".format(node.label)

        pos = nx.kamada_kawai_layout(G)
        plt.figure(i)
        nx.draw_networkx_nodes(G, pos, node_color='#66ffff', cmap=plt.get_cmap('jet'), node_size=500)
        nx.draw_networkx_labels(G, pos, labels=node_label_dict, font_size=10, font_weight='bold', font_color='black')
        nx.draw_networkx_edges(G, pos, edge_color='grey')
        plt.title(str(graph_list[i-1].id))
    plt.show()