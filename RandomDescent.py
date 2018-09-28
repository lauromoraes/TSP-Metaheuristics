# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 23:22:23 2018

@author: Meu computador
"""

from Method import Method

class RandomDescent(Method):
    def __init__(self, solution):
        super(RandomDescent, self).__init__(solution)

    def run(self):
        self.set_metrics('fos','stars')
        
        fo, route = self.solution.fo, self.solution.route
        it, iter_max = 0, 1000

        while it < iter_max:
            it += 1
            improved = True
            while improved:
                new_i, new_j, fo_new_neighbour = self.random_neighbour()
                self.metrics['fos'].append(fo_new_neighbour)
                self.metrics['stars'].append(fo)
                if fo_new_neighbour < fo:
                    it+=1
                    route[new_i], route[new_j] = route[new_j], route[new_i] # Apply movement
                    self.fo = fo = fo_new_neighbour
                else:
#                    it = 0
                    improved = False

        self.solution.fo = fo # Update FO value on Solution object
        return fo