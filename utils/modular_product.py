

from graph import Graph
from node import Node
import sys
import pprint
from parser import parse_graph
from bk_pivot_class import BK
#from view_graph import create_graph


''' building cartesian product of two graphs and making new node objects out
of the given node objects from each graph. In order do get the neighbour
relations right we need to save the nodes of the two input graphs to user
their .neighbour method later'''

def cart_product(G,H):


	cart_product = {} # empty dict to store consolidated nodes as keys and tupel of old nodes as values
	for g in G:
		for h in H:
			cur_node = Node( "{}.{}".format( g.id, h.id), "{} {}".format( g.label, h.label ) )
			cart_product[cur_node] = (g,h)

	return cart_product

''' this function checks if the two given new nodes (of the cartesian product)
of two graphs are neighbours according to the rules of the modular product which'''

def neighbours_in_mp ( tup1, tup2 ):


	if  tup2[0] in tup1[0].neighbours and  tup2[1] in tup1[1].neighbours:
		return True

	elif not ( tup2[0] in tup1[0].neighbours or  tup2[1] in tup1[1].neighbours ):
		return True

	return False


''' this function builds the modular product out of the cartesian product by
applying the neighbour rules of the modular product'''

def mod_product( cartp ):

	modular_set = set() # empty set for storing Node objects of modular product
	for n in cartp.keys() :

		for t in cartp.keys() :

			# prevents that the node (old Tupel nodes) gets compared with itself
			if cross_compare_tupels ( cartp[n], cartp[t] ):
				if neighbours_in_mp( cartp[n], cartp[t] ):

					n.add_neighbour(t)


		# add complete consolidated node (with neighbours) at the end of first for loop
		modular_set.add(n)

	# OUTPUT-------------------------------------------------------------------
	modular_product_as_graph = Graph('h_g',modular_set) # making graph out of modular product nodes
	#modular_product_as_graph.create_undirected_edges() #giving the graph edges


	return modular_product_as_graph

def cross_compare_tupels( tup, t ):
	if not  (tup[0].id == t[0].id or tup[1].id == t[1].id):
		return True
	return False

# EXECUTION  -------------------------------------------------------------------

if __name__ == '__main__':

	try:
		g = parse_graph( sys.argv[1] )
		h = parse_graph( sys.argv[2] )
		modp = mod_product( cart_product( g.nodes, h.nodes ) )
		#print(modp)
		#print(list(modp.nodes)[1].neighbours)
		x = set()
		r = set()
		p = list(modp.nodes)

		bk = BK()
		print(bk.bk_pivot( r, p, x))
		#create_graph(modp.nodes ,modp.edges)

	except Exception as e:
		print(e)
		print( "please provide the two graphs you want to build the modular product with \n example: python3 modular_product.py graph1.graph garph2.graph" )
