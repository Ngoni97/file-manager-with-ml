#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 02:52:42 2025

@author: ngoni97
"""

# reading the contents of a folder and displaying the details as a pandas
# DataFrame

import os
import pandas as pd
import numpy as np
from random import shuffle
from file_extension_tester import listDirFiles


def CollectingData(directory, *, view=False, Shuffle=True):
    """ Collects data and stores it into an array """
    doc_ext = ['.djvu','.doc','.docx','.epub','.gcw','.htm','.html','.ods','.odt',
     '.pdf','.ppt','.pptx','.txt','.xls','.xlsx']
    img_ext = ['.bmp', '.cr2','.eps','.gif','.heif','.jpeg', '.jpg',
               '.nef','.orf','.png','.raw','.sr2','.tif','.tiff','.webp']
    music_ext = ['.aac', '.flac', '.m4a', '.mp3', '.ogg', '.wav', '.wma']
    videos_ext = ['.avchd','.avi','.f4v','.flv','.html5','.m4v','.mkv','.mov','.mp4','.mpg2','.opus','.ogv','.swf','.webm','.wmv']
    prog_ext = ['.action','.c','.cgi','.cs','.data','.dll','.do','.fcgi','.htm','.html','.ipynb', '.java',
                '.jhtml','.jsp','.jspx','.pdsprj','.php','.php3','.php4','.phtml','.py','.qrc',
                '.rb','.rhtml','.rss','.shtml','.swift','.vb','.workspace','.wss','.xhtml',
                '.xml','.yaws']
    exec_ext = ['.apk','.bat','.bin','.cmd','.com','.command','.deb',
                '.exe','.osx','.pif','.run','.sh','.vbs','.wsh']
    
    documents, images, music, videos, programming, executable = listDirFiles(directory, size=False)
    
    # shuffle everything
    if shuffle:
        shuffle(documents)
        shuffle(images)
        shuffle(music)
        shuffle(videos)
        shuffle(programming)
        shuffle(executable)
    else:
        pass
    # then join the shuffled data
    data = documents + images + music + videos + programming + executable
    
    #bytes_to_mbits = 1024 * 1024
    Data = []
    for file in data:
        full_path = directory + '/' + file
        
        # saving to an external text-file for checking the statistics of the previously run processes
        with open('previous_statistics.txt', 'a+') as File:
            if '.' + file.split('.')[-1] in doc_ext:
                Data.append([file, 'document', 
                              os.path.getsize(full_path)])
                File.write('{}, {}, {}\n'.format(file, 'document', 
                                  str(os.path.getsize(full_path))))
            elif '.' + file.split('.')[-1] in img_ext:
                Data.append([file, 'image', 
                              os.path.getsize(full_path)])
                File.write('{}, {}, {}\n'.format(file, 'image', 
                                  str(os.path.getsize(full_path))))
            elif '.' + file.split('.')[-1] in music_ext:
                Data.append([file, 'music', 
                              os.path.getsize(full_path)])
                File.write('{}, {}, {}\n'.format(file, 'music', 
                                  str(os.path.getsize(full_path))))
            elif '.' + file.split('.')[-1] in videos_ext:
                Data.append([file, 'video', 
                              os.path.getsize(full_path)])
                File.write('{}, {}, {}\n'.format(file, 'video', 
                                  str(os.path.getsize(full_path))))
            elif '.' + file.split('.')[-1] in prog_ext:
                Data.append([file, 'programming', 
                              os.path.getsize(full_path)])
                File.write('{}, {}, {}\n'.format(file, 'programming', 
                                  str(os.path.getsize(full_path))))
            elif '.' + file.split('.')[-1] in exec_ext:
                Data.append([file, 'executable program', 
                              os.path.getsize(full_path)])
                File.write('{}, {}, {}\n'.format(file, 'executable program', 
                                  str(os.path.getsize(full_path))))
    # shuffle the data so that it doesn't appear biased since I joined the lists
    # that were already in an orderly manner by their type
    if Shuffle:
        i = 0
        while True:
            shuffle(Data)
            i += 1
            if i == 42:
                break
    else:
        pass
    df = pd.DataFrame(np.array(Data), columns=['filename', 'file type', 'size (bytes)'])

    if view == True:
        print(df)
    else:
        pass
    columns=['filename', 'type', 'size (bytes)']
    return {'data':np.array(Data), 'features_names':columns}

#os.path.getsize(path)
def getSize(filename):
    st = os.stat(filename)
    return st.st_size

if __name__ == "__main__":
    CollectingData('/home/ngoni97/Downloads/Downloads/Unsorted', view=True, Shuffle=False)
# listDirFiles
# collects files and adds them to a list depending on whether they're documents, images, etc.
# need to keep track of the files full path for when moving them to their respective folders


# need to shuffle this Data in the best way as possible
# need to find the best shuffling algorithm to avoid biasing the data when training the ML algorithms