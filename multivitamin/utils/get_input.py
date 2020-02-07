import os

from multivitamin.utils.parser import parse_graph
from multivitamin.custom import labelsep


def process_file( filename ):
    '''
    entry point of graph parsing from command_line. Parses given
    .graph files or all .graph files in the given directory
    '''

    if os.path.isdir(filename):
        print("parsing .graph files in the given directory\n")
        return process_directory(filename)
    else:
        if not filename.endswith('.graph'):
            raise Exception("{} is not a valid input (not a .graph file)!".format(filename))
        return parse_graph( filename ) # this is what is done to the parsed command-line arguments (graphs)



def process_directory( directory_name ):
    '''
    parses all .graph files in the given directory
    '''

    graphs = []
    for filename in os.listdir(directory_name)[:]:
        # print(filename)
        if filename.endswith('.graph'):
            graphs.append(parse_graph((filename)))
            # print(graphs)
    if not graphs:
        raise Exception("No .graph file found in the given directory! Aborting...")

    return graphs


def parse_guide_tree( method ):
    
    if method == "GREEDY":
        return "GREEDY"
    else:
        

def parse_scoring_matrix( matrix_file ):
    '''
    parses the scoring table if given with -t
    '''

    if matrix_file == None:
        print("You did not specify a scoring table.")
        exit()

    elif matrix_file == '-1':
        return '-1'

    file = matrix_file
    scoring_matrix= {}
    with open(file) as f:

        first_line = f.readline().split(labelsep)
        if not first_line[0] == "-":
            gap_score = -1
            print("!warning!: No gap score was specified in first line of {}. Assuming -1.".format(f))
            scoring_matrix[ ('-','-') ] = -1
        else:
            gap_score = int(first_line[1])
            scoring_matrix[ ('-','-') ] = gap_score


        cart_pair_check = list()
        cart_pairs = list()

        for line in f:
            args = line.split(labelsep)
            if len(args)==2:
                scoring_matrix[ (args[0],args[0]) ] = int(args[1])
                cart_pair_check.append(args[0])
            elif len(args)==3:
                cart_pairs.append( (args[0],args[1]) )
                # cart_pairs.append(args[1],args[0])
                scoring_matrix[ (args[0],args[1]) ] = int(args[2])
                scoring_matrix[ (args[1],args[0]) ] = int(args[2])
            else:
                raise Exception("Error in Scoring Matrix:/nUnable to parse: '{}'".format(line))

        scoring_matrix = return_missing_pairs( cart_pair_check, cart_pairs, scoring_matrix, matrix_file, gap_score )
    return scoring_matrix


def return_missing_pairs( char_list, cart_pairs, scoring_matrix, scoring_matrix_file, gap_score ):
    '''
    prints a warning with all missing label pairs generated from the given labels in the scoring table.
    '''

    missing_pairs = list()
    for pair in get_all_cart_pairs( char_list ):
            if "-" in pair:
                scoring_matrix[ pair ] = gap_score
                scoring_matrix[ (pair[1],pair[0]) ] = gap_score
            elif not pair in cart_pairs:
                missing_pairs.append(pair)
                scoring_matrix[ pair ] = 0
                scoring_matrix[ (pair[1],pair[0]) ] = 0
    if missing_pairs:
        print()
        print("!Warning!: the following pairs have not been assigned in {}. Assuming 0:".format(scoring_matrix_file))
        for pair in missing_pairs:
            print("{}{}{}{}0".format( pair[0], labelsep, pair[1], labelsep ))
        print("If you want to forbid the mapping of a specific pair, change the check_semantics() function in custom.py accordingly.")
        print()
    return scoring_matrix




def get_all_cart_pairs( char_list ):
    '''
    generates all possible pairs of the labels given in scoring table
    '''

    all_cart_pairs = []
    for char1 in char_list:
        for char2 in char_list:
            if not (char2, char1) in all_cart_pairs and not char1 == char2 and not "-" in (char1,char2):
                all_cart_pairs.append( (char1, char2) )
                # all_cart_pairs.append( (char2, char1) )
    return all_cart_pairs
