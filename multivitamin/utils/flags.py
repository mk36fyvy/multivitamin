import argparse, os
from argparse import RawTextHelpFormatter

from multivitamin.utils.parser import parse_graph
from multivitamin.utils.get_input import process_file, parse_scoring_matrix, parse_guide_tree


parser = argparse.ArgumentParser(
    description='multiVitamin - A multiple alignment tool for graphs',
    usage='%(prog)s [ -h | -i | -c | -v | -d ] [-a] [-m] [-t] [-l] [-s] [-g] [-o]\nfor example: multiVitamin -ga subVF2 -i g1.graph g2.graph g3.graph', # add [-r]
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
)

# one of these args has to be provided, but not more
group = parser.add_argument_group(
    title='Required arguments (These arguments are mutually exclusive)',
    description='''
-h, --help                          show this help message and exit
-i, --input <files...>              provide .graph files for multiple alignment.
                                      \'.\' takes all .graph files in the directory as
                                      arguments
-c, --coopt <files...>              provide 2 graphs which will be aligned. Co-optimals
                                      will be saved in ./results
-v, --view <files...>               get a visual representation of the given graphs in
                                      one window. This can get confusing for large or
                                      many graphs. Use -d if you want to see one window
                                      per graph.
-d, --disp-mult <files...>          get a visual representation of the given graphs in
                                      one window per graph.
'''
)
mxg = group.add_mutually_exclusive_group(required=True)
mxg.add_argument(
    '-h',
    '--help',
    action='help',
    default=argparse.SUPPRESS,
    help=argparse.SUPPRESS
)

mxg.add_argument(
    '-i',
    '--input',
    dest='files',
    type=process_file,
    nargs='+',
    # help='provide .graph files for multiple alignment. \'.\' takes all .graph files in the directory'
    help=argparse.SUPPRESS
)

mxg.add_argument(
    '-c',
    '--coopt',
    dest='coopt',
    type=process_file,
    nargs='+',
    # help='provide *2* graphs which will be aligned. Co-optimals will be saved in ./results.'
    help=argparse.SUPPRESS
)

mxg.add_argument(
    '-v',
    '--view',
    dest='view',
    type=parse_graph,
    nargs='+',
    # help='get a visual representation of the given graphs in one window. This can get incomprehesible for large graphs and many graphs \n Use -vm if you want to see one window per graph.'
    help=argparse.SUPPRESS
)

mxg.add_argument(
    '-d',
    '--display_multiple',
    dest='view_multiple',
    type=parse_graph,
    nargs='+',
    # help='get a visual representation of the given graphs in one window per graph.',
    help=argparse.SUPPRESS
    # metavar=''
)


# optional parameters
group2 = parser.add_argument_group(
    title='Optional arguments',
    description='''
-a, --algorithm <BK|VF2|subVF2>     indicate an alignment-algorithm (default: BK)
                                      Warning: VF2 is only suited if there is true
                                      graph-subgraph isomorphism!
-m, --mult <GREEDY|file>            indicate the multiple alignment method. "greedy"
                                      is the default. If you want to use your own guide
                                      tree, indicate the path to a file containing the
                                      guide tree in Newick format in the first line.
-t, --table <table>                 use a custom label scoring table. For more
                                      information, check the README.md.
-l, --save-all                      save all the graphs produced during the alignment.
                                      The graphs are saved as "[newick].graph".
-s, --save-shorter                  save an additional version of the alignment graph
                                      with much shorter node ids.
-g, --save-guide                    save the alignment tree in Newick-format as
                                      "newick.txt".
-o, --output                        specify the name of the output graph from the
                                      multiple alignment. The .graph extension is
                                      automatically added.
-r, --representation                show interactive representation of the result graph
                                      with 3Djs. This representation is saved as .html file
                                      in the results directory
'''
)

opt = group2.add_argument_group()

opt.add_argument(
    '-a',
    '--algorithm',
    dest='algorithm',
    type=str,
    default='SUBVF2',
    # help='indicate an alignment-algorithm (BK | VF2 | subVF2) (default: subVF2) \n Warning: VF2 is only suited if there is true graph-subgraph isomorphism!'
    help=argparse.SUPPRESS
)

opt.add_argument(
    '-m',
    '--mult',
    dest='mult',
    type=parse_guide_tree,
    default='GREEDY',
    # help='choose a multiple alignment method (default: greedy) \n greedy is the only one available at the moment'
    help=argparse.SUPPRESS
)

opt.add_argument(
    '-t',
    '--table',
    dest='table',
    type=parse_scoring_matrix,
    default='-1',
    # help='choose a custom scoring matrix'
    help=argparse.SUPPRESS
)

opt.add_argument(
    '-l',
    '--save-all',
    dest='save_all',
    action='store_true',
    # help='save all the graphs produced during the alignment \n The graphs are saved as "[newick].graph"'
    help=argparse.SUPPRESS
)

opt.add_argument(
    '-s',
    '--save-shorter',
    dest='save_shorter',
    action='store_true',
    # help='save an additional version of the alignment graph with much shorter node ids'
    help=argparse.SUPPRESS
)

opt.add_argument(
    '-g',
    '--save-guide',
    dest='save_guide',
    action='store_true',
    # help='save the guide tree in Newick-format as "newick.txt"'
    help=argparse.SUPPRESS
)

opt.add_argument(
    '-o',
    '--output',
    dest='output',
    type=str,
    # help='specify the name of the output graph from the multiple alignment.'
    help=argparse.SUPPRESS
)

# not fully implemented yet
opt.add_argument(
    '-r',
    '--representation',
    dest='representation',
    action='store_true',
    # help='show interactive representation of the result graph in XXX. This representation is saved as .html file in the results directory'
    help=argparse.SUPPRESS
)