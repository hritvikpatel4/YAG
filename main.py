""" Main """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import atexit, itertools, json, nltk, os, pickle, platform, ssl, subprocess, sys, threading, time
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from timer import Timer
from construct_index import Construct_index
from query import Query
from ranking import Ranking

# ---------------------------------------- INIT ----------------------------------------

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Install "elasticsearch", "elasticsearch_dsl" & "elasticsearch-loader"
#subprocess.run([sys.executable, "-m", "pip", "install", "elasticsearch"])
#subprocess.run([sys.executable, "-m", "pip", "install", "elasticsearch_dsl"])
#subprocess.run([sys.executable, "-m", "pip", "install", "elasticsearch-loader"])

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

folder_path = os.path.relpath("../TelevisionNews")
index_name = 'indexfile'
progress_done = False
_platform = platform.platform()
exit_command = "Ctrl + C"

from elasticsearch import Elasticsearch

# Initialize Elasticsearch Client
es_client = Elasticsearch(hosts = ["localhost"])

# Detect the platform
if _platform == "Darwin": # Detect OSX / MacOS
    exit_command = "Cmd + C"

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
    # Cleanup handler
    def cleanup():
        print("\nGot {}! Cleaning up and gracefully exiting...".format(exit_command))

        sys.exit(1)

    atexit.register(cleanup)

    #print("\nMake sure you have started Elasticsearch. To do that, go to 'elasticsearch-7.9.3/bin/' & run 'elasticsearch.bat' -> Windows or 'elasticsearch' -> Other Platforms")

    # TODO: This file 'elasticsearch_index.py' will be added later on. There is some minor issue with it.
    # print("\nMake sure you run 'elasticsearch_index.py' to index the dataset for elasticsearch")

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
    load_index_timer = Timer(text = "\nLoading index complete! Time taken {:0.6f} seconds")
    t = threading.Thread(target = progress_bar) # Progress animation
    t.start()

    load_index_timer.start()
    with open(index_name, 'rb') as fp:
        indexes, index_mapping, idf_dict = pickle.load(fp)

    progress_done = True
    del t
    load_index_timer.stop_print()

    # Initialize Query object
    q = Query()

    # Initialize Ranking object
    r = Ranking(1)

    # Initialize JSON Output
    json_out = dict()

    # Query Loop
    while True:
        try:
            print("\nPlease choose your query type: (Do {} anytime to exit):".format(exit_command))
            print("1. Simple Query")
            print("2. Phrase Query")
            print("3. Wildcard Query")
            choice = int(input("Enter choice number: ").strip())

            if choice > 3 or choice <1:
                print("Invalid choice")
                continue

            print("\nPlease choose your ranking type: (Do Ctrl+C anytime to exit):")
            print("1. Cosine Similarity")
            print("2. Summation of tf-idf scores w.r.t document")
            print("3. Summation of (tf-idf w.r.t doc * tf-idf w.r.t query)  ")
            r_choice = int(input("Enter choice number: ").strip())
            print()
            r.choice = r_choice

            if r.choice > 3 or r.choice <1:
                print("Invalid choice")
                continue

            print("\nPlease type your query (Do {} anytime to exit):".format(exit_command))
            q.text = input()

            k = int(input("Enter K (Top K documents will be returned): ")) # to return top k documents

            json_filename = "(" + q.text + ")+choice-" + str(choice) + "__r_choice-" + str(r_choice) + "_" + time.strftime("%Y-%m-%d___%H-%M-%S") + ".json"

            q.parse(index_mapping)

            if choice == 2:
                q.isPhrase = 1

            elif choice == 3: # indicates a wildcard query
                q.isWC = 1

            # Time the query
            query_timer = Timer()
            query_timer.start()

            results = q.search(indexes)

            # for key, value in results.items():
            #     print(key, index_mapping[key], value)

            final_results = r.rank_all(q.text, results, indexes, idf_dict, q.isWC)

            query_time = query_timer.stop_time()
            del query_timer

            # Write results as json format
            json_out["query_time"] = query_time
            json_out["results"] = len(final_results)
            json_out["hits"] = []

            for docid, score, index in (final_results[:k]):
                # print("DocID: {:5}, Score: {:7.4f}, Index Name: {:15}".format(docid, score, index_mapping[index]))
                filepath = os.path.join(folder_path, index_mapping[index])

                pd_dataframe = pd.read_csv(filepath)
                snippet_column = pd_dataframe["Snippet"]
                #text_column = pd_dataframe["Text"]
                url_column = pd_dataframe["URL"]

                json_out["hits"].append({
                    '_index': index_mapping[index],
                    '_score': score,
                    '_doc_id': docid,
                    '_path': filepath,
                    '_url': url_column[docid],
                    '_snippet': snippet_column[docid],
                    #'_text' : text_column[docid]
                })

            # Uncomment the below line to print json onto the console
            # print(json.dumps(json_out, indent = 4))

            # Writing Json to file
            json_filename = json_filename.replace('*','_')

            with open(json_filename, 'w') as json_outfile:
                json.dump(json_out, json_outfile, indent = 4)

            json_out.clear()

            print("\nLook at the file named '{}' in the current directory for the output\n----------".format(json_filename))

        except ValueError:
            print("\nPlease enter valid choice")
            continue
