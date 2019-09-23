import argparse, os
from argparse import RawTextHelpFormatter

from multivitamin.utils.parser import parse_graph


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


parser = argparse.ArgumentParser(
    description='A multiple alignment tools for graphs',
    usage='use "python %(prog)s --help" for more information',
    formatter_class=RawTextHelpFormatter
)



# arguments which provide the graph files
group = parser.add_argument_group('required arguments', 'one of these arguments is required')
mxg = group.add_mutually_exclusive_group(required=True)
mxg.add_argument(
    '-f',
    '--files',
    dest='files',
    type=parse_graph,
    nargs='+',
    help='provide graph-files for the alignment'
)

mxg.add_argument(
    '-d',
    '--dir-path',
    dest='path',
    type=dir_path,
    help='provide a dir which contains exclusively the graph-files to be aligned'
)



# optional parameters
parser.add_argument(
    '-a',
    '--alignment',
    dest='alignment',
    type=str,
    default='VF2',
    help='choose an alignment-algorithm (BK or VF2) (default: VF2)'
)

parser.add_argument(
    '-g',
    '--guide-tree',
    dest='guide',
    type=str,
    default='upgma',
    help='choose a guide-tree-algorithm (default: upgma)'
)

parser.add_argument(
    '-s',
    '--save-guide',
    dest='save_guide',
    action='store_true',
    help='decide whether to save the guide tree as in Newick-format (default: No)'
)


args = parser.parse_args()




print(args.alignment)
print(args.graphs)
