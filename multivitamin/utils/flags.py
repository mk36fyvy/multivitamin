import argparse, os
from argparse import RawTextHelpFormatter

from multivitamin.utils.parser import parse_graph
from multivitamin.utils.get_input import process_file


parser = argparse.ArgumentParser(
    description='multiVitamin - A multiple alignment tool for graphs',
    usage='use "python3 %(prog)s --help" for more information',
    formatter_class=RawTextHelpFormatter
)

# one of these args has to be provided, but not both
group = parser.add_argument_group('required arguments', 'these arguments are mutually exclusive')
mxg = group.add_mutually_exclusive_group(required=True)
mxg.add_argument(
    '-m',
    # '--multiple',
    dest='files',
    type=process_file,
    nargs='+',
    help='provide .graph files for multiple alignment. \'.\' is a valid input'
)

mxg.add_argument(
    '-c',
    # '--coopt',
    dest='coopt',
    type=process_file,
    nargs='+',
    help='provide *2* graphs which will be aligned. Co-optimals will be saved in ./results.'
)

mxg.add_argument(
    '-v',
    # '--view',
    dest='view',
    type=parse_graph,
    nargs=1,
    help='get a visual representation of *1* given graph'
)



# optional parameters
parser.add_argument(
    '-a',
    '--algorithm',
    dest='algorithm',
    type=str,
    default='BK',
    help='choose an alignment-algorithm (BK or VF2) (default: BK) \n Warning: VF2 is only suited if there is true graph-subgraph isomorphism!'
)

# parser.add_argument(
#     '-g',
#     '--guide-tree',
#     dest='guide',
#     type=str,
#     default='upgma',
#     help='choose a guide-tree-algorithm (default: upgma) \n upgma is the only one available at the moment'
# )

parser.add_argument(
    '-s',
    '--save-all',
    dest='save_all',
    action='store_true',
    help='save all the graphs produced during the alignment \n The graphs are saved as "[newick].graph"'
)

parser.add_argument(
    '-t',
    '--save-shorter',
    dest='save_shorter',
    action='store_true',
    help='save an additional version of the alignment graph with much shorter node ids'
)

parser.add_argument(
    '-g',
    '--save-guide',
    dest='save_guide',
    action='store_true',
    help='save the guide tree in Newick-format as "newick.txt"'
)