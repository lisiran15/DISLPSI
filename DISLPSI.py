# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:42:51 2024

@author: M
"""
import networkx as nx
import random
import numpy as np
import math
import copy
import queue
import time
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
import warnings
# DISLPSI
def DIS(G, O, O_direction, a, Y, nodes_set, t_end_iter):
    
    source_list = np.array([], dtype=int)
    for s in G.nodes:
        
        if Y[s] == 1:
            
            E_T = np.array([], dtype=object)
            
            visited_nodes = np.array([], dtype=int)
            
            q = queue.Queue()
            
            q.put(s)
            visited_nodes = np.append(visited_nodes, s)
            
            
            
            while not q.empty():
                v = q.get()
                # print(q)
                # print(v)
                # print(set(G.neighbors(v)))
                for u in set(G.neighbors(v)):
                    if u not in visited_nodes:
                        if u in O:
                            if O_direction[u] == v or O_direction[u] == -1:
                                q.put(u)
                                edge = tuple((v, u))
                                # print(edge)
                                E_T = np.append(E_T, edge)
                                visited_nodes = np.append(visited_nodes, u)
                                # print(E_T)
                            elif O_direction[u] != v:
                                continue
                                
                        else:
                            q.put(u)
                            edge = tuple((v, u))
                            # print(edge)
                            E_T = np.append(E_T, edge)
                            visited_nodes = np.append(visited_nodes, u)
            # print(E_T)
            # print(len(E_T) / 2)
            
            
            if len(E_T) / 2 == len(G.nodes) - 1:
                # print(s)
                # print(E_T)
                edges_set = convert_to_node_pairs(E_T)
                # print(nodes_set)
                G_2 = Transf_Graph(nodes_set, edges_set)
                    
                # 调用LPSI
                C_s = LPSI(G_2, a, Y, t_end_iter)
                
                # print(C_s)
                if s in C_s:
                    # print(s)
                    source_list = np.append(source_list, s)
                
    return source_list