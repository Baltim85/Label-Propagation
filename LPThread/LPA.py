# -*- coding: utf-8 -*-
'''
@author: Mike.Pack
'''
# coding: utf8

from copy import deepcopy
import random, math, time, sys

from random import randrange
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
import numpy as np
import networkx as nx

sys.path.append('../')
from Helper.LPAConstants import Constant as LPAC
from Helper.LPAMethods import LPAMethods as LPAM

#===============================================================================
# LP (QThread)
#
# Mit dieser Klasse wird der LPA für das Framework als Thread ausgeführt. Dadurch wird 
# ein Freeze der UI unterdrückt. Sämtliche Funktionen die das Programm für die Ausführung
# benötigt finden sich im Package: Helper.LPAMethods
#
#===============================================================================
class LP(QThread):
    # Setup the signals for the main class to visualize the updates after a node was selected
    return_data = pyqtSignal(np.ndarray, dict, str, np.ndarray, nx.Graph)
    return_nodes = pyqtSignal(np.ndarray, dict, str, nx.Graph, str)
    return_update = pyqtSignal(nx.Graph, dict, list, bool, bool, int)
    #return_exit = pyqtSignal(bool)
    noVisual = pyqtSignal(nx.Graph, dict, list, bool, bool, int)
    progress  = pyqtSignal(int)
    
    
    _pause = False
    isKilled = False
    delay = 0.8
    

    #===========================================================================
    # nodesOrder setup the order for the nodes at the beginning.
    #
    # Imput: 
    # graph (nx.Graph) der aktuelle Graph
    # nodes: Die Knoten des Graphen
    # order: Die Reihenfolge wie die Knoten zu Beginn angeordnet werden
    #
    # rule: How the label are set at the beginning
    # k (int):The number for the random choose if rule is Random
    #
    # return: nodes and labels for the graph 
    #===========================================================================
    def nodesOrder(self, graph, nodes, order, rule,k):
        if (order == LPAC._RANDOM.value):
            return random.shuffle(nodes)
        if(order == LPAC._DEC.value):
            degree = dict(sorted(dict(graph.degree).items(), key = lambda item : item[1]))        
            nodes = np.array(list(degree.keys()))
            labs = dict(zip(nodes, range(graph.number_of_nodes())))
            if (rule == LPAC._RANDOM.value):
                labs = {}
                for i in range(len(graph.nodes)):
                    labs[nodes[i]] = randrange(math.floor(k*(np.log2(len(graph.nodes)))))
            return nodes, labs
        if (order == LPAC._INC.value):
            degree = dict(sorted(dict(graph.degree).items(), key = lambda item : item[1], reverse = True))        
            nodes = np.array(list(degree.keys()))
            labs = dict(zip(nodes, range(graph.number_of_nodes())))
            if (rule == LPAC._RANDOM.value):
                labs = {}
                for i in range(len(graph.nodes)):
                    labs[nodes[i]] = randrange(math.floor(k*(np.log2(len(graph.nodes)))))
            return nodes, labs
    
    
    

    #===========================================================================
    # Getter and Setter Methods for the class
    #===========================================================================
    def set_Labels(self, lab):
        self._labs = lab
    def get_Labels(self):
        return self._labs
    
    def pause(self):
        self._pause = True
    
    def resume(self):
        self._pause = False
        #time.sleep(0.01)
        #self._pause = True

    def stepping(self):
        if(self._pause == True):
            self._pause = False
            #print("stepping", self._pause)
            time.sleep(0.0001)
            self._pause = True
            #print("stepping", self._pause)
        else:
            self._pause = True
            #print("stepping", self._pause)
    def kill(self):
        self.isKilled = True
    
    def set_Pause(self, pause):
        self._pause = pause
    def get_Pause(self):
        return self._pause
    
    
    #===========================================================================
    # plot_Neighbors This function is be needed to show from which node the node i 
    # is taken the label
    # 
    # Input: 
    # np_nbr: The neighbors of the node i
    # labels: The labels of every node
    # node: The node itself
    # np_nodes: Each node of the graph 
    # newLabels: The new Label of the node
    # graph (nx.Graph) the actual Graph
    # labelsNew: Is needed for the Asycn version to update the actual label directly
    #===========================================================================
    def plot_Neighbors(self, np_nbr, labels, node, np_nodes, graph, labelsNew):
        for ij in np_nbr:
            if(labels[ij] == labelsNew[node]):
                time.sleep(self.delay)
                if(self.isKilled == True):
                    break
                while self._pause:
                    time.sleep(0)
                
                # sends a signal to the main Window to draw the new nodes
                self.return_nodes.emit(np_nodes ,self.get_Labels(), node, graph, ij)
                while self._pause:
                    time.sleep(0)
                time.sleep(0.5)
                
                break
    


    #===========================================================================
    # get_modularity returns the modularity 
    #===========================================================================
    def get_modularity(self):
        return self._modularity
    
    #===========================================================================
    # set_modularity set the modularity
    #===========================================================================
    def set_modularity(self, modularity):
        self._modularity = modularity
     
    
    def set_noConv(self, text):
        self._text = text
        
    def get_noConv(self):
        return self._text   

    #===========================================================================
    # LP_Sync1 Ist die eigentliche Funktion die den LPA startet nachdem ein Signal
    # der Main-Klasse gesendet wurde  
    #
    # Input:
    # graph (nx.Graph) Der aktuelle Graph
    # k: Der Wert womit festgelegt wird wie zufällig die Labels errechnet werden
    # maxIter: Anzahl der Iterationen bis der Algorithmus terminiert
    # version: Legt die Version Synchron oder Asynchron fest
    # rule: Legt fest wie die Labelvergabe erfolgt
    # selection: Legt fest welches Label nach der maximalen Berechnung der Label
    # gew�hlt wird
    # order: Legt die Riehenfolge der Knoten fest
    # Hop: Legt die Distanz zwischen dem Knoten i und den Nachbarn fest
    # Convergence: Legt fest mit welchem Kriterium der LPA terminieren soll
    # ord: legt Fest ob sich die Riehenfolge der Knoten nach jeder Iteration �ndert
    # visual: Legt fest ob eine Visualisierung der Schritte erfolgen soll. 
    # it: Legt die Anzahl an Iterationen fest
    #
    #===========================================================================
    @pyqtSlot(nx.Graph, int, int, str, str, str, int,  bool, bool, bool, int, int)
    def LP_Sync1(self, graph, k, max_iter, version, rule, 
                selection, hop, convergence, ord, visual, it, n):
        """def LP_Sync1(self, graph, k=1, max_iter=20, version = "Syncron", rule="Unique", 
                selection ="Random",  order = "Random",hop = 1, changes = True, 
                convergence = True):"""
        it += 1
        prog = int((100/n)*it)      
        print("Thread")
        labels = {}
        np_nodes, labels = LPAM.initialize(self, graph, rule, k)   
        labelsNew = {}
        noConvergence = True
        self.set_noConv(False)  
        labelsT1 = {}
        labelsT2 = {}
        modul = []
        modul.append(0)
        ar = []
        i =0
        cIter = 0
        eqLab = 0
        no = False
        self.isKilled = False
        self.set_Labels(labels)
        mod = []
        if(ord == False):
            random.shuffle(np_nodes)
        
        # Legt fest wie oft sich eine Labelkonstelation wiederholen darf, bis der Algorithmus abbricht
        oz =math.ceil(np.log10(len(np_nodes)))
        
        while noConvergence or self.isKilled:
            if(ord == True):
                random.shuffle(np_nodes)

                
            newLabels = deepcopy(labels)  
            for nodes in np_nodes:        
                #np_nbr = self.get_neighbors(graph, nodes, hop)
                np_nbr = LPAM.get_neighbors(self,graph, nodes, hop)
                #nx.set_node_attributes(graph, labels, "Community-ID")
                #self.return_data.emit(np_nodes, self.get_Labels(), nodes, np_nbr, graph)
                #time.sleep(0.5)
                #while self._pause:
                #   time.sleep(0)
                #time.sleep(0.01)
                if(len(np_nbr) == 0):
                    
                    if(version == LPAC._ASYNC.value):
                        labels[nodes] = labels[nodes]
                    else:
                        labelsNew[nodes] = labels[nodes]
                    continue
                
                else:
                    newLabel = LPAM.get_Frequence(self, np_nbr, labels)
                    if(version == LPAC._ASYNC.value):
                        labels[nodes] = LPAM.labelSelection(self,selection, newLabel, nodes, labels, np_nbr, newLabels)
                        while self._pause:
                            time.sleep(0)
                        #time.sleep(0.005)
                        #
                        #nx.set_node_attributes(graph, labels, "Community-ID")
                        #
                        #self.plot_Neighbors(np_nbr, labels, nodes, np_nodes, graph, labels)
                        #time.sleep(0.5)                 
                    else: 
                        labelsNew[nodes] = LPAM.labelSelection(self,selection, newLabel, nodes, labels, np_nbr, newLabels) 
                        while self._pause:
                            time.sleep(0)
                        #time.sleep(0.005)
                        #
                        #nx.set_node_attributes(graph, labelsNew, "Community-ID")
                        #
                        
                        #self.plot_Neighbors(np_nbr, labels, nodes, np_nodes, graph, labelsNew)
                        #time.sleep(0.5)  
            if(visual == True):
                time.sleep(2) 
            while self._pause:
                    time.sleep(0)                   
            if(self.isKilled == True):
                break
            
            if (version == LPAC._SYNC.value):
                labels = deepcopy(labelsNew)
                self.set_Labels(labels)
            

            nx.set_node_attributes(graph, labels, "Community-ID")
            LPAM.modularity(self, graph)
            modul.append(self.get_modularity())
            while self._pause:
                time.sleep(0)
            if(visual == True):
                # �berliefert den Aktuellen Graphen an das Framework um diesen zu Visualisieren
                self.return_update.emit(graph, self.get_Labels(), modul, noConvergence, self.get_noConv(), i)
                time.sleep(1)
                #print("pause", self._pause)
                while self._pause:
                    time.sleep(0)
                if(self.isKilled == True):
                    break

            # Convergence is True 
            if(convergence == True):
                # The Labels of T and T-1 are equal so break 
                if(labels == newLabels):
                    noConvergence = False 
                    self.set_noConv(True)               
                    break
                
                if(visual == False):
                    # This is a backdoor
                    if( i % 2 == 0):
                        if (labels == labelsT1):
                            cIter +=1                      
                        if (labels in ar):
                            eqLab += 1                    
                        elif (labels != labelsT1):
                            labelsT1 = deepcopy(labels)
                            if(labels not in ar):
                                no = True
                            cIter = 0                        
                    elif(i % 2 != 0):
                        if(labels == labelsT2):
                            cIter +=1    
                        if (labels in ar):
                            eqLab += 1
                        elif(labels != labelsT2):
                            labelsT2 = deepcopy(labels)
                            if(labels not in ar):
                                no = True
    
                            cIter = 0
                # Bricht den Algorithmus ab wenn es zur Oszillation oder Schleifenbildung kommt
                if(cIter == oz or eqLab == oz):
                    noConvergence = False
                    self.set_noConv(False)
                    #print(noConvergence)
                    break
            if(max_iter != 0 and convergence == False):
                if (i == max_iter-1):
                    noConvergence = False
                    self.set_noConv(True)
                    #self.set_noConv("Convergence")
                    break

            if(no == True):
                ar = np.append(ar, deepcopy(labels))
                no = False
            i  += 1
            #print(i)
            #print(eqLab)
        if(self.isKilled == True):
            #self.return_exit.emit(True)
            return
        if(visual == True):
            self.return_update.emit(graph, self.get_Labels(), modul, noConvergence, self.get_noConv(), i)
            nx.set_node_attributes(graph, labels, "Community-ID")
            #self.return_exit.emit(True)
        else:
            self.noVisual.emit(graph, self.get_Labels(), modul, noConvergence, self.get_noConv(), i)            
            self.progress.emit(int(prog))
            while self._pause:
                time.sleep(0)
            #self.return_exit.emit(True)
        return modul