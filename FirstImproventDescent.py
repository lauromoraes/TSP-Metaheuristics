# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 23:21:42 2018

@author: Meu computador
"""

from Method import Method

class FirstImproventDescent(Method):
    def __init__(self, solution):
        super(FirstImproventDescent, self).__init__(solution)

    def run(self):
        improved = True
        it = 0
        fo, route = self.solution.fo, self.solution.route
        while improved:
            best_i, best_j, fo_best_neighbour = self.first_improvement_neighbour()
            if fo_best_neighbour < fo:
                it+=1
                route[best_i], route[best_j] = route[best_j], route[best_i] # Apply movement
                self.fo = fo = fo_best_neighbour
            else:
                improved = False
        self.solution.fo = fo # Update FO value on Solution object
        return fo