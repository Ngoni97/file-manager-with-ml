# MainWindow
# どうもありがとうございます == Dōmo arigatōgozaimasu

import sys
import os
import pandas as pd
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

from main_MainWindow import PopUpMainWindow
from linked_directories_class import LinkedDirectory
from file_extension_tester import listDirFiles
from stats_pop_up_window import StatsPopupWindow
from move_files_module import Move, _Move, __Move
from collecting_data import CollectingData
#from dataset_collector_saver import Dataset

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


class MainWindow(QMainWindow):
    def __init__(self, dir_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dir_path = dir_path
        self.Prev = None
        self.prev = None
        self.Current = None
        self.current = None
        self.New__dir = dir_path
        # initially upon launching the app the show statspopup window val is True
        self.ShowStatsPopUpWindow = True
        # reference point for the NewProcess activation
        self._isNewProcess = False # initially it's turned off

        # load the UI file
        uic.loadUi('MainWindow.ui', self)

        self.popUp = PopUpMainWindow() # description pop-up window reference
        self.directory = LinkedDirectory() # linked directories class reference

        self.ListView()
        self.ListView2(self.dir_path)
        
        # the initial state of the stats pop up window
        documents, images, music, videos, programming, executable = listDirFiles(self.dir_path)
        # .filePath converts a QModelIndex to directory path as str
        Data = [documents, images, music, videos, programming, executable]
        self.statsPopup = StatsPopupWindow(Data, self.dir_path) # statistics popup window reference
        
        # File/Folder 
        self.actionNew.triggered.connect(self._NewProcess)
        self.actionOpen.triggered.connect(self._OpenFolder)
        self.actionRecent.triggered.connect(self._RecentProcess)
        self.actionPrev_Directory.triggered.connect(self._prev_Directory)
        
        # Algorithms
        
        # View
        self.actionRowColour.triggered.connect(self._row_color)
        self.actionStatistics.triggered.connect(self.__stats_popup_window) # indirectly calling a private method
        self.actionStatistics.setCheckable(True)
        # the checkable state is On/Checked at the initially launch
        # you can't connect an action signal directly with a function-variable call
        
        # Settings
        self.actionPreferences.triggered.connect(self._Preferences)
        # create a popup window for settings
        # Help

        # opening the description entry pop-up window
        self.selectFolderButton.clicked.connect(self.__Pop_up_Window)

    def ListView(self):
        """ Display view for listView one"""

        self.model = QFileSystemModel(self)
        self.model.setRootPath(self.dir_path) # takes in strings of a directory path
        #self.model.setFilter(QDir.NoDotAndDotDot | QDir.Files) # this one doesn't display folders
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs) # only show directories in the QListView
        # for the meantime let's display all files and directories
        # displaying a listView
        self.listView.setModel(self.model)
        self.listView.setRootIndex(self.model.index(self.dir_path))
        self.directory.addDir(self.model.index(self.dir_path))
        # .index: returns the model item index for the given 'path' and 'column'
        # .setRootIndex: input is a QModelIndex

        # enabling the selection method for listView
        self.select = self.listView.selectionModel()
        self.select.currentChanged.connect(self._Row_changed)

        self.listView.pressed.connect(self._testDirectory)
        # doubleClick to change the directory of the listView window
        self.listView.doubleClicked.connect(self._Change_dir)
        # listView: later on add the option of whether single click or double click opens the selected directory
        

    def ListView2(self, Dir):
        """ Display view for listView2"""
        self.model2 = QFileSystemModel(self)
        self.model2.setRootPath(Dir)
        # displaying a listView2
        self.listView2.setModel(self.model2)
        self.listView2.setRootIndex(self.model2.index(Dir))
        #self.listView2.setSortingEnabled(True)
        # set initial folder name
        self.label_3.setText(Dir)

        self.select2 = self.listView2.selectionModel()
        self.select2.currentChanged.connect(self._row_changed)

        self.listView2.doubleClicked.connect(self._change_dir)

    def _Row_changed(self, current, prev):
        """ Row selection for listView one """
        self.Current = current
        self.Prev = prev
        print('prev directory listView one', self.Prev.data())
        print('current directory listView one', self.Current.data())
        pass

    def _row_changed(self, current, prev):
        """ Row selection for listView2 two """
        #global prev, current
        
        self.prev = prev
        self.current = current
        print('Prev directory listView2', self.prev.data())
        print('Current directory listView2', self.current.data())
        pass

        # testing for directories
        #print('Is it a parent directory Prev = {} : Current = {}?'.format(Prev.parent().data(), Current.parent().data()))
        # fix the part that it is doing nothing if I click on a non-directory file
        # it will have registered the previous directory as the folder I'm in and the file (non-folder)
        # I clicked on is the new directory
        # also link the previous folder if I clicked from listView 1
        # use the idea of singly linked lists

    def _path_changed(self, path):
        print('new path = ', path)
        pass
    
    def _stats_popup_window(self, directory=None,*, view=True): # public method
        """ Display the statistics of a given folder

            takes in a QModelIndex
        """
        # if run from the original root directory New_dir before the update upon launching the app
        # or when you want to access the window from the menubar
        if not isinstance(directory, str):
            # if loading from the _change_dir or the updated path New_dir for the Statistics QAction
            documents, images, music, videos, programming, executable = listDirFiles(self.model.filePath(directory))
        else:
            # if loading form the original root path 
            documents, images, music, videos, programming, executable = listDirFiles(directory)
        #documents, images, music, videos, programming, executable = listDirFiles(self.model.filePath(directory))
        # .filePath converts a QModelIndex to directory path as str
        Data = [documents, images, music, videos, programming, executable]
        # updating the original data
        # if directory is str then use it as it is
        # else convert it from QModelIndex to str
        if not isinstance(directory, str):
            # if QModelIndex
            self.statsPopup = StatsPopupWindow(Data, self.model.filePath(directory)) # statistics popup window reference update
        else:
            # if already str
            self.statsPopup = StatsPopupWindow(Data, directory)
        if view == True:
            self.statsPopup.show()
        else:
            pass
        pass

    def __stats_popup_window(self, val): # private method
        """ private method 
            Updates the display statsPopup window value
        """
        self.ShowStatsPopUpWindow = val
        # if already visible then close, else show
        if self.statsPopup.isVisible():
            self.statsPopup.hide()
        else:
            # if notVisible
            if val == True:
                # and check is True, then
                self.statsPopup.show()
        # when checking off, if the window was already closed then don't show again but keep it closed/notVisible
        # fix the part of only updating whilst the popup window is open
        # it needs to keep a registry of the updated directory path
        # still not updating whilst the popup window if notVisible

    def _display_stats(self, directory):
        ''' Display data in the select folder tab '''
        if not isinstance(directory, str):
            # if loading from the _change_dir or the updated path New_dir for the Statistics QAction
            documents, images, music, videos, programming, executable = listDirFiles(self.model.filePath(directory))
        else:
            # if loading form the original root path 
            documents, images, music, videos, programming, executable = listDirFiles(directory)
        #documents, images, music, videos, programming, executable = listDirFiles(self.model.filePath(directory))

        # .filePath converts a QModelIndex to directory path as str
        self._Data = [documents, images, music, videos, programming, executable]
        
        data = pd.DataFrame(self._Data,
                            columns=['Total'],
                            index=['Documents', 'Images', 'Music', 'Videos', 'Programming', 'Executable'])
        
        self.Model = TableModel(data)
        self.tableView.setModel(self.Model)
    
    def _Change_dir(self, New_dir):
        """ changing directory of listView2 from selecting in the listView one """
        #global New__dir
        self.New__dir = New_dir
        print('testing newDirectory', New_dir)
        self.directory.addDir(New_dir)
        #print('new_dir as string', self.model.filePath(new_dir))
        print(listDirFiles(self.model.filePath(New_dir)))
        # display stats popup window
        if self.ShowStatsPopUpWindow:
            # if checked then show
            self._stats_popup_window(New_dir)
        else:
            # don't show
            if self.ShowStatsPopUpWindow == False:
                self._stats_popup_window(New_dir, view=False)
                pass
        # display in tableView in Select Folder tab
        self._display_stats(New_dir)
        
        # fix Error::  listdir: path should be string, bytes, os.PathLike or None, not QModelIndex
        print('current dir =', self.directory.current_Dir())

        self.model2.setRootPath(self.model.filePath(New_dir)) # getting the listView directory path 
                                                            # and setting it into listView2 model
        # displaying a listView2
        self.listView2.setModel(self.model2)
        self.listView2.setRootIndex(self.model2.index(self.model.filePath(New_dir)))

        # show folder name
        self.label_2.setText(self.model.filePath(New_dir))
        self.label_3.setText(self.model.filePath(New_dir))
        pass

    def _change_dir(self, new_dir): # public method
        """ Change the root directory of listView2 from selecting in the listView2 """
        #global New__dir
        self.New__dir = new_dir
        print('testing newDirectory', new_dir)
        self.directory.addDir(new_dir)
        #print('new_dir as string', self.model.filePath(new_dir))
        print(listDirFiles(self.model.filePath(new_dir)))
        # display stats popup window
        if self.ShowStatsPopUpWindow:
            # if checked then show
            self._stats_popup_window(new_dir)
        else:
            # don't show
            if self.ShowStatsPopUpWindow == False:
                self._stats_popup_window(new_dir, view=False)
                pass
        # display in tableView in Select Folder tab
        self._display_stats(new_dir)
        
        # fix Error::  listdir: path should be string, bytes, os.PathLike or None, not QModelIndex
        print('current dir =', self.directory.current_Dir())

        self.listView2.setRootIndex(new_dir)

        # show folder name
        self.label_2.setText(self.model2.filePath(new_dir))
        self.label_3.setText(self.model2.filePath(new_dir))
        pass

    def _prev_Directory(self): # public method
        """ Return the previous working directory """
        #global New__dir # to update the global variable inside a function you call on the global method
        prev_Dir = self.directory.callDir()
        # if prev_Dir is from listView one, then use the filePath to convert it to the current model of listView2
        # else, if it's from listView2 already then there is no need to convert
        self.model2.setRootPath(self.model.filePath(prev_Dir)) # getting the listView directory path 
                                                            # and setting it into listView2 model
        # displaying a listView2
        self.listView2.setModel(self.model2)
        self.listView2.setRootIndex(self.model2.index(self.model.filePath(prev_Dir)))
        #self.listView2.setRootIndex(prev_Dir)

        # need to update the New__dir after going back to the previous folder directory
        self.New__dir = prev_Dir
        # update the display values
        self._display_stats(prev_Dir)
        if self.ShowStatsPopUpWindow:
            # if checked then show
            self._stats_popup_window(prev_Dir)
        else:
            # don't show
            # but update the statsPopupWindow data
            if self.ShowStatsPopUpWindow == False:
                self._stats_popup_window(prev_Dir, view=False)
                pass
        self.label_2.setText(self.model.filePath(prev_Dir))
        self.label_3.setText(self.model.filePath(prev_Dir))
        pass
        # fix previous directory not working too
    
    def _testDirectory(self, Path): # public method
        #print('testing directory', Path)
        pass
    
    def keyPressEvent(self, event):
        """ pressing enter or return to close the statistics popup window """
        # if pressed key == 'Enter' button: change the directory
        # must have a global reference of the current directory in order to input
        # it here
        if event.key() == Qt.Key_Return:
            print('return pressed')
            if self.Current:
                # if listView
                self._Change_dir(self.Current)
            elif self.current:
                # if listView2
                self._change_dir(self.current)
        elif event.key() == Qt.Key_Enter:
            print('enter pressed')
            if self.Current:
                self._Change_dir(self.Current)
            elif self.current:
                self._change_dir(self.current)
        # add the function of where the keypressedEvent should work between the two listViews
        # that is, if the selectin is in listView or listView2
        # fix the issue of not opening selected directory in listView2 after selecting from listView one;
        # using the 'Enter' & 'Return' keys

