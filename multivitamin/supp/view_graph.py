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
            label_string = "["
            for el in node.label:
	        label_string += el
                label_string += " "
            label_string = label_string[:-1]
            node_label_dict[node] = label_string

        pos = nx.kamada_kawai_layout(G)
        plt.subplot(plot_size,plot_size,i)
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', cmap=plt.get_cmap('jet'), node_size=50)
        nx.draw_networkx_labels(G, pos, labels=node_label_dict, font_size=5, font_weight='bold', font_color='black')
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
            # label_string = "["
            # for el in list(node.label):
            #     print(el)
            #     label_string += el
            #     label_string += "."
            # label_string += "]"
            node_label_dict[node] = node.get_node_label_string()

            # node_label_dict[node] = label_string

        pos = nx.kamada_kawai_layout(G)
        plt.figure(i)
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', cmap=plt.get_cmap('jet'), node_size=50)
        nx.draw_networkx_labels(G, pos, labels=node_label_dict, font_size=7, font_weight='bold', font_color='black')
        nx.draw_networkx_edges(G, pos, edge_color='grey')
        plt.title(str(graph_list[i-1].id))
    plt.show()
