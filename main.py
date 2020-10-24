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

folder_path = "C:\\Users\\hritv\\Documents\\College\\SEM 7\\E5_AIR\\project\\TelevisionNews"
files = os.listdir(folder_path)
# os.remove(folder_path + "\\" + "CNN.200910.csv")

# ---------------------------------------- MAIN FUNCTION ----------------------------------------

if __name__ == '__main__':
    index_timer = Timer(text = "Index construction complete! Time taken {:0.6f} seconds")
    index_construct = Construct_index()
    
    index_timer.start()
    index_construct.construct_index()
    indexes = index_construct.collect_index()
    index_timer.stop()

    # Write the index to a file
    with open('indexfile', 'wb') as fp:
        pickle.dump(indexes, fp)
    