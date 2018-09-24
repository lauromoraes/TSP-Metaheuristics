#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method import *
from Solution import *
from Descent import *
from SimulatedAnnealing import *

class MultiStart(Method):
    def __init__(self, solution):
        super(MultiStart, self).__init__(solution)

    def construct_solution(self, construct_type=1):
        if construct_type < 1 or construct_type > 4:
            construct_type = 1
            print('ERROR: invalid option ({}) for construct method. Switch to "Random Construct Method.".'.format(construct_type))
        solution = self.factory.setup_solution(construct_type)
        return solution

    def improve_solution(self, solution, method_type=1):
        if method_type==1:
            method = FirstImproventDescent(solution)
        elif method_type==2:
            method = BestImproventDescent(solution)
        elif method_type==3:
            method = SimulatedAnnealing(solution)
        solution = method.solution
        return solution

    # def get_neighbour_method(self, neighbour_type=1):
    #     if neighbour_type==1:
    #         neighbour_method = self.best_neighbour
    #     elif neighbour_type==2:
    #         neighbour_method = self.first_improvement_neighbour
    #     elif neighbour_type==3:
    #         neighbour_method = self.random_neighbour
    #     else:
    #         print('ERROR: invalid option ({}) for neighbour search. Switch to "best neighbour search".'.format(neighbour_type))
    #         neighbour_method = self.best_neighbour
    #     return neighbour_method


    def multi_start(self, iter_max=2500, construct_type=1, method_type=1):
        import copy
        fo_star = float('inf')
        cnt=0

        while cnt<iter_max:
            # Construct a solution
            solution = self.construct_solution(construct_type)
            # Improve current solution
            solution = self.improve_solution(solution, method_type)
            if solution.fo < fo_star:
                solution_star = copy.deepcopy(solution)
                fo_star = solution_star.fo
                cnt = 0
            cnt+=1
        self.solution = solution_star
        self.fo = self.solution.fo
        return self.solution


    def run(self):
        self.factory = SolutionFactory(self.distances)
        self.multi_start()
        # self.solution.fo = self.solution.fo # Update FO value on Solution object
        return self.solution.fo