############################ menubar actions ################################

    def _NewProcess(self, Val): # public method
        """ Initialize a New Process
            The action is checkable in order to start a new process you have to activate it.
        """
        self._isNewProcess = Val
        # if Val == True, then allow the process to be carried on
        # otherwise, don't bother
        print('button pressed!', Val)
        pass

    def _OpenFolder(self): # public method
        """ Open a folder to start the sorting process """
        # opens a file
        #QFileDialog.getOpenFileName(self, 'Open File', self.dir_path, 'All Files (*.*);;Text Files (*.txt)')
        # link it to the _change_dir method
        # open a folder
        openDir = QFileDialog.getExistingDirectory(self, 'Open Folder', self.dir_path, options=QFileDialog.ShowDirsOnly)
        # fix the part to only displaying folders
        print(openDir) # returns a path of the selected directory
        self._change_dir(self.model.index(openDir))
        pass

    def _RecentProcess(self): # public method
        """ See the statistics of the recent process together with the paths/directories"""
        # create a pop-up window
        pass

    def _Preferences(self): # public method
        """ Change settings """
        # create another pop-up window
        pass

    def _row_color(self, val): # public method
        """ Change Alternating Row Colours """
        #print(val)
        self.listView.setAlternatingRowColors(val)
        self.listView2.setAlternatingRowColors(val)
        # add the functionality of choosing the colour as per user preference in the settings
        #self.listView.setStyleSheet("alternate-background-color: white;background-color: green;")

    def __Pop_up_Window(self, checked): # private method
        """ Private Method
            Launch the description window
        """
        if self.popUp.isVisible():
            self.popUp.hide()
        else:
            self.popUp.show()

