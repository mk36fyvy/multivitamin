from multivitamin.basic import graph
class Guide_tree():
    '''dummy'''

    def __init__(
                    self,
                    lchild=None,
                    rchild=None,
                    graph=None,
                    label=None
                ):

        if graph is not None or (lchild is not None and rchild is not None):
            self.lchild = lchild if lchild is not None else None
            self.rchild = rchild if rchild is not None else None
            self.graph = graph if graph is not None else None
            self.label = label if label else ""
        else:
            raise Exception("Tree is not a valid guide tree or something else is broken ¯\_(ツ)_/¯")

    def get_lchild( self ):
        return lchild  
    
    def get_rchild( self ):
        return rchild
    
    def get_label ( self ):
        return label
    
    def get_graph( self ):
        if graph is not None:
            return graph
        else:
            align(lchild.get_graph(), rchild.get_graph())
            
    '''define the way a guide_tree is printed'''
    def __str__( self ):
        return "Node:(label: {} ; children:[ {} | {} ])".format(self.label, self.lchild if self.lchild is not None else "", self.rchild if self.rchild is not None else "")

    def __repr__( self ):
        return self.__str__()