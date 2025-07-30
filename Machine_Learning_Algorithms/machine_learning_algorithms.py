#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 04:45:47 2025

@author: ngoni97
"""
# どうもありがとうございます == Dōmo arigatōgozaimasu

import os
import re
import numpy as np
import pickle
import time

# loading machine learning modules
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import LinearSVC

from folder_iterator_class import FolderIterator
from updated_reading_pdf_contents_data_saver_with_concurrent import DocumentContentDataset

""" model_types:
    MultinomialNB
    ComplementNB
    LinearSVC
"""

class LOAD_DATASET():
    def __init__(self, folders=[], *, pages=10, normalise=False, save_as_text_file=True):

        """ folders list must contain full folder paths """
        self.folders = folders
        self.pages = pages
        self.normalise = normalise
        self.save_as_text_file = save_as_text_file

        for folder in self.folders:

            load_folder = DocumentContentDataset(folder, pages=self.pages, 
                                                 normalise=self.normalise, 
                                                 save_as_text_file=self.save_as_text_file)
            pass

class RUNMODEL():
    def __init__(self, folder_path,*, model_type=None,
                  use_saved_model=False, vectoriser='CountVectorizer',
                  test_size=0.3, random_state=42):
        """ model_type:
            - MultinomialNB
            - ComplementNB
            - LinearSVC
        """
        self._folder_path = folder_path
        self.use_saved_model = use_saved_model
        self._model_path = '/home/ngoni97/file-manger-with-ml/Machine_Learning_Algorithms'
        self._vectoriser = vectoriser
        self._model_type = model_type
        self.test_size = test_size
        self.random_state = random_state
        
        # run main
        self.main()
        
    def remove_characters_before_tokenization(self, sentence, keep_apostrophes=False):
        """ remove characters and keeps words only"""
        if not sentence:
            return ""
        # string
        sentence = (sentence.replace('_', ' ')).replace('-', ' ')
        PATTERN = re.compile('[?|$|&|*|%|@|(|)|~]')
        pattern = re.compile('[^a-zA-Z]') if not keep_apostrophes else re.compile('[^a-zA-Z\']')
        replacement = r' '
        
        filtered_sentence = re.sub(pattern, replacement, re.sub(PATTERN, replacement, sentence))
        return ' '.join(filtered_sentence.lower().split())  # Remove extra spaces
    
    def dataCollector(self, path, clean=False):
        import os
        Data = {}
        for item in os.listdir(path):
            new_path = os.path.join(path, item)
            with open(new_path, 'r') as file:
                try:
                    text = file.read()
                except Exception as e:
                    pass
                else:
                    if clean == True:
                        test = self.remove_characters_before_tokenization(text)
                        if test != ' ':
                            Data[item] = self.remove_characters_before_tokenization(text)
                        elif test == ' ':
                            pass
                    else:
                        Data[item] = text
        return Data
    
    def normalize_document(self, doc):
        # lower case and remove special characters\whitespaces
        doc = re.sub(r'[^a-zA-Z0-9\s]', '', doc, re.I)
        doc = doc.lower()
        doc = doc.strip()
        # tokenize document
        tokens = self.wpt.tokenize(doc)
        # filter stopwords out of document
        filtered_tokens = [token for token in tokens if token not in self.stop_words]
        # re-create document from filtered tokens
        doc = ' '.join(filtered_tokens)
        return doc
    
    def labelEncoder(self, labels):
        self.enc = LabelEncoder()
        encoded_labels = self.enc.fit_transform(labels)
        
        return encoded_labels
    
    def VECTORISER(self):
        if self._vectoriser == 'CountVectorizer':
            Vectoriser = CountVectorizer()
            
        elif self._vectoriser == 'TfidfVectorizer':
            Vectoriser = TfidfVectorizer()
        else:
            pass
        return Vectoriser
    
    def return_X_y(self, data_list_obj, labels_list_obj):
        """ returns the normalised X and encoded y datasets """

        self.normalize_corpus = np.vectorize(self.normalize_document)

        self.X = self.normalize_corpus(data_list_obj)
        self.y = self.labelEncoder(labels_list_obj)
        return self.X, self.y

    def modelFitting(self):
        """ fit the model """
        if self._model_type == 'ComplementNB':
            self.MODEL = make_pipeline(self.VECTORISER(), ComplementNB())
        elif self._model_type == 'LinearSVC':
            self.MODEL = make_pipeline(self.VECTORISER(), LinearSVC())
        elif self._model_type == 'MultinomialNB':
            self.MODEL = make_pipeline(self.VECTORISER(), MultinomialNB())
        else:
            print('\nModel type not set')
    
        return self.MODEL
    
    def modelTraining(self, X, y):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)
        
        if self.use_saved_model:
            return self.loadModel()
        else:
            return self.MODEL.fit(self.X_train, self.y_train)

    def modelPredicting(self):
        """ model predict """
        print("Test set score: {:.2f}".format(self.MODEL.score(self.X_test, self.y_test)))
        return self.MODEL.predict(self.X_test)
    
    def accuracy(self):
        """ testing the overall accuracy """
        pass
    
    def Predict(self, value):
        """ return the predicted label"""
        model_pred = self.MODEL.predict([value])
        # add the function to return the corresponding encode label
        return self.enc.inverse_transform(model_pred)[0]

    def saveModel(self):
        """ saving the model for future reference to use as a external model """
        if self._model_type != None:
            self._path = os.path.join(self._model_path, f"{self._model_type}.pkl")
        else:
            pass

        with open(self._path, 'wb') as file:
            pickle.dump(self.MODEL, file)
        pass
    
    def loadModel(self):
        """ loading the model
            this saves times rather than retraing the model every time
        """
        with open(self._path, 'rb') as file:
            self._MODEL = pickle.load(file)
        
        return self._MODEL
    
    def main(self):
        
        roman_numerals = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
                   'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx']
        cardinals = ['nd', 'rd', 'th']
        self.stop_words = nltk.corpus.stopwords.words('english')
        self.stop_words = self.stop_words + list('qwertyuiopasdfghjklzxcvbnm') + roman_numerals + cardinals
        self.wpt = nltk.WordPunctTokenizer()

        folders = FolderIterator(self._folder_path, folder_name=False)

        # collecting the data
        data_list = []
        # creating labels
        labels = []
        for folder in folders.returnCategories():
            data = self.dataCollector(folder, True)
            data_list.append(data)

            labels.extend([os.path.basename(folder)]*len(data))

        Data = []
        for data in data_list:
            Data.extend(list(data.values()))
        
        # normalising the data and encoding the labels
        normalised_data, enc_labels = self.return_X_y(Data, labels)
        
        # fitting the model
        self.modelFitting()

        # training the model
        
        self.modelTraining(normalised_data, enc_labels)

        # saving the model if not already loaded from an external file
        if self.use_saved_model:
            pass
        else:
            self.saveModel()

        # predicting value
        # add later on

        pass

if __name__ == "__main__":
    test_path = '/home/ngoni97/file-manger-with-ml/Test_Data/Saved_Text_Files'

    # start time
    print('process in progress\n')
    start = time.perf_counter()
    test = RUNMODEL(test_path,
                     model_type='MultinomialNB',
                     vectoriser='CountVectorizer',
                      test_size=0.2)
    test_word_1 = 'topology is set theory in higher dimensions'
    test_word_2 = 'machine learning and artificial intelligence'
    test_word_3 = 'solving differential equations using transforms'

    print(test.Predict(test_word_1))
    print(test.Predict(test_word_2))
    print(test.Predict(test_word_3))
    
    # finish time
    finish = time.perf_counter()
    print('\nprocess finished in {:.2f} seconds'.format(finish-start))