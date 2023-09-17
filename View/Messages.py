# -*- coding: utf-8 -*-
'''
@author: Mike.Pack
'''
from PyQt5.Qt import QDialog
from PyQt5 import uic
import sys

sys.path.append('../')

#===============================================================================
# Messages Wird angezeigt, wenn keine Datei ausgewählt wurde und der Algorithmus 
# ausgeführt werden soll. 
#===============================================================================
class Messages (QDialog):
    def __init__(self, parent):
        super(Messages, self).__init__(parent)     
        self.ui = uic.loadUi("..\\UI\\NoFile.ui", self)
        self.ui.btnOk.clicked.connect(self.close)
        
    def run(self):
        self.show()
    
    def clo(self):
        self.close()