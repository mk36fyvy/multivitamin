import sys

from multivitamin.basic.node import Node
from multivitamin.basic.edge import Edge


class Graph():

    def __init__(
        self,
        id=None,
        nodes=None,
        edges=None,
        nodes_labelled=None,
        edges_labelled=None,
        is_directed=None
    ):

        self.id = id if id else ""
        self.nodes = nodes if nodes else set()
        self.edges = edges if edges else set()
        self.nodes_are_labelled = nodes_labelled if nodes_labelled else False
        self.edges_are_labelled = edges_labelled if edges_labelled else False
        self.is_directed = is_directed if is_directed else False

        self.newick = id
        self.abbrev = ""


    def set_id( self, id ):
        self.id = id


    def get_graph( self, id ):
        if self.id == id:
            return self


    def get_inout_neighbours( self ):
        for cur_node in self.nodes:
            for cur_edge in self.edges:

                if cur_node == cur_edge.node1:
                    cur_node.out_neighbours.add( cur_edge.node2 )

                if cur_node == cur_edge.node2:
                    cur_node.in_neighbours.add( cur_edge.node1 )


    def create_undirected_edges( self ):
        done = [] #already checked nodes, used to avoid including reverse edges

        for node in self.nodes:
            for neighbour in node.neighbours:
                if not neighbour in done: #done is for undirected #no bijection
                    cur_edge = Edge(node, neighbour)
                    self.edges.add(cur_edge)

            done.append(node)


    def create_fake_directions( self ):
        if self.is_directed:
            print( "Fake directions should only be created for undirected graphs!" )
            return False
        else:
            for edge in list(self.edges)[:]:
                rev_edge = Edge( edge.node2, edge.node1, edge.label )
                self.edges.add(rev_edge)




    '''allow comparing graphs (number of nodes!) to each other ( ==, >=, <=, <, > )'''
    def __eq__( self, other):
        if not isinstance(other, Graph):
            return NotImplemented
        else:
            return self.id == other.id
            # return len(self.nodes) == len(other.nodes)

    def __gt__( self, other ):
        if not isinstance(other, Graph):
            return NotImplemented
        else:
            if len(self.nodes) == len(other.nodes):
                return len(self.edges) > len(other.edges)
            return len(self.nodes) > len(other.nodes)

    def __lt__( self, other ):
        if not isinstance(other, Graph):
            return NotImplemented
        else:
            if len(self.nodes) == len(other.nodes):
                return len(self.edges) < len(other.edges)
            return len(self.nodes) < len(other.nodes)

    def __ge__( self, other ):
        if not isinstance(other, Graph):
            return NotImplemented
        else:
            if len(self.nodes) == len(other.nodes):
                return len(self.edges) >= len(other.edges)
            return len(self.nodes) >= len(other.nodes)

    def __le__( self, other ):
        if not isinstance(other, Graph):
            return NotImplemented
        else:
            if len(self.nodes) == len(other.nodes):
                return len(self.edges) <= len(other.edges)
            return len(self.nodes) <= len(other.nodes)


    '''define the way a graph is printed'''
    def __str__( self ):
        p_nodes = ""
        for node in self.nodes:
            p_nodes += str(node) + "\n"

        p_edges = ""
        for edge in self.edges:
            p_edges += str(edge) + "\n"

        return "{} ;\n {} ;\n {};\n Nodes labelled? {}\n Edges labelled? {}\n Directed graph? {}".format(self.id, self.nodes, self.edges, self.nodes_are_labelled, self.edges_are_labelled, self.is_directed)

        # return str(self.id) # for debugging purposes

    def __repr__( self ):
        return self.__str__()


    def int_size ( self ):
        return len(self.nodes)


    def gen_dict( self,  value ):
        _dict = {}
        for key in self.nodes:
            _dict[key] = value
        return _dict