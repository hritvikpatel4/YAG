class Ranking:
    def compute_score(self, query, docid, index_trie, tfidf_query):
        tot_score=0
        length=0
        for term in query:
            tot_score+=index_trie[term][docid][1]*tfidf_query[term]  
            length_td+=(index_trie[term][docid][1]*index_trie[term][docid][1])
            length_tq+=(tfidf_query[term]*tfidf_query[term])

        tot_score= tot_score/(math.sqrt(length_tq)*math.sqrt(length_td))

        return [docid,tot_score]

    def rank_all(self,query,answers, index_trie, idf_dict):
        final=[]

        tfidf_query={}
        q=set(query)
        
        for term in q:
            tfidf_query[term]=idf_dict[term]*query.count(term)

        for index in answers:
            for docid in answers[index]:
                final.append(self.compute_score(query,docid,index_trie, tfidf_query).append(index))

        final=sorted(final,key=lambda x:-x[1])




