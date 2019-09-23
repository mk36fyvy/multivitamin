###python -m pip install -U pip
#sudo apt install python3-pip
#pip3 install networkx
#sudo apt-get install python3-matplotlib
#python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
#sudo apt-get install python3.6-tk

#sudo apt-get install python3-scipy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()


'''first number is the number of nodes; second is the edge probability, ergo a float between 0 and 1'''
#d = input("directed? (True or False):\n").upper == "TRUE" #turns cas insensitive string-input to true bool
p = 0.1

'''
this changes the layout of the node display. Planar layout doesn't work with every graph. KK layout is pretty nice
(better than spring_layout) most of the time.
    '''
n_graphs_per_node = 3
counter = 1
while counter <= n_graphs_per_node:
    for n in np.floor(np.exp(np.linspace(1,np.log(30),50))):
        for d in ['2','1']:
            G = nx.fast_gnp_random_graph(int(n), float(p), seed=None, directed=False)


           # if int(n) < 20:
           #     pos = nx.planar_layout(G) #no edge intersections
           # else:
           #     pos = nx.kamada_kawai_layout(G) #nice layout

           # nx.draw(G, pos, with_labels = 1)

            '''
            The functions below return some properties about the graph
            More functions like this can be found here:
            https://networkx.github.io/documentation/networkx-1.10/reference/functions.html
            '''
            #print("Directed? " + str(nx.is_directed(G)))
            #print("Number of nodes: " + str(nx.number_of_nodes(G)))
            #print("Nodes: " + str(nx.nodes(G)))
            #print("Edges: " + str(nx.edges(G)))
            #print("Edgetype:" + str(type(G.edges)))
           # fig_copy = plt.gcf()
#            x = input("do you want to see the plot? (y=yes):\n")
#            if (x=="y"):
#                plt.show() #.show clears the image
#                plt.draw()
#
#            z = input("do you want to save the plot? (y=yes):\n")

#            if z=="y":
#                fig_copy.savefig("RandomGraph.png")
#                print("\nthe random generated graph is saved as RandomGraph.png")
            filename = './{}_{}_{}.graph'.format(int(n), counter, d)
            with open(filename, 'w') as f:
                f.write("AUTHOR: Clemens M., Max. J, Michel K., NetworkX\n")
                f.write("#nodes;" + str(nx.number_of_nodes(G)))
                f.write("\n#edges;"+ str(nx.number_of_edges(G)))
                f.write("\nNodes labelled;"+ "False")
                f.write("\nEdges labelled;"+ "False")
                f.write("\nDirected graph;"+ str(nx.is_directed(G)))
                f.write("\n\n")
                for i in (nx.nodes(G)):
                    f.write(str(i+1))
                    f.write("\n")
                f.write("\n")

                _list= (str(G.edges)).replace("[", "")
                _list = _list.replace("]", "")
                _list = _list.replace("(", "")
                _list = _list.replace(")", "")
                _list = _list.replace(" ", "")
                split_list = _list.split(",")

                # print("split_list:" + str(split_list))
                a=0
                for i in (split_list):
                    if not i == '':
                        f.write(str(int(i)+1))
                        if (a % 2 == 0):
                            f.write(";")
                        else :
                            f.write("\n")
                        a=a+1
                f.close()

                print("\nthe random generated graph is saved as {}".format(filename))

    counter += 1

