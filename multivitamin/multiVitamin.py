import os

from multivitamin.basic.graph import Graph
from multivitamin.utils.guide_tree import Guide_tree
from multivitamin.utils.flags import parser
from multivitamin.utils.graph_writer import write_graph
from multivitamin.utils.modular_product import mod_product, cart_product, get_coopt
from multivitamin.algorithms.bk_pivot_class import BK
from multivitamin.algorithms.vf2_beauty import VF2

''' 
FLAGS:
-a BK VF2 
-c use algorithm for single alignment and save co-optimals
-f save in list as input graphs
-g guide
-n save_guide
-s save_all
'''

args = parser.parse_args()

def main():

    # print(type(args.files[0]))

    if args.files:
        if isinstance(args.files[0], list): #this happens when parsing files from a directory
            graphs = args.files[0] 
        else:
            graphs = args.files

        guide_tree = Guide_tree( graphs, args.algorithm, args.save_all )
        print("Calculating multiple alignment with {} algorithm...".format( args.algorithm ))
        guide_tree.upgma()
        save_results( guide_tree )
    
    elif args.coopt:
        graphs = args.coopt[0]
        
        if not len(graphs) == 2:
            raise Exception("You must provide exactly 2 graph files with '-c' ! Use '-f' if you want to align more graphs.")

        fake_tree = Guide_tree( graphs, args.algorithm, False )
        
        if args.algorithm == "BK":
            modp = mod_product( cart_product( graphs[0].nodes, graphs[1].nodes ) )
            bk = BK()
            x = set()
            r = set()
            p = list(modp.nodes)
            bk.bk_pivot( r, p, x)
            res = get_coopt( bk.results )
            temp = Graph("")
            counter = 1
            for node_set in res:
                temp = fake_tree.make_graph_real( Graph( "({},{})#{}".format( graphs[0].id, graphs[1].id, counter ), node_set ) )
                fake_tree.intermediates.append( temp )
                counter += 1
            save_results( fake_tree )

        elif args.algorithm == "VF2":
            vf2 = VF2( graphs[0], graphs[1] )
            vf2.match()
            for result_graph in vf2.result_graphs:
                fake_tree.intermediates.append( result_graph )
            save_results( fake_tree )

        else: 
            raise Exception("Invalid algorithm name!")
        
    
    else:
        raise Exception("No graph was parsed from the command-line")
    
    


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

    if args.save_all or args.coopt:
        for graph in guide_tree.intermediates:
            write_graph( graph, path )
    else:
        write_graph( guide_tree.result, path )

    if args.save_guide:
        f = open("{}{}/{}".format( os.getcwd(), path, "Newick.txt" ), 'w+')
        f.write(guide_tree.newick)
        f.close
        print("Saved the alignment tree in Newick format as tree.txt\n")