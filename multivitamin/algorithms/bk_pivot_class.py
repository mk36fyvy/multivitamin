import sys
import random
import pprint

from multivitamin.basic.node import Node
from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph


class BK:
    ''' implementing Bron-Kerbosch algorithm where r is the list of possible nodes
    in a clique, p is the list of canditates and x is the garbage collection'''

    def __init__( self ):
        self.results = []

    def find_max_pivot(self, p,x):
        p_union_x = p + list(x)
        helper = 0
        piv = Node('0', '')
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


    '''It is generally recommended to use the pivot version'''
    def bk ( self, r, p, x ):

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



# EXECUTION (PIVOT VERSION) ----------------------------------------------------

if __name__ == '__main__':

    try:
        bk = BK()
        graph = parse_graph(sys.argv[1])
        r = set()
        x = set()
        p = list(graph.nodes)
        bk.bk_pivot ( r, p, x )
        pprint.pprint(bk.results)

    except Exception as e:
        print(e)
        print( ' please provide a graph file as argument \n example: python3 bk_pivot.py graph.graph' )
