#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 04:01:14 2025

@author: ngoni97
"""

# reading the PDFs after colleciing them

import os
from collections.abc import Iterable

from updated_pdf_reader_data_collector_class import PdfDataCollector
from folder_iterator_class import FolderIterator
from file_extension_tester import listDirFiles


class DocumentContentDataset():
    def __init__(self, folder,*,
                 specific_file=None,
                 pages=10, save_as_text_file=False, normalise=False, dpi=300):
        """specific_files refers to pdf, docx, etc. """
        self._folder_path = folder # the parent folder containing the children folders
        self._sepcific_file = specific_file
        self._pages = pages
        self._save_as_text_file = save_as_text_file
        self.normalise = normalise
        self.dpi = dpi
        
        self.Folder = FolderIterator(self._folder_path, folder_name=False)
        self.subFolders = self.Folder.returnCategories()
        # a list of folder -> files, that is the individual lists are
        # folders which contain files
        self.files = [file for file, *_ in
                      [listDirFiles(folder, size=False, fullpath=True) for folder in self.subFolders]]
        
        #print(self.files)

    def returnFiles(self):
        """ Returns a dictionary where the keys are the folder paths
            and the values corresponding to each key are the files (full path) contained
            in the respective folders
        """
        self.Data = {}
        for folders in self.files:
            folder_path_name = os.path.commonprefix(folders)
            self.Data[folder_path_name] = folders
        
        return self.Data
    
    def returnData(self):
        """ Returns a dictionary of files (keys) and their respective text (values)"""
        for file in self.Flatten(self.Data.values()):
            pdf_read = PdfDataCollector(file, self._pages, 
                                        save_as_text_file=self._save_as_text_file,
                                        normalise=self.normalise, dpi=self.dpi)
    
    def Flatten(self, items, ignore_types=(str, bytes)):
        """ Flattening a Nested Sequence
            converts a nested sequence into a single list whilst preserving the order 
            """
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from self.Flatten(x)
            else:
                yield x

if __name__ == "__main__":
    PATH = '/home/ngoni97/Documents/Python Programming'
    test = DocumentContentDataset(PATH, pages=13, save_as_text_file=True, normalise=True)
    print(test.returnFiles().values())
    
    
# link folder_name the file is found
# with the file_name
# and the file_content

# folder_name -> file_name -> file_content

# at the end the folder_name == classification -> sum total file_content of each file

