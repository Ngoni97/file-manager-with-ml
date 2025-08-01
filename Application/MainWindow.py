# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Admin\Documents\File Manager with ML\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 591)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 801, 531))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeView = QtWidgets.QTreeView(self.gridLayoutWidget)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView, 0, QtCore.Qt.AlignLeft)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 532, 351, 31))
        self.progressBar.setProperty("value", 19)
        self.progressBar.setObjectName("progressBar")
        self.start_Button = QtWidgets.QPushButton(self.centralwidget)
        self.start_Button.setGeometry(QtCore.QRect(530, 540, 93, 28))
        self.start_Button.setObjectName("start_Button")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.start_Button)
        self.finish_Button = QtWidgets.QPushButton(self.centralwidget)
        self.finish_Button.setGeometry(QtCore.QRect(710, 540, 93, 28))
        self.finish_Button.setObjectName("finish_Button")
        self.buttonGroup.addButton(self.finish_Button)
        self.stop_Button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_Button.setGeometry(QtCore.QRect(620, 540, 93, 28))
        self.stop_Button.setObjectName("stop_Button")
        self.buttonGroup.addButton(self.stop_Button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionRecent = QtWidgets.QAction(MainWindow)
        self.actionRecent.setObjectName("actionRecent")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionKeyboard_Shortcuts = QtWidgets.QAction(MainWindow)
        self.actionKeyboard_Shortcuts.setObjectName("actionKeyboard_Shortcuts")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionRecent)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuSettings.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionKeyboard_Shortcuts)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_Button.setText(_translate("MainWindow", "Start"))
        self.finish_Button.setText(_translate("MainWindow", "Finish"))
        self.stop_Button.setText(_translate("MainWindow", "Stop"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionRecent.setText(_translate("MainWindow", "Recent"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionKeyboard_Shortcuts.setText(_translate("MainWindow", "Keyboard Shortcuts"))
#import icons_resources_file_rc
"""
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QTreeView, 
    QFileSystemModel,
    QMainWindow)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwarsg):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # creating the QFileDialog widget
        """
