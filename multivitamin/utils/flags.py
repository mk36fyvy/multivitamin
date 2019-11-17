import argparse, os
from argparse import RawTextHelpFormatter

from multivitamin.utils.parser import parse_graph
from multivitamin.utils.get_input import process_file

class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

parser = argparse.ArgumentParser(
    description='multiVitamin - A multiple alignment tool for graphs',
    usage='%(prog)s [ -h | -m | -c | -v | -d ] [-a] [-s] [-t] [-g]\nfor example: multiVitamin -ga VF2 -m g1.graph g2.graph g3.graph',
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
    # formatter_class=CapitalisedHelpFormatter
)

# one of these args has to be provided, but not more
group = parser.add_argument_group(
    title='Required arguments (These arguments are mutually exclusive)',
    description='''
-h, --help                  show this help message and exit
-m, --multiple <files...>   provide .graph files for multiple alignment. \'.\'
                              takes all .graph files in the directory as
                              arguments
-c, --coopt <files...>      provide 2 graphs which will be aligned. Co-optimals
                              will be saved in ./results
-v, --view <files...>       get a visual representation of the given graphs in
                              one window. This can get incomprehesible for large
                              graphs and many graphs. Use -vm if you want to see
                              one window per graph.
-d, --disp-mult <files...>  get a visual representation of the given graphs in
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
    '-m',
    '--multiple',
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
-a, --algorithm <BK|VF2>    indicate an alignment-algorithm (default: BK)
                              Warning: VF2 is only suited if there is true
                              graph-subgraph isomorphism!
-s, --save-all              save all the graphs produced during the alignment.
                              The graphs are saved as "[newick].graph"
-t, --save-shorter          save an additional version of the alignment graph
                              with much shorter node ids
-g, --save-guide            save the guide tree in Newick-format as "newick.txt"
'''
)
opt = group2.add_argument_group()

opt.add_argument(
    '-a',
    '--algorithm',
    dest='algorithm',
    type=str,
    default='BK',
    # help='indicate an alignment-algorithm (BK or VF2) (default: BK) \n Warning: VF2 is only suited if there is true graph-subgraph isomorphism!'
    help=argparse.SUPPRESS
)

# opt.add_argument(
#     '-g',
#     '--guide-tree',
    # dest='guide',
#     type=str,
#     default='upgma',
#     help='choose a guide-tree-algorithm (default: upgma) \n upgma is the only one available at the moment'
# )

opt.add_argument(
    '-s',
    '--save-all',
    dest='save_all',
    action='store_true',
    # help='save all the graphs produced during the alignment \n The graphs are saved as "[newick].graph"'
    help=argparse.SUPPRESS
)

opt.add_argument(
    '-t',
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
