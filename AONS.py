# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:40:05 2024

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

# AONS
def shuntengmogua(G, fangxiang_nodes, O_direction_all, chosen_nodes, candidate_nodes):
    
    fangxiang_nodes2 = copy.deepcopy(fangxiang_nodes)
    
    for i in fangxiang_nodes:
        chosen_nodes.add(i)
        fangxiang_nodes2.remove(i)
        
        best_node = i
        candidate_nodes.discard(best_node)
        candidate_nodes.difference_update(G.neighbors(best_node))
        
        if O_direction_all[i] >= 0:
            
            fangxiang_nodes2.add(O_direction_all[i])
            
    return chosen_nodes, fangxiang_nodes2, candidate_nodes
        

def dongjing_greedy_cover(G, o_ratio_jing, o_ratio, O, O_direction, O_direction_all):
    
    candidate_nodes = set(G.nodes())  
    chosen_nodes = set()  
    fangxiang_nodes = set()
    
    
    if sum(1 for x in O_direction if x >= 0) > 0:
        
        for i in O:
            if O_direction_all[i] >= 0:
                 chosen_nodes.add(i)
                 fangxiang_nodes.add(O_direction_all[i])
                 best_node = i
                 
                 candidate_nodes.discard(best_node)
                 candidate_nodes.difference_update(G.neighbors(best_node))
    
    
    candidate_nodes2 = copy.deepcopy(candidate_nodes)
    
    while len(candidate_nodes2) != 0:
        # print(candidate_nodes2)
        count = len(candidate_nodes2)
        for i in candidate_nodes2:
            if O_direction_all[i] >= 0:
                chosen_nodes, fangxiang_nodes, candidate_nodes2 = shuntengmogua(G, fangxiang_nodes, O_direction_all, chosen_nodes, candidate_nodes)
                # print(chosen_nodes, fangxiang_nodes, candidate_nodes)
                break
            else:
                count -= 1
                
        if len(fangxiang_nodes) == 0 or count == 0: 
            break
        
    # print(chosen_nodes, O_direction_all)
    
    num_chosen_nodes = round(G.number_of_nodes() * o_ratio)
    chosen_nodes_list = list(chosen_nodes)
    if len(chosen_nodes_list) >= num_chosen_nodes:
        chosen_nodes = set(chosen_nodes_list[:num_chosen_nodes])
    else:
        diff_set = set(G.nodes()) - chosen_nodes
        chosen_nodes.update(random.sample(diff_set, num_chosen_nodes - len(chosen_nodes)))
    # print(list(chosen_nodes))    
    new_array = np.array(list(chosen_nodes))  # 将抽取的节点重新封装为NumPy数组
    # print(new_array)
    result = create_O_direction(new_array, O_direction_all)

    return new_array, result