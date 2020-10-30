""" Ranking Class """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import math

# ---------------------------------------- Ranking ----------------------------------------

class Ranking:

    def __init__(self):
        pass
    
    # ---------------------------------------- COMPUTE SCORE ----------------------------------------------------------
        
    def compute_score(self, query, docid, index_trie, tfidf_query):
        """ Computes score for each document w.r.t the query """
        
        tot_score = 0
        length_td = 0
        length_tq = 0

        for term in query:
            tot_score += (index_trie[term][docid][1] * tfidf_query[term]) # tf-idf w.r.t document * tf-idf w.r.t query
            length_td += (index_trie[term][docid][1] * index_trie[term][docid][1])
            length_tq += (tfidf_query[term] * tfidf_query[term])

        tot_score = tot_score / (math.sqrt(length_tq) * math.sqrt(length_td))
        return [docid, tot_score]

    # ---------------------------------------- RANK RESULTS -----------------------------------------------------------
    
    def rank_all(self, query, answers, indexes, idf_dict):
        """ Ranks final list of documents based on tf-idf scores """

        final = list()
        tfidf_query = dict()
        q = set(query)
        
        for index_num in answers:
        
            # tf-idf of each query term w.r.t the query
            for term in q:
                if term in idf_dict[index_num]:
                    qc = math.log(1 + query.count(term), 10) #log normalization of term count in query
                    tfidf_query[term] = idf_dict[index_num][term] * qc
            
            # computing score for each matching document
            for docid in answers[index_num]:
                score = self.compute_score(query, docid, indexes[index_num][0], tfidf_query)
                score.append(index_num)
                final.append(score) # score: [docid, score of document, index_num]

        final = sorted(final, key = lambda x:-x[1]) # sorting in descending order based on score of document

        return final
