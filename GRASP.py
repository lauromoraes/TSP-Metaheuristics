#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method import Method
from SolutionFactory import SolutionFactory
from FirstImproventDescent import FirstImproventDescent
from BestImproventDescent import BestImproventDescent
from SimulatedAnnealing import SimulatedAnnealing


class GRASP(Method):
    def __init__(self, solution):
        super(GRASP, self).__init__(solution)

    def construct_solution(self, construct_type=3):
        if construct_type != 3 and construct_type != 5:
            construct_type = 3
            print('ERROR: invalid option ({}) for construct method. Switch to "Partially Greed Nearest Solution.".'.format(construct_type))
        solution = self.factory.setup_solution(construct_type)
        return solution, solution.fo

    def improve_solution(self, solution, method_type=1):
        if method_type==1:
            method = FirstImproventDescent(solution)
        elif method_type==2:
            method = BestImproventDescent(solution)
        elif method_type==3:
            method = SimulatedAnnealing(solution)
        solution = method.solution
        return solution, solution.fo

    def multi_start(self, iter_max=1500, construct_type=3, method_type=1):
        self.set_metrics('constructedFo','refinedFo','stars')
        
        import copy
        fo_star = float('inf')
        cnt, cnt_abs = 0, 0

        while cnt<iter_max:
            cnt_abs += 1
            # Construct a solution
            solution, constructed_fo = self.construct_solution(construct_type)
            # Improve current solution
            solution, refined_fo = self.improve_solution(solution, method_type)
            if solution.fo < fo_star:
                solution_star = copy.deepcopy(solution)
                fo_star = solution_star.fo
                cnt = 0
                print('UPDATE', cnt_abs, cnt, constructed_fo, refined_fo, fo_star)
            cnt+=1
            self.metrics['constructedFo'].append(constructed_fo)
            self.metrics['refinedFo'].append(refined_fo)
            self.metrics['stars'].append(fo_star)
            if cnt_abs % 100 == 0:
                print(cnt_abs, cnt, constructed_fo, refined_fo, fo_star)
        self.solution = solution_star
        self.fo = self.solution.fo
        return self.solution


    def run(self):
        self.factory = SolutionFactory(self.distances)
        self.multi_start()
        return self.solution.fo