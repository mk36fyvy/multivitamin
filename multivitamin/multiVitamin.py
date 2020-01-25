import os
import pprint

from multivitamin.custom import get_results_dir
from multivitamin.basic.graph import Graph
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.multalign import Multalign
from multivitamin.utils.flags import parser
from multivitamin.utils.graph_writer import write_graph, write_shorter_graph
from multivitamin.utils.modular_product_class import MP
from multivitamin.supp.view_graph import create_graph
from multivitamin.supp.view_graph import create_graphs
from multivitamin.algorithms.bk_pivot_class import BK
from multivitamin.algorithms.vf2_beauty import VF2
from multivitamin.algorithms.vf2_subsub import subVF2

'''
FLAGS:
-a BK VF2 SUBVF2
-c use algorithm for single alignment and save co-optimals
-g guide
-m save in list as input graphs
-n save_guide
-s save_all
-v view
-vm view seperate
'''

args = parser.parse_args()
args.algorithm = args.algorithm.upper()
args.mult = args.mult.upper()

def main():

    # print(type(args.files[0]))


    print("                                                              ")
    print("                 _ _   _       _  _                   _       ")
    print("                | | | (_)     (_)| |                 (_)      ")
    print(" _ __ ___  _   _| | |_ \ \   / / | |_  __ _ _ __ ___  _ _ __  ")
    print("| '_ ` _ \| | | | | __| \ \ / / ||  _|/ _` | '_ ` _ \| | '_ \ ")
    print("| | | | | | |_| | | |_| |\ V /| || |_| (_| | | | | | | | | | |")
    print("|_| |_| |_|\__,_|_|\__|_| \_/ |_| \__|\__,_|_| |_| |_|_|_| |_|")
    print("                                                              ")
    print("                                                  v1.0.0      ")
    print("                                                              ")



    if args.files:
        if isinstance(args.files[0], list): #this happens when parsing files from a directory
            graphs = args.files[0]
        else:
            graphs = args.files

        multalign = Multalign( graphs, args.algorithm, args.mult, args.save_all )
        print("Calculating multiple alignment with {} algorithm...".format( args.algorithm ))
        multalign.multalign()
        save_results( multalign )

    elif args.coopt:
        if isinstance(args.coopt[0], list): #this happens when parsing files from a directory
            graphs = args.coopt[0]
        else:
            graphs = args.coopt

        if not len(graphs) == 2:
            raise Exception("You must provide exactly 2 graph files with '-c' ! Use '-m' if you want to align multiple graphs.")

        fake_align = Multalign( graphs, args.algorithm, args.mult, False )
        print("Calculating alignment using {} algorithm...".format( args.algorithm ))

        if args.algorithm == "BK":
            mp = MP( graphs[0], graphs[1] )
            bk = BK( mp.g, mp.h )
            x = set()
            r = set()
            p = list(mp.modp)
            bk.bk_pivot( r, p, x )
            res = bk.get_coopt()
            res = bk.clique_to_node_set()
            temp = Graph("")
            counter = 1
            for node_set in res:
                temp = fake_align.make_graph_real( Graph( "{}--{}#{}".format(graphs[0].id, graphs[1].id, counter), node_set) )
                # print(temp)
                fake_align.intermediates.append( temp )
                counter += 1
            save_results( fake_align )

        elif args.algorithm == "VF2":
            vf2 = VF2( graphs[0], graphs[1] )
            vf2.match()
            for result_graph in vf2.result_graphs:
                result_graph.create_undirected_edges()
                fake_align.intermediates.append( result_graph )
            save_results( fake_align )

        elif args.algorithm == "SUBVF2":
            subvf2 = subVF2( graphs[0], graphs[1] )
            subvf2.match()
            for result_graph in subvf2.result_graphs:
                result_graph.create_undirected_edges()
                fake_align.intermediates.append( result_graph )
            save_results( fake_align )

        else:
            raise Exception("Invalid algorithm name!")

    elif args.view:
        # print(args.view)
        if isinstance(args.view, list): #this happens when parsing files from a directory
            for i in range(len(args.view)):
                print("Displaying {}...".format(args.view[i].id))
            create_graph( args.view )
        else:
            print("Displaying {}...".format(args.view.id))
            create_graph( args.view )

    elif args.view_multiple:
            # print(args.view_multiple)
            if isinstance(args.view_multiple, list): #this happens when parsing files from a directory
                for i in range(len(args.view_multiple)):
                    print("Displaying {}...".format(args.view_multiple[i].id))
                create_graphs( args.view_multiple )
            else:
                print("Displaying {}...".format(args.view_multiple.id))
                create_graphs( args.view_multiple )

    else:
        raise Exception("No graph was parsed from the command-line")


def save_results( multalign ):
    path = get_results_dir()

    # create results directory
    if not os.path.isdir("{}/{}".format( os.getcwd(), path )): # if results/ does not exist
        try:
            os.mkdir("{}{}".format( os.getcwd(), path ) )
        except:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory {}{}\n All files will be saved here.".format( os.getcwd(), path ))
    else:
        print("\nAll files will be saved in {}{} \n".format( os.getcwd(), path ))

    # save all intermediate alignment graphs, if flag is set
    if args.save_all or args.coopt:
        for graph in multalign.intermediates:
            write_graph( graph, path )
    else:
        write_graph( multalign.result, path )

    # save end alignment graph with much shorter node ids
    if args.save_shorter:
        write_shorter_graph( multalign.result, path )

    # save graph abbreviations used for identifying original nodes in node ids
    f = open("{}{}/{}".format( os.getcwd(), path, "graph_abbreviations.txt" ), 'w+')
    for abbrev, id in multalign.graph_abbreviations.items():
        f.write("{}\t{}\n".format( abbrev, id))
    f.close

    print("")
    print("Saved graph id abbreviations as graph_abbreviations.txt")

    # save newick tree in easily parseable txt file
    if args.save_guide:
        f = open("{}{}/{}".format( os.getcwd(), path, "newick.txt" ), 'w+')
        f.write("{}\n".format(multalign.newick))
        f.close

        print("Saved the alignment tree in Newick format as newick.txt\n")
