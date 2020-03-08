'''
This class contains the core alignment algorithm.
The subgraph-subgraph-isomorphism algorithm is based on VF2 algorithm by Cordella et al (hence the name).
However, given that the classic VF2 algorithm  was designed to find graph-subgraph or graph-graph isomorphisms,
the algorithm was substantially modified.

Basically, the algorithm performs a depth-first search for legal alignments. If you specified illegal alignments
from a label point of view in custom.py, these will be disregarded here. Plus, the search tree is pruned by
all the possible matchings that have already been tried before.
'''

import sys
import pprint

from multivitamin.custom import check_semantics
from multivitamin.basic.node import Node
from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.scoring import Scoring
from multivitamin.supp.progress_bar import print_progress_bar
from multivitamin.utils.parser import edges_contain_doubles


class SubVF2():

    def __init__(self, g, h, scoring_matrix=None):


        if g.int_size() > h.int_size():
            self.small_g = h
            self.large_g = g
        else:
            self.small_g = g
            self.large_g = h

        self.scoring_matrix = scoring_matrix if scoring_matrix else '-1'


        # if the graph is undirected, the inverse edges (1,2 -> 2,1) are
        # constructed to work with the original VF2 algorithm
        if not self.large_g.is_directed:
            self.large_g.create_fake_directions()
        if not self.small_g.is_directed:
            self.small_g.create_fake_directions()


        # Initializing the two core dictionaries that store each node of the
        # Corresponding graph as key and the node of the other graph where it maps
        # As soon as it maps for now we use None as inital value
        self.core_s = self.small_g.gen_dict( None )
        self.core_l = self.large_g.gen_dict( None )

        # forbidden nodes per layer, cleared when backtracked above a layer, reduces search space
        self.forbidden_nodes =  { layer : set() for layer in range(self.large_g.int_size()) } #maximum depth

        self.result_graphs = []
        self.results = []

        # The following attributes are used for subgraph-subgraph matching.
        self.found_complete_matching = False # to turn off subsub search
        self.max_depth_matching = -1
        self.biggest_matches = [] #saves all co-optimals

        # progress bar
        self.i = 0
        print_progress_bar(self.i, len(self.large_g.nodes), prefix = 'Progress:', suffix = 'Complete', length = 50)


    def match( self, last_mapped=(None, None), depth=0 ):
        # print("- Entered Matching at depth {}\n".format(depth))
        if self.s_in_small_g():
            self.found_complete_matching = True
            scoring = Scoring( len(self.small_g.nodes), len(self.large_g.nodes), [self.core_s], self.scoring_matrix )
            scoring.score()

            self.append_result_subgraph( scoring.get_best_result() )
            self.restore_ds( last_mapped[0], last_mapped[1], depth )

            # print("<<< pop {}\n".format(last_mapped))
            return

        found_pair = False
        for choice_l in self.free_ls( depth ): #choosen starting node for large graph, one may think about ordering those in advance to optimize searching tree
            p = self.compute_p( choice_l, depth ) #new compute_pairs from an l_node
            # print("??? candidate pairs:\t{}\n".format(p))
            if depth == 0 and not self.found_complete_matching:
                print_progress_bar(self.i, len(self.large_g.nodes), prefix = 'Estimated progress:', suffix = 'Aligning {} and {}'.format( self.small_g.id, self.large_g.id ), length = 50)
                self.i += 1
            for tup in p:

                if self.is_feasible( tup[0], tup[1] ):
                    found_pair = True
                    self.compute_s_( tup[0], tup[1] )
                    # print(">>> push {}\n".format(tup))
                    self.forbidden_nodes[depth+1] = self.forbidden_nodes[depth].copy()
                    self.match( tup, depth+1 )

            self.forbidden_nodes[depth].add(choice_l) #add the node of the larger graph that was exhaustively explored to the forbidden nodes for all search trees of current or higher depth

        # if the matching isn't continued and the current depth is higher than/
        # equal to the max depth reached until now: save the subgraph
        if not found_pair and not self.found_complete_matching:
            if depth >= self.max_depth_matching:
                if depth > self.max_depth_matching:
                    # print("\n!!! clearing max matchings, new max_depth {}".format(depth))
                    self.max_depth_matching = depth
                    self.biggest_matches = []
                    # print("\n+ added new max matching:\n{}\n".format(self.core_s))
                self.biggest_matches.append(self.core_s.copy())

        if depth > 0:
            self.restore_ds( last_mapped[0], last_mapped[1], depth )


        #if we returned to the start and no "complete" matching has been found
        if depth == 0 and not self.found_complete_matching:
            self.found_complete_matching = True

            scoring = Scoring( len(self.small_g.nodes), len(self.large_g.nodes),self.biggest_matches, self.scoring_matrix )
            scoring.score()

            self.append_result_subgraph( scoring.get_best_result() )
            print_progress_bar(len(self.large_g.nodes), len(self.large_g.nodes), prefix = 'Estimated progress:', suffix = 'Aligning {} and {}'.format( self.small_g.id, self.large_g.id ), length = 50)

            # print("<<< pop {}\n".format(last_mapped))
            return
            # print("<<< pop {}\n".format(last_mapped))


    def s_in_small_g(self):
        """
        checks if every node of the small graph is mapped to a node in the
        large graph and return True or False accordingly
        """

        for node in self.core_s:
            if not self.core_s[node]:
                return False
        return True


    def free_ls( self, depth ):
        if depth == 0:
            _ls = self.large_g.nodes # if no matching was present yet, all nodes of large graph can be choosen

        else:
            _ls = set() # if an alignment was present, compute all neighbours in large graph
            for node in [n for n in self.core_l if self.core_l[n]]: # current matching
                for neigh in node.neighbours:
                    if not self.core_l[neigh]: # neighbours of currently matched l_nodes that are not in the matching themselves
                        _ls.add(neigh)

        return [node for node in _ls if node not in self.forbidden_nodes[depth]] # the things computed above minus currently forbidden nodes


    def compute_p( self, l_node, depth ):
        '''
        computes possible candidates for matching with a given node from the larger graph
        '''
        if depth == 0:
            return self.cart_p2(l_node, self.small_g.nodes) # all of the smaller graph is available at the start

        else:
             diff_s = set()
             for node in [n for n in self.core_s if self.core_s[n]]:
                 for neigh in node.neighbours:
                     if not self.core_s[neigh]:
                         diff_s.add(neigh)

             return self.cart_p2(l_node, diff_s)


    def is_feasible( self, n ,m ):

        '''
        first, checks zero_look ahead (if there are neighbours of the candidate pair that
        are in the current mapping, they have to be mapped to each other) then, checks some
        semantic conditions specified in check_semantics which is imported from
        multivitamin/custom.py
        '''

        # 0-look-ahead
        if not all((
            self.zero_look_ahead(n, m, self.core_l),
            self.zero_look_ahead(m, n, self.core_s) ) ): # is this symmetric for undirected graphs? I left it here until now because I'm not sure
            return False

        return True # moved check_semantics to explicit calls where candidate pairs are generated


    def compute_s_(self, n, m):
        '''
        adds the feasible candidate pair (n, m) to current mapping
        '''

        self.core_l[n] = m
        self.core_s[m] = n


    def restore_ds(self, n, m, depth):
        '''
        in order to return to one level above (i.e depth -= 1), some data structures have
        to be brought back to their original state
        '''

        if any((not n, not m)):
            raise(Exception("None restored"))


        self.core_l[n] = None
        self.core_s[m] = None



