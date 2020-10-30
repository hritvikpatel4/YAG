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
            if index[0].has_key(term):
                if answer is None:
                    answer = set(index[0][term].keys())

                else:
                    # Perform set intersection of sets of docid for each term
                    answer = answer.intersection(set(index[0][term].keys()))

            else:
                answer = set() # Term has not been found. answer is now empty set.

        return answer
