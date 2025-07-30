#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 03:13:36 2025

@author: ngoni97
"""
# どうもありがとうございます == Dōmo arigatōgozaimasu

import os
import timeit
import numpy as np

class FolderIterator():
    def __init__(self, directory, *, folder_name=True):
        self._directory = directory
        self._folder_name = folder_name
    
        # initialise with an empty list when creating a new class instance
        self.categories = []
        self.directory_path_names = []
        
        self.ListFolders(self._directory, self.categories, self.directory_path_names)
        
    def ListFolders(self, parent_path, categories=[], directory_path_names=[]):
        ''' Iterates through directories and returns folder names '''
        
        for folder in os.listdir(parent_path):
            # if it contains only files then append the folder name
            Path = os.path.join(parent_path, folder)
            if os.path.isdir(Path):
                    self.ListFolders(Path, self.categories, self.directory_path_names)
            else:
                 # base case
                 if os.path.isfile(Path):
                     Folder = os.path.basename(os.path.dirname(Path))
                     if Folder in self.categories:
                         pass
                     else:
                         self.categories.append(Folder)
                         self.directory_path_names.append(os.path.dirname(Path))
        
              
        return self.categories, self.directory_path_names
    
    def returnCategories(self):
        """ Return folder names as categories """
        if self._folder_name == True:
            return self.categories
        else:
            return self.directory_path_names
        
    def returnDirPathNames(self):
        """ return folder directory full path names"""
        return self.directory_path_names


def time_it():
    """ timing it """
    SETUP_CODE = '''
from __main__ import FolderIterator
import os
            '''
    TEST_CODE = ''' 
path = "/home/ngoni97/Documents/MATHEMATICS"
FolderIterator(path)
            '''
    print('\n\n' + str(timeit.timeit(setup=SETUP_CODE,
                  stmt=TEST_CODE,
                  number=100)))
    
if __name__ == "__main__":
    
    Test = FolderIterator('/home/ngoni97/Documents/MATHEMATICS', folder_name=False)
    print('\n\nMaths:\n',Test.returnCategories())
    #time_it()
    test = FolderIterator('/home/ngoni97/Documents/PHYSICS')
    print('\n\nPhysics:\n',test.returnCategories())
# =============================================================================
# path = '/home/ngoni97/Documents/MATHEMATICS'
# test = FolderIterator(path)
# =============================================================================
