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
        '''main scoring function. Uses the scoring_matrix provided by the user
        or the score_without_matrix() function for general matrixless scoring.'''
        if self.scoring_matrix_file == "-1":
            self.score_without_matrix()
            return

        else:
            self.score_with_matrix()


    # def score_without_matrix( self ):
    #     '''provides a generic scoring_matrix defined for general multiple
    #     alignment with labels (same labels are rewarded, gaps are punished)'''
    #     self.gap_score = -1
    #     match_score = 4
    #     for graph in self.results:

    #         graph_score = 0

    #         for node in graph:
    #             node_labels = node.get_label()
    #             node_score = 0
    #             gap_amount = 0


    #             for char in label_list:
    #                 if char == "-":
    #                     gap_amount +=1
    #                     label_list.remove(char)
    #             node_score += ((len(label_list)+gap_amount-1)*gap_amount*self.gap_score) #the pairs that would have "-" are simulated here to save time

    #             i = 1
    #             for char1 in label_list[:-1]:
    #                 for char2 in label_list[i:]:
    #                     if char1 == char2:
    #                         node_score += match_score

    #             graph_score += node_score
    #             i+=1

    #         self.res_scores[frozenset(nodes)] = graph_score/len(nodes)
    #         for key,value in self.res_scores.items():
    #             print()
    #             pprint.pprint(value)
    #             pprint.pprint(key)
    #             print()

    #     return

    def score_without_matrix( self ):
        '''provides a generic scoring_matrix defined for general multiple
        alignment with labels (same labels are rewarded, gaps are punished)'''
        self.gap_score = -1
        match_score = 4
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
                            if "-" in (el1, el2):
                                node_score += self.gap_score
                            elif el1 == el2:
                                node_score += match_score
                else:
                    node_score += self.gap_score * node_label_len * mapping_label_len

                # node_score += ((len(node_labels)+gap_amount-1)*gap_amount*self.gap_score) #the pairs that would have "-" are simulated here to save time

                graph_score += node_score

            gap_node_amount = self.large_graph_nodes_len-mapped
            graph_score += self.gap_score * gap_node_amount * node_label_len * mapping_label_len

            self.res_scores[tuple(sorted(res.items()))] = int(graph_score/len(res))

            # for key,value in self.res_scores.items():
            #     print()
            #     pprint.pprint(value)
            #     pprint.pprint(key)
            #     print()

        return


    def score_with_matrix( self ):
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
                                except:
                                    raise Exception("{} or {} were not defined in scoring file".format( el1, el2 ))
                else:
                    node_score += self.gap_score * node_label_len * mapping_label_len

                graph_score += node_score
            gap_node_amount = self.large_graph_nodes_len-mapped
            graph_score += self.gap_score*gap_node_amount*node_label_len*mapping_label_len
            self.res_scores[tuple(sorted(res.items()))] = int(graph_score/(self.large_graph_nodes_len+self.small_graph_nodes_len-(2*mapped)))
            # self.res_scores[tuple(sorted(res.items()))] = int(graph_score)


    def get_best_result( self ):
        res_dict = dict( self.res_scores )
        best_graph = max(res_dict.keys(), key=(lambda k: self.res_scores[k])) #returns key with highest value in dict
        best_graph_value = self.res_scores[best_graph]
        tup = (
            dict(best_graph),
            best_graph_value
        )
        # pprint.pprint(tup)
        return tup



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
                try: # upper part of table defining gap and char equality
                    self.scoring_matrix[ (args[0],args[0]) ] = int(args[1])
                    cart_pair_check.append(args[0])
                except Exception as e: #lower part of the table defining inequal pairs
                    print(e)
                    cart_pairs.append( (args[0],args[1]) )
                    # cart_pairs.append(args[1],args[0])
                    self.scoring_matrix[ (args[0],args[1]) ] = int(args[2])
                    self.scoring_matrix[ (args[1],args[0]) ] = int(args[2])

            self.return_missing_pairs( cart_pair_check, cart_pairs )


    def return_missing_pairs( self, char_list, cart_pairs ):
        missing_pairs = list()
        for pair in self.get_all_cart_pairs( char_list ):
                if not pair in cart_pairs:
                    missing_pairs.append(pair)
                    self.scoring_matrix[ pair ] = 0
                    self.scoring_matrix[ (pair[1],pair[0]) ] = 0
        if missing_pairs:
            print()
            print("!Warning!: the following pairs have not been assigned in {}. Assuming 0:".format(self.scoring_matrix_file))
            for pair in missing_pairs:
                print("{}\t{}\t0".format(pair[0],pair[1]))
            print("If you want to forbid the mapping of a specific pair, change the check_semantics() function in custom.py accordingly.")
            print()


    def get_all_cart_pairs( self, char_list):
        all_cart_pairs = []
        for char1 in char_list:
            for char2 in char_list:
                if not (char2, char1) in all_cart_pairs and not char1 == char2:
                    all_cart_pairs.append( (char1, char2) )
                    # all_cart_pairs.append( (char2, char1) )
        return all_cart_pairs