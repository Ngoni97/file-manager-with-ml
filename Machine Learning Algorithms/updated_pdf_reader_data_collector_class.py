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
from collections.abc import Iterable
import cv2
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from stripping_file_types import fileExtensionStripper

class PdfDataCollector():
    def __init__(self, file_path, pages=None, save_as_text_file=False, *, dpi=300):
        self.file_path = file_path
        self.pages = pages
        self.save_as_text_file = save_as_text_file
        self.dpi = dpi
        
        self.file_name = os.path.basename(self.file_path)
        self.book_dict = {}

        # initialise
        TEXT = self.get_document(self.file_path)
        print("\n\nText =", TEXT)
        
    def remove_characters_before_tokenization(self, sentence,keep_apostrophes=False):
        if not sentence:
            return ""
        # string
        sentence = (sentence.replace('_', ' ')).replace('-', ' ')
        PATTERN = re.compile('[?|$|&|*|%|@|(|)|~]')
        pattern = re.compile('[^a-zA-Z]') if not keep_apostrophes else re.compile('[^a-zA-Z\']')
        replacement = r' '
        
        filtered_sentence = re.sub(pattern, replacement, re.sub(PATTERN, replacement, sentence))
        return '  '.join(filtered_sentence.lower().split())  # Remove extra spaces
    
    def advanced_image_preprocessing(self, image):
        """
        Advanced image preprocessing for better OCR results
        """
        # Convert to grayscale if needed
        if image.mode != 'L':
            image = image.convert('L')
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # 1. Noise reduction
        img_array = cv2.medianBlur(img_array, 3)
        
        # 2. Gaussian blur to smooth
        img_array = cv2.GaussianBlur(img_array, (1, 1), 0)
        
        # 3. Adaptive thresholding for better text separation
        img_array = cv2.adaptiveThreshold(
            img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 4. Morphological operations to clean up
        kernel = np.ones((1, 1), np.uint8)
        img_array = cv2.morphologyEx(img_array, cv2.MORPH_CLOSE, kernel)
        img_array = cv2.morphologyEx(img_array, cv2.MORPH_OPEN, kernel)
        
        # Convert back to PIL Image
        processed_image = Image.fromarray(img_array)
        
        # 5. PIL-specific enhancements
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(processed_image)
        processed_image = enhancer.enhance(1.2)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(processed_image)
        processed_image = enhancer.enhance(1.5)
        
        return processed_image
    
    def convert_pdf_to_images(self, file_path, save_images=False, *, prefix='page', fmt='PNG'):
        destn = '/home/ngoni97/Documents/Documents/File Manager with ML/train_test_text_files/images_test'
        
        if not os.path.exists(destn):
            os.makedirs(destn, exist_ok=True)
        original_images = os.path.join(destn, 'Original Images')
        if not os.path.exists(original_images):
            os.makedirs(original_images, exist_ok=True)
        enhanced_images = os.path.join(destn, 'Enhanced Images')
        if not os.path.exists(enhanced_images):
            os.makedirs(enhanced_images)

        if save_images:
            # original images
            images = convert_from_path(file_path, last_page=self.pages, output_folder=original_images, dpi=self.dpi, fmt=fmt)
    
            for i, img in enumerate(images,1):
                filename = f"{prefix}_{i:04d}.{fmt.lower()}"
                filepath = os.path.join(original_images, filename)
                img.save(filepath, fmt)
                #print(f"Saved: {filepath}")
        else:
            # original images
            images = convert_from_path(file_path, last_page=self.pages, dpi=self.dpi, fmt=fmt)
            print("\nconverted images =", images)

        #Images = {} # enhanced images

        # creating folders corresponding to each book
        saved_images_book_path = os.path.join(enhanced_images, os.path.basename(file_path))
        if not os.path.exists(saved_images_book_path):
            os.makedirs(saved_images_book_path)

        for i, img in enumerate(images,1):
            #Images[f"{prefix}_{i:04d}.{fmt.lower()}"] = self.advanced_image_processing(img)
            Img = self.advanced_image_preprocessing(img)
            file_name = f"{prefix}_{i:04d}.{'PDF'.lower()}"
            file_path = os.path.join(saved_images_book_path, file_name)
            Img.save(file_path, 'PDF')
        
        logger.info(f"Converted {len(images)} pages to PDFs")

        TEXT = self.Read_ocr(saved_images_book_path)

        return TEXT
    
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
    
    def Read_ocr(self, PATH):
        """ Read """
        text = ""
        folder = os.listdir(PATH)
        print("finished loading files\n")
        for page in folder:
            full_path = os.path.join(PATH, page)
            print(f"initialising scanning {full_path}\n")
            #print(full_path)
            with pymupdf.open(full_path) as file:
                try:
                    for pg in file[:1]:
                        text_page = pg.get_textpage_ocr(full=True)
                        print(f"getting text for {full_path}\n")
                        text += text_page.extractTEXT()
                        #print('\npage_{} : {}'.format(idx, remove_characters_before_tokenization(Text)))
                        # Clean up textpage
                        #del text_page
                except Exception as e:
                    logger.error(f"Error reading PDF to text: {e}")
                    #print(f"Error: {e}")
                    pass
        # delete the folder after processed
        #os.rmdir(PATH)
        return self.remove_characters_before_tokenization(text)
    
    def Multithreading(self, file_name):
        """ takes in a folder of files or a single file and uses multithreading to speed up the processing
            if not a single file then it processes the files faster.
        """
        threads = []
        FOLDER = os.listdir(file_name) if not os.path.isfile(file_name) else list(file_name)
        # create threads
        for file in FOLDER:
            thread = Thread(target=self.convert_pdf_to_images, args=(file))
            threads.append(thread)
    
        # start threads
        #start_time = time.perf_counter()
        print("ocr reading process started!\n")
        for thread in threads:
            thread.start()
        # join threads
        for thread in threads:
            thread.join()
            
        print("process finished!\n")
        #finish_time = time.perf_counter()
    
        #print("total time taken = {:.2f}\n".format(finish_time - start_time))

    def get_document(self, filename):
        """ Returns a text file of the selected document"""
        self.Text = ""
        
        # Validate file before processing
        if not os.path.exists(filename):
            return ""
        
        # Setup directory structure
        try:
            # fix this part since it specific to my files tree in my own PC
            self.main_folder_path = os.path.basename(os.path.dirname(os.path.dirname(filename)))
            self.parent_directory = os.path.join(
                '/home/ngoni97/Documents/Documents/File Manager with ML/train_test_text_files', 
                self.main_folder_path
            )
            
            if not os.path.exists(self.parent_directory):
                os.makedirs(self.parent_directory, exist_ok=True)
        except Exception:
            pass
        
        # Create text file path
        base_name = os.path.splitext(os.path.basename(filename))[0]
        text_file_path = os.path.join(self.parent_directory, f"{base_name}.txt")

        digital_pages = 0
        ocr_pages = 0
        doc = None

        try:
            # Open document with explicit error handling
            doc = pymupdf.open(filename)
            if doc is None:
                return ""
            
            doc_length = len(doc)
            if doc_length == 0:
                return ""
            
            pages_to_process = min(self.pages or doc_length, doc_length)
            
            # Test first few pages to determine document type (more conservative)
            test_pages = min(3, doc_length)
            
            for page_num in range(test_pages):
                try:
                    page = doc[page_num]
                    if page is None:
                        continue
                    
                    # Test for digital text first (safer)
                    try:
                        text = page.get_text()
                        if text and text.strip():
                            digital_pages += 1
                            break
                    except Exception:
                        pass
                    
                    # Only test OCR if no digital text found
                    if digital_pages == 0:
                        try:
                            # Use lighter OCR test
                            if hasattr(page, 'get_textpage_ocr'):
                                ocr_pages += 1
                                break
                        except Exception:
                            pass
                            
                except Exception:
                    continue
            
            # Process based on document type
            if digital_pages > 0:
                # Digital PDF processing (safer)
                for page_num in range(pages_to_process):
                    try:
                        page = doc[page_num]
                        if page is None:
                            continue
                        text = page.get_text()
                        if text:
                            self.Text += text
                    except Exception:
                        continue
            
            elif ocr_pages > 0:
                # OCR processing with reduced concurrency
                doc.close()  # Close before OCR to prevent conflicts
                doc = None
                #self.Multithreading(filename)  # Limit OCR pages
                self.Text = self.convert_pdf_to_images(filename)
            
        except Exception as e:
            logger.error(f"Error opening file! {e}")
            pass
        finally:
            # Always close the document
            if doc:
                try:
                    doc.close()
                except:
                    pass

        if self.save_as_text_file and self.Text:
            try:
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(self.Text)
            except Exception:
                pass

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
    FILE_PATH = '/home/ngoni97/Documents/PHYSICS/BIOGRAPHY/newton-opticks-4ed.pdf'
    t_start = time.perf_counter()
    test = PdfDataCollector(FILE_PATH, 13, True, dpi=300)
    #text = test.get_document()
    t_stop = time.perf_counter()
    print("total time = {:.2f}".format(t_stop - t_start))
    #text, clean_text = test.returnText()
    #print(clean_text)
    

    
    

   
# need to delete the existing text file's contents in preparation for storing 
# the next loaded pdf file
# need to change the pathlib directory to the current folder of the application

# use os.path.join(parent_directory, os.path.basename(filename))
# parent_directory here is the File Manager with ML
# and later on will be a database

# create a function to test for whether a file is a digitally-born or ocr scanned pdf
# find a much more efficient method of testing file type
