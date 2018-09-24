#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method import *
import random
import math

class SimulatedAnnealing(Method):
    def __init__(self, solution):
        super(SimulatedAnnealing, self).__init__(solution)
        

    def calcInitialTemperature(self, beta=2., gama=.95, SAmax=2500, initial_temperature=100):
        new_i = new_j = None
        temp = float(initial_temperature)
        processing = True
        fo = fo_star = fo_neighbour = self.solution.fo

        while processing:
            accepteds = 0
            for iterT in xrange(1,SAmax):
                # Gets only Objective Function of Random Neighbour.
                fo_neighbour = self.random_neighbour()[2]
                delta = fo_neighbour - fo
                if delta < 0:
                    accepteds+=1
                else:
                    if random.uniform(0,1) < math.exp(-delta/temp):
                        accepteds+=1
            if accepteds >= gama*SAmax:
                processing = False
            else:
                temp = beta*temp
        return temp

    def simulated_annealing(self, alfa=.98, SAmax=2500):
        import copy
        import matplotlib.pyplot as plt
        import numpy as np

        temp = float(self.initial_temperature)
        processing = True
        # Makes a star solution as deep copy of initial solution
        solution_star = copy.deepcopy(self.solution)
        fo_star = solution_star.fo
        # Current solution
        solution = self.solution
        fo = solution.fo
        route = solution.route

        temps = []
        stars = []
        fos = []

        while temp > 0.01:
            for iterT in xrange(0,SAmax):
                # Gets data of Solution line
                new_i, new_j, new_fo = self.random_neighbour()
                delta = new_fo - fo
                if delta < 0:
                    route[new_i], route[new_j] = route[new_j], route[new_i] # Apply movement
                    solution.fo = fo = new_fo
                    if new_fo < fo_star:
                        solution_star.copy_stats(solution)
                        # solution_star = copy.deepcopy(solution)
                        fo_star = solution_star.fo
                else:
                    if random.uniform(0,1) < math.exp(-delta/temp):
                        route[new_i], route[new_j] = route[new_j], route[new_i] # Apply movement
                        solution.fo = fo = new_fo
                temps.append(temp)
                stars.append(fo_star)
                fos.append(fo)
            temp = alfa*temp
            # temps.append(temp)
            # stars.append(fo_star)
            # fos.append(fo)
        self.solution = copy.deepcopy(solution_star)
        print(self.solution.fo)
        plt.plot(temps)
        plt.plot(stars)
        plt.plot(fos)
        plt.legend(['temps', 'stars', 'fos'])
        plt.show()
        return self.solution


    def run(self):
        self.initial_temperature = self.calcInitialTemperature()
        print('initial_temperature', self.initial_temperature)
        self.simulated_annealing()
        # self.solution.fo = self.solution.fo # Update FO value on Solution object
        return self.solution.fo
        