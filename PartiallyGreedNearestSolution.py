#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Solution import Solution

class PartiallyGreedNearestSolution(Solution):
    def __init__(self, distances, alpha=.1):
        self.alpha = alpha
        super(PartiallyGreedNearestSolution, self).__init__(distances)


    def construct(self):
        import numpy as np
        # Create a empty route allocating all positions as source city - 0 (fisrt and last position must be source city, forming a cycle).
        route=[0 for x in range(self.n_cities)]
        # Number of cities on route
        n = len(route)
        # A list with all remaining cities to be inserted on the route.
        remaining_cities = range(1,n)
        # Setup Objective Function as zero.
        self.fo=0
        # Start from second position on route to penultimate position. 
        for j in range(1, n):
            # Position of last inserted city, defined as Origin City.
            origin = route[j-1]
            # Update new city on actual sequence and get a delta value formed with last and new routes. 
            route[j], delta = self.partiallyNearestNeighbour(origin, remaining_cities, self.alpha)
            # Sum delta to actual Objective Function
            self.fo+=delta
        # Sum to actual Objective Function a delta formed with last inserted city an source city.
        self.fo+=self.distances[route[-1], 0]
        # Return new formed route.
        return np.array(route)