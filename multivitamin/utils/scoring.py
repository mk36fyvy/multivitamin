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
        gap_score = -1
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
                node_score += ((len(label_list)+gap_amount-1)*gap_amount*gap_score)
                
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
        file = self.scoring_matrix
        while open(file) as f:
            for line in f:
                args = line.split(" ")
                if args[2].isinstance("int"):
                    self.scoring_matrix[(args[0],args[1]] = args[2])
                #define gap scores here? maybe special line?