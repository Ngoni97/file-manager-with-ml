#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixed PDF Data Collector with proper concurrency handling
@author: Harold
"""

import os
import re
import pymupdf
import pathlib
from threading import Thread, Lock
import concurrent.futures
import time
from collections.abc import Iterable

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
        
    def remove_characters_before_tokenization(self, sentence, keep_apostrophes=False):
        """Clean text by removing unwanted characters"""
        sentence = (sentence.replace('_', ' ')).replace('-', ' ')
        
        PATTERN = re.compile('[?|$|&|*|%|@|(|)|~]')
        pattern = re.compile('[^a-zA-Z]') if not keep_apostrophes else re.compile('[^a-zA-Z\']')
        replacement = r' '
        
        filtered_sentence = re.sub(pattern, replacement, re.sub(PATTERN, replacement, sentence))
        return filtered_sentence.lower()
    
    def read_ocr(self, page_num, book_path):
        """Read OCR text from a specific page - thread-safe version"""
        __text = ""
        try:
            with pymupdf.open(book_path) as file:
                if page_num < len(file):  # Check if page exists
                    page = file[page_num]
                    try:
                        __Text = page.get_textpage_ocr(dpi=250, full=True)
                        __text = __Text.extractTEXT()
                    except Exception as e:
                        print(f"OCR error on page {page_num}: {e}")
                        pass
                else:
                    print(f"Page {page_num} doesn't exist in document")
        except Exception as e:
            print(f"Error opening document for page {page_num}: {e}")
        
        # Thread-safe dictionary update
        with self.lock:
            self.book_dict[page_num] = __text
        
        return __text
    
    def multithreading_ocr(self, page_numbers, file_name):
        """Multi-threaded OCR processing with proper error handling"""
        threads = []
        
        # Create threads
        for page_num in range(page_numbers):
            thread = Thread(target=self.read_ocr, args=(page_num, file_name))
            threads.append(thread)
        
        print("OCR reading process started!")
        
        # Start threads
        for thread in threads:
            thread.start()
        
        # Join threads with timeout to prevent hanging
        for thread in threads:
            thread.join(timeout=30)  # 30 second timeout per thread
            if thread.is_alive():
                print(f"Thread for page processing timed out")
        
        # Combine text from all pages
        text = ""
        for key in sorted(self.book_dict.keys()):
            text += self.book_dict[key]
        
        self.Text = text
        print("OCR process finished!")
        return text
    
    def get_document(self, filename):
        """Extract text from PDF - handles both digital and OCR PDFs"""
        self.Text = ""
        
        # Setup directory structure
        self.main_folder_path = os.path.basename(os.path.dirname(os.path.dirname(filename)))
        self.parent_directory = os.path.join(
            '/home/ngoni97/Documents/Documents/File Manager with ML/train_test_text_files', 
            self.main_folder_path
        )
        
        if not os.path.exists(self.parent_directory):
            os.makedirs(self.parent_directory, exist_ok=True)
        
        # Create text file path
        base_name = os.path.splitext(os.path.basename(filename))[0]
        text_file_path = os.path.join(self.parent_directory, f"{base_name}.txt")
        
        digital_pages = 0
        ocr_pages = 0
        
        try:
            with pymupdf.open(filename) as file:
                doc_length = len(file)
                pages_to_process = min(self.pages or doc_length, doc_length)
                
                # Test first few pages to determine document type
                for page_num in range(min(5, doc_length)):
                    page = file[page_num]
                    try:
                        if page.get_text().strip():
                            digital_pages += 1
                            break
                    except:
                        pass
                    
                    try:
                        if page.get_textpage_ocr():
                            ocr_pages += 1
                            break
                    except:
                        pass
                
                # Process based on document type
                if digital_pages > 0:
                    print(f'Processing digitally-born PDF: {os.path.basename(filename)}')
                    for page_num in range(pages_to_process):
                        try:
                            page = file[page_num]
                            text = page.get_text()
                            self.Text += text
                        except Exception as e:
                            print(f"Error reading page {page_num}: {e}")
                            continue
                
                elif ocr_pages > 0:
                    print(f'Processing OCR PDF: {os.path.basename(filename)}')
                    self.multithreading_ocr(pages_to_process, filename)
                
                else:
                    print(f"No readable text found in {os.path.basename(filename)}")
                    
        except Exception as e:
            print(f"Error processing document {filename}: {e}")
            return ""
        
        # Save as text file if requested
        if self.save_as_text_file and self.Text:
            try:
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(self.Text)
                print(f"Text saved to: {text_file_path}")
            except Exception as e:
                print(f"Error saving text file: {e}")
        
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
        except Exception as e:
            print(f"Error extracting bookmarks: {e}")
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
        self._max_workers = max_workers or min(4, (os.cpu_count() or 1))
        
        self.results = {}
        self.errors = []
        
        # Get all PDF files
        self.pdf_files = self._get_pdf_files()
        
        print(f"Found {len(self.pdf_files)} PDF files to process")
        
        # Process files
        start_time = time.perf_counter()
        print("Starting PDF processing...")
        self.process_data_concurrent()
        end_time = time.perf_counter()
        
        print(f"Processing completed in {end_time - start_time:.2f}s")
        if self.errors:
            print(f"Encountered {len(self.errors)} errors during processing")
    
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
            processor = PdfDataCollector(file_path, self._pages, self._save_as_text_file)
            raw_text, clean_text = processor.returnText()
            
            result = {
                'file_path': file_path,
                'raw_text': raw_text,
                'clean_text': clean_text if self._clean_text else None,
                'success': True,
                'error': None
            }
            
            return result
            
        except Exception as e:
            error_msg = f"Error processing {file_path}: {str(e)}"
            print(error_msg)
            
            result = {
                'file_path': file_path,
                'raw_text': None,
                'clean_text': None,
                'success': False,
                'error': error_msg
            }
            
            return result
    
    def process_data_concurrent(self):
        """Process all PDFs using ThreadPoolExecutor with proper error handling"""
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
                    result = future.result(timeout=60)  # 60 second timeout
                    
                    if result['success']:
                        self.results[file_path] = result
                        print(f"✓ Processed: {os.path.basename(file_path)}")
                    else:
                        self.errors.append(result)
                        print(f"✗ Failed: {os.path.basename(file_path)}")
                        
                except concurrent.futures.TimeoutError:
                    error_msg = f"Timeout processing {file_path}"
                    print(error_msg)
                    self.errors.append({'file_path': file_path, 'error': error_msg})
                    
                except Exception as e:
                    error_msg = f"Exception processing {file_path}: {str(e)}"
                    print(error_msg)
                    self.errors.append({'file_path': file_path, 'error': error_msg})
    
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
    # Test with a single file first
    test_file = '/home/ngoni97/Documents/PHYSICS/ADVANCED/physics-for-scientists-and-engineers-with-modern-physics-serwayjewett.pdf'
    
    print("Testing single file processing...")
    start = time.perf_counter()
    processor = PdfDataCollector(test_file, pages=5, save_as_text_file=True)
    raw_text, clean_text = processor.returnText()
    end = time.perf_counter()
    
    print(f"Single file processing time: {end - start:.2f}s")
    print(f"Extracted text length: {len(raw_text)} characters")
    
    # Test with folder processing
    print("\nTesting folder processing...")
    test_folder = '/home/ngoni97/Documents/PHYSICS'
    
    start = time.perf_counter()
    dataset = DocumentContentDataset(
        test_folder, 
        pages=5, 
        save_as_text_file=True,
        max_workers=2  # Limit concurrent workers for stability
    )
    end = time.perf_counter()
    
    print(f"Folder processing time: {end - start:.2f}s")
    print(f"Successfully processed: {len(dataset.get_results())} files")
    print(f"Errors: {len(dataset.get_errors())} files")