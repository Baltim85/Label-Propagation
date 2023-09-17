# -*- coding: utf-8 -*-

from copy import deepcopy
import random, math, time, sys, csv

from random import randrange
import numpy as np
import networkx as nx

sys.path.append('../')
from Helper.LPAConstants import Constant as LPAC
from Helper.LPAMethods import LPAMethods as LPAM
from Helper.Helper import HelperMethod as hm
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_comm
from progress.bar import ChargingBar
from tqdm import tqdm


class LP:

    def __init__(self):
        pass

    #===========================================================================
    # nodesOrder setup the order for the nodes at the beginning.
    #
    # Imput: 
    # graph (nx.Graph) the graph itself
    # nodes: The nodes of the graph
    # order: Contains the selected order
    # Random: The nodes will be shuffle random
    # Dec: Order the nodes at the degree. Small degree first
    # Inc: Order the nodes at the degree. Large degree first
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
        self._pause = False
        time.sleep(0.01)
        self._pause = True
       
    def kill(self):
        self.isKilled = True
    
    def set_Pause(self, pause):
        self._pause = pause
    def get_Pause(self):
        return self._pause
    
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
    # LPA ist der Label Propagation ALgorithmus
    #
    # Input: 
    # graph (nx.Graph) Der aktuelle Graph
    # k: Der Wert wenn die Label zufällig berechnet werden
    # maxIter: Anzahl an Iterationen
    # version: Synchron oder Asynchron 
    # rule: Legt die Initialisierung der Label Fest
    # selection: Welches Label soll aus der Menge der Maximalen Label genommen werden
    # hop: DIe Hop Distanz
    # convergence: Soll der Algorithmus bis zur Konvergenz laufen (True) sonst (False)
    # order: Die Reihenfolge der Knoten
    # test: Die Anzahl an Testläufen
    # gName: Name des Graphen
    # writer: Speichert die Werte des Testlaufes
    #
    #===========================================================================
    def LPA(self, graph, k, max_iter, version, rule, 
                selection, hop, convergence, ord1, test, gName, writer):
        
        graph.remove_edges_from(nx.selfloop_edges(graph))
        graph.remove_nodes_from(list(nx.isolates(graph)))
        qbar = tqdm(total = int(test), desc ="Run Test for Graph: " +gName)
        neighbour = ""
        
        self.set_graph(graph)
        self.gn()   
        gn = "Greedy Modularity"
        for j in range(int(test)):
            np_nodes, labels = LPAM.initialize(self, graph, rule, k)   
            labelsNew = {}
            noConvergence = True  
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
            fehlerCode = 0
            maximumI = 1500
            if(ord1 == True):
                random.shuffle(np_nodes)
            
            oz =math.ceil(np.log10(len(np_nodes)))
            
            while noConvergence:
                if(ord1 == False):
                    random.shuffle(np_nodes)
                       
                newLabels = deepcopy(labels)  
                for nodes in np_nodes:        
                    np_nbr = LPAM.get_neighbors(self,graph, nodes, hop)
    
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
                        else: 
                            labelsNew[nodes] = LPAM.labelSelection(self,selection, newLabel, nodes, labels, np_nbr, newLabels) 
                    
                if(self.isKilled == True):
                    break
                
                if (version == LPAC._SYNC.value):
                    labels = deepcopy(labelsNew)
                    self.set_Labels(labels)
                
    
                nx.set_node_attributes(graph, labels, "Community-ID")
                LPAM.modularity(self, graph)
                modul.append(self.get_modularity())
    
                # Convergence is True 
                if(convergence == True):
                    # The Labels of T and T-1 are equal so break 
                    if(labels == newLabels):
                        noConvergence = True                
                        break
                    
                    # This is a backdoor
                    if( i % 2 == 0):
                        # Pr�fe auf direkte Ozsillation
                        if (labels == labelsT1):
                            cIter +=1
                            if(cIter == oz):
                                fehlerCode  = -1
                                noConvergence = False
                                self.set_noConv("No Convergence")
                                break
                        # Prüfe auf indirekte Oszillation                      
                        if (labels in ar):
                            eqLab += 1                   
                            if(eqLab == oz+1):
                                fehlerCode = -2
                                noConvergence = False
                                self.set_noConv("No Convergence")
                                break
                        # Speicher neue Konfig in Liste 
                        elif (labels != labelsT1):
                            labelsT1 = deepcopy(labels)
                            if(labels not in ar):
                                no = True
                            cIter = 0                        
                    elif(i % 2 != 0):
                        if(labels == labelsT2):
                            cIter +=1
                            if(cIter == oz):
                                fehlerCode  = -1
                                noConvergence = False
                                self.set_noConv("No Convergence")
                                break    
                        if (labels in ar):
                            eqLab += 1                   
                            if(eqLab == oz):
                                fehlerCode = -2
                                noConvergence = False
                                self.set_noConv("No Convergence")
                                break
                        elif(labels != labelsT2):
                            labelsT2 = deepcopy(labels)
                            if(labels not in ar):
                                no = True
    
                            cIter = 0
                    
                    
                    # Abbruch nach Erreichung einer Maximalen Anzahl an L�ufen            
                    if (i == maximumI):
                        fehlerCode = -3
                        noConvergence = False
                        self.set_noConv("No Convergence")
                        break
                if(int(max_iter) != 0 and convergence == False):
                    if (i == int(max_iter)-1):
                        noConvergence = True
                        self.set_noConv("Convergence")
                        break
    
                if(no == True):
                    ar = np.append(ar, deepcopy(labels))
                    no = False
                i  += 1
                #print(i)
                #print(eqLab)
    
            self.justTesting(graph, modul, noConvergence)
            if (hop == 0):
                neighbour = "Nbr incl. self"
            if (hop == 1):
                neighbour = "Only Nbr"
            if (hop == 2):
                neighbour = "Nbr plus Nbr of Nbr"
            if (hop == 3):
                neighbour = "Nbr plus Nbr of Nbr incl Self"
                
            if(convergence == True):
                con = "Till Convergence"
            else:
                con = "Max Iteration"
            if (ord1 == False):
                order ="Random Order"
            else:
                order ="Fixed Order"
            j += 1
            qbar.update()
            data = [gName, version, rule, k, order, neighbour, selection, con, self.get_lastMod(), self.get_bestMod(), self.get_conv(), i,  gn, self.get_gnMod(), int(j), fehlerCode]
            writer.writerow(data)
            #AS = True
        qbar.close()
        print("\n")
        return writer
    def justTesting(self, graph, modul, conv):
        #self.plotter.pause()
        self.set_lastMod(modul[-1])
        self.set_bestMod(max(modul))
        self.set_nmi(hm.calcNMI(self, graph))
        if(conv == False):
            self.set_conv("No Convergence")
        else:
            self.set_conv("Convergence")
        #self.writeData(self.get_DataIter())
        #self.set_DataIter(self.get_DataIter()+1)
        
        #print(modul, self.get_lastMod(), self.get_bestMod(), self.get_nmi())
    
    
    
    #===========================================================================
    # gn Der Greddy Modularity ALgorithmus zum vergleichen der Werte der Modularität
    # die mittels dem LPA erreicht wurden.
    #===========================================================================
    def gn(self):
        #communities = girvan_newman(self.get_graph())
        c = list(greedy_modularity_communities(self.get_graph()))
        #node_groups = []
        #for com in next(communities):
        #    node_groups.append(list(com))
        
        #mod = nx_comm.modularity(self.get_graph(), node_groups)
        mod = nx_comm.modularity(self.get_graph(), c) 
        self.set_gnMod(mod)


    def set_gnMod(self, gnMod):
        self.gnMod = gnMod
        
    def get_gnMod(self):
        return self.gnMod
        
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
    
    def set_graph(self, graph):
        self._graph = graph
    def get_graph(self):
        return self._graph
    
    def set_conv(self, conv):
        self.conv = conv
        
    def get_conv(self):
        return self.conv
    