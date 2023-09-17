# -*- coding: utf-8 -*-
'''
@author: Mike.Pack
'''

from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5 import uic
import sys, os
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal

sys.path.append('../')

from LP.LPThreadTest import LPThreadTest as LPT
from View.Messages import Messages as msg
from View.Done import Done as dn


#===============================================================================
# CompleteTest Diese Klasse ruft das Framework auf, mit dem alle Varianten des 
# LPA getestet werden. 
#
# ACHTUNG: Alle Testlaufen zu lassen kann mehrere Stunden bis Tage in 
# Anspruch nehmen, je nach Graphen und Anzahl Testläufe. 
#===============================================================================
class CompleteTest(QDialog):
    data_path = "../"
    ui_folder = Path("../UI/TestAll.ui")
    send_Data = pyqtSignal(tuple, int, int, list)
    def __init__(self, parent): 
        super(CompleteTest, self).__init__(parent)
        self.ui = uic.loadUi(self.ui_folder, self)
        
        self.ui.btn_openFile.clicked.connect(self.openFiles)
        self.set_files(None)
        self.msg_ = msg(self)
        self.pThread = LPT()
        self.thread2 = QThread()
        self.ui.btn_Start.clicked.connect(self.testing)
        self.Done_ = dn(self)

        self.send_Data.connect(self.pThread.runTest)
        self.pThread.values.connect(self.updateP)

        self.pThread.moveToThread(self.thread2)
        self.thread2.start()

    def get_files(self):
        return self.__files


    def set_files(self, value):
        self.__files = value


    def del_files(self):
        del self.__files

    files = property(get_files, set_files, del_files, "files's docstring")
    
    
    
    #===========================================================================
    # openFiles öffnet die Datei zum Testen
    #===========================================================================
    def openFiles(self):
        g_filter = "GraphML (*.graphml)"
        dsc = "Open File"
        path = self.data_path
        file_name = QFileDialog.getOpenFileNames(self, dsc, path, g_filter)[0]
        
        # no file is selected so return 
        if(file_name == []):                 
            return
        else:
            # clear the list of files
            self.ui.GraphList.clear()
            for n in file_name:
                self.ui.GraphList.addItem(os.path.basename(n))
            self.set_files(file_name)
            
    
    #===========================================================================
    # testing führt den Algorithmus aus und durchläuft alle Varianten des LAP
    # 
    # Bei der Wahl mehrere Dateien, werden alle Daten in eine Datei geschrieben.
    #===========================================================================
    def testing(self):
        if(self.get_files() == None):
            self.msg_.exec_()
            return
        else:
            txt_filter ="CSV (*.csv)"
            dsc = "Save File"
            path = self.data_path
            option = QFileDialog.Options()
            name = QFileDialog.getSaveFileName(self, dsc, path, txt_filter, options = option)
            self.send_Data.emit(name, self.ui.sb_MaxIter.value(), self.ui.sb_MaxTest.value(), self.get_files())

            
    #===========================================================================
    # updateP Führt eine Aktualisierung der ProgressBar durch um den Fortschritt zu
    # zeigen.
    # Wurde der komplette Test abgeschlossen, wird der Nutzer darüber Informiert.
    #===========================================================================
    def updateP(self, counter, p):
        self.progressBar.setValue(counter* p)
        progress = counter* p
        if(progress >= 100):
            self.Done_.exec_()
            self.progressBar.setValue(0)
