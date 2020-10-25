""" Query Class """

# ---------------------------------------- IMPORT HERE ----------------------------------------

from word_processor import Word_processor

# ---------------------------------------- Query  ----------------------------------------

class Query:
    def __init__(self):
        self.word_processor = Word_processor()
        self.text = ""

    # ---------------------------------------- PARSE QUERY ----------------------------------------

    def parse(self):
        """ Uses word_processor to parse query into tokens """
        self.text = self.word_processor.process(self.text).split(" ")

    # ---------------------------------------- SEARCH INDEXES ----------------------------------------

    def search(self, indexes):
        """ Searches through indexes and returns result """
        answers = dict() # Stores the results over all indexes
        for i, index in enumerate(indexes):
            answer = None # Stores the result of one index
            for term in self.text:
                if index[0].has_key(term):
                    if answer is None:
                        answer = set(index[0][term].keys()) # Set of docid
                    else:
                        # Perform set intersection of sets of docid for each term
                        answer = answer.intersection(set(index[0][term].keys()))
                else:
                    answer = set() # Term has not been found. answer is now empty set
            if answer != set():
                answers[i] = answer # Mapping of Index id -> List of docid
        return answers
