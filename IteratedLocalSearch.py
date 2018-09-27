# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 22:24:27 2018

@author: Lauro Moraes
"""

from Method import Method

import random

class IteratedLocalSearch(Method):
    def __init__(self, solution):
        super(IteratedLocalSearch, self).__init__(solution)

    def run(self):
        self.setup_local_search(local_search_opt=1)
        self.iterated_local_search()
        return self.solution.fo
    
    def pertubation(self, S, num_levels=2):
        n = self.n_cities-1
        R = S.route
        
        while num_levels > 0:
            num_levels -= 1
            
            # Select two diferent cities i, j
            i = j = random.randint(1,n)
            while j==i:
                j = random.randint(1,n)

            R[i], R[j] = R[j], R[i]
        return S.calc_fo(), S
    
    def setup_local_search(self, local_search_opt = 0):
        local_search_opts = ('RandomDescent', 'FirstImproventDescent', 'BestImproventDescent')
        method_type = local_search_opts[local_search_opt]
        self.local_search_class = getattr(__import__(method_type), method_type)
#        self.method = self.local_search_class(self.solution)
#        self.solution = self.method.solution
    
    def iterated_local_search(self, max_levels=5, iterMax=2500):
        import copy
        S = copy.deepcopy(self.solution)
        level = 1
        cnt, cnt_abs = 0, 0
        while cnt < iterMax:
            cnt += 1
            cnt_abs += 1
            fo_perturbation, S = self.pertubation(S, num_levels=level+1)
            S = self.local_search_class(S).solution
            if cnt_abs % 100 == 0:
                print(cnt_abs, level, fo_perturbation, S.fo, self.solution.fo)
            if S.calc_fo() < self.solution.fo:
                print('UPDATE', cnt_abs, level, fo_perturbation, S.fo, self.solution.fo)
                self.solution = copy.deepcopy(S)
                level, cnt = 1, 0
            else:
                level += 1
                
        self.fo = self.solution.fo
        return self.solution