""" Word Processor Class """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import string
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# ---------------------------------------- Word_processor ----------------------------------------

class Word_processor:
    
    
    def nltk_tag_to_wordnet_tag(self, nltk_tag):
        """ Function to get the wordnet tag of a word based on its POS tag """
        
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:          
            return None
    
    def my_lemmatize(self, text): 
        """ Function to lemmatize """

        lemmatizer = WordNetLemmatizer()
        
        #text_new = list(map(str.lower, nltk.word_tokenize(text)))
        text_new = list(map(str.lower, text.split(' ')))
        
        #tokenize the sentence and find the POS tag for each token
        nltk_tagged = nltk.pos_tag(text_new)  
        
        #tuple of (token, wordnet_tag)
        wordnet_tagged = map(lambda x: (x[0], self.nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
        
        lemmatized_sentence = []
        for word, tag in wordnet_tagged:
            # word = str.lower(w)
            if tag is None:
                #if there is no available tag, append the token as is
                lemmatized_sentence.append(word)
            else:        
                #else use the tag to lemmatize the token
                lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))

        return " ".join(lemmatized_sentence)

    def remove_stopword(self, text):
        """ Function to remove stopwords """

        stop_words = set(stopwords.words('english'))
        not_to_delete = ["not", "no", "up", "down", "under", "above", "below",
                    "own", "on", "off", "out", "through", "won", "against",
                    "now", "before", "after"]

        # retaining some stopwords
        for word in not_to_delete:
            stop_words.remove(word)

        word_tokens = text.split(' ')
        filtered_sentence = [w for w in word_tokens if not w in stop_words]

        return (" ".join(filtered_sentence))

    def clean_text(self, text):
        """ Function to remove special characters and punctuations """

        # decimals?
        text = text.replace("\n", " ").replace("\r", " ")
        punclist = string.punctuation.replace("*","")

        t = str.maketrans(dict.fromkeys(punclist, " "))
        text = text.translate(t)

        t = str.maketrans(dict.fromkeys("'`", ""))
        text = text.translate(t)

        return text

    def process(self, text):
        """ Function to return processed form of a sentence """
        
        return self.my_lemmatize(self.remove_stopword(self.clean_text(text)))
