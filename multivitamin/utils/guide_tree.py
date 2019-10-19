import sys
import pprint

from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.modular_product import mod_product, cart_product
from multivitamin.algorithms.bk_pivot_class import BK
from multivitamin.algorithms.vf2_beauty import VF2


class Guide_tree():

    def __init__(
        self,
        graph_list,
        algorithm,
        save_all,
    ):

        self.algorithm = algorithm
        self.save_all = save_all

        self.graph_abbreviations = {}
        self.graph_list = self.make_mult_id( graph_list )
        self.intermediates = []
        self.result = Graph()
        self.newick = ""


    def upgma( self ):
        if len( self.graph_list ) == 1:
            
            res = self.graph_list[0]

            res.edges = set()
            res.create_undirected_edges()
            
            self.result = res

            self.newick = self.graph_list[0].id
            self.print_alignment( self.result )

            return

        maximum = 0 # is used to save the maximum number of mapped nodes

        for g1 in self.graph_list[:]:
            for g2 in self.graph_list[:]:

                if g1.id == g2.id:
                    continue
           
                results = self.apply_algorithm( g1, g2)

                if len(max(results)) >= maximum:
                    alignment = Graph( "({},{})".format( g1.id, g2.id ), max( results ) )

                    if not list(alignment.nodes)[0].label == "":
                        alignment.nodes_are_labelled = True

                    maximum = len(max(results))
                    alig_one = g1
                    alig_two = g2

        self.graph_list.remove(alig_one)
        self.graph_list.remove(alig_two)

        alignment_graph = self.make_graph_real( alignment )
        
        self.graph_list.append( alignment_graph )
        self.intermediates.append( alignment_graph )

        self.upgma()


    def make_graph_real( self, graph ):
        for node in graph.nodes:
            for neighbour in list(node.neighbours)[:]:
                if not neighbour in graph.nodes:
                    node.remove_neighbour(neighbour)
        graph.edges = set()
        graph.create_undirected_edges()
        return graph


    def apply_algorithm( self, graph1, graph2 ):
        if self.algorithm == "BK":  
            modp = mod_product( cart_product( graph1.nodes, graph2.nodes ) )
            bk = BK()
            x = set()
            r = set()
            p = list(modp.nodes)
            bk.bk_pivot( r, p, x)
            return bk.results

        elif self.algorithm == "VF2":
            vf2 = VF2( graph1, graph2 )
            vf2.match()
            return vf2.results


    def print_alignment( self, graph ):
        print("")
        print("********************************************************************")
        print("*                                                                  *")
        print("*                           RESULTS                                *")
        print("*                                                                  *")
        print("********************************************************************")
        print("")
        print("---GRAPH ABBREVIATIONS--------------")
        print("")
        for abbrev, id in self.graph_abbreviations.items():
            print("{}\t>>\t{}".format( abbrev, id) )
        print("")
        print("")
        print("---ALIGNMENT------------------------")
        print("")
        print("*NODES (ID, LABEL, NEIGHBOURS)")
        for node in graph.nodes:
            print("{}".format(node))
        print("")
        print("*EDGES (ID, LABEL)")
        for edge in graph.edges:
            print("{}".format(edge))
        print("")
        print("")
        print("---NEWICK TREE----------------------")
        print("")
        print(graph.id)
        print("")
        print("*******************************************************************")
        print("")


    def make_mult_id( self, graph_list ):
        id_list = {}

        for graph in graph_list:
            if len(graph.id) < 3:
                # i is the number of occurrences of the short graph id in the id_list dicitonary
                i = len( [x for x in id_list.values() if x.startswith(graph.id)] ) + 1 
                id_list[graph.id] = graph.id + str(i)

            else:
                i = len( [x for x in id_list.values() if x.startswith(graph.id[0:2])] ) + 1
                id_list[graph.id] = graph.id[0:2] + str(i)
            self.graph_abbreviations[id_list[graph.id]] = graph.id

        for graph in graph_list:
            for node in graph.nodes:
                node.mult_id = "{}.{}".format( id_list[graph.id], node.id )

        return graph_list




if __name__ == '__main__':

    g_list = []

    for arg in sys.argv[1:]:
        g = parse_graph(arg)
        g_list.append( g )

    guide_tree = Guide_tree( g_list, "BK", False )

    guide_tree.upgma()
    print(guide_tree.result)
