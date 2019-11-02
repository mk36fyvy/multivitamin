import sys
import pprint

from multivitamin.custom import check_semantics
from multivitamin.basic.node import Node
from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph


class VF2():

    def __init__(self, g, h):

        self.null_n = Node("0", "")

        self.g = g
        self.h = h

        '''makes sure, that small_g is the smaller graph'''
        self.type = 'subgraph'
        if h == g:
            self.type = 'isomorphism'

        self.small_g, self.large_g = g, h
        if g.int_size() > h.int_size():
            self.small_g = h
            self.large_g = g

        #  '''if the graph is undirected, the inverse edges (1,2 -> 2,1) are
        # constructed to work with the original VF2 algorithm'''
        if not self.large_g.is_directed:
            self.large_g.create_fake_directions()
        if not self.small_g.is_directed:
            self.small_g.create_fake_directions()

        self.large_g.get_inout_neighbours()
        self.small_g.get_inout_neighbours()
        # Initialiazing the two core dictionaries that store each node of the
        # Corresponding graph as key and the node of the other graph where it maps
        # As soon as it mapps for now we use self.null_n as inital value
        self.core_s = self.small_g.gen_dict( self.null_n )
        self.core_l = self.large_g.gen_dict( self.null_n )

        # initialiazing the terminal sets for each graph. These are dictionaries
        # that store the node as values and the recursion depth as keys where the
        # nodes entered the corresponding set. For now we initialiazing them with 0 '''
        self.in_s = self.out_s = self.small_g.gen_dict( 0 )
        self.in_l = self.out_l = self.large_g.gen_dict( 0 )

        self.result_graphs = []
        self.results = []


    def match( self, last_mapped=(Node("0", ""), Node("0", "")), depth=0 ):

        if self.s_in_small_g():
            self.append_result_graph( self.core_s )
            self.restore_ds( last_mapped[0], last_mapped[1], depth )
            return 

        td = self.set_inout( last_mapped[0], last_mapped[1], depth )
        p = self.compute_p(td)

        for tup in p:

            if self.is_feasible(tup[0], tup[1], depth, td):
                self.compute_s_( tup[0], tup[1], depth )

                self.match( tup, depth+1 )

        self.restore_ds( last_mapped[0], last_mapped[1], depth )


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

        if all( ( td["out_l"] ,td["out_s"] ) ):
            return self.cart_p(self.out_l, self.legal_max(self.out_s))

        elif all(( td['in_l'], td['in_s'], not td['out_l'], not td['out_s'] )):
            return self.cart_p(self.in_l,  self.legal_max(self.in_s))

        elif not any((td["in_l"], td["in_s"], td["out_l"], td["out_s"])):
        # else:
            # all mapped nodes are in m_l (large_g) or m_s (small_g)
            m_l = {n for n in self.core_l if self.core_l[n] != self.null_n}
            m_s = {n for n in self.core_s if self.core_s[n] != self.null_n}

            # In diff_l are all nodes that are in the large graph, but not mapping
            diff_l = self.large_g.nodes - m_l
            diff_s = self.small_g.nodes - m_s  # see above
            
            return self.cart_p(diff_l, max(diff_s))
        return set() # this return is not reached, if diverging from original algorithm description


    def is_feasible( self, n ,m, depth, td):
        #0-look-ahead
        if not all((
            self.zero_look_ahead(n, m, self.core_l),
            self.zero_look_ahead(m, n, self.core_s) ) ):
            return False

        if self.type == "isomorphism":
            # 1-look-ahead
            if not ( td["in_l"] == td["in_s"] and td["out_l"] == td["out_s"] ):
                return False

        elif self.type == "subgraph":
            # 1-look-ahead
            if not ( td["in_l"] >= td["in_s"] and td["out_l"] >= td["out_s"] ):
                return False

        elif not self.two_look_ahead(depth, td):
            return False

        return check_semantics( n, m ) # this method is imported from multivitamin/custom.py


    def compute_s_(self, n, m, depth):
        self.core_l[n] = m
        self.core_s[m] = n


    def restore_ds(self, n, m, depth):

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
            pass

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

        for node, node_depth in self.in_s.items():
            if not self.core_s[node] == self.null_n:
                continue
            if node_depth != 0:
                td["in_s"] += 1
        
        for node, node_depth in self.out_s.items():
            if not self.core_s[node] == self.null_n:
                continue
            if node_depth != 0:
                td["out_s"] += 1
        
        for node, node_depth in self.in_l.items():
            if not self.core_l[node] == self.null_n:
                continue
            if node_depth != 0:
                td["in_l"] += 1
        
        for node, node_depth in self.out_l.items():
            if not self.core_l[node] == self.null_n:
                continue
            if node_depth != 0:
                td["out_l"] += 1
        

        return td


    def cart_p( self, node_dict, t_max ):
        """creates the cartesian product """
        cp = set()
        for node in node_dict:
            if self.core_l[node] == self.null_n:
                cp.add( (node, t_max) )
        return cp


    # def legal_max(self, t_dict):
    #     '''returns node from t_dict with max id'''
    #     max_node = self.null_n
    #     for node in t_dict:
    #         if t_dict[node] > 0 and self.core_s[node] != self.null_n:
    #             continue
    #         elif node > max_node:
    #             max_node = node
    #     return max_node

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

            # Since we only contemplating neighbours of n n_ has to be an in or
            # An out neighbour, it is sufficient to only check it m_ is out
            # Neighbour of m
            elif n_ in n.out_neighbours and not  m_ in m.out_neighbours:
                return False
        return True


    def two_look_ahead(self, depth, td):
        free_n1 = len(self.large_g.nodes) - depth - td["in_l"] - td["out_l"]
        free_n2 = len(self.small_g.nodes) - depth - td["in_s"] - td["out_s"]

        if self.type == "isomorphism":
            return free_n1 == free_n2
        elif self.type == "subgraph":
            return free_n1 >= free_n2


    def restore_terminals(self, t_dict, dict_key, core, depth):
        for node in t_dict:
            if core[node] == self.null_n and t_dict[node] == depth:
                t_dict[node] = 0


# RESULT PROCESSING -----------------------------------------------------------

    def append_result_graph( self, result ):
        '''creates a graph which contains the concatenated mapped nodes. 
        Then, it adds the neighbours to the new nodes following the 
        original neighbours.'''

        result_graph = Graph("({},{})#{}".format(
            self.small_g.id, 
            self.large_g.id, 
            len(self.result_graphs)+1
            ), 
            set()
            )
        for key, value in result.items():
            cur_node = Node( "{}.{}".format( key.id, value.id), "{}".format( key.label ) )
            cur_node.mult_id = "{}.{}".format( key.mult_id, value.mult_id)

            for node in result_graph.nodes: # f.ex. 1.2
                orig_node = Node("")
                for n in result.keys(): # original nodes from small graph
                    if set(n.mult_id.split(".")).issubset( set(node.mult_id.split(".")) ):
                        orig_node = n
                        break
                if key in orig_node.neighbours:
                    node.add_neighbour( cur_node )
                    cur_node.add_neighbour( node )
            result_graph.nodes.add(cur_node)

        self.result_graphs.append( result_graph )
        self.results.append( result_graph.nodes )




if __name__ == "__main__":

    large_g = parse_graph(sys.argv[1])
    small_g = parse_graph(sys.argv[2])

    vf2 = VF2(large_g, small_g)
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
