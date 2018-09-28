#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SolutionFactory(object):
    def __init__(self, distances):
        self.distances=distances

    def setup_solution(self, solution_type):
        solution=None
        if solution_type==1:
            solution=RandomSolution(self.distances)
        elif solution_type==2:
            solution=GreedNearestSolution(self.distances)
        elif solution_type==4:
            solution=GreedCheapestSolution(self.distances)
        else:
            print('ERROR: invalid solution type: {}'.format(solution_type))
        return solution

class Solution(object):
    def __init__(self, distances):
        self.distances=distances
        self.fo=-1
        self.n_cities=len(distances)
        self.route=self.construct()
        self.fo=self.calc_fo()
        if self.fo==-1:
            self.fo=self.calc_fo()

    def construct(self):
        raise NotImplementedError('Please implement this method')

    def __str__(self):
        self.fo=self.calc_fo()
        return '* ROUTE: {}\n* FO: {}'.format(' > '.join([str(x) for x in self.route]), self.fo)

    def calc_fo(self):
        # raise NotImplementedError('Please Implement this method')
        total=0
        for i in range(len(self.route)-1):
            origin, destination = self.route[i], self.route[i+1]
            total+=self.distances[origin, destination]
        self.fo = float(total)
        return self.fo
    
    def delta(self, i, j):
        n = self.n_cities-1
        i_before = n-1 if i==0   else i-1
        j_before = n-1 if j==0   else j-1
        i_after = i+1
        j_after = j+1
        # i_after  = 0   if i==n-1 else i+1
        # j_after  = 0   if j==n-1 else j+1
        R, D = self.route, self.distances
        return D[R[i_before], R[i]] + D[R[i], R[i_after]] + D[R[j_before], R[j]] + D[R[j], R[j_after]]

    def copy_stats(self, another_solution):
        for i in range(len(self.route)):
            self.route[i]=another_solution.route[i]
        self.fo = another_solution.fo

    def nearestNeighbour(self, origin, remaining_cities):
        dist, nearest_index = float('inf'), 0
        for i in range(len(remaining_cities)):
            destination = remaining_cities[i]
            # print(origin, destination)
            # print('>', i, destination, self.distances[origin, destination])
            # print('Origin {} - Dest {}: {}'.format(origin,destination, self.distances[origin, destination]))
            if dist > self.distances[origin, destination]:
                nearest, nearest_index, dist = destination, i, self.distances[origin, destination]
        # print('Origin {} - Dest {}'.format(origin,nearest))
        del remaining_cities[nearest_index]
        return nearest, dist

class GreedCheapestSolution(Solution):
    ''' Construct a Solution object by Chepeast Insertion procedure. '''
    def __init__(self, distances):
        super(GreedCheapestSolution, self).__init__(distances)

    def findCheapestPosition(self, current_city, route):
        best_delta, cheapest_position = float('inf'), 1
        for i in range(1,len(route)):
            origin, destination = route[i-1], route[i]
            delta = self.distances[origin, current_city] + self.distances[current_city, destination] - self.distances[origin, destination]
            if delta < best_delta:
                cheapest_position = i
                best_delta = delta
        return cheapest_position, best_delta

    def construct(self):
        self.fo=0
        route=[0 for x in range(3+1)]
        remaining_cities = range(1,self.n_cities)

        # Start a route by mounting a cycle with two cities using nearest neighbour aproach.
        for j in range(1, 3):
            origin = route[j-1]
            route[j], delta = self.nearestNeighbour(origin, remaining_cities)

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
            route.insert(best_position, remaining_cities[best_remaining])
            del remaining_cities[best_remaining]

        # Return new formed route.
        return route

class GreedNearestSolution(Solution):
    def __init__(self, distances):
        super(GreedNearestSolution, self).__init__(distances)

    def construct(self):
        # Create a empty route allocating all positions as source city - 0 (fisrt and last position must be source city, forming a cycle).
        route=[0 for x in range(self.n_cities+1)]
        # Number of cities on route
        n = len(route)-1
        # A list with all remaining cities to be inserted on the route.
        remaining_cities = range(1,n)
        # Setup Objective Function as zero.
        self.fo=0
        # Start from second position on route to penultimate position. 
        for j in range(1, n):
            # Position of last inserted city, defined as Origin City.
            origin = route[j-1]
            # Update new city on actual sequence and get a delta value formed with last and new routes. 
            route[j], delta = self.nearestNeighbour(origin, remaining_cities)
            # Sum delta to actual Objective Function
            self.fo+=delta
        # Sum to actual Objective Function a delta formed with last inserted city an source city.
        self.fo+=self.distances[route[-2], 0]
        # Return new formed route.
        return route

class RandomSolution(Solution):
    def __init__(self, distances):
        super(RandomSolution, self).__init__(distances)
        self.route=self.construct()
        self.fo=self.calc_fo()

    def construct(self):
        import random
        aux=range(1,len(self.distances))
        random.shuffle(aux)
        return [0]+aux+[0]