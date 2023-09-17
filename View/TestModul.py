# -*- coding: utf-8 -*-
'''
@author: Mike.Pack
'''

from PyQt5.QtWidgets import QFileDialog, QDialog, QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys, os, csv, time
import networkx as nx
import matplotlib.pyplot as plt
from itertools import count
from pathlib import Path

from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
from asyncio.tasks import wait

sys.path.append('../')

from Helper.LPAConstants import Constant as LPAC
from Helper.Helper import HelperMethod as hm

from View.Messages import Messages as msg
from View.Done import  Done as dn
from LPThread.LPA import LP
#from View.FullyTest import runAll as ra
from View.CompleteTest import CompleteTest as ra
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

#===============================================================================
# RunTest Dieses ist die Hauptklasse des Frameworkes. 
# Neben den Einstellungen wie der Algorithmus ausgeführt wird, wird hier rüber
# der Graph Visualisiert, es erfolgt eine Darstellung der Daten in Form einer
# Tabelle und zusätzlich ist es möglich den Graphen wie auch die Tabelle 
# zu speichern. 
#
#===============================================================================
class RunTest(QMainWindow):
    data_folder = "../"
    ui_folder = Path("../UI/RunTest22.ui")
    max_row_Count = 100000

    send_fig = pyqtSignal(nx.Graph, int, int, str, str, str, int,  bool, bool, bool, int, int)
    def __init__(self):
        super(RunTest, self).__init__()      

        self.ui = uic.loadUi(self.ui_folder, self)
        self.set_files(None)
        self.ui.btn_openFile.clicked.connect(self.openFiles)
        self.modula = []
        self.set_mod(self.modula)
        self.msg_ = msg(self)
        self.Done_ = dn(self)
        self._color_index = 0
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar(self.canvas, self))     
        layout.addWidget(self.canvas)
        self.widget.setLayout(layout)     

        self.tabWidget.setTabText(0, "Setup")
        self.tabWidget.setTabText(1, "Table View")
        self.ui.btn_save.clicked.connect(self.saveFile)
        self.ui.btn_LPA.clicked.connect(self.defaultLPA)
        
        self.set_gnMod(None)
        
        self.plotter = LP()
        self.thread = QThread()
        self.ui.btn_run.clicked.connect(self.run_Algo)
        self.send_fig.connect(self.plotter.LP_Sync1) 
        self.plotter.return_update.connect(self.updateGraphic)
        #self.plotter.return_exit.connect(self.gn)
        self.plotter.noVisual.connect(self.justTesting)
        self.plotter.progress.connect(self.updateProgess)
        
        #move to thread and start
        self.plotter.moveToThread(self.thread)
        self.thread.start()
        
        self.ui.btn_Stop.clicked.connect(self.stop)
        self.ui.btn_Step.clicked.connect(self.step)
        self.ui.btn_Pause.clicked.connect(self.pause)
        self.ui.btn_saveTable.clicked.connect(self.handleSave)
        
        self.ui.rb_Random_2.clicked.connect(self.kActive)
        self.ui.rb_Unique_2.clicked.connect(self.kInactive)
        
        
        self.ui.rb_MaxIter.clicked.connect(self.iterActive)
        self.ui.rb_Stabil.clicked.connect(self.iterInactive)
        
        self.ui.rb_noVisual.clicked.connect(self.testActive)
        self.ui.rb_visual.clicked.connect(self.testInactive)
    
        
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 50)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setColumnWidth(6, 100)
        self.tableWidget.setColumnWidth(7, 150)
        self.tableWidget.setColumnWidth(8, 150)
        self.tableWidget.setColumnWidth(9, 150)
        self.tableWidget.setColumnWidth(10, 150)
        self.tableWidget.setColumnWidth(11, 150)
        self.tableWidget.setColumnWidth(12, 150)
        self.tableWidget.setColumnWidth(13, 150)
        #self.tableWidget.setColumnWidth(14, 150)
        self.tableWidget.setHorizontalHeaderLabels(["Graph", "Mode", "Initialize", "K", "Update Order", "Neighbor", "Label Sel.", "Convergence Rule", "Modularity", "Best Modularity", "Convergence", "Iterations", "Compare with", "Modularity"])
        self.tableWidget.setRowCount(self.max_row_Count)
        
        self.fullTest = ra(self)
        
        self.ui.btn_RunAll.clicked.connect(self.runCompact)

    def get_md(self):
        return self.__md


    def set_md(self, value):
        self.__md = value


    def del_md(self):
        del self.__md


    def get_iteration(self):
        return self.__iteration


    def set_iteration(self, value):
        self.__iteration = value


    def del_iteration(self):
        del self.__iteration

    
    def set_p(self, p):
        self._p = p
    def get_p(self):
        return self._p
    
      
    def updateProgess(self, count):
        self.progressBar.setValue(count)
        self.set_p = False
    
    def kActive(self):
        self.ui.sb_K_2.setEnabled(True)
            
    def kInactive(self):
        self.ui.sb_K_2.setEnabled(False)
        
    def iterActive(self):
        self.ui.sb_MaxIter.setEnabled(True)
            
    def iterInactive(self):
        self.ui.sb_MaxIter.setEnabled(False)
    
    def testActive(self):
        self.ui.sb_MaxTest.setEnabled(True)
            
    def testInactive(self):
        self.ui.sb_MaxTest.setEnabled(False)
     
    def runCompact(self):
        
        self.fullTest.exec_()
    
       
    #===========================================================================
    # openFiles Öffnet die jeweiligen graphml Datei und ruft die Funktion auf
    # damit eine Darstellung des Graphen erfolgt. 
    # Zus�tzlich wird der Algorithmus auf Standard zurück gesetzt, sodass
    # immer der klassische LPA Eingestellt ist. 
    #
    # Zusätzlich werten sämtliche Werte aus verherigen Testläufen auf Null gesetzt.
    #===========================================================================
    def openFiles(self):
        filter = "GraphML (*.graphml)"#;;GML (*.gml);;GEFX (*.gexf)"  # @ReservedAssignment
        dsc = "Open File"
        path = self.data_folder
        file_name, _ = QFileDialog.getOpenFileName(self, dsc, path, filter)
        
        # no file is selected so return 
        if(file_name == ""):          
            return
        else:
            # clear the list of files
            #print(file_name, " ", file_name[0])
            
            self.ui.GraphList.clear()
            #for n in file_name:
            self.ui.GraphList.addItem(os.path.basename(file_name))
            self.set_files(file_name)
            self.set_FileName(os.path.basename(file_name))
            #print(self.get_FileName())
            
            graph = self.plotGraph(file_name)
            self.set_graph(graph)
            self.modula =[]
            self.set_mod(self.modula)
            self.defaultLPA()
            #self.reset_Setup()
            self.setStartValues()
            self.gn(True)

    #===========================================================================
    # setStartValues Setzt alle Werte zurück auf den Standard
    #===========================================================================
    def setStartValues(self):
        self.set_DataIter(0)        
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(self.max_row_Count)
        self.set_avgM(None)
        self.set_lastMod(None)
        self.set_Pause(False)
        self.set_Step(False)
        self.set_newRun(True)

    #===========================================================================
    # saveFile Speichert den aktuellen Graphen nachdem der LPA ausgeführt wurde
    # als Graph Datei ab. Zur Auswahl stehen hier .graphml, .gml sowie gexf
    #===========================================================================
    def saveFile(self):     
        Ffilter ="GraphML (*.graphml);;GML (*.gml);;GEXF (*.gexf)"
        dsc = "Save Graph File"
        path = self.data_folder
        option = QFileDialog.Options()
        name = QFileDialog.getSaveFileName(self, dsc, path, Ffilter, options = option)
        if(name == []):
            return
        if(name[0].endswith(".graphml")):
            nx.write_graphml(self.get_graph(), name[0], encoding='utf-8', prettyprint=True)
        if(name[0].endswith(".gml")):
            nx.write_gml(self.get_graph(), name[0])
        if(name[0].endswith(".gexf")):
            nx.write_gexf(self.get_graph(), name[0])
      
    #===========================================================================
    # handleSave Speichert die Tabelle mit den Ergebnisse als .csv Datei ab
    #===========================================================================
    def handleSave(self):
        path = QFileDialog.getSaveFileName(
                self, 'Save Table', '', 'CSV(*.csv)')   
        try:
            f = open(path[0], 'w', encoding='UTF8', newline='')
        except FileNotFoundError:
            return
        header = []
        for j in range(self.tableWidget.model().columnCount()):
            header.append(self.tableWidget.horizontalHeaderItem(j).text())

        writer = csv.writer(f)
        writer.writerow(header)
        for row in range(self.tableWidget.rowCount()):
            header = []
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item is not None:
                    header.append(item.text())
            writer.writerow(header)

    
    #===========================================================================
    # writeData Schreibt die Ergebnisse eines Testlaufes in die Tabelle des Frameworks
    #====================== =====================================================
    def writeData(self, i):
        #print(self.get_AlgoVersion().value)
        self.tableWidget.setItem(i, 0, QTableWidgetItem(self.get_FileName()))
        self.tableWidget.setItem(i, 1, QTableWidgetItem(self.get_AlgoVersion().value))
        self.tableWidget.setItem(i, 2, QTableWidgetItem(self.get_AlgoLabels().value))
        self.tableWidget.setItem(i, 3, QTableWidgetItem(str(self.get_AlgoK())))
        self.tableWidget.setItem(i, 4, QTableWidgetItem(self.get_AlgoOrder()))
        self.tableWidget.setItem(i, 5, QTableWidgetItem(self.get_AlgoNbr()))
        self.tableWidget.setItem(i, 6, QTableWidgetItem(self.get_AlgoLS().value))
        self.tableWidget.setItem(i, 7, QTableWidgetItem(self.get_AlgoConv()))
        self.tableWidget.setItem(i, 8, QTableWidgetItem(str(self.get_lastMod())))
        self.tableWidget.setItem(i, 9, QTableWidgetItem(str(self.get_bestMod())))
        self.tableWidget.setItem(i, 10, QTableWidgetItem(str(self.get_conv())))
        #self.tableWidget.setItem(i, 11, QTableWidgetItem(str(self.get_nmi())))
        self.tableWidget.setItem(i, 11, QTableWidgetItem(str(self.get_iteration())))
        self.tableWidget.setItem(i, 12, QTableWidgetItem("Greedy Modularity"))
        self.tableWidget.setItem(i, 13, QTableWidgetItem(str(self.get_gnMod())))
        
        
    #===========================================================================
    # plotGraph Diese Funktion führt die Visualisierung des Graphen in der UI durch 
    # 
    # 
    # Input:
    # fileName: Der Name der Datei die eingelesen wurde 
    #
    # return: Liefert als Ergebniss den Graphen g zurück
    #===========================================================================
    def plotGraph(self, fileName):
            self.set_File(fileName)
            self.figure.clf()
            plt.subplot(211)
            graph = nx.read_graphml(fileName)            
            graph = nx.DiGraph.to_undirected(graph)#, as_view = True)
            graph.remove_edges_from(nx.selfloop_edges(graph))
            graph.remove_nodes_from(list(nx.isolates(graph)))
            
            #self.set_pos(nx.fruchterman_reingold_layout(graph))
            self.set_pos(nx.fruchterman_reingold_layout(graph))
            #self.set_pos(nx.spring_layout(graph))   
            nx.draw(graph, pos = self.get_pos(), node_size = LPAC._NODE_SIZE.value, width =1)
            plt.subplot(212)
            self.canvas.draw_idle()          
            G = graph
            return G          
    


    #===========================================================================
    # setupAlgo Mit dieser Funktion werden die Einstellungen gespeichert, wie 
    # der Algorithmus ausgeführt werden soll. 
    #
    #===========================================================================
    def setupAlgo(self):
        self.set_MaxIter(self.ui.sb_MaxIter.value())
        self.set_MaxTest(self.ui.sb_MaxTest.value())
        
        if(self.ui.rb_Unique_2.isChecked()):
            labels = [LPAC._UNIQUE]
            k = [1]   
        if(self.ui.rb_Random_2.isChecked()):
            labels = [LPAC._RANDOM]
            k = [self.ui.sb_K_2.value()]

        if(self.ui.rb_Hop0.isChecked()):
            neighbors = [0]
            self.set_AlgoNbr("Incl. Self")
        if(self.ui.rb_Hop1.isChecked()):
            neighbors = [1]
            self.set_AlgoNbr("Only Nbr")
        if(self.ui.rb_Hop2.isChecked()):
            neighbors = [2]
            self.set_AlgoNbr("Nbr plus Nbr of Nbr")
        if(self.ui.rb_Hop02.isChecked()):
            neighbors = [3]
            self.set_AlgoNbr("Nbr plus Nbr of Nbr incl. self")
        if(self.ui.rb_RLabel.isChecked()):
            label_selection = [LPAC._RANDOM]        
        if(self.ui.rb_SLabel.isChecked()):
            label_selection = [LPAC._SELF]
        if(self.ui.rb_first.isChecked()):
            label_selection = [LPAC._FIRST]
        if(self.ui.rb_Last.isChecked()):
            label_selection = [LPAC._LAST]
        if(self.ui.rb_Median.isChecked()):
            label_selection = [LPAC._MEDIAN]
        
        if(self.ui.rb_Stabil.isChecked()):
            convergence = [True]
            self.set_AlgoConv("Stable")
        if(self.ui.rb_MaxIter.isChecked()):
            convergence = [False]
            self.set_AlgoConv("Max Iteration")
        if(self.ui.rb_sync.isChecked()):
            version = [LPAC._SYNC]
        if(self.ui.rb_async.isChecked()):
            version = [LPAC._ASYNC]
                
        if(self.ui.rb_Fixed.isChecked()):
            order = [False]
            self.set_AlgoOrder("Fixed Order")
        if(self.ui.rb_Rnd.isChecked()):
            order = [True]
            self.set_AlgoOrder("Shuffle Order per Iter")
        
        if self.ui.rb_visual.isChecked():
            self.set_Visual(True)
        if self.ui.rb_noVisual.isChecked():
            self.set_Visual(False)
            
        self.set_AlgoK(k[0])      
        self.set_AlgoLabels(labels[0])
        self.set_AlgoLS(label_selection[0])
        
        self.set_AlgoVersion(version[0])
        return labels, k, version, neighbors, label_selection, convergence, order
    
    
    #===========================================================================
    #
    #
    #===========================================================================
    def set_AlgoLS(self, aLS):
        self._aLS = aLS
    def get_AlgoLS(self):
        return self._aLS

    def set_DataIter(self, dI):
        self._dI = dI
    def get_DataIter(self):
        return self._dI

    def set_AlgoConv(self, aConv):
        self._aConv = aConv
    def get_AlgoConv(self):
        return self._aConv
    
    def set_AlgoOrder(self, aOrder):
        self._aOrder = aOrder
    def get_AlgoOrder(self):
        return self._aOrder
    
    def set_FileName(self, fileN):
        self._fileN = fileN
    def get_FileName(self):
        return self._fileN

    def set_newRun(self, newRun):
        self._newRun = newRun
    def get_newRun(self):
        return self._newRun

    def set_Visual(self, vis):
        self._vis = vis
    def get_Visual(self):
        return self._vis

    def set_AlgoLabels(self, aLabels):
        self._aLabels = aLabels
    def get_AlgoLabels(self):
        return self._aLabels
    
    def set_AlgoK(self, ak):
        self._ak = ak
    def get_AlgoK(self):
        return self._ak
    
    def set_AlgoVersion(self, aVersion):
        self._aVersion = aVersion
    def get_AlgoVersion(self):
        return self._aVersion
    
    def set_AlgoNbr(self, aNbr):
        self._aNbr = aNbr
    def get_AlgoNbr(self):
        return self._aNbr
    
    
    #===========================================================================
    # run_Algo Mit dieser Funktion wird der eigentliche LPA gestartet
    # Hier werden unter anderem weitere Variablen zunächst auf die
    # Default Einstellungen gesetzt bevor der LPA ausgeführt wird. 
    #===========================================================================
    def run_Algo(self):     
        # if no file is selected a Error UI will be shown
        if(self.get_files() == None):
            self.msg_.exec_()
            return 
        else:
            # Start the algorithm
            if(self.get_newRun() == True):
                self.plotter.resume()
                self.plotter.kill()
                time.sleep(1)
                self.canvas.figure.clf()
                self.set_Pause(False)
                self.set_Step(False)
                self.set_newRun(False)
                labels, k, version, neighbors, label_selection, convergence, order = self.setupAlgo()
                n = 1
                if (self.get_Visual() == False): 
                    n = self.get_MaxTest()
                for it in range(n):
                    self.send_fig.emit(self.get_graph(), k[0], self.get_MaxIter(),version[0].value, labels[0].value, label_selection[0].value, neighbors[0], convergence[0], order[0], self.get_Visual(), it, n)
            if(self.get_Pause() == True):
                self.set_Pause(False)
                self.plotter.resume()
            if(self.get_Step() == True):
                self.plotter.stepping()
            if(self.get_newRun() == False):
                self.plotter.resume()
         
          
        
    #===========================================================================
    # gn Führt zum Vergleich der Modularität den Greedy Modularity Algorithmus aus
    #===========================================================================
    def gn(self, bool):

        c = list(greedy_modularity_communities(self.get_graph()))
        
        mod = nx_comm.modularity(self.get_graph(), c) 
        self.set_gnMod(mod)
    
    
    
        
    #===========================================================================
    # updateGraphic In dieser Funktion wird der Graph nachdem eine Iteration abgeschlossen
    # wurde erneut in dem UI gezeichnet, um die Entwicklung der Labels zu zeigen.
    #
    # Input:
    # graph Der aktuelle Graph
    # labels: Die aktuellen Labels des Graphen
    # modul: Die Modularität der Community Einteilung des aktuellen Graphen
    # conv: Wert ob eine Konvergenz vorliegt oder nicht. 
    # Liegt Konvergenz vor so wird der Algorithmus nach dem Update
    # beendet
    # c: Liegt Konvergenz vor wird der entsprechende Wert in einem String gespeichert
    # iterations: Enthält die Anazahl an Iterationen die bislang durchlaufen wurden
    #===========================================================================
    def updateGraphic(self, graph, labels, modul, conv, c, iterations):
        
        self.set_iteration(iterations +1)
        self.plotter.pause()
        self.canvas.figure.clf()
        self.set_avgM(modul)
        self.set_graph(graph)
        plt.subplot(211)
        groups = set(nx.get_node_attributes(graph,'Community-ID').values())
        mapping = dict(zip(sorted(groups),count()))
        nodes = graph.nodes()
        colors = [mapping[graph.nodes[n]['Community-ID']] for n in nodes]
 
        nx.draw(graph, pos = self.get_pos(), labels = labels, node_color= colors,  node_size = 125, width =1, cmap=plt.set_cmap("gist_rainbow"))
        plt.subplot(212)
        str_AvgMod = str("Average Modularity after " + str(len(modul)) + " runs")
        #str_AvgMod1 = str("Setup: " + version[i].value)
        plt.plot(modul, marker="x", label=str_AvgMod)
        plt.ylabel("Modularity Q", size=10, labelpad=5)
        plt.xlabel("Iterations " + self.get_FileName(), size=10, labelpad=5)
        plt.grid(True)
        self.set_lastMod(modul[-1])

        
        #plt.subplot(224)
        
        
        #md = self.get_mod()
        #print(self.get_mod())
        #if(len(md) == 3):
        #    bu = []
        #    bu.append(md[-2])
        #    bu.append(md[-1])
        #    bu.append(self.get_mod())
        #    md.clear()
            
        #    md = bu
        #    self.set_mod(bu)
        
        #for i in range(len(md)):
            
        #    str_AvgMod = str("Modularity after " + str(len(md[i])) + " runs")
        #    plt.plot(md[i], marker="x", label=str_AvgMod)
        #    plt.ylabel("Modularity Q", size=10, labelpad=5)
        #    plt.xlabel("Iterations " + self.get_FileName(), size=10, labelpad=5)
        #    plt.grid(True)
        self.set_bestMod(max(modul))
        
        self.canvas.draw()
        self.canvas.flush_events()
        self.set_Labels(labels)
        print("update ")
        if(self.get_Step() == True):
            
            self.plotter.stepping()
            self.set_Step(False)
        else:
            self.plotter.resume()
            
        if(c == False):
            self.set_conv("No Convergence")
        else:
            self.set_conv("Convergence")
        if(conv == False):
            self.stop()
            #self.Done_.exec_()
        

    #===========================================================================
    # justTesting Diese Funktion wird ausgef�hrt, wenn keine Visualisierung des
    # Graphen erwünscht wird. 
    # Dient dem schnellen Erheben von Daten mittels dem Framework
    #
    # Input: 
    # graph: Der aktuelle Graph
    # labels: Die aktuellen Label des Netzwerkes
    # modul: Die aktuelle Modularität der Community Einteilung
    # conv: Liegt Konvergenz vor oder nicht
    # c: Wenn Konvergenz vorliegt wird ein entsprechender String f�r die Tabelle erzeugt
    # iterations: Entspricht der Anzahl an maximalen Iterationen
    #
    #===========================================================================
    def justTesting(self, graph, labels, modul, conv, c, iterations):
        self.set_iteration(iterations +1)
        self.plotter.pause()
        self.set_lastMod(modul[-1])
        self.set_bestMod(max(modul))
        self.set_nmi(hm.calcNMI(self, self.get_graph()))
        if(c == False):
            self.set_conv("No Convergence")
        else:
            self.set_conv("Convergence")
        self.writeData(self.get_DataIter())
        self.set_DataIter(self.get_DataIter()+1)
        
        #print(modul, self.get_lastMod(), self.get_bestMod(), self.get_nmi())
        self.set_newRun(True)
        self.plotter.resume()
    

    #===========================================================================
    # stop will stop the thread and set the graph to standart
    #===========================================================================
    def stop(self):
        if(self.get_files() == None):
            self.msg_.exec_()
            return 
        else:
            self.plotter.resume()
            self.plotter.kill()
            time.sleep(1)
            self.set_Pause(False)
            self.modula.append(self.get_avgM())
            
            self.set_mod(self.modula)
            self.set_nmi(hm.calcNMI(self, self.get_graph()))
            #self.gn(True)
            self.writeData(self.get_DataIter())
            self.set_DataIter(self.get_DataIter()+1)
            self.set_newRun(True)
            time.sleep(0.1)
            self.Done_.exec_()
        
        #========================== Thread Options =================================   
    #===========================================================================
    # pause will stop the LPThread
    #===========================================================================
    def pause(self):
        if(self.get_files() == None):
            self.msg_.exec_()
            return 
        else:
            self.plotter.pause()
            self.set_Pause(True)
    
    
    #===========================================================================
    # step Allows to run the LPThread step by step
    #===========================================================================
    def step(self):
        if(self.get_files() == None):
            self.msg_.exec_()
            return 
        else:
            self.plotter.pause()
            self.set_Step(True)
            self.run_Algo()
       
    def defaultLPA(self):
        self.ui.rb_sync.toggle()
        self.ui.rb_Unique_2.toggle()
        self.ui.sb_K_2.setEnabled(False)
        self.ui.sb_K_2.setValue(1)
        self.ui.rb_Rnd.toggle()
        
        self.ui.rb_Hop1.toggle()
        self.ui.rb_RLabel.toggle()
        self.ui.rb_Stabil.toggle()
        self.ui.sb_MaxIter.setValue(5)
        self.ui.sb_MaxIter.setEnabled(False)
    
    
    #===========================================================================
    # drawingGraph if the thread is stop this will redraw the graph
    #===========================================================================
    def drawingGraph(self):
        nx.draw(self.get_graph(), pos = self.get_pos(), labels = self.get_Labels(),  node_size = 125, width = 1)
        self.canvas.draw()
            
    def set_graph(self, graph):
        self._graph = graph
    def get_graph(self):
        return self._graph
    
    def set_nmi(self, nmi):
        self._nmi = nmi
    def get_nmi(self):
        return self._nmi
      
    def set_lastMod(self, m):
        self._m = m
    def get_lastMod(self):
        return self._m
    
    def set_bestMod(self, bestMod):
        self._bestMod = bestMod
    def get_bestMod(self):
        return self._bestMod    

    def set_Labels(self, lab):
        self._labs = lab
    def get_Labels(self):
        return self._labs
  
    def get_Edgecolor(self):
        return self._edgeColor 
    
    def set_Edgecolor(self, edgeColor):
        self._edgeColor = edgeColor  
  
    def set_avgM(self, modularity):
        self._modularity = modularity
    def get_avgM(self):
        return self._modularity
    
    def set_mod(self, mod):
        self.mod = mod
    def get_mod(self):
        return self.mod
    
    def set_File(self, text):
        self._text = text
    
    def get_File(self):
        return self._text
    
    def set_pos(self, pos):
        self._pos = pos
    
    def get_pos(self):
        return self._pos   

    def set_files(self, files):
        self._files = files    
        
    def get_files(self):
        return self._files
    
    def set_Pause(self, pause):
        self._pause = pause
    def get_Pause(self):
        return self._pause
    
    def set_Step(self, step):
        self._step = step
    def get_Step(self):
        return self._step    
    
    def set_MaxIter(self, maxIter):
        self.maxIter = maxIter
        
    def get_MaxIter(self):
        return self.maxIter
    
    def set_MaxTest(self, maxTest):
        self.maxTest = maxTest
        
    def get_MaxTest(self):
        return self.maxTest
    
    def set_gnMod(self, gnMod):
        self.gnMod = gnMod
        
    def get_gnMod(self):
        return self.gnMod
    
    def set_conv(self, conv):
        self.conv = conv
        
    def get_conv(self):
        return self.conv
    iteration = property(get_iteration, set_iteration, del_iteration, "iteration's docstring")
    md = property(get_md, set_md, del_md, "md's docstring")
    
def main():
    app = QApplication(sys.argv)
    view = RunTest()
    view.show()
    
    
    sys.exit(app.exec_())
    
    app.deleteLater()
    #LP.exit()
    
    
if __name__ == "__main__":
    main()