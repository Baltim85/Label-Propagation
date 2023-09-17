# -*- coding: utf-8 -*-
'''
@author: Mike.Pack
'''

import numpy as np
from Helper.LPAConstants import Constant as LPAC
from random import randrange
import random, itertools, math
import networkx as nx
import networkx.algorithms.community as nx_comm


#===============================================================================
# LPAMethods Diese Klasse enthält die einzelnen Module des Label Propagation Algorithmus.
# Darunter er zählt die Wahl der Nachbarn, Verteilung der Labels wie auch die Auswahl
# welches Label gewählt werden soll.
#===============================================================================
class LPAMethods:
    
    
    #===========================================================================
    # getNeighbors Liefert ein Array zurück, in dem die Nachbarn des Knotens (i) gespeichert sind. 
    #
    # Input: 
    # graph (nx.Graph): Beschreibt den aktuellen Graphen
    # node: Ist der gerade aktuelle Knoten zu dem die Nachbarn ermittelt werden  
    # hop (int): Beschreibt in welcher Distanz die Nachbarn betrachtet werden
    #
    # Return:
    # Array Gibt die Nachbarn des aktuellen Knotens zurück
    #
    #===========================================================================
    def get_neighbors(self, graph, node, hop):
        np_nbr = np.array(list(graph.neighbors(node)))
        np_nbrOfnbr = [] 
        if(hop == 0):
            
            np_nbr =np.append(np_nbr, node)
            return np_nbr
        if (hop == 1):
            return np.array(list(graph.neighbors(node)))
            #return np_nbr
        if (hop == 2):
                    
            for i in np_nbr:
                nbr_list = list(graph.neighbors(i))
                #print(nbr_list)
                if(node in nbr_list):
                    #print(nbr_list)
                    nbr_list.remove(node)
                    #print(nbr_list)
                np_nbrOfnbr = np.append(np_nbrOfnbr, np.array(nbr_list))
                #print(np_nbrOfnbr)                
                np_nbrOfnbr = np.append(np_nbrOfnbr, i)
                #print(np_nbrOfnbr)
            np_nbrOfnbr = np.unique(np_nbrOfnbr)
            #np_nbrOfnbr = np.delete(np_nbrOfnbr, np.argwhere(np_nbrOfnbr == node))
            #np_nbrOfnbr = np.delete(np_nbrOfnbr, node)
            return np_nbrOfnbr
        if (hop == 3):
            for i in np_nbr:
                np_nbrOfnbr = np.append(np_nbrOfnbr, np.array(list(graph.neighbors(i))))                
                np_nbrOfnbr = np.append(np_nbrOfnbr, i)
            np_nbrOfnbr = np.unique(np_nbrOfnbr)
            return np_nbrOfnbr
        
    #===========================================================================
    # labelSelection Diese Funktion liefert aus der Menge der möglichen Labels
    # ein Label f�r den Knoten (i) zurück
    #
    # Input:
    # rule: Beschreibt, welche Regel für die Wahl des Labels angewendet werden soll
    # newLabel: Enthält die Menge der möglichen Labels f�r den Knoten i
    # node: Ist der gerade aktive Knoten, der bearbeitet wird
    # np_nbr: Enthält die Menge der Nachbarn des Knoten i
    # newLabels: Enthält die Menge aller Label in dem Netzwerk
    #
    # return: 
    # Liefert für den aktuellen Knoten i das neue Label zurück
    #===========================================================================   
    def labelSelection(self, rule, newLabel, node, labels, np_nbr, newLabels):
        if (rule == LPAC._RANDOM.value):
            return random.sample(newLabel,1)[0]
        if(rule == LPAC._SELF.value):       
            for k in np_nbr:
                if(labels[node] == newLabels[k] ):
                    return labels[node]
            return  random.sample(newLabel,1)[0]    
        if(rule == LPAC._FIRST.value):
            return newLabel[0]
        if(rule == LPAC._LAST.value):
            return newLabel[-1]
        if(rule == LPAC._MEDIAN.value):
            if(len(newLabel) > 1):
                #print(len(newLabel))
                if(len(newLabel) % 2 == 0):
                    numOne = newLabel[math.floor(len(newLabel) / 2)]
                    numTwo = newLabel[math.floor(len(newLabel) / 2)-1]
                    labelL = []
                    labelL.append(numOne)
                    labelL.append(numTwo)
                    return random.sample(labelL,1)[0]
                return newLabel[math.floor(len(newLabel) / 2)]
            return random.sample(newLabel,1)[0]      


    #===========================================================================
    # initialize Legt für die Knoten des Graphen die Labels fest, nachdem
    # der Graph geladen wurde.
    #
    # Input:
    # nx.Graph: Der geladene Graph
    #
    # String rule: Legt fest wie die Knoten im Graphen vergeben werden
    # F�r "Unique" erhält jeder Knoten ein eindeutiges Label (Standard)
    # "Random" jeder Knoten erhält zufällig ein Label in abhängigkeit von k
    #
    # int k:
    #
    # Return:
    # numpy.array nodes: Die Knoten des Graphen
    # dict: Ein Dictinory mit der Menge der Labels und Knoten 
    #===========================================================================
    def initialize(self, graph, rule,k):
        nodes = np.array(graph.nodes())
        if (rule == LPAC._UNIQUE.value):
            
            labs = dict(zip(nodes, range(graph.number_of_nodes())))
        if (rule == LPAC._RANDOM.value):
            labs = {}
            for i in range(len(graph.nodes)):
                labs[nodes[i]] = randrange(math.floor(k*(np.log2(len(graph.nodes)))))
        return nodes, labs


    #===========================================================================
    # get_Frequence Berechnet nachdem die Labels der Nachbarn des Knoten i ermittelt
    # wurden, welches Label am häufigsten vorkommt.
    #
    # Input: 
    # neighbors: Enthält die Nachbarn des Knoten i
    # labels: Enthält die Menge aller Label
    # 
    # return: Liefert das häufig vorkommenden Label zurück. 
    #===========================================================================
    def get_Frequence(self, neighbors, labels):
        labs = sorted(labels[node] for node in neighbors)
        labs = [(len(list(c)), l) for l, c in itertools.groupby(labs)]        
        m = max(labs)[0]
        return [l for c, l in labs if c == m]

    #===========================================================================
    # modularity Berechnet die Modularität für, den gerade aktuellen Graphen
    #
    # input: 
    # nx.Graph: Der aktuelle Graph
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

