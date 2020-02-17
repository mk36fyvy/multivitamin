import pprint

from multivitamin.basic.node import Node


class Scoring():

    def __init__(
        self,
        small_graph_nodes_len,
        large_graph_nodes_len,
        results,
        scoring_matrix = None
    ):
        self.results = results
        self.null_n = Node("-1", [])

        self.small_graph_nodes_len = small_graph_nodes_len
        self.large_graph_nodes_len = large_graph_nodes_len

        self.scoring_matrix_file = scoring_matrix
        self.scoring_matrix = scoring_matrix

        self.gap_score = -1
        self.res_scores = {} # dictionary with graphs as keys and scores as values


    def score( self ):
        '''
        main scoring function. Uses the scoring_matrix provided by the user
        or the score_without_matrix() function for generic matrixless scoring.
        '''

        if self.scoring_matrix_file == "-1":
            self.score_without_matrix()
            return

        else:
            self.score_with_matrix()


    def score_without_matrix( self ):
        '''
        provides a generic scoring_matrix defined for general multiple
        alignment with labels (same labels are rewarded, gaps are punished)
        '''

        self.gap_score = 0
        exact_match_score = 1
        for res in self.results:

            graph_score = 0
            mapped = 0

            node_label_len = len(next(iter(res.keys())).mult_id) # label length of nodes from smaller graph
            mapping_label_len = 0
            for mapping in res.values():
                if mapping != self.null_n:
                    mapping_label_len = len(mapping.mult_id) # label length of nodes from larger graph
                    break

            for node, mapping in res.items():

                node_labels = node.get_label()
                mapping_labels = mapping.get_label()
                node_score = 0
                if mapping != self.null_n:
                    mapped += 1

                    for el1 in node_labels:
                        for el2 in mapping_labels:
                            if "-" in el1:
                                node_score += self.gap_score
                            elif "-" in el2:
                                node_score += self.gap_score
                            elif el1 == el2:
                                node_score += exact_match_score
                # else:
                #     node_score += self.gap_score * node_label_len * mapping_label_len

                graph_score += node_score

            gap_node_amount = self.large_graph_nodes_len-mapped
            graph_score += self.gap_score * gap_node_amount * node_label_len * mapping_label_len

            self.res_scores[tuple(sorted(res.items()))] = int(graph_score/len(res))

        return


    def score_with_matrix( self ):
        '''
        scores alignments by applying user-defined scores from scoring table parsed in
        get_input.py
        '''

        self.gap_score = self.scoring_matrix[("-","-")]
        for res in self.results:

            graph_score = 0
            mapped = 0

            node_label_len = len(next(iter(res.keys())).mult_id) # label length of nodes from smaller graph
            mapping_label_len = 0
            for mapping in res.values():
                if mapping != self.null_n:
                    mapping_label_len = len(mapping.mult_id) # label length of nodes from larger graph
                    break

            for node, mapping in res.items():

                node_labels = node.get_label()
                mapping_labels = mapping.get_label()
                node_score = 0
                if mapping != self.null_n:
                    mapped += 1
                    for el1 in node_labels:
                        for el2 in mapping_labels:
                            if "-" in (el1,el2):
                                node_score += self.gap_score
                            else:
                                try:
                                    node_score += self.scoring_matrix[ (el1,el2) ]
                                except KeyError:
                                    print("{} or {} were not defined in scoring file".format( el1, el2 ))
                                    raise
                else:
                    node_score += self.gap_score * node_label_len * mapping_label_len

                graph_score += node_score
            gap_node_amount = self.large_graph_nodes_len-mapped
            graph_score += self.gap_score*gap_node_amount*node_label_len*mapping_label_len
            self.res_scores[tuple(sorted(res.items()))] = int(graph_score/(self.large_graph_nodes_len+self.small_graph_nodes_len-(2*mapped)))


    def get_best_result( self ):
        '''
        finds the best, i.e. highest scoring result in self.res_scores which are created by score()
        '''

        res_dict = dict( self.res_scores )
        best_graph = max(res_dict.keys(), key=(lambda k: self.res_scores[k])) #returns key with highest value in dict
        best_graph_value = self.res_scores[best_graph]
        tup = (
            dict(best_graph),
            best_graph_value
        )
        return tup