App = QApplication(sys.argv)
App.setStyle('Fusion')
# for Windows OS
#dirPath = "C:\\Users\\Admin"
# for Kali Linux OS
dirPath = "/media/ngoni97/9ine7even/Users/Admin"
window = MainWindow(dir_path=dirPath)
window.show()
sys.exit(App.exec_())

# add the setting that the user can choose the initial directory
# which the application loads upon launching
# Use QSortFilterProxyModel to display only directories/folders in the listView
# and all files in the treeView
# use singly linked list for tracing back the directory tree
# fix the part of returning to the original directory
# it starts to take reference after selecting from the main directory
# must keep a reference to the main directory
# show the progressbar only when the process is running
# display the statistics of the folder content after selecting
# activate the Enter action
# fix the keyPressEvent to specify the exact keyboard key pressed to activate the action

# the stats popup window is not popping
# still the popup window not showing

# if statistics action is off then don't display popup window
# only display in the view select folder tab

# add selected folder label in the Selected Folder and View Folders tabs
# also add the function of searching for a folder in the selected directory

# activate the keyboard keyEvent when you press enter/return key in the listView widgets


# create a function that searches for a specific folder
# whilst searching it should highlight matching cases and eliminate those that don't match
# it's kinda a replica of the Windows file explorer search function

# create a function that takes the contents inside a folder a display them using pandas as a DataFrame table

# add the function of increasing the dimensions of the window by dragging the corners!!