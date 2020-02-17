from ete3 import Tree

from multivitamin.basic import graph



class Guide_tree():
    '''
    Is initialized by Tree() object and graph list. The Tree() object is constructed from a user provided guide tree.
    '''

    def __init__(
                    self,
                    tree=None,
                    graph_list=None
                ):

        self.tree = tree
        self.graph_list = graph_list

        root_node = tree.get_tree_root()
        self.root = Guide_tree_element( root_node )

        self.extend_tree( self.root )


    def extend_tree( self, el ):
        _lchild = el.node.get_children()[0]
        _rchild = el.node.get_children()[1]

        if _lchild.is_leaf():
            el.lchild = Guide_tree_element( _lchild )
            el.lchild.set_graph( _lchild.name, self.graph_list )
        else:
            el.lchild = Guide_tree_element( _lchild )
            self.extend_tree( el.lchild )

        if _rchild.is_leaf():
            el.rchild = Guide_tree_element( _rchild )
            el.rchild.set_graph( _rchild.name, self.graph_list )
        else:
            el.rchild = Guide_tree_element( _rchild )
            self.extend_tree( el.rchild )


    def __str__( self ):
        '''define the way a guide_tree is printed'''
        return self.tree

    def __repr__( self ):
        return self.__str__()



class Guide_tree_element():
    '''
    One element (node) in a Guide_tree() object.
    '''

    def __init__(
                    self,
                    node
                ):

        self.node = node
        self.lchild = None
        self.rchild = None
        self.graph = None

    def set_graph( self, name, graph_list ):
        for graph in graph_list:
            if graph.id == name:
                self.graph = graph
                return


    def __str__( self ):
        '''define the way a guide_tree_element is printed'''
        return "Node:(children:[ {} | {} ])".format(self.lchild if self.lchild else "", self.rchild if self.rchild else "")

    def __repr__( self ):
        return self.__str__()