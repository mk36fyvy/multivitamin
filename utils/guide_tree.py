from algorithms.vf2_beauty import VF2
from modular_product import *
from bk_pivot_class import BK
from parser import parse_graph
from graph import Graph
import sys


# TODO: Change graph_list to dict with g.id as key
def upgma( graph_list ):

    #alignment = Graph('0')
    if len( graph_list ) == 1:
        make_graph_real(graph_list[0])
        graph_list[0].create_undirected_edges()
        print_alignment(graph_list[0])
        return graph_list
    maximum = 0

    for g1 in graph_list[:]:
        for g2 in graph_list[:]:

            if g1.id == g2.id:
                continue

            modp = mod_product( cart_product( g1.nodes, g2.nodes))
            bk = BK()
            x = set()
            r = set()
            p = list(modp.nodes)

            bk.bk_pivot( r, p, x)
           # print(bk.bk_pivot(r,p,x))

            if len(max(bk.results)) >= maximum:
                alignment = Graph( "({},{})".format( g1.id, g2.id ), max( bk.results ) )
                # alignment.create_undirected_edges()
                maximum = len(max(bk.results))
                alig_one = g1
                alig_two = g2

    graph_list.remove(alig_one)
    graph_list.remove(alig_two)
    graph_list.append( alignment )
    upgma(graph_list)

def make_graph_real(graph):
    for node in graph.nodes:
        for neighbour in list(node.neighbours)[:]:
            if not neighbour in graph.nodes:
                node.remove_neighbour(neighbour)
    # for edge in list(graph.edges)[:]:
    #     if not all((edge.node1 in graph.nodes, edge.node2 in graph.nodes)):
    #         graph.edges.remove(edge) 

def print_alignment(graph):
    


    #OUTPUT----------------------
    print()
    print("********************************************************************")
    print("*                                                                  *")
    print("*                           RESULTS                                *")
    print("*                                                                  *")
    print("********************************************************************")
    print()
    print()
    print("---ALIGNMENT---------")
    print()
    print("*NODES (ID, LABEL, NEIGHBOURS")
    for node in graph.nodes:
        print("{}".format(node))
    print()
    print("*EDGES (ID, LABEL)")
    for edge in graph.edges:
        print("{}".format(edge))
    print()
    print()
    print("---NEWICK TREE-------")
    print()
    print(graph.id)
    print()


if __name__ == '__main__':

    g_list = []

    for arg in sys.argv[1:]:
        g = parse_graph(arg)
        g_list.append( g )

    #print(g_list)
    res = upgma( g_list )
    print(res)
