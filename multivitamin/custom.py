'''if basic modules (graphs, nodes, edges) are needed, uncomment the lines below'''
# from multivitamin.basic.node import Node
# from multivitamin.basic.edge import Edge
# from multivitamin.basic.graph import Graph

def check_semantics( n, m ):
    '''This function is used in VF2 algorithm to decide,
    whether aligning two nodes is allowed from the
    label point of view.
    In the sample example below, two nodes will only
    be accepted as a legal matching, if the two
    labels are exactly the same.

    Insert your scoring logic below:'''

#    if n.label == m.label:
#        return True
#    else:
#        return False

    return True

def get_results_dir():
    '''define, where the result files will be saved.
    Default is a dir named 'results' in the current
    working directory'''

    return "/results"
