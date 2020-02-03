import sys
import pprint
import os

from multivitamin.basic.node import Node
from multivitamin.basic.edge import Edge
from multivitamin.basic.graph import Graph
from multivitamin.custom import labelsep, no_label_dummy


def parse_graph( doc ):
    check_list = [] #contains #nodes #edges, if they are labelled and if graph is directed
    nodes = set()
    edges = set()

    limit = 5000 # graphs with an edge amount above this number will trigger additional print statements to indicate progress

    with open(doc) as d:
        indicator = 0 #counts the empty lines (0: check_list, 1: nodes, 2: edges)
        edge_counter = 0 #counts the processed edges to give some completion feedback

        for line in d:
            line = line.replace("\n", "")
            split_list = line.split(";")

            #if line is empty
            if not line:
                indicator += 1
                #print("Accessing block #{}".format(indicator))
                continue

            #building check_list
            elif indicator == 0:

                arg = split_list[-1]  #last element in row is interpreted

                if arg.upper() == "COMMENT":
                    continue

                elif line.startswith( "//" ):
                    continue

                elif arg.upper() in ( "TRUE", "FALSE" ):
                    check_list.append( arg.upper()  == "TRUE" )

                elif line.upper().startswith( "AUTHOR" ):
                    print( "Reading {} from {}".format( doc.split("/")[-1], line.split(" ",1)[1] ) )
                    continue

                else:
                    try:
                        check_list.append( int(arg) ) #indicates number of nodes/edges

                    except:
                        print( "Something's wrong with the first paragraph. Please check and try again." )
                        print( "Aborting..." )
                        raise Exception("Parsing one of your graphs was not successful.")

            #building nodes
            elif indicator == 1:

                cur_node = Node( *split_list )
                if cur_node.label:
                    cur_node.label = cur_node.label.split(labelsep)
                else:
                    cur_node.label = [no_label_dummy]

                nodes.add( cur_node )

            #building labeled and/or directed edges
            elif indicator == 2:

                for node in nodes:
                    if node.id == split_list[0]:
                        split_list[0] = node

                    elif node.id == split_list[1]:
                        split_list[1] = node

                cur_edge = Edge( *split_list )
                edges.add( cur_edge )
                edge_counter += 1

                if edge_counter % limit == 0:
                    print("Already processed {} edges".format(edge_counter))

            else:
                print( "Wrong input file format. File contains too many empty lines." )
                print( "Aborting..." )
                raise Exception("Parsing one of your graphs was not successful.")


    print_if_big(limit, edges, "Some illegalities are tested...")
    issues = ""

    if check_list[0] != len(nodes):
        issues += "Indicated number of nodes ({}) doesn't fit actual number of nodes ({}). \n".format(check_list[0], len(nodes))

    if check_list[1] != len(edges):
        issues += "Indicated number of edges ({}) doesn't fit actual number of edges ({}). \n".format(check_list[1], len(edges))

    if not check_list[2]:
        for node in nodes:
            if node.label != [no_label_dummy]:
                issues += "One or more nodes are labelled. If this is intended, please indicate this at the beginning of the graph file \n"
                break

    if not check_list[3]: #if edges are not labelled
        for edge in edges:
            if edge.label != "":
                issues += "One or more edges are labelled. If this is intended, please indicate this at the beginning of the graph file \n"
                break

    #This test is not suitable for big graphs and must therefore be skipped
    if not check_list[4]:  #if graph is undirected
        if len(edges) < limit:
            if edges_contain_doubles( edges ):  #(a,b) and (b,a)
                issues += "Undirected graph can contain any edge only once. \n"
        else:
            print("Warning: Due to the graph size (number of edges exceeding " + str(limit) + "), it is not controlled whether there are doubled edges. Please make sure your undirected graph does not contain edges as in (n1,n2) and (n2,n1)")

    print_if_big(limit, edges, "Done.")

    #evaluates if any issues have been detected. If not, parsing continues.
    if issues == "":
        print_if_big(limit, edges, "Getting node neighbours...")
        get_node_neighbours(limit, nodes, edges)
        print_if_big(limit, edges, "Done.")
        g = Graph(
                    os.path.basename(doc)[:-6],
                    # doc.split("/")[-1][:-6], # removes path and '.graph' extension
                    nodes,
                    edges,
                    check_list[2],
                    check_list[3],
                    check_list[4]
        )

        print( "Successfully parsed " + os.path.basename(doc)[:-6] + "\n" )
        return g

    else:
        print( "There are some issues with the input file: \n" )
        print( issues )
        print( "Aborting..." )
        exit()


'''This function works, because is_reverse_of only checks {(n1,n2) and (n2,n1},
not {(n1,n2) and (n1,n2)} (second case is sorted out because edges is a set)'''
def edges_contain_doubles( edges ):
    for edge1 in edges:
        for edge2 in edges:
            if edge1.is_reverse_of(edge2):
                return True
    return False


def get_node_neighbours(limit, nodes, edges):
    nodes_w_neighbours = nodes
    counter = 0

    for cur_edge in edges:
        for cur_node in nodes:

            if cur_node == cur_edge.node1:
                cur_node.neighbours.add( cur_edge.node2 )

            if cur_node == cur_edge.node2:
                cur_node.neighbours.add( cur_edge.node1 )

        # nodes_w_neighbours.add(cur_node)
        counter += 1
        if counter % limit == 0:
            print("Processing edge {} of {} ...".format(counter, len(edges)))

    return nodes_w_neighbours


def print_if_big(limit, edges, message):
    if(len(edges)) > limit:
        print( message )



if __name__ == "__main__":
    g = parse_graph(sys.argv[1])
    print(g)