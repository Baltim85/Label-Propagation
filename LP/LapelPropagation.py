'''
@author: Mike.Pack
'''
# coding: utf8
import random

import numpy as np
from copy import deepcopy
import networkx.algorithms.community as nx_comm
import networkx as nx
import sys, math
#from time import time
#import ujson
#from _functools import partial
#import concurrent.futures

sys.path.append('../')
from Helper.LPAConstants import Constant as LPAC
from Helper.LPAMethods import LPAMethods as LPAM

#import multiprocessing
#from multiprocessing import Pool
#import functools

###### Not Used ###############################################################
#===============================================================================
# LapelPropagation Diese Klasse wird 
#===============================================================================
class LapelPropagation:
    
    #===========================================================================
    # Default constructor for LPA
    #===========================================================================
    def __init__(self):
        self.set_modularity(0.0000)
        self.set_maxIter(0)
        pass
    

    #===========================================================================
    # modularity will calculate the modularity for the actual graph and sets the 
    # modularity
    #
    # input: 
    # nx.Graph: The actual graph which is be used for the label Propagation Algorithm
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
        #fm = dict(zip(labelsNew.keys(), labelsNew.values()))
        return labelsNew
    
    #===========================================================================
    # Default
    #===========================================================================
    #def LP_Sync(self, graph, k, max_iter=20, version = False, rule="Unique", selection ="random", hop = 1, order = "random"
    def LP_Sync(self, graph, k, max_iter, version, rule, selection, hop, convergence, order):
        
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

        no = False
        
        oz =math.ceil(np.log10(len(np_nodes)))
        
        if(order == False):
            random.shuffle(np_nodes)
        while noConvergence:
            if(order == True):
                random.shuffle(np_nodes)

            #newLabels = deepcopy(labels)

            newLabels = self.fast_copy(labels)

            
            """if (version == LPAC._SYNC.value):
                pool = multiprocessing.Pool(processes=4)
                sy_prop = functools.partial(self.propagationStep, graph = graph, hop =  hop,labels =  labels, version =  version, labelsNew = labelsNew, selection = selection,newLabels=  newLabels)
                with Pool() as pool:
                #chunks = len(np_nodes) // 4 or 1
                #with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
                    #res = pool.map(sy_prop, np_nodes[:])
                    pool.map(sy_prop, np_nodes[:])
                    pool.close()
                    pool.join()
                    #k = []
                    #v = []
                    #gl = {}
                    #for r in res:
                    #    k.append(r)
                    print(labelsNew)
                    #print(res[0].keys(), res[0].values())
                    #for i in range(len(res)):
                    #    print(i)
                    #    k.append(res[i].keys())
                    #    v.append(res[i].values())
                    #print(k, v)
                    #gl = (dict(zip(k.keys(), v.values())))
                    #print(gl)
                    #res = executor.map(sy_prop, np_nodes, chunksize = chunks)
                    #pool.close()
                    #pool.join()
                    #print(res)"""
                     
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

                #labels = deepcopy(labelsNew)
            if(convergence == True):
                
                if(labels == newLabels):
                    noConvergence = False                
                    nx.set_node_attributes(graph, labels, "Community-ID")
                    LPAM.modularity(self, graph)
                    modul.append(self.get_modularity())
                    break
                if( i % 2 == 0):
                    if (labels == labelsT1):
                        j = 1
                        break
                    if (labels in ar):
                        eqLab += 1
                    
                    elif (labels != labelsT1):
                        labelsT1 = self.fast_copy(labels)
                        if(labels not in ar):
                            no = True
                        cIter = 0
                        
                elif(i % 2 != 0):
                    if(labels == labelsT2):
                        #cIter +=1
                        j = 1
                        break    
                    if (labels in ar):
                        eqLab += 1
                    elif(labels != labelsT2):
                        labelsT2 = self.fast_copy(labels)
                        #labelsT2 = deepcopy(labels)
                        if(labels not in ar):
                            no = True
                        cIter = 0
                if(cIter == oz or eqLab == oz or i == 100):
                    j = 1
                    break

            if(max_iter != 0 and convergence == False):
                if (i == max_iter-1):
                    noConvergence = False
                    nx.set_node_attributes(graph, labels, "Community-ID")
                    LPAM.modularity(self, graph)
                    modul.append(self.get_modularity())
                    break
            nx.set_node_attributes(graph, labels, "Community-ID")
            
            LPAM.modularity(self,graph)

            modul.append(self.get_modularity())
            
            if(no == True):
                ar = np.append(ar, deepcopy(labels))
                no = False
            i  += 1

        
        
        return i+1, self.get_modularity(), modul, j
    