import sys
import pprint
from ete3 import Tree

from multivitamin.basic.node import Node
from multivitamin.basic.graph import Graph
from multivitamin.basic.guide_tree import Guide_tree
from multivitamin.utils.parser import parse_graph, edges_contain_doubles
from multivitamin.utils.modular_product_class import MP
from multivitamin.utils.scoring import Scoring
from multivitamin.algorithms.bk_pivot_class import BK
from multivitamin.algorithms.vf2_beauty import VF2
from multivitamin.algorithms.vf2_subsub import subVF2


class Multalign():

    def __init__(
        self,
        graph_list,
        algorithm,
        method,
        save_all,
        scoring_matrix=None
    ):

        self.algorithm = algorithm
        self.method = method
        self.save_all = save_all

        self.graph_abbreviations = {}
        self.graph_list = self.make_mult_id( graph_list )
        self.intermediates = []
        self.result = Graph()
        self.newick = ""

        self.already_done = {}

        self.scoring_matrix = scoring_matrix if scoring_matrix else "-1"


    def multalign( self ):
        '''
        performs multiple alignment according to specified multiple alignment algorithm.
        '''

        if self.method == "GREEDY":
            self.greedy()

        elif self.method == "PROGRESSIVE":
            raise AttributeError("This is not yet implemented, sorry! Please use the default setting.")

        else:
            print("Aligning along the provided guide tree...")
            self.guided_alignment( self.method ) # in this case, self.method contains the alignment tree as tree object


    def greedy( self ):
        '''
        performs multiple alignment following a greedy approach: Every pairwise alignment is
        calculated and the best scoring co-optimal is chosen. Then, the best scored pairwise
        alignment is chosen. Then, all pairwise alignments with this new graph are calculated
        and scored and so on.
        '''

        if len( self.graph_list ) <= 1:
            try:
                res = self.graph_list[0]
            except:
                return

            res.edges = set()
            res.create_undirected_edges()
            self.result = res
            self.newick = self.graph_list[0].newick
            return

        maximum_score = float('-inf') # is used to save the maximum number of mapped nodes
        counter = 1 # makes sure that every graph couple is only processed once

        for g1 in self.graph_list[:-1]:
            for g2 in self.graph_list[counter:]:
                if g1.id == g2.id:
                    continue

                if ( g1.id, g2.id ) in self.already_done.keys():
                    max_alignment = self.already_done[( g1.id, g2.id )]
                else:
                    # print()
                    # print("Aligning {} and {}...".format(g1.id,g2.id))
                    # print(g1)
                    # print(g2)
                    # print()
                    max_alignment = self.apply_algorithm( g1, g2 )[0]
                    self.already_done[( g1.id, g2.id )] = max_alignment

                if max_alignment[1] > maximum_score: #subVF2

                    alignment = Graph( "{}-{}".format( g1.abbrev, g2.abbrev ), max_alignment[0] )
                    alignment.abbrev = alignment.id
                    alignment.newick = "({},{})".format( g1.newick, g2.newick)

                    maximum_score = max_alignment[1]
                    alig_one = g1
                    alig_two = g2

            counter += 1

        self.graph_list.remove(alig_one)
        self.graph_list.remove(alig_two)

        self.remove_element( self.already_done, ( alig_one.id, alig_two.id) )

        alignment_graph = self.make_graph_real( alignment )
        alignment_graph = self.generate_graph_bools( alignment_graph )

        self.graph_list.append( alignment_graph )
        self.intermediates.append( alignment_graph )

        if Node("null", []) in alignment.nodes and self.algorithm == "VF2":
            raise Exception("VF2 could not produce a multiple alignment of all the given graphs. \n The classical VF2 algorithm can only process *graph-subgraph*-isomorphism. \n Please consider using subVF2 algorithm instead.")

        self.greedy()


    def guided_alignment( self, tree ):

        def get_graph( el ):
            if el.graph is not None:
                return el.graph
            else:
                alignment = self.apply_algorithm( get_graph(el.lchild), get_graph(el.rchild))[0]
                graph = Graph( "{}-{}".format( el.lchild.graph.abbrev, el.rchild.graph.abbrev ), alignment[0] )
                graph.abbrev = graph.id
                graph.newick = "({},{})".format( el.lchild.graph.newick, el.rchild.graph.newick)
                alignment_graph = self.make_graph_real( graph )
                alignment_graph = self.generate_graph_bools( alignment_graph )
                el.graph = alignment_graph
                return alignment_graph

        gt = Guide_tree( tree, self.graph_list )
        gt.root.graph = get_graph( gt.root )
        res = gt.root.graph
        res.edges = set()
        res.create_undirected_edges()
        self.result = res
        self.newick = gt.root.graph.newick




    # ---- HELPER METHODS ------------------------------------------------------------------------------------

    
    
    def make_graph_real( self, graph ):
        '''
        takes an alignment consisting only of nodes with neighbours, creates the
        appropriate edges and returns an *undirected* graph.
        '''

        graph.edges = set()
        graph.create_undirected_edges()
        return graph


    def apply_algorithm( self, graph1, graph2 ):
        '''
        performs pairwise alignment using the algorithm provided. At the moment,
        SUBVF2 algorithm is the only working algorithm for multiple alignment
        '''

        if self.algorithm == "BK":
            raise Exception("BK algorithm is not usable for multiple alignment at the moment. But it is slow as hell anyway. Please use 'subVF2', which is also the default algorithm.")

            mp = MP( graph1, graph2 )

            bk = BK( graph1, graph2 )
            x = set()
            r = set()
            p = list(mp.modp)
            bk.bk_pivot( r, p, x)
            results = bk.clique_to_node_set()

            max_res = results[0]
            max_res_neighbour_sum = 0
            for res in results:
                for max_node in max_res:
                    max_res_neighbour_sum += len(max_node.neighbours)
                neighbour_sum = 0
                for node in res:
                    neighbour_sum += len(node.neighbours)
                if neighbour_sum > max_res_neighbour_sum:
                    max_res = res
                    max_res_neighbour_sum = neighbour_sum
            return max_res

        elif self.algorithm == "VF2":
            raise Exception("VF2 algorithm is not really what you want for multiple alignment. Trust me. Really. Use 'subVF2' instead, please. Thanks.")

            vf2 = VF2( graph1, graph2 )
            vf2.match()
            if not vf2.results:
                vf2.results.append([Node("null","")])
            return max(vf2.results)

        elif self.algorithm == "SUBVF2":
            subvf2 = subVF2( graph1, graph2, self.scoring_matrix )
            subvf2.match()
            return subvf2.results


    def generate_graph_bools( self, graph ):
        if not list(graph.nodes)[0].label == "":
            graph.nodes_are_labelled = True

        if len(graph.nodes) > 1:
            try:
                if not list(graph.edges)[0].label == "":
                    graph.edges_are_labelled = True
            except: #graph has no edges
                graph.nodes_are_labelled = False

        if edges_contain_doubles( graph.edges ):
            graph.is_directed = True

        return graph


    def remove_element( self, dictionary, key):
        """
        Returns a shallow copy of the dictionary without a specified key.
        """

        _dict = dictionary.copy()
        _dict.pop(key, None)
        return _dict


    def make_mult_id( self, graph_list ):
        '''
        takes a list of all graphs for multiple alignments and provides them with
        unique IDs for the alignment. These consist of the first 2 characters of
        the graph file name and a number that increments each time the 2-char-name
        is already taken.
        '''

        id_list = {}

        for graph in graph_list:
            if len(graph.id) < 3:
                # i is the number of occurrences of the short graph id in the id_list dictionary
                i = len( [x for x in id_list.values() if x.startswith(graph.id)] ) + 1
                graph.abbrev = graph.id + str(i)
                id_list[graph.id] = graph.abbrev

            else:
                i = len( [x for x in id_list.values() if x.startswith(graph.id[0:2])] ) + 1
                graph.abbrev = graph.id[0:2] + str(i)
                id_list[graph.id] = graph.abbrev
            self.graph_abbreviations[id_list[graph.id]] = graph.id

        for graph in graph_list:
            for node in graph.nodes:
                # print(type(node.mult_id))
                # print(node.mult_id)
                node.mult_id.append("{}:{}".format( graph.abbrev, node.id ))

        return graph_list


    def __str__( self ):
        if not self.result:
            return ""
        r = ""
        r += "\n*****************************************************************\n"
        r += "*                                                               *\n"
        r += "*                          RESULTS                              *\n"
        r += "*                                                               *\n"
        r += "*****************************************************************\n\n"
        r += "---GRAPH ABBREVIATIONS--------------\n\n"
        for abbrev, id in self.graph_abbreviations.items():
            r += "  {}\t>>\t{}\n".format( abbrev, id)
        r += "\n\n---ALIGNMENT------------------------\n\n"
        r += "*NODES (ID, LABEL, NEIGHBOURS)\n"
        node_list = list(self.result.nodes)
        node_list.sort( key= lambda x: x.label, reverse=True )
        for node in node_list:
            r += "  {}\n".format(node)
        r += "\n*EDGES (ID, LABEL)\n"
        for edge in self.result.edges:
            r += "{}\n".format(edge)
        r += "\n\n---NEWICK TREE----------------------\n\n"
        r += self.result.newick
        r += "\n********************************************************************\n\n"
        return r

