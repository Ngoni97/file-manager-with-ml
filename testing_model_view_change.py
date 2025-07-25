#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 01:27:04 2025

@author: ngoni97
"""

# testing model view change in another listView after clicking from another listView

import os, sys
from PyQt5 import uic
from PyQt5 import uic
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import QModelIndex, Qt, QDir, QAbstractTableModel
from PyQt5.QtWidgets import (
    QApplication,
    QTreeView, 
    QListView,
    QFileSystemModel,
    QMainWindow,
    QAction,
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout)

        
class MainWindow(QMainWindow):
    def __init__(self, dir_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('testing_model_view_change.ui', self)
        self.dir_path = dir_path
        self._dir_path = dir_path
       
        #self.model = QFileSystemModel(self) 
        #self.model2 = QFileSystemModel(self)
        
        self.ListView1()
        self.ListView2(self._dir_path)

        
    def ListView1(self):
        """ listView display function"""
        self.model = QFileSystemModel(self)
        self.model.setRootPath(self.dir_path) # takes in strings of a directory path
        #self.model.setFilter(QDir.NoDotAndDotDot | QDir.Files) # this one doesn't display folders
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs) # only show directories in the QListView
        # for the meantime let's display all files and directories
        # displaying a listView
        self.listView.setModel(self.model)
        self.listView.setRootIndex(self.model.index(self.dir_path))
        # .index: returns the model item index for the given 'path' and 'column'
        # .setRootIndex: input is a QModelIndex
        # doubleClick to change the directory of the listView window
        self.listView.doubleClicked.connect(self._change_dir)
        
    def _change_dir(self, new_dir): # public method
        """ Change the root directory for the listView2 """
        global path
        path = new_dir
        print('testing newDirectory', new_dir)
        print('listView directory path name ', self.model.filePath(new_dir))
        
        self.ListView2(self.model.filePath(new_dir))
        pass
        
    def ListView2(self, Dir):
        """ listView2 display function"""
        model2 = QFileSystemModel(self)
        if isinstance(Dir, QModelIndex):
            print('directory from listView1', model2.filePath(Dir))
            model2.setRootPath(model2.filePath(Dir))
            model2.setFilter(QDir.AllEntries)
            self.listView2.setModel(model2)
            self.listView2.setRootIndex(Dir)
        else:
            model2.setRootPath(Dir)
            model2.setFilter(QDir.AllEntries)
            self.listView2.setModel(model2)
            self.listView2.setRootIndex(model2.index(Dir))
            #self.listView2.setSortingEnabled(True)
    
App = QApplication(sys.argv)  
dirPath = "/media/ngoni97/9ine7even/Users/Admin"
window = MainWindow(dir_path=dirPath)
window.show()
sys.exit(App.exec_())           
    