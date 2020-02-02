""" Node object with an id (str), a label (str) and neighbours (set) """
import copy
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


    def get_label( self ):
        label_copy = copy.deepcopy(self.label)
        return label_copy


    def get_mult_id( self ):
        mult_id_copy = copy.deepcopy( self.mult_id )
        print(type(mult_id_copy))
        return mult_id_copy


    def insert_fillers_to_label( self, mapping_label_len, filler, i ):
        '''add fillers (gaps) to label or mult_id during mutliple alignment'''
        if i == 0:
            for n in range(mapping_label_len):
                self.label.insert(0, filler)
        elif i == -1:
            for n in range(mapping_label_len):
                self.label.append(filler)
    
    def insert_fillers_to_multid( self, mapping_label_len, filler, i ):
        '''add fillers (gaps) to label or mult_id during mutliple alignment'''
        if i == 0:
            for n in range(mapping_label_len):
                self.mult_id.insert(0, filler)
        elif i == -1:
            for n in range(mapping_label_len):
                self.mult_id.append(filler)


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
                string += "."
            string = string[:-1]
            return string

    def get_node_label_string( self ):
        string = "["
        for el in self.label:
            string += el
            string += "."
            print(el)
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


