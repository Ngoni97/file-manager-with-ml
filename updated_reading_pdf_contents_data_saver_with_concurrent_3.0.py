#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 00:14:06 2025

@author: ngoni97
"""

import os
import re
import pymupdf
import pathlib
from threading import Thread, Lock
import concurrent.futures
import time
from collections.abc import Iterable
import cv2
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import matplotlib.pyplot as plt

# Import your other modules (assuming they exist)
# from stripping_file_types import fileExtensionStripper
# from folder_iterator_class import FolderIterator
# from file_extension_tester import listDirFiles

class PdfDataCollector:
    def __init__(self, file_path, pages=None, save_as_text_file=False):
        self.file_path = file_path
        self.pages = pages
        self.save_as_text_file = save_as_text_file
        
        self.file_name = os.path.basename(self.file_path)
        self.book_dict = {}
        self.lock = Lock()  # Thread safety for book_dict
        
        # Validate file exists and is accessible
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"Cannot read file: {file_path}")
        
    def remove_characters_before_tokenization(self, sentence, keep_apostrophes=False):
        """Clean text by removing unwanted characters"""
        sentence = (sentence.replace('_', ' ')).replace('-', ' ')
        
        PATTERN = re.compile('[?|$|&|*|%|@|(|)|~]')
        pattern = re.compile('[^a-zA-Z]') if not keep_apostrophes else re.compile('[^a-zA-Z\']')
        replacement = r' '
        
        filtered_sentence = re.sub(pattern, replacement, re.sub(PATTERN, replacement, sentence))
        return filtered_sentence.lower()
    
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
    
    def convert_pdf_to_images(self, file_path, save_images=False, prefix='page', fmt='PNG'):
        destn = '/home/ngoni97/Documents/Documents/File Manager with ML/train_test_text_files/images_test'
        if save_images:
            if not os.path.exists(destn):
                os.makedirs(destn, exist_ok=True)
            original_images = os.path.join(destn, 'Original Images')
            if not os.path.exists(original_images):
                os.makedirs(original_images, exist_ok=True)
            self.enhanced_images = os.path.join(destn, 'Enhanced Images')
            if not os.path.exists(self.enhanced_images):
                os.makedirs(self.enhanced_images)
            
            images = convert_from_path(file_path, last_page=10, dpi=300, output_folder=original_images, fmt='png')
    
            for i, img in enumerate(images,1):
                filename = f"{prefix}_{i:04d}.{fmt.lower()}"
                filepath = os.path.join(original_images, filename)
                img.save(filepath, fmt)
                print(f"Saved: {filepath}")
        else:
            images = convert_from_path(file_path, last_page=10, dpi=300, fmt=fmt)

        # saving enhanced versions
        Images = []
        for image in images:
            enhanced_image = self.advanced_image_preprocessing(image)
            Images.append(enhanced_image)
    
        for i, enhanced_image in enumerate(Images, 1):
            file_name = f"{prefix}_{i:04d}.{fmt.lower()}"
            file_path = os.path.join(self.enhanced_images, file_name)
            enhanced_image.save(file_path, fmt)
            print(f"Saved as pdf: {file_path}")   
            
    def read_ocr(self, page_num, book_path):
        """Read OCR text from a specific page - thread-safe version"""
        __text = ""
        doc = None
        try:
            # Open document with error checking
            doc = pymupdf.open(book_path)
            if doc is None:
                return ""
            
            if page_num >= len(doc):
                return ""
                
            page = doc[page_num]
            if page is None:
                return ""
            
            try:
                text_page = page.get_textpage_ocr(dpi=150, full=True)  # Reduced DPI for stability
                if text_page:
                    __text = text_page.extractTEXT()
                    # Clean up textpage
                    del text_page
            except Exception:
                pass
                
        except Exception:
            pass
        finally:
            # Always close the document
            if doc:
                try:
                    doc.close()
                except:
                    pass
        
        # Thread-safe dictionary update
        with self.lock:
            self.book_dict[page_num] = __text
        
        return __text
    
    def read_pdf(self, folder):
        pass
    
    def multithreading_ocr(self, page_numbers, file_name):
        """Multi-threaded OCR processing with proper error handling"""
        # Limit concurrent threads to prevent segfaults
        max_concurrent = min(2, page_numbers)  # Very conservative limit
        
        # Process in batches to avoid overwhelming system
        batch_size = max_concurrent
        
        for batch_start in range(0, page_numbers, batch_size):
            batch_end = min(batch_start + batch_size, page_numbers)
            threads = []
            
            # Create threads for this batch
            for page_num in range(batch_start, batch_end):
                thread = Thread(target=self.read_ocr, args=(page_num, file_name))
                threads.append(thread)
            
            # Start and wait for batch completion
            for thread in threads:
                thread.start()
            
            # Join with shorter timeout and cleanup
            for thread in threads:
                thread.join(timeout=10)  # Shorter timeout
                if thread.is_alive():
                    pass  # Thread will be cleaned up by Python
            
            # Small delay between batches to prevent resource conflicts
            time.sleep(0.1)
        
        # Combine text from all pages
        text = ""
        for key in sorted(self.book_dict.keys()):
            text += self.book_dict[key]
        
        self.Text = text
        return text
    
    def get_document(self, filename):
        """Extract text from PDF - handles both digital and OCR PDFs"""
        self.Text = ""
        
        # Validate file before processing
        if not os.path.exists(filename):
            return ""
        
        # Setup directory structure
        try:
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
            test_pages = min(3, doc_length)  # Reduced from 5 to 3
            
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
                self.multithreading_ocr(min(pages_to_process, 5), filename)  # Limit OCR pages
            
        except Exception:
            pass
        finally:
            # Always close the document
            if doc:
                try:
                    doc.close()
                except:
                    pass
        
        # Save as text file if requested
        if self.save_as_text_file and self.Text:
            try:
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(self.Text)
            except Exception:
                pass
        
        return self.Text
    
    def returnText(self):
        """Return both raw and cleaned text"""
        self._text = self.get_document(self.file_path)
        self.__text = self.remove_characters_before_tokenization(self._text)
        return self._text, self.__text
    
    def get_bookmarks(self, filepath):
        """Extract bookmarks from PDF"""
        self.bookmarks = {}
        try:
            with pymupdf.open(filepath) as file:
                toc = file.get_toc()
                for level, title, page in toc:
                    self.bookmarks[page] = title
        except Exception:
            pass
        return self.bookmarks


class DocumentContentDataset:
    def __init__(self, folder, *, specific_file=None, pages=10, 
                 clean_text=True, save_as_text_file=False, max_workers=None):
        """
        Process PDFs from a folder structure using concurrent processing
        
        Args:
            folder: Path to folder containing PDF files
            specific_file: Process specific file only
            pages: Number of pages to process per PDF
            clean_text: Whether to clean extracted text
            save_as_text_file: Whether to save as text files
            max_workers: Maximum number of concurrent workers
        """
        self._folder_path = folder
        self._specific_file = specific_file
        self._pages = pages
        self._clean_text = clean_text
        self._save_as_text_file = save_as_text_file
        # Very conservative concurrency to prevent segfaults
        self._max_workers = min(max_workers or 1, 2)  # Maximum 2 workers
        
        self.results = {}
        self.errors = []
        
        # Get all PDF files
        self.pdf_files = self._get_pdf_files()
        
        # Process files
        start_time = time.perf_counter()
        self.process_data_concurrent()
        end_time = time.perf_counter()
    
    def _get_pdf_files(self):
        """Get all PDF files from the folder structure"""
        pdf_files = []
        
        if os.path.isfile(self._folder_path):
            if self._folder_path.lower().endswith('.pdf'):
                pdf_files.append(self._folder_path)
        else:
            for root, dirs, files in os.walk(self._folder_path):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))
        
        return pdf_files
    
    def process_single_file(self, file_path):
        """Process a single PDF file - thread-safe"""
        try:
            # Add file validation
            if not os.path.exists(file_path):
                return {
                    'file_path': file_path,
                    'raw_text': None,
                    'clean_text': None,
                    'success': False,
                    'error': 'File not found'
                }
            
            # Check file size to prevent memory issues
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                return {
                    'file_path': file_path,
                    'raw_text': None,
                    'clean_text': None,
                    'success': False,
                    'error': 'File too large'
                }
            
            processor = PdfDataCollector(file_path, self._pages, self._save_as_text_file)
            raw_text, clean_text = processor.returnText()
            
            # Clean up processor
            del processor
            
            result = {
                'file_path': file_path,
                'raw_text': raw_text,
                'clean_text': clean_text if self._clean_text else None,
                'success': True,
                'error': None
            }
            
            return result
            
        except Exception:
            result = {
                'file_path': file_path,
                'raw_text': None,
                'clean_text': None,
                'success': False,
                'error': 'Processing failed'
            }
            
            return result
    
    def process_data_concurrent(self):
        """Process all PDFs using ThreadPoolExecutor with proper error handling"""
        # Process files sequentially if only 1 worker or few files
        if self._max_workers == 1 or len(self.pdf_files) <= 2:
            for file_path in self.pdf_files:
                result = self.process_single_file(file_path)
                if result['success']:
                    self.results[file_path] = result
                else:
                    self.errors.append(result)
                # Small delay between files to prevent resource conflicts
                time.sleep(0.1)
        else:
            # Use concurrent processing with very conservative settings
            with concurrent.futures.ThreadPoolExecutor(max_workers=self._max_workers) as executor:
                # Submit all tasks
                future_to_file = {
                    executor.submit(self.process_single_file, file_path): file_path 
                    for file_path in self.pdf_files
                }
                
                # Process completed tasks
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result(timeout=30)  # Reduced timeout
                        
                        if result['success']:
                            self.results[file_path] = result
                        else:
                            self.errors.append(result)
                            
                    except concurrent.futures.TimeoutError:
                        self.errors.append({'file_path': file_path, 'error': 'Timeout'})
                        
                    except Exception:
                        self.errors.append({'file_path': file_path, 'error': 'Processing failed'})
    
    def get_results(self):
        """Get processing results"""
        return self.results
    
    def get_errors(self):
        """Get processing errors"""
        return self.errors
    
    def flatten(self, items, ignore_types=(str, bytes)):
        """Flatten nested sequences"""
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from self.flatten(x)
            else:
                yield x


if __name__ == "__main__":
    # Test with a single file first - safest approach
    test_file = '/home/ngoni97/Documents/PHYSICS/ADVANCED/physics-for-scientists-and-engineers-with-modern-physics-serwayjewett.pdf'
    
    try:
        start = time.perf_counter()
        processor = PdfDataCollector(test_file, pages=3, save_as_text_file=True)  # Reduced pages
        raw_text, clean_text = processor.returnText()
        end = time.perf_counter()
        
        # Clean up
        del processor
        
        # Test with folder processing - very conservative
        test_folder = '/home/ngoni97/Documents/PHYSICS'
        print('process started\n')
        start = time.perf_counter()
        dataset = DocumentContentDataset(
            test_folder, 
            pages=3,  # Reduced pages
            save_as_text_file=True,
            max_workers=1  # Sequential processing to prevent segfaults
        )
        end = time.perf_counter()
        print('time taken = {:.2f}\n'.format(end - start))
        
        # Clean up
        del dataset
        
    except Exception:
        pass

# try to use PIL for OCR and see the difference