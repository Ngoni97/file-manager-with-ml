#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 00:50:46 2025

@author: ngoni97
"""
# どうもありがとうございます == Dōmo arigatōgozaimasu
# testing multithreading and multiprocessing

# reading the PDFs after colleciing them

import os
import pandas as pd
from collections.abc import Iterable
from threading import Thread
import multiprocessing as mp
import concurrent.futures
import time
import os, pathlib, pymupdf, fitz
import re

from dataset_collector_saver_class import LoadDataset 
from pdf_reader_data_collector_class_2 import PdfDataCollector # change back to  original if it doesn't work
from stripping_file_types import fileExtensionStripper
from folder_iterator_class import FolderIterator
from file_extension_tester import listDirFiles


class DocumentContentDataset():
    def __init__(self, folder,*,
                 specific_file=None,
                 pages=10, clean_text=True, save_as_text_file=False):
        """specific_files refers to pdf, docx, etc. """
        self._folder_path = folder # the parent folder containing the children folders
        self._specific_file = specific_file
        self._pages = pages
        self._clean_text = clean_text
        self._save_as_text_file = save_as_text_file
        
        self.Folder = FolderIterator(self._folder_path, folder_name=False)
        self.subFolders = self.Folder.returnCategories()
        # a list of folder -> files, that is the individual lists are
        # folders which contain files
        self.files = [file for file, *_ in
                      [listDirFiles(folder, size=False, fullpath=True) for folder in self.subFolders]]
        self.returnFiles()

        t1 = time.perf_counter()
        print('document_selector in progress\n')
        self.document_selector(self._folder_path)
        t2 = time.perf_counter()
        print('document_selector finished in {}s\n'.format(round(t2 - t1, 3)))

        t3 = time.perf_counter()
        print("reading pdf's and writing text files in progress\n")
        #self.returnData()
        self.processData()
        t4 = time.perf_counter()
        print("reading and writing finished in {}s\n".format(round(t4 - t3, 3)))


    def document_selector(self, folder_path):
        """ Separates digitally-born pdf's and scanned ones
            
            Returns two separate lists of the digitally-born pdf's and scanned pdf's 
        """
        self.digital_pdf = []
        self.scanned_pdf = []

        folders_collector = FolderIterator(folder_path, folder_name=False)
        folders = folders_collector.returnCategories()

        for folder in folders:
            files = listDirFiles(folder, size=False, fullpath=True)
            #print(files)
            for filename in files[0]:
                with pymupdf.open(filename) as file:
                    for i in range(2, 5):
                        try:
                            test_page = file[i]
                        except Exception:
                            pass
                        else:
                            if test_page:
                                try:
                                    test_get_page_text = test_page.get_text(option='text',
                                                                            clip=pymupdf.INFINITE_RECT())
                                    if test_get_page_text:
                                        if filename not in self.digital_pdf:
                                            self.digital_pdf.append(filename)
                                        else:
                                            pass
                                except Exception:
                                    _test_get_page_text = test_page.get_textpage_ocr(flags=pymupdf.TEXTFLAGS_WORDS,dpi=300,full=True)
                                    if _test_get_page_text:
                                        if filename not in self.scanned_pdf:
                                            self.scanned_pdf.append(filename)
                                        else:
                                            pass
                            else:
                                pass

        return self.digital_pdf, self.scanned_pdf
        
    def Get_Normal_Document(self, filename, pages, save_as_text_file=False):
        """ Returns a text file of the selected document """
        
        self.Text = ""
        self.main_folder_path = os.path.basename(os.path.dirname(os.path.dirname(filename)))
        self.parent_directory = os.path.join('/home/ngoni97/Documents/Documents/File Manager with ML/train_test_text_files', self.main_folder_path)
        
        if not os.path.exists(self.parent_directory):
            os.mkdir(self.parent_directory)
        else:
            pass
        
        self.path = os.path.join(self.parent_directory, os.path.basename(filename))
        if self.path.strip('.pdf'):
            #print('path is a pdf')
            text_file_path = pathlib.Path(self.path.strip('.pdf') + '.txt')
        else:
            #print('path is not a pdf')
            text_file_path = pathlib.Path(self.path + '.txt')
            pass
        
        # detect Tesseract OCR language support folder
        with pymupdf.open(filename) as file: # open a document
                for page in file[5:pages]: # iterate the document pages
                    try:
                        text = page.get_text(option='text',
                                                 clip=pymupdf.INFINITE_RECT())
                        self.Text += text
                    except Exception:
                            text = page.get_textpage_ocr(flags=pymupdf.TEXTFLAGS_WORDS,dpi=300,full=True)
                            self.Text += text.extractTEXT()
                
        if save_as_text_file == True:
            if self.Text != '':
                _Text = self.Text
                with open(text_file_path, 'wb') as text_file: # create a text output
                    text_file.write(_Text.encode('utf8')) # get plain text (is in UTF-8), write text of page
                    text_file.write(bytes((12,))) # write page delimiter (from feed 0x0C)
            else:
                pass
        
    def Get_Scanned_Document(self, filename, pages, save_as_text_file=False):
        """ Returns a text file of the selected document """
        
        self.Text = ""
        self.main_folder_path = os.path.basename(os.path.dirname(os.path.dirname(filename)))
        self.parent_directory = os.path.join('/home/ngoni97/Documents/Documents/File Manager with ML/train_test_text_files', self.main_folder_path)
        
        if not os.path.exists(self.parent_directory):
            os.mkdir(self.parent_directory)
        else:
            pass
        
        self.path = os.path.join(self.parent_directory, os.path.basename(filename))
        if self.path.strip('.pdf'):
            #print('path is a pdf')
            text_file_path = pathlib.Path(self.path.strip('.pdf') + '.txt')
        else:
            #print('path is not a pdf')
            text_file_path = pathlib.Path(self.path + '.txt')
            pass
        
        # detect Tesseract OCR language support folder
        with pymupdf.open(filename) as file: # open a document
                for page in file[5:pages]: # iterate the document pages
                    try:
                        text = page.get_textpage_ocr(flags=pymupdf.TEXTFLAGS_WORDS,dpi=300,full=True)
                    except Exception:
                        pass
                    else:
                        self.Text += text.extractTEXT()

                if self.Text =='':
                   for page in file[5:pages]: # iterate the document pages
                    try:
                        text = page.get_textpage_ocr(dpi=300,full=True)
                    except Exception:
                        pass
                    else:
                        self.Text += text.extractTEXT()
                else:
                    pass
                        
        if save_as_text_file == True:
            _Text = self.Text
            #print('Text type=', type(Text))
            with open(text_file_path, 'wb') as text_file: # create a text output
                text_file.write(_Text.encode('utf8')) # get plain text (is in UTF-8), write text of page
                text_file.write(bytes((12,))) # write page delimiter (from feed 0x0C)
    
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
    
    def run_command_norm_pdf(self, filename):
        return self.Get_Normal_Document(filename, self._pages, self._save_as_text_file)
    
    def run_command_scanned_pdf(self, filename):
        return self.Get_Scanned_Document(filename, self._pages, self._save_as_text_file)
    
    def processData(self):
        """ Returns a dictionary of files (keys) and their respective text (values)"""

        # using another method
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.run_command_norm_pdf, file) for file in self.digital_pdf]
            
            concurrent.futures.wait(results)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.run_command_scanned_pdf, file) for file in self.scanned_pdf]
            
            concurrent.futures.wait(results)
            
            """for result in results:
                print(result.result())"""
            
    """def returnData(self):
        print(self.digital_pdf)
        print('\ndigital_pdf total=', len(self.digital_pdf), '\n\n')
        print(self.scanned_pdf)
        print('\nscanned_pdf total=', len(self.scanned_pdf))
        # digitally-born pdf's
        _process_1 = mp.Process(target=self.processData, args=('norm',))
        # scanned pdf's
        _process_2 = mp.Process(target=self.processData, args=('scan',))
        # start all processes
        _process_1.start()
        _process_2.start()
        # wait till all processes are done
        _process_1.join()
        _process_2.join()
            
        pass"""
        
    def Flatten(self, items, ignore_types=(str, bytes)):
        """ Flattening a Nested Sequence
            converts a nested sequence into a single list whilst preserving the order 
            """
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from self.Flatten(x)
            else:
                yield x
                
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

                
if __name__ == "__main__":
    path_1 = '/home/ngoni97/Documents/Python Programming'
    path_2 = '/home/ngoni97/Documents/PHYSICS'
    Path = '/home/ngoni97/Documents/MATHEMATICS'
    # start
    print('process in progress\n')
    start = time.perf_counter()
    test = DocumentContentDataset(path_1, pages=13, save_as_text_file=True)
   
    #test.returnData()
    # end
    end = time.perf_counter()
    print('process finished\n')
    
    print('time taken for execution = {}s'.format(round(end-start, 3)))

    
# link folder_name the file is found
# with the file_name
# and the file_content

# folder_name -> file_name -> file_content

# at the end the folder_name == classification -> sum total file_content of each file


# error: Get_Scanned_Document is not working properly, it still skips out scanned pdf's
# so, for now I am gonna work with the digitally-born pdf's with the machine learning algorithms
# the problem is that the algorithm works perfectly if fed files one at a time and not as threads
