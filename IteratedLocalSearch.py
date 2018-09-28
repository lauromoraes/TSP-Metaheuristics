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
        self.set_metrics('foPerturbation','foRefinemet','foStar', 'level')
        self.setup_local_search(local_search_opt=1)
        self.iterated_local_search()
#        self.plot_metrics()
        return self.solution.fo
    
    def pertubation(self, S, num_levels=2):
        n = self.n_cities-2
        R = S.route
        new_fo = S.fo
        
        while num_levels > 0:
            num_levels -= 1
            
            # Select two diferent cities i, j
            i = j = random.randint(1,n)
            while j==i:
                j = random.randint(1,n)
            delta1 = S.delta(i, j)
            R[i], R[j] = R[j], R[i]
            delta2 = S.delta(i, j)
            new_fo = new_fo - delta1 + delta2
#            print(i, j, delta1, delta2, new_fo, (new_fo-delta2+delta1) )
        S.fo = new_fo
        return new_fo, S
#        return S.calc_fo(), S
    
    def setup_local_search(self, local_search_opt = 1):
        local_search_opts = ('RandomDescent', 'FirstImproventDescent', 'BestImproventDescent')
        method_type = local_search_opts[local_search_opt]
        self.local_search_class = getattr(__import__(method_type), method_type)
#        self.method = self.local_search_class(self.solution)
#        self.solution = self.method.solution
    
    def iterated_local_search(self, max_levels=5, iterMax=500):
        import copy
        S = copy.deepcopy(self.solution)
        level, maxRepeatsOnLevel = 1, 5
        cnt, cnt_abs = 0, 0
        while cnt < iterMax:
            cnt += 1
            cnt_abs += 1
            fo_perturbation, S = self.pertubation(S, num_levels=level+1)
            S = self.local_search_class(S).solution
            self.metrics['foPerturbation'].append(fo_perturbation)
            self.metrics['foRefinemet'].append(S.fo)
            self.metrics['foStar'].append(self.solution.fo)
            self.metrics['level'].append(level)
            if cnt_abs % 100 == 0:
                print(cnt_abs, level, fo_perturbation, S.fo, self.solution.fo)
            if S.calc_fo() < self.solution.fo:
                print('UPDATE', cnt_abs, level, fo_perturbation, S.fo, self.solution.fo)
                self.solution = copy.deepcopy(S)
                level, cnt, repeatsOnLevel = 1, 0, 1
            else:
                if repeatsOnLevel > maxRepeatsOnLevel:
                    level += 1
                    repeatsOnLevel = 1
                else:
                    repeatsOnLevel += 1
                
        self.fo = self.solution.fo
        return self.solution