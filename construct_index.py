""" Construct Index Class """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import bisect, nltk, os, pygtrie, string
import multiprocessing
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from timer import Timer

# ---------------------------------------- INIT ----------------------------------------

folder_path = "C:\\Users\\hritv\\Documents\\College\\SEM 7\\E5_AIR\\project\\TelevisionNews"
files = os.listdir(folder_path)

# ---------------------------------------- Construct_index ----------------------------------------

class Construct_index:
	def __init__(self):
		self.indexes = list()
	
	# ---------------------------------------- PREPROCESS ----------------------------------------

	def my_lemmatize(self, text):
		""" Lemmatization """
		
		lemmatizer = WordNetLemmatizer()
		text = text.split()
		data = []
    
		for word in text:
			lword = lemmatizer.lemmatize(word)
			data.append(lword)
			
		return " ".join(data)

	def remove_stopword(self, text):
		""" Function to remove stopwords """
		
		stop_words = set(stopwords.words('english'))
		not_to_delete = ["not", "no", "up", "down", "under", "above", "below", "own", "on", "off", "out", "through", "won", "against", "now", "before", "after"]    
    
    	# retaining some stopwords
		for word in not_to_delete:
			stop_words.remove(word)
		
		word_tokens = word_tokenize(text)
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
		
		return (" ".join(filtered_sentence))

	def clean_text(self, text):
		""" Function to remove special characters and punctuations """
    	
		# decimals?
		text = text.replace("\n", " ").replace("\r", " ")
		punclist = string.punctuation
		
		t = str.maketrans(dict.fromkeys(punclist, " "))
		text = text.translate(t)
		
		t = str.maketrans(dict.fromkeys("'`", ""))
		text = text.translate(t)
		
		return text

	def pre_process(self, file_path, col = "Snippet"):
		""" Wrapper function, called for each file
			Returns a dataframe with new preprocessed column 'Text' """
		
		df = pd.read_csv(file_path)
		data = []
		column = df[col]
		
		for row in column:
			data.append(self.my_lemmatize(self.remove_stopword(self.clean_text(row))))
			
		df["Text"] = data
		
		return df
	
	# ---------------------------------------- MISC ----------------------------------------

	def update_trie(self, term, docid, pos, trie):
		""" Updating positional index """
		
		if term in trie:
			if docid in trie[term]:
				# Insert into sorted list of positions
				bisect.insort(trie[term][docid], pos)
				
			else:
				trie[term][docid] = [pos]
				
		else:
			trie[term] = {docid:[pos]}
	
	# ---------------------------------------- INDEX CONSTRUCTION ----------------------------------------

	def construct_index_helper(self, file_path):
		""" Helper function to create index for each file
			Returns (normal index, reverse index)
			Trie node: key, value pairs
					   key - <term>, value- {docId1: [pos1, pos2, pos3...], docId2: [pos1,pos2...]} """
		
		file_path = folder_path + "\\" + file_path
		df = self.pre_process(file_path)
		corpus = df["Text"]

		# Creating 2 tries
		index_trie = pygtrie.CharTrie()
		rev_trie = pygtrie.CharTrie()

		for i in range(len(corpus)):
			row = word_tokenize(corpus[i])

		for j in range(len(row)):
			self.update_trie(row[j], i, j, index_trie)
			self.update_trie(row[j][::-1], i, j, rev_trie)

		return (index_trie, rev_trie)
	
	def construct_index(self):
		""" Interface for constructing index. Only this function is available to the client """
		# Here is the secret to the fast processing :)
		# Lets call it the "Google Logic"
		# Dont tell about this technique to others else we will lose our market share xD
		
		pool = multiprocessing.Pool(multiprocessing.cpu_count())
		result = pool.map(self.construct_index_helper, files)
		self.indexes.append(result)
		pool.close()
		pool.join()
	
	# ---------------------------------------- INDEX STORE ----------------------------------------

	def collect_index(self):
		""" Returns the built-up index. Only this function is available to the client """
		return self.indexes
