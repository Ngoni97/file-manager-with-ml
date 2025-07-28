#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 02:08:47 2025

@author: ngoni97
"""

# stripping the file type endings
import re
from file_extension_tester import listDirFiles, fileExtensions

def fileExtensionStripper(directory):
    documents, images, music, videos, programming, executable = listDirFiles(directory, size=False)
    doc_ext, img_ext, music_ext, videos_ext, prog_ext, exec_ext = fileExtensions()
    
    Documents, Images, Music, Videos, Programming, Executable = [],[],[],[],[],[]
    # for documents
    for file in documents:
        # testing for document extensions
        for extension in doc_ext:
            pattern = re.compile('{}$'.format(extension))
            test = re.search(pattern, file)
            if test:
                result = re.sub(pattern, r'', file)
                if result in Documents:
                    pass
                else:
                    Documents.append(result)
    # for images
    for file in images:
        # testing for document extensions
        for extension in img_ext:
            pattern = re.compile('{}$'.format(extension))
            test = re.search(pattern, file)
            if test:
                result = re.sub(pattern, r'', file)
                if result in Videos:
                    pass
                else:
                    Videos.append(result)
    # for music
    for file in music:
        # testing for document extensions
        for extension in music_ext:
            pattern = re.compile('{}$'.format(extension))
            test = re.search(pattern, file)
            if test:
                result = re.sub(pattern, r'', file)
                if result in Music:
                    pass
                else:
                    Music.append(result)
    # for videos
    for file in videos:
        # testing for document extensions
        for extension in videos_ext:
            pattern = re.compile('{}$'.format(extension))
            test = re.search(pattern, file)
            if test:
                result = re.sub(pattern, r'', file)
                if result in Videos:
                    pass
                else:
                    Videos.append(result)
    # for programming
    for file in programming:
        # testing for document extensions
        for extension in prog_ext:
            pattern = re.compile('{}$'.format(extension))
            test = re.search(pattern, file)
            if test:
                result = re.sub(pattern, r'', file)
                if result in Programming:
                    pass
                else:
                    Programming.append(result)
    # for executable
    for file in executable:
        # testing for document extensions
        for extension in doc_ext:
            pattern = re.compile('{}$'.format(extension))
            test = re.search(pattern, file)
            if test:
                result = re.sub(pattern, r'', file)
                if result in Executable:
                    pass
                else:
                    Executable.append(result)
                    
    return Documents, Images, Music, Videos, Programming, Executable

if __name__ == "__main__":
    test_path = "/home/ngoni97/Downloads/Downloads/Unsorted"
    Documents, Images, Music, Videos, Programming, Executable = fileExtensionStripper(test_path)
    
    print('\ndocuments =',Documents)
    print('\nimages =',Images)
    print('\nmusic =',Music)
    print('\nvideos =',Videos)
    print('\nprogramming =',Programming)
    print('\nexecutable =',Executable)