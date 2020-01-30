import pprint

# from multivitamin.basic.graph import Graph

class Scoring():

    def __init__(
        self,
        results,
        scoring_matrix = None
    ):

        self.results = results
        self.scoring_matrix = self.parse_scoring_matrix( scoring_matrix ) if scoring_matrix else "-1"

        self.gap_score = -1
        self.res_scores = {} # dictionary with graphs as keys and scores as values


    def score( self ):
        '''main scoring function. Uses the scoring_matrix provided by the user
        or the score_without_matrix() function for general matrixless scoring.'''
        if self.scoring_matrix == "-1":
            self.score_without_matrix()
            return

        else:
            pass


    def score_without_matrix( self ):
        '''provides a generic scoring_matrix defined for general multiple
        alignment with labels (same labels are rewarded, gaps are punished)'''
        self.gap_score = -1
        match_score = 4
        for nodes in self.results:
            
            graph_score = 0

            for node in nodes:
                label_list = node.label.split(" ")
                node_score = 0
                gap_amount = 0
                
                for char in label_list:
                    if char == "-":
                        gap_amount +=1
                        label_list.remove(char)
                node_score += ((len(label_list)+gap_amount-1)*gap_amount*gap_score) #the pairs that would have "-" are simulated here to save time
                
                i = 1
                for char1 in label_list[:-1]:
                    for char2 in label_list[i:]:
                        if char1 == char2:
                            node_score += match_score
                
                graph_score += node_score
                i+=1

            self.res_scores[frozenset(nodes)] = graph_score/len(nodes)
            # for key,value in self.res_scores.items():
                # print()
                # pprint.pprint(value)
                # pprint.pprint(key)
                # print()

        return


    def parse_scoring_matrix( self, matrix ):
        file = matrix
        with open(file) as f:
            
            first_line = f.readline().split("\t")
            if first_line[0] == "-":
                self.gap_score = int(first_line[1])
                next(f) #skips the first line in the for-loop later
            else:
                print("!warning!: No gap score was specified in first line of {}. Assuming -1.".format(f))

            cart_pair_check = list()
            cart_pairs = list()

            for line in f:
                args = line.split("\t")
                if isinstance(args[1], int): # upper part of table defining gap and char equality
                    cart_pair_check.append(args[0])
                    self.scoring_matrix[args[0],args[0]] = int(args[1])
                elif isinstance(args[1], str): #lower part of the table defining inequal pairs
                    cart_pairs.append(args[0],args[1])
                    # cart_pairs.append(args[1],args[0])
                    self.scoring_matrix[args[0],args[1]] = int(args[2])
                    self.scoring_matrix[args[1],args[0]] = int(args[2])
                else:
                    raise(Exception("The scoring table {} does not seem to be correctly formatted.".format(f)))

            self.return_missing_pairs( cart_pair_check, cart_pairs )
            

    def return_missing_pairs( self, char_list, cart_pairs ):
        missing_pairs = list()
        for pair in self.get_all_cart_pairs( char_list ):
                if not pair in cart_pairs:
                    missing_pairs.append(pair)
        if missing_pairs:
            print()
            print("!Warning!: the following pairs have not been assigned in the scoring table. Assuming 0:")
            for pair in missing_pairs:
                print("{}\t{}\t0".format(pair[0],pair[1]))
            print("If you want to forbid the mapping of a specific pair, change the check_semantics() function in custom.py accordingly.")
            print()

    def get_all_cart_pairs( self, char_list):
        all_cart_pairs = []
        for char1 in char_list:
            for char2 in char_list:
                if not (char2, char1) in all_cart_pairs:
                    all_cart_pairs.append( (char1, char2) )
                    # all_cart_pairs.append( (char2, char1) )
        return all_cart_pairs