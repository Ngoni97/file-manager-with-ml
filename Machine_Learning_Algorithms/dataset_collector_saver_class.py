#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 01:36:21 2025

@author: ngoni97
"""
# どうもありがとうございます == Dōmo arigatōgozaimasu

import os
import re
import numpy as np
from collections import OrderedDict
from collections.abc import Iterable

from folder_iterator_class import FolderIterator
from stripping_file_types import fileExtensionStripper

class LoadDataset(object):
    def __init__(self, directory,*,tar_names=None,Type=None,rmChar=False,_dict=False,folder_name=False):
        self.directory = directory
        self._tar_names = tar_names
        self._Type = Type
        self._rmChar = rmChar
        self.__dict = _dict
        self.__folder_name = folder_name
        
        self.target_names = []
        self.dir_path_names = []
        self.Data = {}
        self.Documents, self.Images, self.Music, self.Videos, self.Programming, self.Executable = [],[],[],[],[],[]
        
        self.folder = FolderIterator(self.directory, folder_name=self.__folder_name)
        self.categories = self.folder.returnCategories()
        self.dir_path_names = self.folder.returnDirPathNames()
        
        #print(self.categories, self.dir_path_names, sep='\n\n')
        
        self.data = self.__Dataset(folder_name=self.__folder_name,_dict_=self.__dict)
        self._data = self.SpecificDataset(tar_names=self._tar_names, Type=self._Type, rmChar=self._rmChar)
        #print(self.data)
        #print('\n\ntotal files in Data:', len(Data[0]))

    def __Dataset(self, folder_name,*, _dict_=None):
        """ collects files from a specific directory
            strips the file type
            """
        
        for path in self.dir_path_names:
            Documents, Images, Music, Videos, Programming, Executable = fileExtensionStripper(path)
            
            if self.__folder_name == False:
                if self.__dict == False:
                    self.Data[path] = [Documents, Images, Music, Videos, Programming, Executable]
                elif self.__dict == True:
                    self.Data[path] = {'documents': Documents, 'images': Images, 'music': Music,
                                  'videos': Videos, 'programming': Programming, 
                                  'executable': Executable}
                else:
                    pass
            elif self.__folder_name == True:
                if self.__dict == False:
                    self.Data[os.path.basename(path)] = [Documents, Images, Music, Videos, Programming, Executable]
                elif self.__dict == True:
                    self.Data[os.path.basename(path)] = {'documents': Documents, 'images': Images, 'music': Music,
                                  'videos': Videos, 'programming': Programming, 
                                  'executable': Executable}
                else:
                    pass
            else:
                pass
        #print(self.Data)       
        return self.Data

    def SpecificDataset(self,*,tar_names, Type, rmChar):
        """ takes in the specific targeted category names 
        and returns the data paired with those categories
        """
        # must specify the type of data 
        # either documents, images, or videos, etc., for training
        # as there will be folders with mixed contents
        # which is the sole purpose of the application
        
        # when training: tar_names == subfolders inside the parent selected folder
        # when testing or fully functional in the app: tar_names == limited subfolders
        # also inside the parent selected folder
        
        
        if tar_names == None:
            target_names = self.data.keys()
        else:
            target_names = self._tar_names
        
        if Type == None:
            # return nothing
            pass
        elif Type == 'documents':
            # return documents
            self._documents = {}
            # must take into consideration that if self.__folder_name==False
            # then it saves paths rather than the folder names
            # so must add the function of choosing in the list of full path directories
            
            if self.__folder_name == False:
                Paths = [os.path.basename(file) for file in self.dir_path_names]
                common_prefix = os.path.commonprefix(self.dir_path_names)
                for path in set(target_names).intersection(set(Paths)):
                    if rmChar:
                        Item = [self.remove_characters_before_tokenization(file, True)
                         for file in self.data[os.path.join(common_prefix,path)]['documents']]
                        self.Documents.append(Item)
                        self._documents[path] = {'data':Item,
                                                 'labels': [path]*len(Item)}
                        
                    else:
                        new_path = os.path.join(common_prefix, path)
                        self.Documents.append(self.data[new_path]['documents'])
            else:
                for item in set(target_names).intersection(set(self.categories)):
                        if rmChar:
                            Item = [self.remove_characters_before_tokenization(file, True)
                             for file in self.data[item]['documents']]
                            self.Documents.append(Item)
                            self._documents[item] = {'data':Item,
                                                     'labels': [item]*len(Item)}
                            
                            
                        else:
                            self.Documents.append(self.data[item]['documents'])
                            
            if len(self._tar_names) == 1:
                return self.Documents
            else:
                self._labels = []
                for item in self._documents.keys():
                    self._labels.extend(self._documents[item]['labels'])
                self.combined_documents = [file for file in self.Flatten(self.Documents)]
                self.OrderedDict_ = OrderedDict(zip(self.combined_documents, self._labels)) #self._documents # returns a dictionary
                return self.combined_documents
            pass
        elif self._Type == 'images':
            # return images
            for item in target_names:
                if item in self.categories:
                    self.Images.append(self.data[item]['images'])
            return self.Images
            pass
        elif self._Type == 'music':
            # return music
            for item in target_names:
                if item in self.categories:
                    self.Music.append(self.data[item]['music'])
            return self.Music
            pass
        elif self._Type == 'videos':
            # return programming
            for item in target_names:
                if item in self.categories:
                    self.Videos.append(self.data[item]['videos'])
            return self.Videos
            pass
        elif self._Type == 'programming':
            # return programming
            for item in target_names:
                if item in self.categories:
                    self.Programming.append(self.data[item]['programming'])
            return self.Programming
            pass
        elif self._Type == 'executable':
            # return executable
            for item in target_names:
                if item in self.categories:
                    self.Executable.append(self.data[item]['executable'])
            return self.Executable
            pass

    def remove_characters_before_tokenization(self, sentence,keep_apostrophes=False):
        sentence = (sentence.replace('_', ' ')).replace('-', ' ')
        if keep_apostrophes:
            PATTERN = r'[?|$|&|*|%|@|(|)|~]' # add other characters here to remove them
            pattern = re.compile('[^a-zA-Z]') # remove numbers
            #filtered_sentence = re.sub(PATTERN, r' ', sentence)
            filtered_sentence = re.sub(pattern, r' ', re.sub(PATTERN, r'', sentence))
        else:
            PATTERN = r'[^a-zA-Z0-9]' # only extract alpha-numeric characters
            pattern = re.compile('[^a-zA-Z]') # remove numbers
            filtered_sentence = re.sub(pattern, r' ', re.sub(PATTERN, r'', sentence))
        return filtered_sentence.lower()
    
    def Flatten(self, items, ignore_types=(str, bytes)):
        """ Flattening a Nested Sequence
            converts a nested sequence into a single list whilst preserving the order 
            """
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from self.Flatten(x)
            else:
                yield x
    
    def returnDataset(self):
        """ Returns the dataset """
        return self._data
    
    def returnLabels(self):
        """ Return the corresponding labels for the text documents dataset """
        return self._labels
    
    def returnDataDict(self):
        """ Return the ordered dictionary of the features-labels pair """
        return self.OrderedDict_
    
if __name__ == "__main__":
    
    test_path = '/home/ngoni97/Documents/MATHEMATICS'
    maths_Data = LoadDataset(test_path,
                       tar_names=['ADVANCED', 'ORDINARY AND PARTIAL DIFFERENTIAL EQUATIONS'],
                       Type='documents',
                       rmChar=False,
                       _dict=True,
                       folder_name=False)
    print('Maths:\n', maths_Data.returnDataset())
    print('\n\nMaths dict_keys:\n', maths_Data.returnDataDict().keys())
    print('maths labels:\n', maths_Data.returnLabels())
    
    Test_path = '/home/ngoni97/Documents/PHYSICS'
    physics_Data = LoadDataset(Test_path,
                       tar_names=['ADVANCED'],
                       Type='documents',
                       rmChar=True,
                       _dict=True,
                       folder_name=True)
    print('\n\nPhysics:\n', physics_Data.returnDataset())


# create a function that return a sentence-folder_label pair
# create multiple functions for other files like videos, images, etc.
# as for the documents, am currently using text-classification algorithms

# when running from the application then tar_names will be a collected list of the
# selected folder, it won't be entered manually

# add stop_words remover

# error: folder_name=False is not working
# test if rmChar==False and _dict==False is working