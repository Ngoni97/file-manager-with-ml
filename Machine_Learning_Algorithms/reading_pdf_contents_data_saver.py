#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 04:01:14 2025

@author: ngoni97
"""

# reading the PDFs after colleciing them

import os
import pandas as pd
from collections.abc import Iterable

from dataset_collector_saver_class import LoadDataset
from pdf_reader_data_collector_class import PdfDataCollector
from stripping_file_types import fileExtensionStripper
from folder_iterator_class import FolderIterator
from file_extension_tester import listDirFiles


class DocumentContentDataset():
    def __init__(self, folder,*,
                 specific_file=None,
                 pages=10, clean_text=True, read_ocr=False, save_as_text_file=False):
        """specific_files refers to pdf, docx, etc. """
        self._folder_path = folder # the parent folder containing the children folders
        self._sepcific_file = specific_file
        self._pages = pages
        self._clean_text = clean_text
        self._read_ocr = read_ocr
        self._save_as_text_file = save_as_text_file
        
        self.Folder = FolderIterator(self._folder_path, folder_name=False)
        self.subFolders = self.Folder.returnCategories()
        # a list of folder -> files, that is the individual lists are
        # folders which contain files
        self.files = [file for file, *_ in
                      [listDirFiles(folder, size=False, fullpath=True) for folder in self.subFolders]]
        
        print(self.files)
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
        self.data = {}
        for file in self.Flatten(self.Data.values()):
            pdf_read = PdfDataCollector(file, self._pages, 
                                        read_ocr=self._read_ocr, 
                                        save_as_text_file=self._save_as_text_file)
            
            text, clean_text = pdf_read.returnText()
            if self._clean_text == True:
                self.data[file] = clean_text
            else:
                self.data[file] = text
                pass
        return self.data
    
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
    path = '/home/ngoni97/Documents/Python Programming'
    test = DocumentContentDataset(path, pages=13, read_ocr=True)
    print(test.returnFiles().values())
    data = test.returnData()
    
# link folder_name the file is found
# with the file_name
# and the file_content

# folder_name -> file_name -> file_content

# at the end the folder_name == classification -> sum total file_content of each file

