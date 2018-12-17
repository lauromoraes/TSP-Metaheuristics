# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 22:24:27 2018

@author: Lauro Moraes
"""

from Method import Method

import random
import numpy as np

class VariableNeighborhoodSearch(Method):
    def __init__(self, solution):
        super(VariableNeighborhoodSearch, self).__init__(solution)

    def run(self):
        self.set_metrics('foShake','foLocalSearch','foStar', 'level')
        self.setup_local_search(local_search_opt=1)
        self.variable_neighborhood_search()
#        self.plot_metrics()
        return self.solution.fo

    def selectPoints2opt(self):
        n = self.n_cities-1
        while True:
            i = j = random.randint(0,n)
            while j==i:
                j = random.randint(0,n)
            if i > j:
                i, j = j, i
            if j == i+2:
                continue
            if j==n:
                if i==0:
                    continue
                else:
                    i, j = 0, i
            break
        return i, j

    def selectPoints3opt(self):
        return sorted(random.sample(xrange(self.n_cities+1), 3))

    def swap3opt(self, S, R):
        a, b, c = self.selectPoints3opt()
        d, e, f = a+1, b+1, c+1
        R = list(R)
        which = random.randint(0, 3)
        if which == 0:
            new_R = R[:a+1] + R[c:b-1:-1] + R[e:d-1:-1] + R[f:]
        elif which == 1:
            new_R = R[:a+1] + R[d:e+1]    + R[b:c+1]    + R[f:]
        elif which == 2:
            new_R = R[:a+1] + R[d:e+1]    + R[c:b-1:-1] + R[f:]
        elif which == 3:
            new_R = R[:a+1] + R[e:d-1:-1] + R[b:c+1]    + R[f:]
        return np.array(new_R), S.calc_fo(R)

    def swap1opt(self, S, R):
        i, j = self.selectPoints2opt()
        n = len(R)-1
        i = j = random.randint(1,n)
        while j==i:
            j = random.randint(1,n)
        delta1 = S.delta(i, j)
        R[i], R[j] = R[j], R[i]
        delta2 = S.delta(i, j)
        new_fo = S.fo - delta1 + delta2
        return R, new_fo

    def swap2opt(self, S, R):
        i, j = self.selectPoints2opt()
        new_route = list(R[0:i])
        new_route.extend(reversed(R[i:j+1]))
        new_route.extend(R[j+1:])
        delta1 = S.delta(i, j)
        delta2 = S.delta(i+1, j+1)
        delta3 = S.delta(i, i+1)
        delta4 = S.delta(j, j+1)
        new_fo = S.fo + ((delta1+delta2)-(delta3+delta4))
        return new_route, new_fo

    def shake(self, S, k=0):
        n = self.n_cities-1
        R = S.route
        new_fo = S.fo

        i, j = self.selectPoints2opt()

        k = random.randint(0, 3)

        if k==0:
            R, new_fo = self.swap1opt(S, R)
        elif k==1:
            R, new_fo = self.swap2opt(S, R)
        elif k==2:
            R, new_fo = self.swap3opt(S, R)
        else:
            R, new_fo = self.swap1opt(S, R)

        S.fo = new_fo
        return new_fo, S
#        return S.calc_fo(), S
    
    def setup_local_search(self, local_search_opt = 1):
        local_search_opts = ('RandomDescent', 'FirstImproventDescent', 'BestImproventDescent')
        method_type = local_search_opts[local_search_opt]
        self.local_search_class = getattr(__import__(method_type), method_type)
#        self.method = self.local_search_class(self.solution)
#        self.solution = self.method.solution
    
    def variable_neighborhood_search(self, max_levels=5, iterMax=500):
        import copy
        S = copy.deepcopy(self.solution)
        level, maxRepeatsOnLevel = 0, 5
        cnt, cnt_abs = 0, 0
        while cnt < iterMax:
            # ============= Counters ================
            cnt += 1
            cnt_abs += 1
            # ============== Shake =================
            fo_shake, S = self.shake(S, k=level)
            # =========== Local Search =============
            S = self.local_search_class(S).solution
            # ============== Plot ==================
            self.metrics['foShake'].append(fo_shake)
            self.metrics['foLocalSearch'].append(S.fo)
            self.metrics['foStar'].append(self.solution.fo)
            self.metrics['level'].append(level)
            # ============== Track ==================
            if cnt_abs % 100 == 0:
                print(cnt_abs, level, fo_shake, S.fo, self.solution.fo)
            # ========= Neighborhood Change =========
            if S.calc_fo() < self.solution.fo:
                print('UPDATE', cnt_abs, level, fo_shake, S.fo, self.solution.fo)
                self.solution = copy.deepcopy(S)
                level, cnt = 0, 0
            else:
                level += 1
                
        self.fo = self.solution.fo
        return self.solution