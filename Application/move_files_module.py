#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 02:02:59 2025

@author: ngoni97
"""

import os
import shutil
import pathlib

#from file_extension_tester import listDirFiles

# option 1: shutil.move() 

def Move(source, destination, file_type, folder_name=None):
    """ Source and Destination must be string paths 
        Moving using shutil.move() method
    """
    while True:
        try:
            # test if the source and destination directory exist
            os.path.exists(source)
            if not os.path.exists(destination):
                os.makedirs(destination, exist_ok=True)
        except FileNotFoundError as e:
            print('Error:', e)
        else:
            # if error isn't raised then continue
            src = source
            destn = destination + '/'
            break
            # if '\\' doesn't work then try '/'
    
    # must call in the listDirFiles when fully functioning
    files = [file for file in os.listdir(src) if file.endswith(file_type)]
    print('files =\n', files)
    # if the folder doesn't exist
    # if folder exists then don't create another one just use the existing one 
    # else, create a new folder depending on the name given
    if folder_name != None:
        # if folder doesn't exist already
        new_dir = destn + str(folder_name)
        os.mkdir(new_dir)
        
        # moving multiple files or folders art once
        for file in files:
            old_path = src + '/' + file
            new_path = new_dir + '/' + file
            shutil.move(old_path, new_path)
    else:
        # if it exists already
        # moving multiple files or folders art once
        for file in files:
            old_path = src + '/' + file
            new_path = destn + file
            shutil.move(old_path, new_path)
        pass
    
    #shutil.move(src, destn) # moving one file/folder

    
# option 2: os.rename()
def _Move(source, destination, file_type, folder_name=None):
    """ Moving using os.move() method """
    while True:
        try:
            # test if the source and destination directory exist
            os.path.exists(source)
            os.path.exists(destination)
        except FileNotFoundError as e:
            print('Error:', e)
        else:
            # if error isn't raised then continue
            src = source
            destn = destination + '/'
            break
            # if '\\' doesn't work then try '/'
       
    files = [file for file in os.listdir(src) if file.endswith(file_type)]
    print('files =\n', files)
    # if the folder doesn't exist
    # if folder exists then don't create another one just use the existing one 
    # else, create a new folder depending on the name given
    if folder_name != None:
        # if folder doesn't exist already
        new_dir = destn + str(folder_name)
        os.mkdir(new_dir)
        
        # moving multiple files or folders art once
        for file in files:
            old_path = src + '/' + file
            new_path = new_dir + '/' + file
            os.rename(old_path, new_path)
    else:
        # if it exists already
        # moving multiple files or folders art once
        for file in files:
            old_path = src + '/' + file
            new_path = destn + file
            os.rename(old_path, new_path)
        pass
    
    
# option 3: pathlib.Path().rename()
def __Move(source, destination, file_type, folder_name=None):
    """ Moving using pathlib.Path().rename() method """
    while True:
        try:
            # test if the source and destination directory exist
            os.path.exists(source)
            os.path.exists(destination)
        except FileNotFoundError as e:
            print('Error:', e)
        else:
            # if error isn't raised then continue
            src = source
            destn = destination + '/'
            break
            # if '\\' doesn't work then try '/'
    
    files = [file for file in os.listdir(src) if file.endswith(file_type)]
    print('files =\n', files)
    # if the folder doesn't exist
    # if folder exists then don't create another one just use the existing one 
    # else, create a new folder depending on the name given
    if folder_name != None:
        # if folder doesn't exist already
        new_dir = destn + str(folder_name)
        os.mkdir(new_dir)
        
        # moving multiple files or folders art once
        for file in files:
            old_path = src + '/' + file
            new_path = new_dir + '/' + file
            pathlib.Path(old_path).rename(new_path)
    else:
        # if it exists already
        # moving multiple files or folders art once
        for file in files:
            old_path = src + '/' + file
            new_path = destn + file
            pathlib.Path(old_path).rename(new_path)
        pass
        
if __name__ == "__main__":
        
    # test directory
    source = '/home/ngoni97/Downloads'
    destination = '/home/ngoni97/Downloads'

    #Move(source, destination, '.pdf', 'files')
    #__Move(source, destination, '.pdf', 'files3')
    _Move(source, destination + '/files2', '.pdf')
    
    input('\n\nPress enter to quit/exit.')