# HELPER FUNCTIONS ------------------------------------------------------------

    def cart_p2( self, l_node, s_nodes ):
        '''cartesian product of l_node with all available s_nodes'''
        cp = set()
        for s_node in s_nodes:
            # if not self.core_s[s_nodes]: # redundant because compute_p checks for nodes not in core_s
            if check_semantics(l_node, s_node):
                cp.add( (l_node, s_node) )
        return cp


    def legal_max(self, t_dict):
        '''returns node from t_dict with max id'''
        max_node = None
        for node in t_dict:
            if t_dict[node] > 0 and self.core_s[node]:
                continue
            elif node > max_node or not max_node:
                max_node = node
        return max_node


    def zero_look_ahead( self, n, m, core ):
        '''every neighbour of n has to be mapped to a neighbour of m'''
        for n_ in n.neighbours:
            m_ = core[n_] # Mapping of v
            if not m_ : # If mapping doesn't exist, proceed
                continue
            # If n_ is a neighbour of n m_ must be a neighbour of m
            if not m_ in m.neighbours: # this checks for induced subgraphs: every mapped neigbour of n must be mapped to a neighbour of m
                return False

            # if m_ in m.neighbours: # this would check for (less than induced) subgraphs: at least one mapped neigbour of n must be mapped to a neighbour of m
                # return True
        # return False


        # I shortened this section because we're not dealing with directed graphs anymore. if one was to generalize the algo to directed graphs again, in and out neighbours should be checked separately again
        return True



