import sys

from multivitamin.utils.parser import parse_graph

def g_writer(g):

    z = "y" #input("do you want to save the plot? (y=yes):\n")

    if z=="y":
        f = open('Graphwirter.graph', 'w')
        f.write("AUTHOR: Clemens M., Max. J, Michel K., NetworkX\n")
        f.write("#nodes;" + str(len(g.nodes)))
        f.write("\n#edges;"+ str(len(g.edges)))
        f.write("\nNodes labelled;"+ str(g.nodes_are_labelled))
        f.write("\nEdges labelled;"+ str(g.edges_are_labelled))
        f.write("\nDirected graph;"+ str(g.is_directed))
        f.write("\n\n")
        if g.nodes_are_labelled == "False":
            for i in (g.nodes):
                split_list = i.split(" ")
                f.write(split_list[1])
                f.write(";\n")
            f.write("\n")
        else:
            for i in (g.nodes):
                _list=(str(i))
                _list = _list.replace("'", "")
                split_list = _list.split(" ")
                f.write(split_list[2])
                f.write(";")
                f.write(split_list[3])
                f.write("\n")
            f.write("\n")

        if not g.is_directed:
            for edge1 in g.edges:
                reverse=False
                for edge2 in g.edges:
                    if edge1.is_reverse_of(edge2):
                        reverse=True                        
                if reverse==False:
                    print(edge1)
                    _list=(str(edge1))
                    _list = _list.replace("'", "")
                    _list = _list.replace("(", "")
                    _list = _list.replace(")", "")
                    _list = _list.replace(" ", "")
                    _list = _list.replace("to", ";")
                    split_list = _list.split(" ")
                    f.write(_list)
        else:
            for edge1 in g.edges:
                _list=(str(edge1))
                _list = _list.replace("'", "")
                _list = _list.replace("(", "")
                _list = _list.replace(")", "")
                _list = _list.replace(" ", "")
                _list = _list.replace("to", ";")
                split_list = _list.split(" ")
                f.write(_list)
    f.close()
    print("\nthe graph is saved as Graphwirter.graph")

        #print("split_list:" + str(split_list))


# EXECUTION  -------------------------------------------------------------------

if __name__ == '__main__':
    try:
        g = parse_graph( sys.argv[1] )
        g_writer(g)
    except Exception as e:
        print(e)
        print("please provide the graph you want to test the graphwriter with \n example: python3 graph_writer.py /home/clm/graph_alignment/graphs/graph1.graph")
#python3 graph_writer.py /home/clm/graph_alignment/graphs/graph1.graph
