""" Main """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import nltk, os, pickle, sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from timer import Timer
from construct_index import Construct_index
from query import Query

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
        indexes_data = index_construct.collect_index() # Indexes and index_mapping
        index_timer.stop()

        # Write the index to a file
        with open(index_name, 'wb') as fp:
            pickle.dump(indexes_data, fp)

    print("Loading index")

    # Load index
    with open(index_name, 'rb') as fp:
        indexes, index_mapping = pickle.load(fp)

    # Initialize Query object
    q = Query()

    # Query Loop
    while True:
        print("Please type your query (Do Ctrl+C anytime to exit):")
        
        try:
            q.text = input()
            q.parse()

            results = q.search(indexes)

            for key, value in results.items():
                print(index_mapping[key], value)
            
            print("\n----------\n")
        
        except KeyboardInterrupt:
            print("\nGot Ctrl+C as input. Cleaning up and gracefully exiting...")
            sys.exit(1)
