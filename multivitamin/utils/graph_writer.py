import sys
import os
import getpass #to get username for AUTHOR line

from multivitamin.utils.parser import parse_graph


def write_graph(graph, path):
    f = open("{}{}/{}.graph".format( os.getcwd(), path, graph.id ), 'w+')
    f.write("AUTHOR: {}\n".format( getpass.getuser() ))
    f.write("#nodes;{}\n".format( len(graph.nodes) ))
    f.write("#edges;{}\n".format( len(graph.edges) ))
    f.write("Nodes labelled;{}\n".format( graph.nodes_are_labelled) )
    f.write("Edges labelled;{}\n".format(graph.edges_are_labelled) )
    f.write("Directed graph;{}\n".format( graph.is_directed ))

    f.write("\n")

    for node in (graph.nodes):
        if node.label == "":
            f.write("{}\n".format( node.id ))
        else:
            f.write("{};{}\n".format( node.id, node.label ))

    f.write("\n")

    if not graph.edges_are_labelled:
        for edge in graph.edges:
            f.write("{};{}\n".format( edge.node1.id, edge.node2.id ))
    else:
        for edge in graph.edges:
            f.write("{};{};{}\n".format( edge.node1.id, edge.node2.id, edge.label ))

    f.close()

    print("Saved graph as {}.graph".format( graph.id ))




if __name__ == '__main__':
    try:
        g = parse_graph( sys.argv[1] )
        write_graph(g, "./")
    except Exception as e:
        print(e)
        print("Please provide a graph you want to test the graphwriter with \n \t example: python3 graph_writer.py graph1.graph")