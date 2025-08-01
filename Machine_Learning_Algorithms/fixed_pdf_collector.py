#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 21:58:40 2025

@author: ngoni97
"""
# どうもありがとうございます == Dōmo arigatōgozaimasu

# a class for reading the contents pages of pdf files
# aids in the data collection for training the ml-classification algorithms
import os, re
import pymupdf
import nltk
from threading import Thread, Lock
import time
import cv2
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PdfDataCollector():
    """
    A class that takes in a pdf file and reads the text
    and saves it as a text file
    """
    def __init__(self, file_path, pages=None, save_as_text_file=False, normalise=False, *, dpi=300, save_images=False):
        self.file_path = file_path
        self.pages = pages
        self.save_as_text_file = save_as_text_file
        self.normalise = normalise
        self.dpi = dpi
        self.save_images = save_images
        
        self.file_name = os.path.basename(self.file_path)
        self.book_dict = {}
        # Thread safe locking
        self.lock = Lock()

        # initialise
        TEXT = self.get_document(self.file_path)
        
    def remove_characters_before_tokenization(self, sentence,keep_apostrophes=False):
        """ remove characters and keeps words only"""
        if not sentence:
            return ""
        # string
        sentence = (sentence.replace('_', ' ')).replace('-', ' ')
        PATTERN = re.compile('[?|$|&|*|%|@|(|)|~]')
        pattern = re.compile('[^a-zA-Z]') if not keep_apostrophes else re.compile('[^a-zA-Z\']')
        replacement = r' '
        
        filtered_sentence = re.sub(pattern, replacement, re.sub(PATTERN, replacement, sentence))
        return ' '.join(filtered_sentence.lower().split())  # Remove extra spaces

    def normalize_document(self, doc):
        """ tokenize and remove stopwords """
        # stopwords
        roman_numerals = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
                   'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx']
        cardinals = ['nd', 'rd', 'th']
        self.stop_words = nltk.corpus.stopwords.words('english')
        self.stop_words = self.stop_words + list('qwertyuiopasdfghjklzxcvbnm') + roman_numerals + cardinals
        self.wpt = nltk.WordPunctTokenizer()

        # lower case and remove special characters\whitespaces
        doc = re.sub(r'[^a-zA-Z0-9\s]', '', doc, re.I)
        doc = doc.lower()
        doc = doc.strip()
        # tokenize document
        tokens = self.wpt.tokenize(doc)
        # filter stopwords out of document
        filtered_tokens = [token for token in tokens if token not in self.stop_words]
        # re-create document from filtered tokens
        doc = ' '.join(filtered_tokens)
        return doc

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
        """ converts a single book into a series of single PDFs as per page, saves it in the respective folder
            then processes those pages
        """
        destn = '/home/ngoni97/file-manger-with-ml/Test_Data'
        # initialise directories
        if not os.path.exists(destn):
            os.makedirs(destn, exist_ok=True)

        enhanced_images = os.path.join(destn, 'Enhanced_Images')
        if not os.path.exists(enhanced_images):
            os.makedirs(enhanced_images)

        # original images
        images = convert_from_path(file_path, last_page=self.pages, dpi=self.dpi, fmt=fmt)

        # creating folders corresponding to each book
        saved_images_book_path = os.path.join(enhanced_images, os.path.basename(file_path))
        if not os.path.exists(saved_images_book_path):
            os.makedirs(saved_images_book_path)

        for i, img in enumerate(images,1):
            Img = self.advanced_image_preprocessing(img)
            file_name = f"{prefix}_{i:04d}.{'PDF'.lower()}"
            file_path = os.path.join(saved_images_book_path, file_name)
            Img.save(file_path, 'PDF')
        
        logger.info(f"Converted {len(images)} pages to PDFs")

        TEXT = self.Multithreading(saved_images_book_path)

        return self.normalize_document(TEXT) if self.normalise else TEXT
    
    def Read_ocr(self, FULL_PATH):
        """ Read OCR scanned documents """
        text = ""
        page = os.path.basename(FULL_PATH).strip('.pdf').strip('page_')
        with pymupdf.open(FULL_PATH) as file:
            try:
                for pg in file[:1]:
                    try:
                        text_page = pg.get_textpage_ocr(full=True)
                        text += text_page.extractTEXT()
                    except Exception as e:
                        logger.error(f"pymupdf error: {e}")
                        pass
                    else:
                        self.book_dict[page] = self.remove_characters_before_tokenization(text)
            except Exception as e:
                    logger.error(f"Reading OCR PDF to text error: {e}")
                    pass
    
    def Multithreading(self, PATH):
        """ takes in a folder of files and uses multithreading to speed up the processing """
        threads = []
        FOLDER = os.listdir(PATH)

        # create threads
        for file in FOLDER:
            path = os.path.join(PATH, file)
            thread = Thread(target=self.Read_ocr, args=(path,))
            threads.append(thread)

        with self.lock:
            for thread in threads:
                thread.start()
                time.sleep(1)
            # join threads
            for thread in threads:
                thread.join()
                time.sleep(0.5)
        
        Text = ""
        for page in sorted(self.book_dict):
            Text += self.book_dict[page]

        # delete the folder when done
        if not self.save_images:
            for file in os.listdir(PATH):
                os.remove(os.path.join(PATH, file)) # first remove the files
            os.rmdir(PATH) # then finally remove the parent directory

        return Text

    def is_text_extractable(self, page):
        """
        Test if a page has extractable text without triggering OCR initialization
        """
        try:
            # Get text using standard method first
            text = page.get_text()
            if text and len(text.strip()) > 50:  # Arbitrary threshold for meaningful text
                return True
            
            # Check for text blocks/fonts as an indicator of digital text
            text_dict = page.get_text("dict")
            if text_dict and "blocks" in text_dict:
                for block in text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            if "spans" in line:
                                for span in line["spans"]:
                                    if span.get("text", "").strip():
                                        return True
            
            return False
        except Exception:
            return False

    def has_images_or_drawings(self, page):
        """
        Check if page has images or drawings that might need OCR
        """
        try:
            # Check for images
            image_list = page.get_images()
            if image_list:
                return True
            
            # Check for drawings/paths
            drawings = page.get_drawings()
            if drawings:
                return True
            
            return False
        except Exception:
            return False

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
                '/home/ngoni97/file-manger-with-ml/Test_Data/Saved_Text_Files', 
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
            
            # Test first few pages to determine document type
            test_pages = min(5, doc_length)
            
            for page_num in range(test_pages):
                try:
                    page = doc[page_num]
                    if page is None:
                        continue
                    
                    # Test for digital text first (safer approach)
                    if self.is_text_extractable(page):
                        digital_pages += 1
                    elif self.has_images_or_drawings(page):
                        # Only count as OCR if there are images/drawings but no extractable text
                        ocr_pages += 1
                            
                except Exception as e:
                    logger.error(f"Error testing page {page_num}: {e}")
                    continue
            
            logger.info(f"Document analysis: {digital_pages} digital pages, {ocr_pages} OCR pages")
            
            # Process based on document type
            if digital_pages > 0:
                # Digital PDF processing (safer)
                logger.info(f"Processing digitally-born pdf: {os.path.basename(filename)}")
                for page_num in range(pages_to_process):
                    try:
                        page = doc[page_num]
                        if page is None:
                            continue
                        text = page.get_text()
                        if text:
                            self.Text += text
                    except Exception as e:
                        logger.error(f"Error extracting text from page {page_num}: {e}")
                        continue
            
            elif ocr_pages > 0:
                # OCR processing with reduced concurrency
                logger.info(f"Processing OCR scanned pdf: {os.path.basename(filename)}")
                doc.close()  # Close before OCR to prevent conflicts
                doc = None
                self.Text = self.convert_pdf_to_images(filename)
            
            else:
                # Fallback: try to extract any available text
                logger.warning(f"No clear document type detected for {filename}, attempting text extraction")
                for page_num in range(pages_to_process):
                    try:
                        page = doc[page_num]
                        if page is None:
                            continue
                        text = page.get_text()
                        if text and text.strip():
                            self.Text += text
                    except Exception as e:
                        logger.error(f"Error in fallback text extraction from page {page_num}: {e}")
                        continue
                
                # If still no text, try OCR as last resort
                if not self.Text.strip():
                    logger.info("No text found, falling back to OCR processing")
                    if doc:
                        doc.close()
                        doc = None
                    self.Text = self.convert_pdf_to_images(filename)
            
        except Exception as e:
            logger.error(f"Error opening file {filename}: {e}")
            return ""
        finally:
            # Always close the document
            if doc:
                try:
                    doc.close()
                except Exception as e:
                    logger.error(f"Error closing document: {e}")

        if self.save_as_text_file and self.Text:
            try:
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    if self.normalise:
                        text_file.write(self.remove_characters_before_tokenization(self.normalize_document(self.Text)))
                    else:
                        text_file.write(self.remove_characters_before_tokenization(self.Text))
            except Exception as e:
                logger.error(f"Error saving text file: {e}")

        result = (self.remove_characters_before_tokenization(self.normalize_document(self.Text))
                   if self.normalise else self.remove_characters_before_tokenization(self.Text))

        return result
    
if __name__ == "__main__":

    FILE_PATH = '/home/ngoni97/Documents/MATHEMATICS/Principia Mathematica/Principia_Mathematica [volume.I] alfred_north_whitehead x betrand_russell.pdf'
    
    test = PdfDataCollector(FILE_PATH, 13, True, True, dpi=300, save_images=True)
