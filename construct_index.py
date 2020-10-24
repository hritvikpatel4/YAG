""" Construct Index Class """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import bisect, nltk, os, pygtrie, string
import multiprocessing
import pandas as pd
from bidict import bidict
from nltk.tokenize import word_tokenize
from word_processor import Word_processor

# ---------------------------------------- Construct_index ----------------------------------------

class Construct_index:
	def __init__(self, folder_path):
		self.indexes = list() # List of indexes. One index for each csv file
		self.folder_path = folder_path
		self.index_mapping = bidict(
			{
				i:os.listdir(folder_path)[i] for i in range(len(os.listdir(folder_path)))
			}
		) # Store bidirectional mapping between index number and index name for fast two-way lookup
		self.word_processor = Word_processor()

	# ---------------------------------------- PREPROCESS ----------------------------------------

	def pre_process(self, file_path, col = "Snippet"):
		""" Wrapper function, called for each file
			Returns a dataframe with new preprocessed column 'Text' """
		
		df = pd.read_csv(file_path)
		data = []
		column = df[col]
		
		for row in column:
			data.append(self.word_processor.process(row))
			
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

		file_path = os.path.join(self.folder_path, file_path)
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
		self.indexes = pool.map(self.construct_index_helper, self.index_mapping.inverse)
		pool.close()
		pool.join()

	# ---------------------------------------- INDEX STORE ----------------------------------------

	def collect_index(self):
		""" Returns the built-up index and mapping. Only this function is available to the client """
		return self.indexes, self.index_mapping
