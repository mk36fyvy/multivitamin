class Scoring():

    def __init__(
        self,
        results,
        scoring_matrix
    ):

        self.results = results
        self.scoring_matrix = scoring_matrix if scoring_matrix else get_scoring_matrix()

        self.res_scores = {} # dictionary with graphs as keys and scores as values

    
    def get_scoring_matrix():
        '''provides a generic scoring_matrix defined for basic molecule graph
        alignment'''

        return {
            ("c","c")
        }


    def score():
        pass