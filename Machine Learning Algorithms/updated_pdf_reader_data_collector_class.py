#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 21:58:40 2025

@author: ngoni97
"""

# a class for reading the contents pages of pdf files
# aids in the data collection for training the ml-classification algorithms
import os, re
import pymupdf, fitz
import pathlib
from threading import Thread
import concurrent.futures
import time

from stripping_file_types import fileExtensionStripper

class PdfDataCollector():
    def __init__(self, file_path, pages=None, save_as_text_file=False):
        self.file_path = file_path
        self.pages = pages
        self.save_as_text_file = save_as_text_file
        
        self.file_name = os.path.basename(self.file_path)
        self.book_dict = {}
        
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
    
    def read_ocr(self, page_num, book_path):
        __text = ""
        with pymupdf.open(book_path) as file:
            page = file[page_num]
            try:
                __Text = page.get_textpage_ocr(dpi=250, full=True)
            except Exception:
                pass
            else:
                __text += __Text.extractTEXT()
    
        # saving the information in a dictionary
        self.book_dict[page_num] = __text
        
        return __text
    
    def Multithreading(self, page_numbers, file_name):
        
        threads = []
    
        # create threads
        for page_num in range(page_numbers):
            thread = Thread(target=self.read_ocr, args=(page_num, file_name))
            threads.append(thread)
    
        # start threads
        #start_time = time.perf_counter()
        print("ocr reading process started!\n")
        for thread in threads:
            thread.start()
        # join threads
        for thread in threads:
            thread.join()
    
        text = ""
        for key in sorted(self.book_dict.keys()):
            text += self.book_dict[key]
            
        self.Text = text
            
        print("process finished!\n")
        #finish_time = time.perf_counter()
    
        #print("total time taken = {:.2f}\n".format(finish_time - start_time))

    def get_document(self, filename):
        """ Returns a text file of the selected document"""
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
        
        self.count = 0
        self.Count = 0
        # detect Tesseract OCR language support folder
        with pymupdf.open(filename) as file: # open a document, change fitz or pymupdf
            for item in file[1:5]:
                try:
                    if item.get_text():
                        self.count += 1
                        break
                    elif item.get_textpage_ocr():
                        self.Count += 1
                        break
                except Exception:
                    pass
                           
            if self.count != 0:
                #print('using digitally-born pdf methods on {}\n'.format(os.path.basename(filename)))
                for page in file[:self.pages]: # iterate the document pages
                    try:
                        text = page.get_text()
                    except Exception:
                        pass
                    else:
                        self.Text += text
            else:
                pass
            
        if self.Count != 0:
                self.Multithreading(self.pages, filename)
        else:
            pass

        if self.save_as_text_file == True:
            Text = self.Text
            #print('Text type=', type(Text))
            with open(text_file_path, 'wb') as text_file: # create a text output
                text_file.write(Text.encode('utf8')) # get plain text (is in UTF-8), write text of page
                text_file.write(bytes((12,))) # write page delimiter (from feed 0x0C)
    
            #with open(text_file_path, 'rb') as file:
                #File = file.read()
                #return File
        #print('\nself.Text type=', type(self.Text))
        return self.Text
    
    def returnText(self):
        """ Returns the text of the document"""
        self._text = self.get_document(self.file_path) # a string
        self.__text = self.remove_characters_before_tokenization(self._text)
        return self._text, self.__text
        
    def get_bookmarks(self, filepath):
        """ Returns bookmarks if any else None"""
        self.bookmarks = {}
        with fitz.open(filepath) as file:
            toc = file.get_toc()
            for level, title, page in toc:
                self.bookmarks[page] = title
        return self.bookmarks
    
    def returnBookmarks(self, file_path):
        """ return a dictionary of the bookmarks else empty """
        
        return self.bookmarks

if __name__ == "__main__":
    #file_path = '/home/ngoni97/Documents/Python Programming/Machine Learning/2-Aurélien-Géron-Hands-On-Machine-Learning-with-Scikit-Learn-Keras-and-Tenso.pdf'
    #file_path = '/home/ngoni97/Documents/PHYSICS/ADVANCED/Fluid Mechanics__An Introduction to the Theory of Fluid Flows.pdf'
    file_path = '/home/ngoni97/Documents/PHYSICS/ADVANCED/physics-for-scientists-and-engineers-with-modern-physics-serwayjewett.pdf'
    File_path = '/home/ngoni97/Documents/MATHEMATICS/Principia Mathematica/Principia_Mathematica [volume.I] alfred_north_whitehead x betrand_russell.pdf'
    t_start = time.perf_counter()
    test = PdfDataCollector(File_path, 13, True)
    text = test.returnText()
    t_stop = time.perf_counter()
    print("total time = {:.2f}".format(t_stop - t_start))
    text, clean_text = test.returnText()
    print(clean_text)
    

    
    

   
# need to delete the existing text file's contents in preparation for storing 
# the next loaded pdf file
# need to change the pathlib directory to the current folder of the application

# use os.path.join(parent_directory, os.path.basename(filename))
# parent_directory here is the File Manager with ML
# and later on will be a database

# create a function to test for whether a file is a digitally-born or ocr scanned pdf
# find a much more efficient method of testing file type
