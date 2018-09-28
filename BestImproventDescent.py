# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 23:20:48 2018

@author: Lauro Moraes
"""
from Method import Method

class BestImproventDescent(Method):
    def __init__(self, solution):
        super(BestImproventDescent, self).__init__(solution)

    def run(self):
        self.set_metrics('fos','stars')
        improved = True
        it = 0
        fo, route = self.solution.fo, self.solution.route
        while improved:
            best_i, best_j, fo_best_neighbour = self.best_neighbour()
            self.metrics['fos'].append(fo_best_neighbour)
            self.metrics['stars'].append(self.fo)
            if fo_best_neighbour < fo:
                it+=1
                route[best_i], route[best_j] = route[best_j], route[best_i] # Apply movement
                self.fo = fo = fo_best_neighbour
            else:
                improved = False
        self.solution.fo = fo # Update FO value on Solution object
        return fo, self.solution