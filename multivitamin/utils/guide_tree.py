import sys

from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.modular_product import *
from multivitamin.algorithms.bk_pivot_class import BK
from multivitamin.algorithms.vf2_beauty import VF2


class Guide_tree():

    def __init__(
        self,
        graph_list
    ):

        self.graph_list = []
        self.newick = ""


    def upgma( self ):

        #alignment = Graph('0')
        if len( self.graph_list ) == 1:
            
            result = self.graph_list[0]
            
            self.make_graph_real( result )
            result.create_undirected_edges()
            self.print_alignment( result )
            
            return result

        
        maximum = 0 # is used to save 

        for g1 in self.graph_list[:]:
            for g2 in self.graph_list[:]:

                if g1.id == g2.id:
                    continue

                modp = mod_product( cart_product( g1.nodes, g2.nodes ) )
                bk = BK()
                x = set()
                r = set()
                p = list(modp.nodes)

                bk.bk_pivot( r, p, x)

                if len(max(bk.results)) >= maximum:
                    alignment = Graph( "({},{})".format( g1.id, g2.id ), max( bk.results ) )
                    maximum = len(max(bk.results))
                    alig_one = g1
                    alig_two = g2

        self.graph_list.remove(alig_one)
        self.graph_list.remove(alig_two)
        self.graph_list.append( alignment )
        
        self.upgma()


    def make_graph_real( self, graph ):
        for node in graph.nodes:
            for neighbour in list(node.neighbours)[:]:
                if not neighbour in graph.nodes:
                    node.remove_neighbour(neighbour)
    

    def print_alignment( self, graph ):
        
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

    guide_tree = Guide_tree( g_list )

    res = guide_tree.upgma()
    print(res)
