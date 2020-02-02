import sys
import random
import pprint

from multivitamin.basic.node import Node
from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.modular_product_class import MP


class BK:
    ''' implementing Bron-Kerbosch algorithm where r is the list of possible nodes
    in a clique, p is the list of canditates and x is the garbage collection'''

    def __init__(
        self,
        g,
        h,
        ):

        self.g = g
        self.h = h

        self.results = []


    def find_max_pivot( self, p, x ):
        p_union_x = p + list(x)
        helper = 0
        piv = Node('-1', [])

        for v in p_union_x:
            cur_len_intersection = len([n for n in v.neighbours if n in p_union_x])
            if cur_len_intersection > helper:
                piv = v
                helper = cur_len_intersection

        return piv


    def bk_pivot ( self, r, p, x ):

        if not any ( [p, x] ): # if p and x are empty return r as max clique and end

            # print('clique: ', r)
            self.results.append(r)
            return r

        pivot = self.find_max_pivot( p, x )
        # pivot = random.choice( p + list(x) )  # choosing pivot randomly from union of p, x

        # loop through candidates p without neighbours of pivot element
        for v in p[:]:

            if  v in pivot.neighbours: # bk with pivot only takes
                continue

            r_ = r | {v} # concatenate r and v

            # intersection of x respectively p and neighbours of v
            x_ = x & v.neighbours
            p_ = [n for n in v.neighbours if n in p ]

            self.bk_pivot ( r_, p_, x_ ) # recursive call of Bron-Kerbosch

            p.remove(v) # taking current node out of canditates
            x.add(v) # adding current node to garbage collection


    def bk ( self, r, p, x ):
        '''It is generally recommended to use the pivot version'''

        # when p and x are empty return r as max clique
        if not any ( [ p, x ] ):
            #print('clique')
            #pprint.pprint(r)
            self.results.append( r )
            return r

        for v in p[:]:

            r_ = r | {v} # concatenate r and v

            # intersection of x respectively p and neighbours of v
            x_ = x & v.neighbours
            p_ = [n for n in v.neighbours if n in p]

            self.bk ( r_, p_, x_ ) # recursive call of bronkerbosch

            p.remove(v) # taking current node out of canditates
            x.add(v) # adding current node to garbage collection


    def clique_to_node_set( self ):
        '''repairs the edges from clique to real alignment graph,
        because cliques may contain more edges than the original graph(s)'''

        results = self.get_coopt()
        res_list = []

        for clique in results:

            for node in clique:
                for neighbour in list(node.neighbours)[:]:
                    if not neighbour in clique:
                        node.remove_neighbour(neighbour)

            curr_node_set = set()
            for node in clique:

                corr_n = self.get_corr_node( node )
                new_neighbours = set()

                for neighbour in node.neighbours:

                    for corr_neighbour in corr_n.neighbours:
                        if set(corr_neighbour.mult_id.split(".")).issubset(set(neighbour.mult_id.split("."))):
                            new_neighbours.add(neighbour)
                curr_node = Node( node.id, node.label, new_neighbours)
                curr_node.mult_id = node.mult_id
                curr_node_set.add(curr_node)

            res_list.append(curr_node_set)

        return res_list


    def get_coopt( self ):

        res = []
        cur_max = 0

        for result in self.results:
            if len(result) > cur_max:
                cur_max = len(result)
        for result in self.results:
            if len(result) == cur_max and not result in res:
                res.append(result)
        return res


    def get_corr_node( self, clique_node ):
        old_id = clique_node.mult_id.split(".")

        for node in self.g.nodes:
            if set( node.mult_id.split(".") ).issubset(set( old_id )):
                return node



if __name__ == '__main__':

    try:
        mp = MP (parse_graph(sys.argv[1]), parse_graph(sys.argv[2]))
        bk = BK(mp.g, mp.h)
        r = set()
        x = set()
        p = list(mp.modp)
        bk.bk_pivot ( r, p, x )
        pprint.pprint(bk.results)

    except Exception as e:
        print(e)
        print( 'Please provide a graph file as argument \n example: python3 bk_pivot.py graph.graph' )
