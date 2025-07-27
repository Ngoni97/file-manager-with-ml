# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 14:42:58 2024

@author: Ngoni
"""

import sys
import os
from PyQt5 import uic
from PyQt5.QtCore import QModelIndex, Qt, QDir, QAbstractTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import pandas as pd

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            val  = self._data.iloc[index.row(), index.column()]
            return str(val)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
            

class StatsPopupWindow(QMainWindow, QDialog):
    def __init__(self, Data, directory_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Data = Data
        self._directory = directory_path # directory path to be used in the label
        
        # load the UI file
        uic.loadUi('statistics_popup_window.ui', self)
        
        data = pd.DataFrame(self._Data,
                            columns=['Total'],
                            index=['Documents', 'Images', 'Music', 'Videos', 'Programming', 'Executable'])
        
        self.model = TableModel(data)
        self.tableView.setModel(self.model)
        self.label.setText(self._directory)

        self.OkButton.clicked.connect(self.accept)
        
    def keyPressEvent(self, event):
        '''if isinstance(event, QKeyEvent):
            key_text = event.text()
            print('pressed key text =', key_text)'''
            # if pressed key == 'Enter' button: change the directory
            # must have a global reference of the current directory in order to input
            # it here
        if event.key() == Qt.Key_Return:
            print('return pressed')
            self.close()
            
        elif event.key() == Qt.Key_Enter:
            print('enter pressed')
        
    def accept(self):
        self.close()

if __name__ == "__main__":
    from file_extension_tester import listDirFiles

    App = QApplication(sys.argv)
    documents, images, music, videos, programming, executable = listDirFiles("C:/Users/Admin/Downloads/Unsorted")
    Data = [documents, images, music, videos, programming, executable]    
    window = StatsPopupWindow(Data)
    window.show()
    sys.exit(App.exec_())

