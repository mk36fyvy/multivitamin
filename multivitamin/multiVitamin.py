from multivitamin.utils.flags import *


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

    # print(args)

    graphs = []

    if args.files:
        for graph in args.files:
            graphs.append(graph)
    
    print(graphs)

    # make new guide_tree class
    # just do it, (BK, then VF2)
    #   get newick if wanted, 
    #   get intermediate graphs if wanted,
    #   get end result, print it, save it in a logfile 



    