import sys
import pprint

from multivitamin.basic.node import Node
from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph
from multivitamin.algorithms.bk_pivot_class import BK

class MP:

	def __init__(
		self,
		g,
		h,
	):
		self.g = g 
		self.h = h
		self.modp = self.mod_product( self.g.nodes, self.h.nodes )


	def cart_product( self, g_nodes, h_nodes ):
		'''
		creating the cartesian product of two graphs and making new node objects out
		of the given node objects from each graph. In order do get the neighbour
		relations right, we need to save the nodes of the two input graphs to get access 
		to their neighbours later
		'''

		cart_product = {} # empty dict to store consolidated nodes as keys and tupel of old nodes as values
		for g_node in g_nodes:
			for h_node in h_nodes:
				#check_semantics here?
				# cur_node = Node( "{}.{}".format( g_node.id, h_node.id), "{} {}".format( g_node.label, h_node.label ) )
				cur_node = Node( "{}.{}".format(g_node.id, h_node.id), "{}".format(g_node.label) )
				cur_node.mult_id = "{}.{}".format( g_node.mult_id, h_node.mult_id)
				cart_product[cur_node] = (g_node, h_node)
		# pprint.pprint(cart_product)
		return cart_product



	def neighbours_in_mp ( self, tup1, tup2 ):
		'''checks if the two given new nodes (of the cartesian product)
		of two graphs are neighbours according to the rules of the modular product'''

		if  tup2[0] in tup1[0].neighbours and  tup2[1] in tup1[1].neighbours:
			return True

		elif not ( tup2[0] in tup1[0].neighbours or  tup2[1] in tup1[1].neighbours ):
			return True

		return False



	def mod_product( self, g_nodes, h_nodes ):
		''' this function builds the modular product out of the cartesian product by
		applying the neighbour rules of the modular product'''

		cartp = self.cart_product( g_nodes, h_nodes)
		modular_set = set() # empty set for storing Node objects of modular product
		for n in cartp.keys() :

			for t in cartp.keys() :
				# print(t)
				# prevents that the node (old Tupel nodes) gets compared with itself
				if self.cross_compare_tupels ( cartp[n], cartp[t] ):
					if self.neighbours_in_mp( cartp[n], cartp[t] ):

						n.add_neighbour(t)

			modular_set.add(n) # add complete consolidated node (with neighbours) at the end of first for loop

		# OUTPUT-------------------------------------------------------------------
		# modular_product_as_graph = Graph('h_g',modular_set) # making graph out of modular product nodes
		#modular_product_as_graph.create_undirected_edges() #giving the graph edges
		# pprint.pprint(modular_set)
		return modular_set


	def cross_compare_tupels( self, tup, t ):
		if not  (tup[0].id == t[0].id or tup[1].id == t[1].id):
			return True
		return False




if __name__ == '__main__':
	try:
		mp = MP( sys.argv[1], sys.argv[2] )
		#print(list(modp.nodes)[1].neighbours)
		x = set()
		r = set()
		p = list(mp.modp)

		bk = BK( mp.g, mp.h )
		bk.bk_pivot( r, p, x )
		# bk.bk( r, p, x)

		res = bk.get_coopt()

		pprint.pprint(res)

	except Exception as e:
		print(e)
		print( "please provide the two graphs you want to build the modular product with \n example: python3 modular_product.py graph1.graph graph2.graph" )
