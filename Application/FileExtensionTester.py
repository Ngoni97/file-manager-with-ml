# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 13:23:20 2024

@author: Ngoni
"""
# どうもありがとうございます == Dōmo arigatōgozaimasu

# test for file exensions and report the statistics
# used to creare the message dialog for what kind of files to are in a directory
# to help with the choice of the algorithm whether it be automatic or intentionally

import os 
import timeit

def fileExtensions():
    doc_ext = ['.djvu', '.doc', '.docx', '.epub', '.gcw', '.htm', '.html', 
               '.ods', '.odt', '.pdf', '.ppt', '.pptx', '.txt', '.xls', '.xlsx']
    img_ext = ['.bmp', '.cr2', '.eps', '.gif', '.heif', '.jpeg', '.jpg', '.nef',
               '.orf', '.png', '.raw', '.sr2', '.tif', '.tiff', '.webp']
    music_ext = ['.aac', '.flac', '.m4a', '.mp3', '.ogg', '.wav', '.wma']
    videos_ext = ['.avchd', '.avi', '.f4v', '.flv', '.html5', '.m4v', '.mkv',
                  '.mov', '.mp4', '.mpg2', '.opus', '.ogv', '.swf', '.webm', '.wmv']
    prog_ext = ['.action', '.c', '.cgi', '.cs', '.data', '.dll', '.do', '.fcgi',
                '.htm', '.html', '.ipynb', '.java', '.jhtml', '.jsp', '.jspx',
                '.pdsprj', '.php', '.php3', '.php4', '.phtml', '.py', '.qrc', '.rb',
                '.rhtml', '.rss', '.shtml', '.swift', '.vb', '.workspace', '.wss',
                '.xhtml', '.xml', '.yaws']
    exec_ext = ['.apk', '.bat', '.bin', '.cmd', '.com', '.command', '.deb', '.exe', '.osx',
                '.pif', '.run', '.sh', '.vbs', '.wsh']
    return doc_ext, img_ext, music_ext, videos_ext, prog_ext, exec_ext

def listDirFiles(path, size=True, fullpath=False):
    # if size==False, then return the data as a list
    files = [file for file in os.listdir(path)]
    # loading file extensions
    doc_ext, img_ext, music_ext, videos_ext, prog_ext, exec_ext = fileExtensions()
    # creating lists to append respective files
    documents = []
    images = []
    music = []
    videos = []
    programming = []
    executable = []
    
    # if fullpath is True
    if fullpath == False:
        # appending respective files
        for file in files:
            for item in doc_ext:
                if file.endswith(item):
                    documents.append(file)
            for item in img_ext:
                if file.endswith(item):
                    images.append(file)
            for item in music_ext:
                if file.endswith(item):
                    music.append(file)
            for item in videos_ext:
                if file.endswith(item):
                    videos.append(file)
            for item in prog_ext:
                if file.endswith(item):
                    programming.append(file)
            for item in exec_ext:
                if file.endswith(item):
                    executable.append(file)
    else:
        # appending respective files
        for file in files:
            for item in doc_ext:
                if file.endswith(item):
                    documents.append(os.path.join(path,file))
            for item in img_ext:
                if file.endswith(item):
                    images.append(os.path.join(path,file))
            for item in music_ext:
                if file.endswith(item):
                    music.append(os.path.join(path,file))
            for item in videos_ext:
                if file.endswith(item):
                    videos.append(os.path.join(path,file))
            for item in prog_ext:
                if file.endswith(item):
                    programming.append(os.path.join(path,file))
            for item in exec_ext:
                if file.endswith(item):
                    executable.append(os.path.join(path,file))
                
    if size == True:
        print('documents',documents, '\n\nimages', images, '\n\nmusic',
              music, '\n\nvideos', videos, '\n\nprogramming', programming, '\n\nexecutable', executable)
        return len(documents), len(images), len(music), len(videos), len(programming), len(executable)
    elif size == False:
        return [documents, images, music, videos, programming, executable]
    else:
        print('Invalid option!')

def time_it():
    """ timing it """
    SETUP_CODE = '''
from __main__ import listDirFiles
import os
            '''
    TEST_CODE = ''' 
path = "/home/ngoni97/Downloads/Downloads/Unsorted"
listDirFiles(path)
            '''
    print('\n\n' + str(timeit.timeit(setup=SETUP_CODE,
                  stmt=TEST_CODE,
                  number=1000)))
            
#listDirFiles("C:/Users/Admin/Downloads/Other Stuff")
if __name__ == "__main__":
    time_it()
 
# windows os
#path = "C:/Users/Admin/Downloads/Other Stuff"

""" later on add the feature of reporting other files not listed in the main lists """