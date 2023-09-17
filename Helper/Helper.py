# -*- coding: utf-8 -*-
'''
@author: Mike.Pack
'''

from sklearn import metrics as me
import networkx as nx
from Helper.LPAConstants import Constant as LPAC
import numpy as np
import itertools
import networkx.algorithms.community as nx_comm

#===============================================================================
# HelperMethod: Enthält einige Hilfsfunktionen wie das Berechnen der Modularität
# und Berechnung der durchschnittlichen Konvergenz des Algorithmus
#===============================================================================
class HelperMethod:
    
    
    
    """def __init__(self):
        pass
    """
    
    #===========================================================================
    # calcNMI: Berechnet die NMI des aktuellen Netzwerkes
    #
    # g: Ist der gerade aktuellen Graph   
    #===========================================================================
    def calcNMI(self,g):
        labs =list(nx.get_node_attributes(g, LPAC._LABELS.value).values())
        if(labs == []):
            return 0
        coms=list(nx.get_node_attributes(g, "Community-ID").values())
        nmi = me.normalized_mutual_info_score(coms, labs)
        return nmi
    

    #===========================================================================
    # calculateAverage: Berechnet die durchschnittliche Modularität sowie
    #                    die durchschnittliche Konvergenz des Algorithmus
    #
    # modeS: Beschreibt die Modularität des aktuellen Graphen 
    # j: Beschreibt die Anzahl an Testläufen, die zur Konvergenzührten
    # n: Beschreibt die Anzahl der Testläufe, die im gesamten gemacht wurden.
    #
    #===========================================================================
    def calculateAverage(self, modeS, j, n):
        averageMod = None
        array = np.array([x for x in itertools.zip_longest(*modeS, fillvalue=0)])
        modularity = (np.sum(np.array([x for x in itertools.zip_longest(*modeS, fillvalue=0)]), axis=1))  # / np.array(np.count_nonzero(array, axis=1))
        indexes = np.array(np.count_nonzero(array, axis=1))                                            
        i = 0
        while i < len(indexes):
            if(indexes[i] == 0):
                modularity = np.delete(modularity, i)
                indexes = np.delete(indexes, i)
                i = 0
            else:
                i += 1
        indexes = indexes[indexes != 0]
        modularity = modularity / indexes
        averageConvergence = (j / n) *100 #(100) - ((j * 100) / (n + 1))
        if(averageConvergence <= 0):
            averageConvergence = 0
        
        if(len(modularity)!= 0):
            averageMod = sum(modularity) / len(modularity)
        if(averageMod == None):
            averageMod = 0.0
        
        
        return averageMod, averageConvergence
    

     
    #===========================================================================
    # bestWorstValue: Berechnet, ob die aktuellen Werte des aktuellen Laufes sich verbessert
    #                haben. Wenn ja, werden diese Werte gespeichert.
    # 
    # bestModularity: Enth�lt die beste Modularität, die bislang gemessen wurde von allen  
    #                 Testläufen.
    # modularity:     Enthält die Modularit�t des aktuellen Laufes 
    # best_nmi:        Enthält die bislang am besten gemessene NMI
    # nmi:            Beschreibt die gerade aktuelle NMI
    # best_std:        Enthält die bislang best gemessene STD
    # std:            Ist die aktuelle STD des Netzwerkes
    #===========================================================================
    def bestWorstValue(self, bestModularity, modularity, best_nmi, nmi, best_std, std):
        if(bestModularity < modularity or bestModularity == 0):
            bestModularity = modularity                                              
        if(best_nmi < nmi or best_nmi == 0):
            best_nmi = nmi
        if(best_std < std or best_std == 0):
            best_std = std    
        return bestModularity, best_nmi, best_std
    
    
    #===========================================================================
    # modularityO Berechnet die Modularität des aktuellen Graphen, und liefert den Wert an die 
    #            aufrufende Funktion zurück
    #
    # input: 
    # nx.Graph: Der aktuelle Graph, f�r den die Modularität berechnet werden, soll
    #
    #===========================================================================
    def modularityO(self, graph):
        # get the communities from the graph 
        #print(graph.nodes.data())
        coms=nx.get_node_attributes(graph, LPAC._LABELS.value)
        if(coms == {}):
            #print("empty")
            return
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
        return mod
    

                    