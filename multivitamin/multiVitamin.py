import os

from multivitamin.utils.guide_tree import Guide_tree
from multivitamin.utils.flags import parser
from multivitamin.utils.graph_writer import write_graph

''' 
FLAGS:
-f -d  save in list as input graphs
-a BK VF2 
-g guide
-s save_all
-n save_guide
'''

args = parser.parse_args()

def main():

    # print(type(args.files[0]))

    if args.files:
        if isinstance(args.files[0], list): #this happens when parsing files from a directory
            graphs = args.files[0] 
        else:
            graphs = args.files
    else:
        raise Exception("No graph was parsed from the command-line")
    
    guide_tree = Guide_tree( graphs, args.algorithm, args.save_all )

    print("Calculating multiple alignment with {} algorithm...".format( args.algorithm ))
    guide_tree.upgma()

    save_results( guide_tree )


def save_results( guide_tree ):
    path = "/results"
    
    if not os.path.isdir("{}/{}".format( os.getcwd(), path )):
        try:
            os.mkdir("{}{}".format( os.getcwd(), path ) )
        except:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory {}{}\n All files will be saved here.".format( os.getcwd(), path ))
    else:
        print("\nAll files will be saved in {}{} \n".format( os.getcwd(), path ))

    if args.save_all:
        for graph in guide_tree.intermediates:
            write_graph( graph, path )
    else:
        write_graph( guide_tree.result, path )

    if args.save_guide:
        f = open("{}{}/{}".format( os.getcwd(), path, "Newick.txt" ), 'w+')
        f.write(guide_tree.newick)
        f.close
        print("Saved the alignment tree in Newick format as tree.txt\n")