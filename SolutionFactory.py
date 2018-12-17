#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Solution import Solution
from RandomSolution import RandomSolution
from GreedNearestSolution import GreedNearestSolution
from PartiallyGreedNearestSolution import PartiallyGreedNearestSolution
from GreedCheapestSolution import GreedCheapestSolution
from PartiallyGreedCheapestSolution import PartiallyGreedCheapestSolution

class SolutionFactory(object):
    def __init__(self, distances):
        self.distances=distances

    def setup_solution(self, solution_type):
        solution=None
        if solution_type==1:
            solution=RandomSolution(self.distances)
        elif solution_type==2:
            solution=GreedNearestSolution(self.distances)
        elif solution_type==3:
            solution=PartiallyGreedNearestSolution(self.distances, alpha=.1)
        elif solution_type==4:
            solution=GreedCheapestSolution(self.distances)
        elif solution_type==5:
            solution=PartiallyGreedCheapestSolution(self.distances, alpha=.1)
        else:
            print('ERROR: invalid solution type: {}'.format(solution_type))
        return solution