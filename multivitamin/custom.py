'''if basic modules (graphs, nodes, edges) are needed, uncomment the lines below'''
# from multivitamin.basic.node import Node
# from multivitamin.basic.edge import Edge
# from multivitamin.basic.graph import Graph


# This variable is used to define the separator between node's label elements
# in your graph input file
labelsep = " "

# This variable is used as 'dummy label' for nodes without label. It makes
# multiple alignment between graphs with and without labels more well-arranged. 
# If you do not wish to use a dummy label, assign an empty string ""
no_label_dummy = "#"

# Don't allow labels listed here to match with any other label. 
# Accepts iterable of Strings only.
force_exact_matching = ["H"]

# Forbid matching of specific label pairs. Pairs are defined as 2-tuples of Strings.
# Labels already specified in force_exact_matching don't need to be included here.
forbidden_matchings = [("C","O")]


def check_semantics( n, m ):
    '''
    This function is used in VF2 algorithm to decide,
    whether aligning two nodes is allowed from the
    label point of view.
    '''
    
    for label in force_exact_matching:
        if label in n.label:
            if label in m.label:
                return True
            else:
                return False
        else:
            if label in m.label:
                return False

    for left,right in forbidden_matchings:
        if left in n.label and right in m.label:
            return False
        if left in m.label and right in n.label:
            return False
    
    return True


def get_results_dir():
    '''define, where the result files will be saved.
    Default is a directory named 'results' in the current
    working directory'''

    return "/results"
