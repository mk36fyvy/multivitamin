""" Node object with an id (str), a label (str) and neighbours (set) """
class Node():


    def __init__ (
                    self,
                    id,
                    label=None,
                    neighbours=None
                ):

        self.id = id
        self.mult_id = ""
        self.label = label if label else ""
        self.neighbours = neighbours if neighbours else set()
        self.in_neighbours = set()
        self.out_neighbours = set()


    def add_neighbour(self, node):
        '''add a neighbour to the neighbours set of the node'''
        self.neighbours.add(node)


    def remove_neighbour(self, node):
        '''remove a neighbour from the neighbours set of the node'''
        self.neighbours.remove(node)


    '''allow comparing nodes to each other ( all operations )'''
    def __eq__( self, other ):
        if not isinstance(other, Node):
            return NotImplemented
        else:
            return self.node_id() == other.node_id()
            # return all( (self.id == other.id, self.label == other.label, self.neighbours == other.neighbours) )
            # return all( (self.id == other.id, self.label == other.label) )



    def __ne__( self, other ):
        if not isinstance(other, Node):
            return NotImplemented
        else:
            return any( (self.id != other.id, self.label != other.label, self.neighbours != other.neighbours) )


    def __lt__( self, other ):
        if not isinstance(other, Node):
            return NotImplemented
        else:
            return self.id < other.id


    def __le__( self, other ):
        if not isinstance(other, Node):
            return NotImplemented
        else:
            return self.id <= other.id


    def __gt__( self, other ):
        if not isinstance(other, Node):
            return NotImplemented
        else:
            return self.id > other.id


    def __ge__( self, other ):
        if not isinstance(other, Node):
            return NotImplemented
        else:
            return self.id >= other.id


    def __hash__( self ):
        return hash((self.id, self.label))


    def node_id( self ):
        if self.mult_id == "" or self.mult_id == ".":
            return self.id
        else:
            return self.mult_id


    '''define the way, a node is printed'''
    def __str__( self ):

        neighbours_string = " "

        for neighbour in self.neighbours:
            neighbours_string += neighbour.node_id()
            neighbours_string += ", "
        neighbours_string = neighbours_string[:-2]
        neighbours_string += " "
        return  self.node_id() + "   '" + self.label + "'   (" + str(neighbours_string) + ")"


    def __repr__(self):
        return self.__str__()


