#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 04:15:22 2025

@author: ngoni97
"""

# Folder iterator

import os
import timeit

categories = [] # these are the target names for the specific data groups

def ListFolders(parent_path, categories=[]):
    ''' Iterates through directories and returns folder names '''
    for folder in os.listdir(parent_path):
        # if it contains only files then append the folder name
        Path = os.path.join(parent_path, folder)
        if os.path.isdir(Path):
                ListFolders(Path, categories)
        else:
             # base case
             if os.path.isfile(Path):
                 Folder = os.path.basename(os.path.dirname(Path))
                 if Folder in categories:
                     pass
                 else:
                     categories.append(Folder)
                     
    return categories
        

def time_it():
    """ timing it """
    SETUP_CODE = '''
from __main__ import ListFolders
import os
            '''
    TEST_CODE = ''' 
path = "/home/ngoni97/Documents/Documents"
ListFolders(path)
            '''
    print('\n\n' + str(timeit.timeit(setup=SETUP_CODE,
                  stmt=TEST_CODE,
                  number=100)))
    
if __name__ == "__main__":
    Test = ListFolders('/home/ngoni97/Documents/Documents')
    print(Test)
    time_it()
    # an average of 332.9248445080011s time complexity
    
    
# =============================================================================
# ListFolders('/home/ngoni97/Documents/Documents/German') # the base case
# test = ListFolders('/home/ngoni97/Documents/Documents/MATHEMATICS') # the general case
# print(test)
# Test = ListFolders('/home/ngoni97/Documents/Documents')
# print(Test)
# =============================================================================

# =============================================================================
# for subfolders in a folder:
#     then if the subfolder contains other subfolders:
#         iterate the subfolders
#             until the base case is reached:
#                 terminate the iteration
# =============================================================================


# error: it's loading other folders outside the initial directory
# it works it was just a shortcut in the parent directory
# need to fix it to return a big dictionary containing all the information