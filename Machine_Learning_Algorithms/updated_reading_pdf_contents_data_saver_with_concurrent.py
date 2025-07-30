#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updated on Tue Jul  8 00:37:18 2025

@author: ngoni97
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 00:50:46 2025

@author: ngoni97
"""
# どうもありがとうございます == Dōmo arigatōgozaimasu
# using multithreading

# reading the PDFs after colleciing them

import os
from collections.abc import Iterable
from threading import Lock
import concurrent.futures
import time
import os
 
from fixed_pdf_collector import PdfDataCollector
from folder_iterator_class import FolderIterator
from file_extension_tester import listDirFiles

class DocumentContentDataset():
    """ A class that takes in a folder and reads the pdf files inside
        concurrently and returns text files 
    """

    def __init__(self, folder,*, specific_file,
                 pages=10, normalise=False, save_as_text_file=False):
        
        self._folder_path = folder # the parent folder containing the children folders
        self.specific_file = specific_file # specific_files refers to pdf, docx, etc. 
        self._pages = pages
        self.normalise = normalise
        self._save_as_text_file = save_as_text_file
        self.lock = Lock()
        
        self.Folder = FolderIterator(self._folder_path, folder_name=False)
        self.subFolders = self.Folder.returnCategories()

        self.files = [file for file, *_ in
                      [listDirFiles(folder, size=False, fullpath=True) for folder in self.subFolders]]
        
        self.returnFiles()
        # start the process
        self.processData()

    def start_process(self, file):
        """
        Initialises the data collector saver,
        which collects pdf files data and then saves it as a text file

        Parameters
        ----------
        file : pdf file path
            can be entered as a directory or file name

        Returns
        -------
        text file
            that has been filtered and is saved locally in the default directory

        """
        self.process = PdfDataCollector(file, self._pages, self._save_as_text_file, normalise=self.normalise)

        return self.process
    
    def processData(self):
        """ Returns a dictionary of files (keys) and their respective text (values)"""

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.start_process, file) for file in list(self.Flatten(self.files))]
            
            concurrent.futures.wait(results)
            with self.lock:
                for result_ in results:
                    result_.result()
                    time.sleep(0.5)

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
    path_1 = '/home/ngoni97/Documents/Python Programming'
    path_2 = '/home/ngoni97/Documents/PHYSICS'
    path_3 = '/home/ngoni97/Documents/MATHEMATICS'
   
    test = DocumentContentDataset(path_3, pages=13, save_as_text_file=True)
