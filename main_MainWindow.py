"""
Author: Ngonidzashe
date initialised: 2024/09/28 (the initial date of the project commencement)
date modified: 2024/10/31 
"""
# Main Application

# import from the different separate customised modules

import sys
import os
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    )

# use this code after compiling the application
from Pop_up_window_3 import Ui_MainWindow
"""
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
"""

class PopUpMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(PopUpMainWindow, self).__init__(*args, **kwargs)
        #uic.loadUi('Pop-up_window.ui', self)
        self.setupUi(self)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('brown'))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # curent setFontFamily & setPointSize used upon opening the application
        self.font = QFont() # I referenced the font as self.font for future updating
        self.font.setFamily("Consolas")
        self.font.setPointSize(11)
        self.textEdit.setFont(self.font)

        self.fontComboBox.setCurrentFont(self.font)
        # link this with the QFontComboBox current font
        # also link the font point size with the QSpinBox current value

        # connecting buttons
        self.clear_button.clicked.connect(self._clear) # clear button
        self.ok_button.clicked.connect(self._Ok) # OK button
        self.cancel_button.clicked.connect(self._Cancel) # Cancel button

        # connecting the spinbox to the fontpointsize
        self.spinBox.valueChanged.connect(self._font_size)
        
        # setting the current font
        self.fontComboBox.currentFontChanged.connect(self._current_font)

    def _clear(self):
        self.textEdit.clear()

    def _Ok(self):
        """ Trigger the process of sorting and link it with the progress bar """
        # below is the debugging code
        if os.path.exists("/text_document.txt"):
            with open("text_document.txt", 'a') as file:
                file.write(str(self.textEdit.toPlainText()))
        else:
            with open("text_document.txt", 'w+') as file:
                file.write(str(self.textEdit.toPlainText()))
            
    def _Cancel(self):
        self.close()

    def _font_size(self, value):
        #print('font size changed')
        # update the current font point size
        self.font.setPointSize(int(value))
        self.textEdit.setFont(self.font)
        
    def _current_font(self, value):
        # update the current font
        #print('font changed')
        self.font = value
        self.textEdit.setFont(self.font) # changing the current font
        #self.textEdit.currentFont()

if __name__ == "__main__":   
    App = QApplication(sys.argv)
    window = PopUpMainWindow()
    # adding styling
    App.setStyle('Fusion')
    window.show()
    sys.exit(App.exec_())

# enabled pasting in the QTextEdit
# save current settings to an external text file,
# so that upon opening the application you run it and populate the Ui with the settings
# update the file whenever the current settings are changed whilest running the application

# ! ! ! ! ! ! ! !
# trying to fix the problem of relapsing to the current fontFamily and current font size whenever
# I try to clear the entry field using the backspace button


######
# must update the initial values for fontComboBox, fontSpinBox,
