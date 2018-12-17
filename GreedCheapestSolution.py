#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Solution import Solution

class GreedCheapestSolution(Solution):
    ''' Construct a Solution object by Chepeast Insertion procedure. '''
    def __init__(self, distances):
        super(GreedCheapestSolution, self).__init__(distances)

    def construct(self):
        import numpy as np
        self.fo=0
        route=[0 for x in range(3)]
        remaining_cities = range(1,self.n_cities)

        # Start a route by mounting a cycle with two cities using nearest neighbour aproach.
        for j in range(1, 3):
            origin = route[j-1]
            nearest, delta = self.nearestNeighbour(origin, remaining_cities)
            route[j] = nearest
        # print(route)

        # Allocate all remaining cities by iterative cheapest insertion procedure.
        while len(remaining_cities)>0:
            best_delta = float('inf')
            for i in range(len(remaining_cities)):
                # Remove and return first element from remaining list to be inserted on the current route.
                current_city = remaining_cities[i]
                # Find position on actual route to insert current city with minimum delta value.
                cheapest_position, delta = self.findCheapestPosition(current_city, route)
                if best_delta > delta:
                    best_delta, best_position, best_remaining = delta, cheapest_position, i
            # Insert current city on cheapest position of current route.
            # print("CHEAP {} - {}".format(remaining_cities[best_remaining], best_position))
            route.insert(best_position, remaining_cities[best_remaining])
            # print(route)
            del remaining_cities[best_remaining]
        # Return new formed route.
        return np.array(route)