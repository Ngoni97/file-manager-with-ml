#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 03:11:09 2025

@author: ngoni97
"""
# どうもありがとうございます == Dōmo arigatōgozaimasu

# documents data collecter and saver

# need to collect the data and save it without the file type end string
# e.g., 'my_file.pdf' should be saved as 'my_file'

import os
import re
from file_extension_tester import listDirFiles

tar_names = []
directory_path_names = []
def TargetNames(parent_path, *, target_names=[], direct):
    ''' collects folder names and use them as target names '''
    tar_names = []
    directory_path_names = []
    # continue iterating until it reaches the last folder that doesn't contain any
    # other folders
    
    ''' Iterates through directories and returns folder names '''
    for folder in os.listdir(parent_path):
        # if it contains only files then append the folder name
        Path = os.path.join(parent_path, folder)
        if os.path.isdir(Path):
                TargetNames(Path)
        else:
             # base case
             if os.path.isfile(Path):
                 Folder = os.path.basename(os.path.dirname(Path))
                 if Folder in tar_names:
                     pass
                 else:
                     tar_names.append(Folder)
                     directory_path_names.append(os.path.dirname(Path))

    return tar_names, directory_path_names

def Dataset(Directory, *, _dict=False, folder_name=False):
    """ collects files from a specific directory
        strips the file type and save it in a list and text-file
        """
    target_names, directory_path_names = TargetNames(Directory)
    Data = {}
    for path in directory_path_names:
        documents, images, music, videos, programming, executable = listDirFiles(path, size=False)
        
        # documents
        Documents = [(file.split('.')[:-1])[0] for file in documents]
        """with open('documents101.txt', 'w') as file:
            for item in Documents:
                file.write(item + '\n')"""
        # images
        Images = [(file.split('.')[:-1])[0] for file in images]
        """with open('images101.txt', 'w') as file:
            for item in Images:
                file.write(item + '\n')"""
        # music
        Music = [(file.split('.')[:-1])[0] for file in music]
        """with open('music101.txt', 'w') as file:
            for item in Music:
                file.write(item + '\n')"""
        #videos
        Videos = [(file.split('.')[:-1])[0] for file in videos]
        """with open('videos101.txt', 'w') as file:
            for item in Videos:
                file.write(item + '\n')"""
        # programming
        Programming = [(file.split('.')[:-1])[0] for file in programming]
        """with open('programming101.txt', 'w') as file:
            for item in programming:
                file.write(item + '\n')"""
        # executable
        Executable = [(file.split('.')[:-1])[0] for file in executable]
        """with open('executable101.txt', 'w') as file:
            for item in Executable:
                file.write(item + '\n')"""
        
        if folder_name == False:
            if _dict == False:
                Data[path] = [Documents, Images, Music, Videos, Programming, Executable]
            elif _dict == True:
                Data[path] = {'documents': Documents, 'images': Images, 'music': Music,
                              'videos': Videos, 'programming': Programming, 
                              'executable': Executable}
            else:
                pass
        elif folder_name == True:
            if _dict == False:
                Data[os.path.basename(path)] = [Documents, Images, Music, Videos, Programming, Executable]
            elif _dict == True:
                Data[os.path.basename(path)] = {'documents': Documents, 'images': Images, 'music': Music,
                              'videos': Videos, 'programming': Programming, 
                              'executable': Executable}
            else:
                pass
        else:
            pass
            
    return Data, target_names

def SpecificDataset(directory, *, tar_names=None, Type=None, rmChar=False):
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
    
    data, categories = Dataset(directory, _dict=True, folder_name=True)
    
    if tar_names == None:
        target_names = data.keys()
    else:
        target_names = tar_names
        
    Documents, Images, Music, Videos, Programming, Executable = [],[],[],[],[],[]
    
    if Type == None:
        # return nothing
        pass
    elif Type == 'documents':
        # return documents
        for item in set(target_names).intersection(set(categories)):
                if rmChar:
                    Documents.append(
                        [remove_characters_before_tokenization(file, True)
                         for file in data[item]['documents']])
                else:
                    Documents.append(data[item]['documents'])
        return Documents
        pass
    elif Type == 'images':
        # return images
        for item in target_names:
            if item in categories:
                Images.append(data[item]['images'])
        return Images
        pass
    elif Type == 'music':
        # return music
        for item in target_names:
            if item in categories:
                Music.append(data[item]['music'])
        return Music
        pass
    elif Type == 'videos':
        # return programming
        for item in target_names:
            if item in categories:
                Videos.append(data[item]['videos'])
        return Videos
        pass
    elif Type == 'programming':
        # return programming
        for item in target_names:
            if item in categories:
                Programming.append(data[item]['programming'])
        return Programming
        pass
    elif Type == 'executable':
        # return executable
        for item in target_names:
            if item in categories:
                Executable.append(data[item]['executable'])
        return Executable
        pass

def remove_characters_before_tokenization(sentence,keep_apostrophes=False):
    sentence = (sentence.replace('_', ' ')).replace('-', ' ')
    if keep_apostrophes:
        PATTERN = r'[?|$|&|*|%|@|(|)|~]' # add other characters here to remove them
        filtered_sentence = re.sub(PATTERN, r'', sentence)
    else:
        PATTERN = r'[^a-zA-Z0-9 ]' # only extract alpha-numeric characters
        filtered_sentence = re.sub(PATTERN, r'', sentence)
    return filtered_sentence.lower()

if __name__ == "__main__":
    print(""" this is a module run directly\n\n""")
    
# =============================================================================
#     path = '/home/ngoni97/Downloads/Downloads'
# 
#     Data, target_names = Dataset(path, _dict=True, folder_name=True)
#     #print(Data)
#     print(target_names)
# =============================================================================
    
    test_path_1 = '/home/ngoni97/Documents/MATHEMATICS'
    test_path_2 = '/home/ngoni97/Documents/PHYSICS'
    documents = SpecificDataset(test_path_2,
                                tar_names=['ADVANCED'],
                                Type='documents', rmChar=True)
    print(documents)
# =============================================================================
#     '''/home/ngoni97/Downloads/Downloads'''
#     target_names, directory_path_names = TargetNames(
#         '/home/ngoni97/Documents/Documents/MATHEMATICS')
#     print(target_names)
#     print('\n\n', directory_path_names)
# =============================================================================

# later on add the functionality of leaving out files that are 90-100% numerical
# as they polute the dataset which is fed into a text_classifier ml-algorithm

# must collect folder names and use them as categories and encode them into numbers
# then collect all the files in the respective folders for training the algorithm
# need to shuffle the contents in the respective folders to better train the text-classification
# ml-algorithm

# create a function that selects specific data depending on the specified target_names


# The following code snippet shows how to remove special characters before tokenization:
# =============================================================================
# import re
# def remove_characters_before_tokenization(sentence,keep_apostrophes=False):
#     sentence = sentence.strip()
#     if keep_apostrophes:
#         PATTERN = r'[?|$|&|*|%|@|(|)|~|_]' # add other characters here to remove them
#         filtered_sentence = re.sub(PATTERN, r'', sentence)
#     else:
#         PATTERN = r'[^a-zA-Z0-9 ]' # only extract alpha-numeric characters
#         filtered_sentence = re.sub(PATTERN, r'', sentence)
#     return filtered_sentence
# =============================================================================
# ERROR: it's recalling previously loaded data
# like if you run the function multiple times it will continue appending new data from
# different directories