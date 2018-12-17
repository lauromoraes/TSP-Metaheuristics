#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random

class Solution(object):
    def __init__(self, distances):
        self.distances=distances
        self.fo=-1
        self.n_cities=len(distances)
        self.precision = 4
        self.route=self.construct()
        self.fo=self.calc_fo()
        if self.fo==-1:
            self.fo=self.calc_fo()

    def construct(self):
        raise NotImplementedError('Please implement this method')

    def __str__(self):
        self.fo=self.calc_fo()
        return '* ROUTE: {}\n* FO: {}'.format(' > '.join([str(x) for x in np.concatenate((self.route, [self.route[0]]))]), self.fo)

    def calc_fo(self, R=None):
        if R == None:
            R = self.route
        D = self.distances
        total=0.0
        # print(self.route)
        for i in range(1, len(R)):
            origin, destination = R[i-1], R[i]
            total+=D[origin, destination]
            # print(i-1, i, R[i-1], R[i])
        total+=self.distances[R[-1], R[0]]
        # print(R[-1], R[0])
        self.fo = round(float(total), self.precision)
        return self.fo
    
    def delta(self, i, j):
        n = self.n_cities
        i_before = n-1 if i==0   else i-1
        j_before = n-1 if j==0   else j-1
        i_after  = 0   if i==n-1 else i+1
        j_after  = 0   if j==n-1 else j+1
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

    def partiallyNearestNeighbour(self, origin, remaining_cities, alpha=.1):
        from random import randint
        from operator import itemgetter
        rank = list()
        dist, nearest_index = float('inf'), 0
        for i in range(len(remaining_cities)):
            destination = remaining_cities[i]
            dist = self.distances[origin, destination]
            rank.append((destination, i, self.distances[origin, destination]))
        rank.sort(key=itemgetter(2))
        cut = randint(0, int(len(rank)*alpha))
        del remaining_cities[rank[cut][1]]
        return rank[cut][0], rank[cut][2]

    def findCheapestPosition(self, current_city, route):
        best_delta, cheapest_position = float('inf'), 1
        D = self.distances
        for i in range(1,len(route)):
            origin, destination = route[i-1], route[i]
            delta = D[origin, current_city] + D[current_city, destination] - D[origin, destination]
            if delta < best_delta:
                cheapest_position = i
                best_delta = delta
        origin, destination = route[-1], route[0]
        delta = D[origin, current_city] + D[current_city, destination] - D[origin, destination]
        if delta < best_delta:
            cheapest_position = len(route)
            best_delta = delta
        return cheapest_position, best_delta

    def get_adjancent_cities_indexes(self, i):
        n = self.n_cities
        i_before = n-1 if i==0   else i-1
        i_after  = 0   if i==n-1 else i+1
        return i_before, i_after

    def reciprocal_exchange_perturbation(self):
        # Setup local variables
        n = self.n_cities-1
        # Select two distict indexes
        i = j = random.randint(0, n)
        while i == j:
            j = random.randint(0, n)
        delta1 = self.delta(i, j)
        self.route[i], self.route[j] = self.route[j], self.route[i]
        delta2 = self.delta(i, j)
        self.fo = self.fo - delta1 + delta2

        return self.route, self.fo


    def insertion_perturbation(self):
        # Setup local variables
        D, R = self.distances, self.route
        new_route = list()

        n = self.n_cities-1

        # Select two distict indexes
        i = j = random.randint(0, n)
        while i == j:
            j = random.randint(0, n)

        # Sort indexes to i < j
        if i > j:
            i, j = j, i

        # === Get relative indexes ===
        origin_1, destination_1 = self.get_adjancent_cities_indexes(i)
        origin_2, destination_2 = self.get_adjancent_cities_indexes(j)

        # print('{}, {}, {} | {}, {}, {}'.format(i, origin_1, destination_1, j, origin_2, destination_2))
        # print('{}, {}, {} | {}, {}, {}'.format(R[i], R[origin_1], R[destination_1], R[j], R[origin_2], R[destination_2]))

        # === Calculate costs ===
        # # Get origin and destination cities from i
        # delta_1 = D[R[origin_1], R[destination_1]] - D[R[origin_1], R[i]] - D[R[i], R[destination_1]]

        # # Get origin and destination cities from j
        # delta_2 = D[R[origin_2], R[i]] + D[R[i], R[j]] - D[R[origin_2], R[j]]

        # # Calculate new fo
        # new_fo = round(self.fo + delta_1 + delta_2, self.precision)

        # === Create new route ===
        # From beggining to origin of i
        new_route.extend(R[:i])
        # From destination of i to origin of j
        new_route.extend(R[destination_1:j])
        # Insert i
        new_route.append(R[i])
        # from j to end of route
        new_route.extend(R[j:])

        # print(self.route)
        # print(new_route)
        # print(len(new_route),  len(self.route))
        # print(new_fo,  self.calc_fo(R=new_route), (new_fo-self.calc_fo(R=new_route)))

        # # Verify lenght and cost integrity
        # assert len(new_route) == len(self.route)
        # assert new_fo == self.calc_fo(R=new_route)

        new_fo = self.calc_fo(R=new_route)

        return new_route, new_fo


    # def findPartiallyCheapestPosition(self, current_city, route, alpha=.1):
    #     from random import randint
    #     rank = list()
    #     best_delta, cheapest_position = float('inf'), 1
    #     D = self.distances
    #     for i in range(1,len(route)):
    #         origin, destination = route[i-1], route[i]
    #         delta = D[origin, current_city] + D[current_city, destination] - D[origin, destination]
    #         rank.append((delta, len(route)))
    #     origin, destination = route[-1], route[0]
    #     delta = D[origin, current_city] + D[current_city, destination] - D[origin, destination]
    #     rank.append((delta, len(route)))
    #     sorted(rank, key=lambda x:x[0])
    #     pos = randint(0, int(len(rank)*alpha))
    #     return rank[pos][1], rank[pos][0]