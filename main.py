""" Main """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import itertools, json, nltk, os, pickle, sys, threading, time
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from timer import Timer
from construct_index import Construct_index
from query import Query
from ranking import Ranking

# ---------------------------------------- INIT ----------------------------------------

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

folder_path = os.path.relpath("../TelevisionNews")
index_name = 'indexfile'
progress_done = False

# ---------------------------------------- MISC ----------------------------------------

# Progress bar animation
def progress_bar():
    for progress in itertools.cycle(['|', '/', '-', '\\']):
        if progress_done:
            break

        sys.stdout.flush()
        sys.stdout.write('\rLoading index ' + progress)
        sys.stdout.flush()

        time.sleep(0.1)
    
    sys.stdout.flush()
    return

# ---------------------------------------- MAIN FUNCTION ----------------------------------------

if __name__ == '__main__':
    if not(os.path.exists(index_name)): # Index has not been constructed yet
        print("\nIndex is now being constructed.")
        index_timer = Timer(text = "Index construction complete! Time taken {:0.6f} seconds")
        index_construct = Construct_index(folder_path)

        index_timer.start()
        index_construct.construct_index()
        indexes_data = index_construct.collect_index() # Indexes ,index_mapping, idf_dict
        index_timer.stop_print()

        # Write the index to a file
        with open(index_name, 'wb') as fp:
            pickle.dump(indexes_data, fp)
        
        del index_timer
        del index_construct

    # Load index
    print()
    t = threading.Thread(target = progress_bar) # Brains behind the progress animation :)
    t.start()
    
    with open(index_name, 'rb') as fp:
        indexes, index_mapping, idf_dict = pickle.load(fp)
    
    progress_done = True
    print("\nLoading index successful!")
    del t

    # Initialize Query object
    q = Query()

    # Initialize Ranking object
    r = Ranking()

    # Query Loop
    while True:
        print("Please type your query (Do Ctrl+C anytime to exit):")
        
        try:
            q.text = input()

            json_filename = q.text + "_" + time.strftime("%Y%m%d-%H%M%S") + ".result"

            q.parse(index_mapping)

            results = q.search(indexes)

            # for key, value in results.items():
            #     print(key, index_mapping[key], value)
            # print("\n----------\n")
            
            # Time the query
            query_timer = Timer()
            query_timer.start()
            final_results = r.rank_all(q.text, results, indexes, idf_dict)
            query_time = query_timer.stop_time()

            del query_timer

            # Write results as json format
            json_out = {}
            json_out["query_time"] = query_time
            json_out["results"] = len(final_results)
            json_out["hits"] = []
            
            for docid, score, index in (final_results):
                # print("DocID: {:5}, Score: {:7.4f}, Index Name: {:15}".format(docid, score, index_mapping[index]))
                filepath = os.path.join(folder_path, index_mapping[index])

                pd_dataframe = pd.read_csv(filepath)
                snippet_column = pd_dataframe["Snippet"]
                url_column = pd_dataframe["URL"]
                
                json_out["hits"].append({
                    '_index': index_mapping[index],
                    '_score': score,
                    '_doc_id': docid,
                    '_path': filepath,
                    '_url': url_column[docid],
                    '_snippet': snippet_column[docid]
                })
            
            # Uncomment the below line to print json onto the console
            # print(json.dumps(json_out, indent = 4))

            # Writing Json to file
            with open(json_filename, 'w') as json_outfile:
                json.dump(json_out, json_outfile, indent = 4)
            
            json_out.clear()

            print("\nLook at the file named '{}' in the current directory for the output\n----------".format(json_filename))
        
        except KeyboardInterrupt:
            print("\nGot Ctrl+C as input. Cleaning up and gracefully exiting...")
            
            # Cleaning up
            json_out.clear()
            del q
            del r
            
            sys.exit(1)
