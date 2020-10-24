""" Main """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import nltk, os, pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from timer import Timer
from construct_index import Construct_index

# ---------------------------------------- INIT ----------------------------------------

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

folder_path = os.path.relpath("../TelevisionNews")
index_name = 'indexfile'

# ---------------------------------------- MAIN FUNCTION ----------------------------------------

if __name__ == '__main__':

    if not(os.path.exists(index_name)): # Index has not been constructed yet
        print("Index is now being constructed.")
        index_timer = Timer(text = "Index construction complete! Time taken {:0.6f} seconds")
        index_construct = Construct_index(folder_path)

        index_timer.start()
        index_construct.construct_index()
        indexes = index_construct.collect_index()
        index_timer.stop()

        # Write the index to a file
        with open(index_name, 'wb') as fp:
            pickle.dump(indexes, fp)

    # Open index
    with open(index_name, 'rb') as fp:
        indexes = pickle.load(fp)

    print(len(indexes[0]), type(indexes[0][1]))
