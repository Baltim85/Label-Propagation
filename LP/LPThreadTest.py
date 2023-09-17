# -*- coding: utf-8 -*-
'''
@author: Mike.Pack
'''
# coding: utf8
import random

import numpy as np
from copy import deepcopy
import networkx.algorithms.community as nx_comm
import networkx as nx
import sys, math, csv, os
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

sys.path.append('../')
from Helper.LPAConstants import Constant as LPAC
from Helper.LPAMethods import LPAMethods as LPAM
from Helper.Helper import HelperMethod as hm

#===============================================================================
# LPThreadTest Diese Klasse wird als Thread gesetzt und dient dem Testen aller Varianten
# dadurch soll ein Freeze der UI verhindert werden. 
#===============================================================================
class LPThreadTest(QThread):

    def get_noConv(self):
        return self.__noConv


    def set_noConv(self, value):
        self.__noConv = value


    def del_noConv(self):
        del self.__noConv


    def get_mod_eqaul_zero(self):
        return self.__modEqaulZero


    def get_mod_less_zero(self):
        return self.__modLessZero


    def get_mod_greater_zero(self):
        return self.__modGreaterZero


    def set_mod_eqaul_zero(self, value):
        self.__modEqaulZero = value


    def set_mod_less_zero(self, value):
        self.__modLessZero = value


    def set_mod_greater_zero(self, value):
        self.__modGreaterZero = value


    def del_mod_eqaul_zero(self):
        del self.__modEqaulZero


    def del_mod_less_zero(self):
        del self.__modLessZero


    def del_mod_greater_zero(self):
        del self.__modGreaterZero


    def get_ozsillation(self):
        return self.__ozsillation


    def get_n_oszillation(self):
        return self.__nOszillation


    def get_abord(self):
        return self.__abord


    def set_ozsillation(self, value):
        self.__ozsillation = value


    def set_n_oszillation(self, value):
        self.__nOszillation = value


    def set_abord(self, value):
        self.__abord = value


    def del_ozsillation(self):
        del self.__ozsillation


    def del_n_oszillation(self):
        del self.__nOszillation


    def del_abord(self):
        del self.__abord


    def get_e_code(self):
        return self.__eCode


    def set_e_code(self, value):
        self.__eCode = value


    def del_e_code(self):
        del self.__eCode


    def get_avg_iter(self):
        return self.__avgIter


    def set_avg_iter(self, value):
        self.__avgIter = value


    def del_avg_iter(self):
        del self.__avgIter

    values = pyqtSignal(int, float)
  
    
    #===========================================================================
    # modularity Berechnet die Modularität des aktuellen Graphen, und liefert den Wert an die 
    #            aufrufende Funktion zurück
    #
    # input: 
    # nx.Graph: Der aktuelle Graph, für den die Modularität berechnet werden, soll
    #
    #===========================================================================
    def modularity(self, graph):
        # get the communities from the graph 
        coms=nx.get_node_attributes(graph,  "Community-ID")
        
        # convert the dict to numpy arrays, for a faster calculation
        keys = np.array(list(coms.keys()))
        values= np.array(list(coms.values()))      
        
        #=======================================================================
        # create a set containing each node that belongs to the same community
        # 
        # Lets have the nodes 1 till 8 and for every node the community is been calculated 
        # [{'3'}, {'1'}, {'4', '2'}, {'5'}, {'8'}, {'6', '7'}]
        # Node 3 belongs to its own community also node 1, 5 and 8
        # The nodes 4,2 belongs to the same community and also nodes 6 and 7
        #=======================================================================
        comm = [set([keys[val] for val in range(len(coms)) if (values[val] == value)]) for value in set(coms.values())]
        
        # calculate the modularity using networkx
        mod = nx_comm.modularity(graph, comm)
        self.set_modularity(mod)
    
    
    def get_numer(self):
        return self.__numer


    def get_pause(self):
        return self.__pause


    def set_numer(self, value):
        self.__numer = value


    def set_pause(self, value):
        self.__pause = value


    def del_numer(self):
        del self.__numer


    def del_pause(self):
        del self.__pause

    def get_max_iter(self):
        return self.__maxIter


    def set_max_iter(self, value):
        self.__maxIter = value


    def del_max_iter(self):
        del self.__maxIter


    def get_counter(self):
        return self.__counter


    def set_counter(self, value):
        self.__counter = value


    def del_counter(self):
        del self.__counter


    def get_p(self):
        return self.__p

    def set_p(self, value):
        self.__p = value

    def del_p(self):
        del self.__p

    def get_j(self):
        return self.__j


    def set_j(self, value):
        self.__j = value


    def del_j(self):
        del self.__j


    def get_average_mod(self):
        return self.__averageMod


    def get_average_convergence(self):
        return self.__averageConvergence


    def set_average_mod(self, value):
        self.__averageMod = value


    def set_average_convergence(self, value):
        self.__averageConvergence = value


    def del_average_mod(self):
        del self.__averageMod


    def del_average_convergence(self):
        del self.__averageConvergence


    def get_comy(self):
        return self.__comy


    def set_comy(self, value):
        self.__comy = value


    def del_comy(self):
        del self.__comy


    def get_mod_g(self):
        return self.__modG


    def set_mod_g(self, value):
        self.__modG = value


    def del_mod_g(self):
        del self.__modG


    def get_test_runs(self):
        return self.__test_runs


    def set_test_runs(self, value):
        self.__test_runs = value


    def del_test_runs(self):
        del self.__test_runs


    def get_files(self):
        return self.__files


    def set_files(self, value):
        self.__files = value


    def del_files(self):
        del self.__files


    def get_mode_s(self):
        return self.__mode_s


    def set_mode_s(self, value):
        self.__mode_s = value


    def del_mode_s(self):
        del self.__mode_s


    def get_best_modularity(self):
        return self.__bestModularity


    def get_worst_mod(self):
        return self.__worstMod


    def get_max_i(self):
        return self.__max_i


    def get_min_i(self):
        return self.__min_i


    def get_nmi(self):
        return self.__nmi


    def get_best_nmi(self):
        return self.__best_nmi


    def get_best_std(self):
        return self.__best_std


    def get_std(self):
        return self.__std


    def get_average_modularity(self):
        return self.__averageModularity


    def get_iterations(self):
        return self.__iterations


    def set_best_modularity(self, value):
        self.__bestModularity = value


    def set_worst_mod(self, value):
        self.__worstMod = value


    def set_max_i(self, value):
        self.__max_i = value


    def set_min_i(self, value):
        self.__min_i = value


    def set_nmi(self, value):
        self.__nmi = value


    def set_best_nmi(self, value):
        self.__best_nmi = value


    def set_best_std(self, value):
        self.__best_std = value


    def set_std(self, value):
        self.__std = value


    def set_average_modularity(self, value):
        self.__averageModularity = value


    def set_iterations(self, value):
        self.__iterations = value



    def del_best_modularity(self):
        del self.__bestModularity


    def del_worst_mod(self):
        del self.__worstMod


    def del_max_i(self):
        del self.__max_i


    def del_min_i(self):
        del self.__min_i


    def del_nmi(self):
        del self.__nmi


    def del_best_nmi(self):
        del self.__best_nmi


    def del_best_std(self):
        del self.__best_std


    def del_std(self):
        del self.__std


    def del_average_modularity(self):
        del self.__averageModularity


    def del_iterations(self):
        del self.__iterations
    
     
    bestModularity = property(get_best_modularity, set_best_modularity, del_best_modularity, "bestModularity's docstring")
    worstMod = property(get_worst_mod, set_worst_mod, del_worst_mod, "worstMod's docstring")
    max_i = property(get_max_i, set_max_i, del_max_i, "max_i's docstring")
    min_i = property(get_min_i, set_min_i, del_min_i, "min_i's docstring")
    nmi = property(get_nmi, set_nmi, del_nmi, "nmi's docstring")
    best_nmi = property(get_best_nmi, set_best_nmi, del_best_nmi, "best_nmi's docstring")
    best_std = property(get_best_std, set_best_std, del_best_std, "best_std's docstring")
    std = property(get_std, set_std, del_std, "std's docstring")
    averageModularity = property(get_average_modularity, set_average_modularity, del_average_modularity, "averageModularity's docstring")
    iterations = property(get_iterations, set_iterations, del_iterations, "iterations's docstring")
    mode_s = property(get_mode_s, set_mode_s, del_mode_s, "mode_s's docstring")
    files = property(get_files, set_files, del_files, "files's docstring")
    test_runs = property(get_test_runs, set_test_runs, del_test_runs, "test_runs's docstring")
    modG = property(get_mod_g, set_mod_g, del_mod_g, "modG's docstring")
    comy = property(get_comy, set_comy, del_comy, "comy's docstring")
    #averageMod = property(get_average_mod, set_average_mod, del_average_mod, "averageMod's docstring")
    #averageConvergence = property(get_average_convergence, set_average_convergence, del_average_convergence, "averageConvergence's docstring")
    j = property(get_j, set_j, del_j, "j's docstring")
    p = property(get_p, set_p, del_p, "p's docstring")
    counter = property(get_counter, set_counter, del_counter, "counter's docstring")
    maxIter = property(get_max_iter, set_max_iter, del_max_iter, "maxIter's docstring")
    numer = property(get_numer, set_numer, del_numer, "numer's docstring")
    pause = property(get_pause, set_pause, del_pause, "pause's docstring")
    
    
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
     
    #===========================================================================
    # get_maxIter returns the maximal numer of Iterations
    #===========================================================================
    def get_maxIter(self):
        return self._maxIter
    
    #===========================================================================
    # set_maxIter set the maximal number of Iterations till stopping
    #===========================================================================
    def set_maxIter(self, maxIter):
        self._maxIter = maxIter

    
    #===========================================================================
    # resetValues Diese Funktion setzt alle Werte wieder auf null zurück
    #, nachdem ein Testlauf abgeschlossen wurde, damit immer mit
    # aktuellen Werten gerechnet wird. 
    #===========================================================================
    def resetValues(self):
        self.set_best_modularity(0.00)
        self.set_worst_mod(0.0)
        self.set_max_i(0.0)
        self.set_min_i(0.0)
        
        self.set_nmi(0.0)
        self.set_best_nmi(0.0)
        self.set_best_std(0.0)
        self.set_std(0.0)
        
        self.set_mode_s([])
        self.set_average_modularity([])
        self.set_iterations([])
        self.set_e_code([])
        self.set_ozsillation(0)
        self.set_n_oszillation(0)
        self.set_abord(0)
        self.set_mod_eqaul_zero(0)
        self.set_mod_less_zero(0)
        self.set_mod_greater_zero(0)
    
    

    
    #===========================================================================
    # calcAverage Berechnet die durchschnittlichen Werte für die spätere Auswertung. 
    # Dazu zählen die durchschnittliche Modularität, sowie die durchschnittliche 
    # Anzahl an Iterationen
    #===========================================================================
    def calcAverage(self):    
        averagMod, averagConvergence = hm.calculateAverage(self, self.get_mode_s(), self.get_j(), self.get_test_runs())
        self.set_average_mod(averagMod)
        self.set_average_convergence(averagConvergence)
        #print(self.get_iterations())
        acgI = []
        avgI = np.sum(self.get_iterations())
        #print(avgI)
        self.set_iterations(avgI / self.get_test_runs())
     
    
    #===========================================================================
    # calc Berechnet nach einem Testlauf die jeweils Besten werte die erreicht wurden
    # und speichert diese in den settern.
    #
    # Input: 
    # iterations: Die Anzahl an Iterationen, die der Testlauf benötigte
    # modu: Enthält die Werte der durchschnittlichen Modularität, die wären der Testläufe
    # erreicht wurde
    # modul: Enthält die Werte der Modularität aller Testläufe für einen Graphen
    # cIter: Enthält die Anzahl wie oft der Algorithmus nicht Terminierte
    # g ist der aktuelle Graph
    #===========================================================================
    def calc(self, iteration, modu, modul, cIter,g):
        
        self.get_average_modularity().append(modu)
        self.get_iterations().append(iteration)
        self.get_mode_s().append(modul)
        
        if(self.get_mod_g() != None):
            self.set_comy([self.get_mod_g(), modu])
            self.set_std(np.std(self.get_comy()))
        self.set_nmi(hm.calcNMI(self, g))
    
        bestModularity, best_nmi, best_std = hm.bestWorstValue(self, self.get_best_modularity(),  modu, self.get_best_nmi(), self.get_nmi(), self.get_best_std(), self.get_std())
        self.set_best_modularity(bestModularity)
        self.set_best_nmi(best_nmi)
        self.set_best_std(best_std) 
        self.set_j(self.get_j() + cIter)
        #self.progressBar.setValue(self.get_counter()* self.get_p())     


    #===========================================================================
    # setupAlgo Mit dieser Funktion erhält der Label Propagation Algorithmus
    # alle Varianten, die von dem Framework genutzt werden können. 
    #===========================================================================
    def setupAlgo(self):
        #self.set_max_iter(self.ui.sb_MaxIter.value())
        version = [LPAC._SYNC.value, LPAC._ASYNC.value]
        labels = [LPAC._UNIQUE.value, LPAC._RANDOM.value]
        k = [1, 2]   
        order = [True, False]
        neighbors = [0, 1, 2, 3]
        label_selection=[LPAC._RANDOM.value, LPAC._SELF.value, LPAC._FIRST.value, LPAC._LAST.value, LPAC._MEDIAN.value]
        convergence = [True, False] 
        #self.set_test_runs(self.ui.sb_MaxTest.value())
        testSize = len(version) * 3 * len(order) * len(neighbors)*len(label_selection)*len(convergence)
        return labels, k, version, neighbors, label_selection, convergence, order, testSize
 
    #===========================================================================
    # fast_copy wird statt der Funktion deepCopy verwendet um etwas Performance 
    # bei dem Kopieren der Arrays zu erreichen
    #===========================================================================
    def fast_copy(self, d):
        output = d.copy()
        for key, value in output.items():
            output[key] = self.fast_copy(value) if isinstance(value, dict) else value        
        return output

    def propagationStep(self, np_nodes, graph, hop, labels, version, labelsNew, selection, newLabels):
        #for nodes in np_nodes:     
        #print(len(np_nodes))   
        np_nbr = LPAM.get_neighbors(self, graph, np_nodes, hop)
        if(len(np_nbr) == 0):
            
            if(version == LPAC._ASYNC.value):
                labels[np_nodes] = labels[np_nodes]
            else:
                labelsNew[np_nodes] = labels[np_nodes]
            #continue               
        else:
            newLabel = LPAM.get_Frequence(self, np_nbr, labels)
            if(version == LPAC._ASYNC.value):
                labels[np_nodes] = LPAM.labelSelection(self, selection, newLabel, np_nodes, labels, np_nbr, newLabels)
            else: 
                labelsNew[np_nodes] = LPAM.labelSelection(self, selection, newLabel, np_nodes, labels, np_nbr, newLabels)
        return labelsNew

    #===========================================================================
    # runTest Innerhalb dieser Funktion wird der LPA ausgeführt und sämtliche Berechnunngen
    # durchgeführt, nachdem ein Testlauf für eine Variante abgeschlossen wurde.
    # Zusätzlich werden die Daten auch in eine .csv Datei geschrieben, wenn alle
    # Testläufe abgeschlossen wurden. 
    #
    # name: Ist der Name, der Datei in die geschrieben wird
    # i: Die Anzahl der maximalen Iterationen
    # testRuns: Die Anzahl der Testläufe, die für eine Konfiguration durchlaufen werden, soll
    # file: Die graphml Datei mit dem jeweiligen Graphen
    #
    # Output:
    # Liefert eine .csv Datei zurück mit allen Ergebnissen
    #===========================================================================

    @pyqtSlot(tuple, int, int, list)
    def runTest(self, name, i, testRuns, file):
        
        self.set_max_iter(i)
        self.set_test_runs(testRuns)
        self.set_files(file)
        try:
            outFile = open(name[0], 'w', encoding='UTF8', newline='')
        except FileNotFoundError:
            return
        header2 = ["Graph", "Mode", "Initialize", "K", "Update Order", "Neighbor", "Label Sel.", "Convergence", "Avg.Modularity", "Best Modularity", "Convergence", "Avg. Iterations", "Oszillation", "n Oszillation", "Abbruch", "Mod < 0", "Mod = 0", "Mod > 0"]
        writer = csv.writer(outFile)
        #writer = csv.writer(outFile)
        writer.writerow(header2)
        
        namesG = []
        errorCo = []
        self.set_mod_g(0)
        iterat = 0
        labels, k, version, neighbors, label_selection, convergence, order, testSize = self.setupAlgo()
        self.resetValues()
        self.set_p((100/(testSize*self.get_test_runs()*len(self.get_files()))))
        self.set_counter(1)
        for file in self.get_files():
            for vers in version: 
                for conv in convergence:
                    for ks in k:
                        for lab in labels:
                            if(ks == 2):
                                lab = LPAC._RANDOM.value
                            for nbr in neighbors:
                                for ls in label_selection:
                                    for ords in order:
                                        self.set_j(0)
                                        
                                        namesG.append(os.path.basename(file))
                                        for n in range(self.get_test_runs()):
                                            g = nx.read_graphml(file)
                                            g.remove_edges_from(nx.selfloop_edges(g))
                                            g.remove_nodes_from(list(nx.isolates(g)))
                                            if (lab == LPAC._RANDOM.value and ks >= 0): 
                                                iteration, modu, modul, cIter, errorC= self.LP_Test(g, ks, self.get_max_iter(), vers, lab, ls, nbr,conv, ords)     
                                                #iteration, modu, modul, cIter= self.prop.LP_Sync(g, ks, self.get_MaxIter(), vers, lab, ls, nbr,conv, o)                     
                                            else:
                                                #self.LP_Test(g, ks, self.get_max_iter(), vers, lab, ls, nbr,conv, o)
                                                iteration, modu, modul, cIter, errorC = self.LP_Test(g, ks, self.get_max_iter(), vers, lab, ls, nbr,conv, ords)
                                            self.calc(iteration, modu, modul, cIter, g)
                                            self.set_mod_g(hm.modularityO(self,g))
                                            self.set_counter(self.get_counter() + 1)
                                            errorCo.append(errorC)
                                            self.set_e_code(errorCo)
                                            if(modu < 0):
                                                self.set_mod_less_zero(self.get_mod_less_zero() + 1)
                                            if(modu == 0):
                                                self.set_mod_eqaul_zero(self.get_mod_eqaul_zero() + 1)
                                            if(modu > 0):
                                                self.set_mod_greater_zero(self.get_mod_greater_zero() + 1)

                                        
                                        self.calcAverage()
                                        for c in self.get_e_code():
                                            if (c == -1):
                                                self.set_ozsillation(self.get_ozsillation() + 1)
                                            if (c == -2):
                                                self.set_n_oszillation(self.get_n_oszillation() + 1)
                                            if( c== -3):
                                                self.set_abord(self.get_abord() + 1)
                                        if(vers == LPAC._ASYNC.value):
                                            str1 = "Asyncronous"
                                        if(vers == LPAC._SYNC.value):
                                            str1 = "Syncronous"

                                        if(conv == True):
                                            con = "Till Convergence"
                                        else:
                                            con = "Max Iteration"
                                        if(ords == True):
                                            ol = "Shuffle order per Iter"
                                        else:
                                            ol = "Fixed order"
                                        if (nbr == 0):
                                            neighbor = "Nbr incl. self"
                                        if (nbr == 1):
                                            neighbor = "Only Nbr"
                                        if (nbr == 2):
                                            neighbor = "Nbr plus Nbr of Nbr"
                                        if (nbr == 3):
                                            neighbor = "Nbr plus Nbr of Nbr incl Self"
                                        #header2 = ["Graph", "Mode", "Initialize", "K", "Update Order", "Neighbor", "Label Sel.", "Convergence", "Avg.Modularity", "Best Modularity", "Avg. Convergence" "NMI", "STD"]
                                        #data = [os.path.basename(file), str1, lab, ks, ol, neighbor, ls, con, self.get_average_mod(), self.get_best_modularity(),self.get_average_convergence(), self.get_iterations(), self.get_best_nmi(), self.get_best_std(), self.get_ozsillation(), self.get_n_oszillation(), self.get_abord()
                                        #       , self.get_mod_less_zero(), self.get_mod_eqaul_zero(), self.get_mod_greater_zero()]
                                        data = [os.path.basename(file), str1, lab, ks, ol, neighbor, ls, con, self.get_average_mod(), self.get_best_modularity(),self.get_average_convergence(), self.get_iterations(), self.get_ozsillation(), self.get_n_oszillation(), self.get_abord()
                                                , self.get_mod_less_zero(), self.get_mod_eqaul_zero(), self.get_mod_greater_zero()]
                                        self.values.emit(self.get_counter(), self.get_p())
                                        writer.writerow(data)
                                        outFile.flush()
                                        #print(iterat)
                                        iterat += 1   
                                        errorCo = []
                                        self.resetValues()    
                            # Dient eines Abbruches     
                            if(ks == 2):
                                break                     


        outFile.close()
   
    #===========================================================================
    # LP_Test Ist der eigentliche LPA in dem der Graph nun entsprechen, in 
    # Communities unterteilt wird. 
    #
    # Input:
    # graph: Der aktuelle Graph 
    # k: Der Wert für die zufällige Vergabe bei der zufälligen Labelvergabe
    # max_iter: Die Anzahl an maximalen Iterationen der der LPA durchlaufen soll
    # version: Legt fest ob Synchron oder Asynchron
    # rule: Legt fest, ob die Labels zufällig oder einzigartig sind
    # selection: Legt fest welches Label aus der Anzahl möglicher Label gewählt werden soll
    # "Random" "First, "Last", "Median", "Self
    # Hop: Beschreib die Distanz zwischen den Knoten i und den Nachbarn f�r 
    # die Berechnung des neuen Labels
    # convergencen legt fest wie der Algorithmus Terminiert
    # order: Legt die Reihenfolge der Knoten zu Beginn fest
    #===========================================================================

    #@pyqtSlot(nx.Graph, int, int, str, str,str, int, bool, bool)
    def LP_Test(self, graph, k, max_iter, version, rule, selection, hop, convergence, order):
        
        np_nodes, labels = LPAM.initialize(self, graph, rule, k)   
        labelsNew = {}
        noConvergence = True  
        modul = []
        labelsT1 = {}
        labelsT2 = {}
        ar = []
        i =0
        cIter = 0
        eqLab = 0
        j = 0
        errorCode = 0
        no = False
        maximumI = 1500
        oz =math.ceil(np.log10(len(np_nodes)))
        
        if(order == False):
            random.shuffle(np_nodes)
        while noConvergence:
            if(order == True):
                random.shuffle(np_nodes)

            #newLabels = deepcopy(labels)

            newLabels = self.fast_copy(labels)

            for nodes in np_nodes:  
                
                np_nbr = LPAM.get_neighbors(self, graph, nodes, hop)
                if(len(np_nbr) == 0):
                    
                    if(version == LPAC._ASYNC.value):
                        labels[nodes] = labels[nodes]
                    else:
                        labelsNew[nodes] = labels[nodes]
                    continue               
                else:
                    newLabel = LPAM.get_Frequence(self, np_nbr, labels)
                    if(version == LPAC._ASYNC.value):
                        labels[nodes] = LPAM.labelSelection(self, selection, newLabel, nodes, labels, np_nbr, newLabels)
                    else: 
                        labelsNew[nodes] = LPAM.labelSelection(self, selection, newLabel, nodes, labels, np_nbr, newLabels)
            if (version == LPAC._SYNC.value):
                labels = self.fast_copy(labelsNew)

            
            if(convergence == True):
                
                # Standard Variante f�r die Konvergenz
                if(labels == newLabels):
                    noConvergence = False                
                    nx.set_node_attributes(graph, labels, "Community-ID")
                    LPAM.modularity(self, graph)
                    modul.append(self.get_modularity())
                    j = 1
                    break
                # Ermittelt ob es zu einer Schleifenbildung kommt
                if( i % 2 == 0):
                    if (labels == labelsT1):
                        #j = 1
                        cIter += 1
                        #break
                        if(cIter == oz):
                            errorCode = -1
                            break
                    if (labels in ar):
                        
                        eqLab += 1
                        if(eqLab == oz):
                            errorCode = -2
                            break
                    elif (labels != labelsT1):
                        labelsT1 = self.fast_copy(labels)
                        if(labels not in ar):
                            no = True
                        cIter = 0
                        
                elif(i % 2 != 0):
                    if(labels == labelsT2):
                        cIter +=1
                        if(cIter == oz):
                            errorCode = -1
                            break
                        #j = 1
                        #break    
                    if (labels in ar):
                        eqLab += 1
                        if(eqLab == oz):
                            errorCode = -2
                            break
                    elif(labels != labelsT2):
                        labelsT2 = self.fast_copy(labels)
                        #labelsT2 = deepcopy(labels)
                        if(labels not in ar):
                            no = True
                        cIter = 0
                if (i == maximumI):
                        fehlerCode = -3
                        noConvergence = False
                        self.set_noConv("No Convergence")
                        break

            if(max_iter != 0 and convergence == False):
                if (i == max_iter-1):
                    noConvergence = False
                    nx.set_node_attributes(graph, labels, "Community-ID")
                    LPAM.modularity(self, graph)
                    modul.append(self.get_modularity())
                    j = 1
                    break
            nx.set_node_attributes(graph, labels, "Community-ID")
            
            LPAM.modularity(self,graph)

            modul.append(self.get_modularity())
            
            if(no == True):
                ar = np.append(ar, deepcopy(labels))
                no = False
            i  += 1

        i += 1
        #self.values.emit(i, self.get_modularity(), modul, j, graph)
        
        return i+1, self.get_modularity(), modul, j, errorCode
    
    avgIter = property(get_avg_iter, set_avg_iter, del_avg_iter, "avgIter's docstring")
    eCode = property(get_e_code, set_e_code, del_e_code, "eCode's docstring")
    ozsillation = property(get_ozsillation, set_ozsillation, del_ozsillation, "ozsillation's docstring")
    nOszillation = property(get_n_oszillation, set_n_oszillation, del_n_oszillation, "nOszillation's docstring")
    abord = property(get_abord, set_abord, del_abord, "abord's docstring")
    modEqaulZero = property(get_mod_eqaul_zero, set_mod_eqaul_zero, del_mod_eqaul_zero, "modEqaulZero's docstring")
    modLessZero = property(get_mod_less_zero, set_mod_less_zero, del_mod_less_zero, "modLessZero's docstring")
    modGreaterZero = property(get_mod_greater_zero, set_mod_greater_zero, del_mod_greater_zero, "modGreaterZero's docstring")
    noConv = property(get_noConv, set_noConv, del_noConv, "noConv's docstring")
    