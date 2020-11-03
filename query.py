""" Query Class """

# ---------------------------------------- IMPORT HERE ----------------------------------------

from word_processor import Word_processor

# ---------------------------------------- Query  ----------------------------------------

class Query:
    
    def __init__(self):
        self.word_processor = Word_processor()
        self.text = ""
        self.index_num = None # Holds value of specified index (if any)

    # ---------------------------------------- PARSE QUERY ----------------------------------------

    def parse(self, index_mapping):
        """ Uses word_processor to parse query into tokens """

        # Plain query - <query>
        # Specifying index - <query> | index_name.csv

        if '|' in self.text:
            self.text, index_name = self.text.split('|')
            index_name = index_name.strip() # Remove whitespace
            
            try:
                self.index_num = index_mapping.inverse[index_name]
            
            except KeyError:
                print("The index {} was not found. Searching on all indexes.".format(index_name))
        
        self.text = self.word_processor.process(self.text).split(" ")

    # ---------------------------------------- SEARCH INDEXES ----------------------------------------

    def search(self, indexes):
        """ Searches through indexes and returns result """

        answers = dict() # Stores the results over all indexes

        if self.index_num is not None: # query specifies index
            index = indexes[self.index_num]
            answer = self.search_index(index)
            answers[self.index_num] = answer

            self.index_num = None # Reset for next query
            return answers

        for i, index in enumerate(indexes):
            answer = self.search_index(index)

            if answer != set():
                answers[i] = answer # Mapping of Index id -> List of docid

        return answers

    def search_index(self, index):
        """ Searches one index and returns the results. """
        
        answer = None # Stores set of docid

        for term in self.text:

            # checking for wildcard operator in term
            if '*' in term:
                if answer is None:
                    answer = self.search_wildcard(index, term)

                else:
                    # Perform set intersection of sets of docid for each term
                    wc_result = self.search_wildcard(index, term)

                    if wc_result is not None:
                        answer = answer.intersection(wc_result)

            elif index[0].has_key(term):
                if answer is None:
                    answer = set(index[0][term].keys())
                
                else:
                    # Perform set intersection of sets of docid for each term
                    answer = answer.intersection(set(index[0][term].keys()))

            else:
                answer = set() # Term has not been found. answer is now empty set.

        return answer

    # ---------------------------------------- WILDCARD QUERY ----------------------------------------

    def search_wildcard(self, index, wc_term):
        """ Searches in one index based on wildcard query for a single term
            Returns set of docids that contain terms matching the regex """

        is_suffix = 0
        results = list()

        # handling suffix queries
        if wc_term.startswith('*'):
            is_suffix = 1
            wc_term = wc_term[::-1] # reversing the term
            matched_info = self.find_match(index, wc_term, is_suffix)

            for item in matched_info:
                results.extend(matched_info[item])

            return set(results)
           
        # handling prefix queries
        elif wc_term.endswith('*'):
            matched_info = self.find_match(index, wc_term, is_suffix)

            for item in matched_info:
                results.extend(matched_info[item])

            return set(results)

        # handling a*b type queries
        else:  
            pref = wc_term.split("*")[0]
            suff = wc_term.split("*")[1]
            a1 = self.find_match(index, pref + '*', 0) # terms matching a* 
            a2 = self.find_match(index, suff[::-1] + '*', 1) # terms matching *b

            if(a1 != dict() and a2 != dict()):
                common_terms = set(a1.keys()).intersection(set(map(lambda x:x[::-1], a2.keys())))   
                docids = list()

                for term in common_terms:
                    docids.extend(a1[term])
                
                return set(docids)
            
            return set()  # return empty set if no term matches both, the prefix and suffix

    def find_match(self, index, wc_term, is_suffix):        
        """ Searches in either trie of an index based on prefix/suffix query 
            returns dictionary of terms matching the wildcard query: {<matching_term> : <list of docids>} """

        try:
            # index[0] - normal trie (for prefix query)
            # index[1] - reverse trie (for suffix query)
            # finding elements that satisfy prefix
            match_info = index[is_suffix].items(prefix = wc_term[0:len(wc_term) - 1])
            term_docids = dict()

            for i in range(len(match_info)):
                term = match_info[i][0]
                docid_list = match_info[i][1].keys()
                term_docids[term] = docid_list
            
            return term_docids

        except KeyError: # returning empty dictionary in case of key error due to prefix mismatch
            return dict()
