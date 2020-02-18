""" Node object with an id (str), a label (str) and neighbours (set) """
import copy
# from functools import lru_cache


class Node():


    def __init__(
                    self,
                    id,
                    label=None,
                    neighbours=None
                ):

        self.id = id
        self.label = label if label else list()
        self.neighbours = neighbours if neighbours else set()

        self.mult_id = list()
        self.in_neighbours = set()
        self.out_neighbours = set()


    def add_neighbour(self, node):
        '''add a neighbour to the neighbours set of the node'''
        self.neighbours.add(node)


    def remove_neighbour(self, node):
        '''remove a neighbour from the neighbours set of the node'''
        self.neighbours.remove(node)


#     @lru_cache(maxsize=128)
    def get_neighbours(self):
        return self.neighbours

    def get_label( self ):
        label_copy = copy.deepcopy(self.label)
        return label_copy


    def get_mult_id( self ):
        mult_id_copy = copy.deepcopy( self.mult_id )
        return mult_id_copy


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
        return hash((self.id))


    def node_id( self ):
        '''
        returns mult_id if not empty. Else returns id
        '''
        if self.mult_id == [] or self.mult_id == ["."]:
            return self.id
        else:
            return self.mult_id


    def get_node_id_string( self ):
        if self.mult_id == [] or self.mult_id == ["."]:
            return self.id
        else:
            string = " "
            for id in self.mult_id:
                string += str(id)
                string += "°"
            string = string[:-1]
            return string

    def get_node_label_string( self ):
        string = "["
        for el in self.label:
            string += el
            string += " "
        string = string[:-1]
        string += "]"
        return string

    '''define the way, a node is printed'''
    def __str__( self ):

        neighbours_string = " "

        for neighbour in self.neighbours:
            neighbours_string += str(neighbour.get_node_id_string())
            neighbours_string += ", "
        neighbours_string = neighbours_string[:-2]
        neighbours_string += " "

        label_string = " "

        for char in self.label:
            label_string += char
            label_string += "\t"
        label_string = label_string[:-1]
        label_string += " "

        return  self.get_node_id_string() + "   '" + label_string + "'   (" + str(neighbours_string) + ")"

    def __repr__(self):
        return self.__str__()


