#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from Method import Method

random.seed(17)


class BestImproventDescent(Method):
    def __init__(self, solution):
        super(BestImproventDescent, self).__init__(solution)

    def run(self):
        improved = True
        it = 0
        fo, route = self.solution.fo, self.solution.route
        while improved:
            best_i, best_j, fo_best_neighbour = self.best_neighbour()
            if fo_best_neighbour < fo:
                it+=1
                route[best_i], route[best_j] = route[best_j], route[best_i] # Apply movement
                self.fo = fo = fo_best_neighbour
            else:
                improved = False
        self.solution.fo = fo # Update FO value on Solution object
        return fo
        
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
    
class RandomDescent(Method):
    def __init__(self, solution):
        super(RandomDescent, self).__init__(solution)

    def run(self):
        fo, route = self.solution.fo, self.solution.route
        it, iter_max = 0, 100

        while it < iter_max:
            it += 1
            improved = True
            while improved:
                new_i, new_j, fo_new_neighbour = self.random_neighbour()
                if fo_new_neighbour < fo:
                    it+=1
                    route[new_i], route[new_j] = route[new_j], route[new_i] # Apply movement
                    self.fo = fo = fo_new_neighbour
                else:
#                    it = 0
                    improved = False

        self.solution.fo = fo # Update FO value on Solution object
        return fo