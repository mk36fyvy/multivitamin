'''if basic modules (graphs, nodes, edges) are needed, uncomment the lines below'''
# from multivitamin.basic.node import Node
# from multivitamin.basic.edge import Edge
# from multivitamin.basic.graph import Graph


# This variable is used to define the separator between node's label elements
# in your graph input file
labelsep = " "

def check_semantics( n, m ):
    '''This function is used in VF2 algorithm to decide,
    whether aligning two nodes is allowed from the
    label point of view.
    In the sample example below, two nodes will only
    be accepted as a legal matching, if the two
    labels are exactly the same.

    Insert your scoring logic below:'''

    #example for forbidding a pair:
    forbid( ("C", "H"), n, m)
    
    return True

def forbid( pair, n, m ):
    if pair[0] in n.label and pair[1] in m.label:
        return False
    elif pair[1] in n.label and pair[0] in m.label:
        return False


def get_results_dir():
    '''define, where the result files will be saved.
    Default is a dir named 'results' in the current
    working directory'''

    return "/results"
