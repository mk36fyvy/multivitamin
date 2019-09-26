import argparse, os
from argparse import RawTextHelpFormatter

from multivitamin.utils.parser import parse_graph
from multivitamin.utils.get_input import process_file


parser = argparse.ArgumentParser(
    description='A multiple alignment tool for graphs',
    usage='use "python %(prog)s --help" for more information',
    formatter_class=RawTextHelpFormatter
)

# TODO: Add debug options ( parser, modular product, ?)

# arguments which provide the graph files
group = parser.add_argument_group('required arguments', 'this argument is required')
mxg = group.add_mutually_exclusive_group(required=True)
mxg.add_argument(
    '-f',
    '--files',
    dest='files',
    type=process_file,
    nargs='+',
    help='provide .graph files for the alignment'
)

# mxg.add_argument(
#     '-d',
#     '--dir-path',
#     dest='path',
#     type=process_directory,
#     nargs='+',
#     help='provide a dir which contains the .graph files to be aligned (other files or subdirs are ignored)'
# )



# optional parameters
parser.add_argument(
    '-a',
    '--algorithm',
    dest='algorithm',
    type=str,
    default='BK',
    help='choose an alignment-algorithm (BK or VF2) (default: BK) \n Warning: VF2 is only suited if there is true graph-subgraph isomorphism!'
)

parser.add_argument(
    '-g',
    '--guide-tree',
    dest='guide',
    type=str,
    default='upgma',
    help='choose a guide-tree-algorithm (default: upgma) - upgma is the only available at the moment'
)

parser.add_argument(
    '-s',
    '--save-all',
    dest='save_all',
    action='store_true',
    help='decide whether to save all the graphs produced during the alignment (default: No) - The graphs are saved as "[newick].graph"'
)

parser.add_argument(
    '-n',
    '--save-guide',
    dest='save_guide',
    action='store_true',
    help='decide whether to save the guide tree in Newick-format as "tree.txt" (default: No)'
)