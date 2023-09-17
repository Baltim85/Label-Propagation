# -*- coding: utf-8 -*-
from PyQt5.Qt import QDialog
from PyQt5 import uic
import sys

sys.path.append('../')


#===============================================================================
# Done Wird ausgeführt, wenn die Berechnung des Graphen abgeschlossen wurde,
# oder wenn die Berechnung abgebrochen wurde.
#===============================================================================
class Done (QDialog):
    def __init__(self, parent):
        super(Done, self).__init__(parent)     
        self.ui = uic.loadUi("..\\UI\\Beendet.ui", self)
        self.ui.btnOk.clicked.connect(self.close)
        
    def run(self):
        self.show()
    
    def clo(self):
        self.close()