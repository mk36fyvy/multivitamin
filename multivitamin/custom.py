'''if basic modules (graphs, nodes, edges) are needed, decomment the lines below'''
from multivitamin.basic.node import Node
from multivitamin.basic.edge import Edge
from multivitamin.basic.graph import Graph

'''
this function is used in VF2 algorithm to decide, 
whether aligning to nodes is allowed from the 
label point of view. 
In the sample example below, two nodes will only 
be accepted as a legal matching, if the two 
labels are exactly the same.
'''
def check_semantics( n, m ):
    if n.label == m.label:
        return True
    else:
        return False
