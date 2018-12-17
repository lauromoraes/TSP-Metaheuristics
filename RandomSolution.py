#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Solution import Solution

class RandomSolution(Solution):
    def __init__(self, distances):
        super(RandomSolution, self).__init__(distances)
        self.route=self.construct()
        self.fo=self.calc_fo()

    def construct(self):
        import random
        import numpy as np
        aux=range(0,len(self.distances))
        random.shuffle(aux)
        return np.array(aux)