# RESULT PROCESSING -----------------------------------------------------------

    def append_result_subgraph( self, result ):
        '''
        creates a graph which contains the concatenated mapped nodes from
        subgraph. Then, it adds the neighbours to the new nodes following the
        original neighbours.
        '''

        node_dict={} #used to reconstruct the neighbours
        final_node_set = set()
        in_l_and_mapped = set()

        node_label_len = len(next(iter(self.core_s)).mult_id) # label length of nodes from smaller graph
        mapping_label_len = len(next(iter(self.core_l)).mult_id) # label length of nodes from larger graph

        for node, mapping in result[0].items():

            if mapping: # nodes that were actually mapped
                cur_node = Node(
                                "{}.{}".format(node.id, mapping.id), #id
                                node.label + mapping.label, #label
                            )
                cur_node.mult_id = node.mult_id + mapping.mult_id
                in_l_and_mapped.add(mapping)
                node_dict[mapping] = cur_node
                node_dict[node] = cur_node
            else: # nodes from small graph that were not mapped against a node from larger graph
                new_label = node.get_label()
                for i in range(mapping_label_len):
                    new_label.append("-")
                cur_node = Node(
                                "{}.".format( node.id ),
                                new_label
                            )
                cur_node.mult_id = node.get_mult_id()
                for i in range(mapping_label_len):
                    cur_node.mult_id.append("_____")

                node_dict[node] = cur_node

            final_node_set.add(cur_node)

        for node, mapping in self.core_l.items():
            if node not in in_l_and_mapped: # nodes from large graph that were not mapped against nodes from smaller graph
                cur_node = Node(
                                ".{}".format( node.id ),
                                node.get_label()
                            )
                for i in range(node_label_len):
                    cur_node.label.insert( 0, "-" )

                cur_node.mult_id = node.get_mult_id()
                for i in range( node_label_len ):
                    cur_node.mult_id.insert( 0, "_____" )

                node_dict[node] = cur_node
                final_node_set.add(cur_node)

        # reconstructing the neighbours
        i = 1
        for node1 in list(node_dict.keys())[:-1]:
            for node2 in list(node_dict.keys())[i:]:
                if node2 in node1.neighbours:
                    node_dict[node1].neighbours.add(node_dict[node2])
                    node_dict[node2].neighbours.add(node_dict[node1])

            i += 1

        result_graph = Graph("{}-{}#{}".format(
                    self.small_g.id,
                    self.large_g.id,
                    len(self.result_graphs)+1
                ),
                final_node_set
            )

        self.result_graphs.append( result_graph )
        self.results.append( (result_graph.nodes,result[1]) )


    def get_real_result_graph( self ):
        result = self.result_graphs[0]
        result = self.generate_graph_bools( result )
        result.create_undirected_edges()
        return result


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



if __name__ == "__main__":

    large_g = parse_graph(sys.argv[1])
    small_g = parse_graph(sys.argv[2])

    vf2 = SubVF2(large_g, small_g)
    vf2.match()

    print("")
    print("********************************************************************")
    print("*                                                                  *")
    print("                    RESULTS for {} and {}".format( vf2.small_g.id, vf2.large_g.id) )
    print("*                                                                  *")
    print("********************************************************************")
    print("")
    print("")

    counter = 1
    for result in vf2.result_graphs:

        print("--- RESULT #{} ------------------------------------------".format(counter))
        print("")
        print (result.id)
        print("")

        for node in result.nodes:
            print(node)
        print("")
        for edge in result.edges:
            print(edge)
        print("")
        counter += 1
    print("")