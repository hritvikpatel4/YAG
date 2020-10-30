""" Word Processor Class """

# ---------------------------------------- IMPORT HERE ----------------------------------------

import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# ---------------------------------------- Word_processor ----------------------------------------

class Word_processor:
    
    def my_lemmatize(self, text):
        """ Lemmatization """

        lemmatizer = WordNetLemmatizer()
        text = text.split()
        data = []

        for word in text:
            lword = lemmatizer.lemmatize(str.lower(word))
            data.append(lword)

        return " ".join(data)

    def remove_stopword(self, text):
        """ Function to remove stopwords """

        stop_words = set(stopwords.words('english'))
        not_to_delete = ["not", "no", "up", "down", "under", "above", "below",
                    "own", "on", "off", "out", "through", "won", "against",
                    "now", "before", "after"]

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

    def process(self, text):
        """ Function to return processed form of a sentence """
        return self.my_lemmatize(self.remove_stopword(self.clean_text(text)))
