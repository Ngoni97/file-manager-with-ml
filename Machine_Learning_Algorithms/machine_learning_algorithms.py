#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 04:45:47 2025

@author: ngoni97
"""

import os
import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from joblib import dump, load
import pickle
import time

# loading machine learning modules
import sklearn
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import LinearSVC

from dataset_collector_saver_class import LoadDataset
from folder_iterator_class import FolderIterator


class RUNMODEL():
    def __init__(self, folder_path,*, model_type=None,
                  use_saved_model=False, vectoriser='CountVectorizer',
                  test_size=0.3, random_state=42):
        self._folder_path = folder_path
        self.use_saved_model = use_saved_model
        self._model_path = '/home/ngoni97/Documents/Documents/File Manager with ML'
        # change this later to save models in a database
        self._vectoriser = vectoriser
        self._model_type = model_type
        self.test_size = test_size
        self.random_state = random_state
        
        # run main
        self.main()
        
    def remove_characters_before_tokenization(self, sentence,keep_apostrophes=False):
        # string
        sentence = (sentence.replace('_', ' ')).replace('-', ' ')
        # bytes
        #b_sentence = (sentence.replace(b'_', b' ')).replace(b'-', b' ')
            
        # string
        PATTERN = re.compile('[?|$|&|*|%|@|(|)|~]') # add other characters here to remove them
        pattern = re.compile('[^a-zA-Z]') # remove numbers
        replacement = r' '
        # bytes
        b_PATTERN = re.compile(b'[?|$|&|*|%|@|(|)|~]') # add other characters here to remove them
        b_pattern = re.compile(b'[^a-zA-Z]') # remove numbers
        b_replacement = re.compile(b' ')
            
        if keep_apostrophes:
            filtered_sentence = re.sub(pattern, replacement, re.sub(PATTERN, replacement, sentence))
        else:
            filtered_sentence = re.sub(pattern, replacement, re.sub(PATTERN, replacement, sentence))
        return filtered_sentence.lower()
    
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

    def modelPredicting(self, X_test, y_test):
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
            self._path = os.path.join(self._model_path, str(self._model_type) + '.pkl')
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
        #print('loaded folders =\n', folders)
        # collecting the data
        data_list = []
        # creating labels
        labels = []
        for folder in folders.returnCategories():
            data = self.dataCollector(folder, True)
            data_list.append(data)

            labels.extend([os.path.basename(folder)]*len(data))
        #print('labels =\n', labels)
        #print('\nlength of labels =\n', len(labels))
        Data = []
        for data in data_list:
            Data.extend(list(data.values()))
        #print('Data =\n', Data)
        #print('\nlength of Data =', len(Data))
        #print('Data type =', type(Data), '\n')
        # normalising the data and encoding the labels
        normalised_data, enc_labels = self.return_X_y(Data, labels)
        
        # fitting the model
        self.modelFitting()

        # training the model
        #print('normalised_data type =', type(normalised_data))
        #print('enc_labels =\n', enc_labels)
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
    test_path = '/home/ngoni97/Documents/Documents/File Manager with ML/train_test_text_files'

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