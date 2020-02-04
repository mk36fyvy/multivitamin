import sys
import pprint

from multivitamin.custom import check_semantics
from multivitamin.basic.node import Node
from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.scoring import Scoring


class subVF2():

    def __init__(self, g, h, scoring_matrix=None):

        self.null_n = Node("-1", [])

        self.g = g
        self.h = h
        self.scoring_matrix = scoring_matrix if scoring_matrix else '-1'

        '''makes sure, that small_g is the smaller graph'''
        self.type = 'subgraph'
        if h == g:
            self.type = 'isomorphism'

        self.small_g, self.large_g = g, h
        if g.int_size() > h.int_size():
            self.small_g = h
            self.large_g = g

        # if the graph is undirected, the inverse edges (1,2 -> 2,1) are
        # constructed to work with the original VF2 algorithm
        if not self.large_g.is_directed:
            self.large_g.create_fake_directions()
        if not self.small_g.is_directed:
            self.small_g.create_fake_directions()

        self.large_g.get_inout_neighbours()
        self.small_g.get_inout_neighbours()

        # Initializing the two core dictionaries that store each node of the
        # Corresponding graph as key and the node of the other graph where it maps
        # As soon as it mapps for now we use self.null_n as inital value
        self.core_s = self.small_g.gen_dict( self.null_n )
        self.core_l = self.large_g.gen_dict( self.null_n )

        # initialiazing the terminal sets for each graph. These are dictionaries
        # that store the node as values and the recursion depth as keys where the
        # nodes entered the corresponding set. For now we initialiazing them with 0 '''
        self.in_s = self.small_g.gen_dict( 0 )
        self.out_s = self.small_g.gen_dict( 0 )
        self.in_l = self.large_g.gen_dict( 0 )
        self.out_l = self.large_g.gen_dict( 0 )

        self.result_graphs = []
        self.results = []

        # The following attributes are used for subgraph-subgraph matching.
        self.found_complete_matching = False # to turn off subsub search
        self.max_depth_matching = -1
        self.biggest_matches = [] #saves all co-optimals


    def match( self, last_mapped=(Node("-1", []), Node("-1", [])), depth=0 ):

        if self.s_in_small_g():
            self.found_complete_matching = True
            scoring = Scoring( len(self.g.nodes), len(self.h.nodes), [self.core_s], self.scoring_matrix )
            scoring.score()

            self.append_result_subgraph( scoring.get_best_result() )
            self.restore_ds( last_mapped[0], last_mapped[1], depth )
            return

        td = self.set_inout( last_mapped[0], last_mapped[1], depth )
        p = self.compute_p(td)

        found_pair = False
        for tup in p:

            if self.is_feasible(tup[0], tup[1], depth, td):
                found_pair = True
                self.compute_s_( tup[0], tup[1] )

                self.match( tup, depth+1 )

        # if the matching isn't continued and the current depth is higher than/
        # equal to the max depth reached until now: save the subgraph
        if not found_pair and not self.found_complete_matching:
            if depth > self.max_depth_matching:
                self.max_depth_matching = depth
                self.biggest_matches = []
                self.biggest_matches.append(self.core_s.copy())
            elif depth == self.max_depth_matching:
                self.biggest_matches.append(self.core_s.copy())

        if depth > 0:
            self.restore_ds( last_mapped[0], last_mapped[1], depth )


        #if we returned to the start and no "complete" matching has been found
        if depth == 0 and not self.found_complete_matching:
            self.found_complete_matching = True

            scoring = Scoring( len(self.g.nodes), len(self.h.nodes),self.biggest_matches, self.scoring_matrix )
            scoring.score()

            self.append_result_subgraph( scoring.get_best_result() )
            return


    def s_in_small_g(self):
        """
        checks if every node of the small graph is mapped to a node in the
        large graph and return True or False accordingly
        """

        for node in self.core_s:
            if self.core_s[node] == self.null_n:
                return False
        return True


    def compute_p(self, td):
        '''
        computes the candidate pairs from terminal sets. If all the terminal
        are empty, candidate pairs are computed from the sets of non-mapped
        nodes.
        '''

        if all( ( td["out_l"] ,td["out_s"] ) ):
            return self.cart_p1(self.out_l, self.legal_max(self.out_s))

        elif all(( td['in_l'], td['in_s'] )):
            return self.cart_p1(self.in_l,  self.legal_max(self.in_s))

        elif not any((td["in_l"], td["in_s"], td["out_l"], td["out_s"])):

            # all mapped nodes are in m_l (large_g) or m_s (small_g)
            m_l = {n for n in self.core_l if self.core_l[n] != self.null_n}
            m_s = {n for n in self.core_s if self.core_s[n] != self.null_n}

            # In diff_l are all nodes that are in the large graph, but not mapping
            diff_l = set(self.large_g.nodes) - m_l
            diff_s = set(self.small_g.nodes) - m_s  # see above

            return self.cart_p2(diff_l, max(diff_s))
        return set()


    def is_feasible( self, n ,m, depth, td):
        '''
        first, checks zero_look ahead (if there are neighbours of the candidate pair that
        are in the current mapping, they have to be mapped to each other) then, checks some 
        semantic conditions specified in check_semantics which is imported from
        multivitamin/custom.py
        '''

        #0-look-ahead
        if not all((
            self.zero_look_ahead(n, m, self.core_l),
            self.zero_look_ahead(m, n, self.core_s) ) ):
            return False

        return check_semantics( n, m ) # this function is imported from multivitamin/custom.py


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

        if any((n==self.null_n, m==self.null_n)):
            raise(Exception("null node restored"))

        self.restore_terminals(self.in_l, "in_l", self.core_l, depth)
        self.restore_terminals(self.out_l, "out_l", self.core_l, depth)
        self.restore_terminals(self.in_s, "in_s", self.core_s, depth)
        self.restore_terminals(self.out_s, "out_s", self.core_s, depth)

        self.core_l[n] = self.null_n
        self.core_s[m] = self.null_n


