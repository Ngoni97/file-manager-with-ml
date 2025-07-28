#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 20:30:09 2025

@author: ngoni97
"""

# opening pdf files using PyPDF2

import PyPDF2
import os

class OpeningPdf():
    def __init__(self, filename, pagenumber):
        self.filename = filename
        self.pg_number = pagenumber
        
    
        Page, page_text = self.__open_page(self.file_path, self.pages)
        print(Page)
        self.__open_pages(self.file_path, self.pages)

    def __open_page(self, filename, pagenumber):
        """ Private method
            Opening the pdf file single page"""
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            Text = ""

            # reading the contents of the first page
            if pagenumber != None:
                page = reader.pages[pagenumber]
                text = page.extract_text()
                Text += text
                
                with open('saved_page.txt', 'w', encoding='utf-8') as text_file:
                    text_file.write(Text)
            else:
                pass

        return text, Text
    
    def __open_pages(self, filename, max_pages=None):
        """ Private method
            Opening the pdf file maximum number of selected pages"""
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            # total number of pages
            total_pages = len(reader.pages)

            # reading the contents of the selected pages
            if max_pages == None:
                max_pages = total_pages
            else:
                max_pages = max_pages
             
            Text = ""
            for page in reader.pages[:max_pages]:
                text = page.extract_text()
                Text += text + '\n'
            if os.path.exists('saved_pages.txt'):
                # if the file already exists then append new pages
                with open('saved_pages.txt', 'a+', encoding='utf-8') as text_file:
                    text_file.write(Text +'\n')
            else:
                # create a new file
                with open('saved_pages.txt', 'w+', encoding='utf-8') as text_file:
                    text_file.write(Text + '\n')
    