# HELPER FUNCTIONS ------------------------------------------------------------
    def set_inout(self, n, m, depth):
        '''
        Saves number of nodes for each terminal set in td and sets ssr /
        recursion depth, if not set. Used for computing candidate set p.
        '''

        td = {"in_l": 0, "out_l": 0, "in_s": 0, "out_s": 0}

        # makes sure, the first selected node gets depth
        try:  # This is needed, because the very first try will fail (null_n not in in_l)
            if self.in_l[n] == 0 and self.out_l[n] == 0:
                self.in_l[n] = depth
                self.out_l[n] = depth

            if self.in_s[m] == 0 and self.out_s[m] == 0:
                self.in_s[m] = depth
                self.out_s[m] = depth
        except:
            return td

        # Compute terminal_dicts and length for the large graph
        for v in n.neighbours:
            if not self.core_l[v] == self.null_n :
                continue

            if v in n.in_neighbours:
                # saves current depth for terminal node in case it hasn't depth yet
                if self.in_l[v] == 0: self.in_l[v] = depth

            if v in n.out_neighbours :
                if self.out_l[v] == 0: self.out_l[v] = depth

        # compute terminal_dicts for the small graph
        for v in m.neighbours:
            if not self.core_s[v] == self.null_n:
                continue

            if v in m.in_neighbours:
                if self.in_s[v] == 0: self.in_s[v] = depth

            if v in m.out_neighbours:
                if self.out_s[v] == 0: self.out_s[v] = depth

        return td


    def cart_p1( self, node_dict, t_max ):
        """
        creates the cartesian product of the node set in node_dict that are in terminal sets 
        (which means they are mapped to null node in core and do not have a depth of 0)
        """
        cp = set()
        for node in node_dict:
            if self.core_l[node] == self.null_n and not node_dict[node] == 0:
                cp.add( (node, t_max) )
        return cp

    def cart_p2( self, node_dict, t_max ):
            """
            creates the cartesian product of the node set in node_dict that are not in the
            current mapping and not in terminal sets (which means they are mapped to null 
            node while it is made sure, that all terminal sets are empty)
            """
            cp = set()
            for node in node_dict:
                if self.core_l[node] == self.null_n:
                    cp.add( (node, t_max) )
            return cp


    def legal_max(self, t_dict):
        '''returns node from t_dict with max id'''
        max_node = self.null_n
        for node in t_dict:
            if t_dict[node] > 0 and self.core_s[node] != self.null_n:
                continue
            elif node > max_node:
                max_node = node
        return max_node


    def zero_look_ahead( self, n, m, core ):
        '''every neighbour of n has to be mapped to a neighbour of m'''
        for n_ in n.neighbours:

            m_ = core[n_] # Mapping of v

            if m_ == self.null_n : # If mapping doesn't exist, proceed
                continue

            # If n_ is an in neighbour of n m_ must be an in neighbour of m
            elif n_ in n.in_neighbours:
                if not m_ in m.in_neighbours:
                    return False

            # Since we're only contemplating neighbours of n n_ has to be an in
            # or an out neighbour, it is sufficient to only check it m_ is out
            # Neighbour of m
            elif n_ in n.out_neighbours and not  m_ in m.out_neighbours:
                return False
        return True


    def restore_terminals(self, t_dict, dict_key, core, depth):
        for node in t_dict:
            if core[node] == self.null_n and t_dict[node] == depth:
                t_dict[node] = 0


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

            if mapping != self.null_n: # nodes that were actually mapped
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



if __name__ == "__main__":

    large_g = parse_graph(sys.argv[1])
    small_g = parse_graph(sys.argv[2])

    vf2 = subVF2(large_g, small_g)
    vf2.match()

    print("")
    print("********************************************************************")
    print("*                                                                  *")
    print("                    RESULTS for {} and {}".format( vf2.g.id, vf2.h.id) )
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
