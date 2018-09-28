#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class Method(object):
    def __init__(self, solution):
        self.initial_solution=self.solution=solution
        self.n_cities=solution.n_cities
        self.distances=solution.distances
        self.fo=solution.fo
        self.metrics=None
        self.run()

    def run(self):
        raise NotImplementedError('Please implement this method')
    
    def set_metrics(self, *names):
        self.metrics = { metricName:[] for metricName in list(names) }
        return self.metrics
    
    def plot_metrics(self):
        import matplotlib.pyplot as plt
        
        for metricName, values in self.metrics.items():
            plt.plot(values)
        plt.legend(self.metrics.keys())
        plt.show()
    
    def local_search(self, solution, method_type=1):
        from Descent import FirstImproventDescent, BestImproventDescent, SimulatedAnnealing

        if method_type==1:
            method = FirstImproventDescent(solution)
        elif method_type==2:
            method = BestImproventDescent(solution)
        elif method_type==3:
            method = SimulatedAnnealing(solution)

        return solution.fo, method.solution

    def search_neighbour(self):
        raise NotImplementedError('Please implement this method')

    def best_neighbour(self):
        n=self.n_cities
        route=self.solution.route
        fo_best_neighbour=fo=self.fo
        best_i = best_j = None

        # For each city i
        for i in range(1,n-1):
            # For each city j
            for j in range(i+1, n):
                # Verify total value with edges formed with selecteds cities and respectives neighbours. Called delta value.
                delta1 = self.delta(i, j)
                # Apply movement. Switch allocation of cities i and j on the route.
                route[i], route[j] = route[j], route[i]
                # Verify new delta value.
                delta2 = self.delta(i, j)
                # Calculate new Objective Function formed by switch.
                fo_neighbour = fo - delta1 + delta2
                # Verify if this new Objective Function is better.
                if fo_neighbour < fo_best_neighbour:
                    # Store current best positions.
                    best_i, best_j = i, j
                    # Store new best Objective Function.
                    fo_best_neighbour = fo_neighbour
                # Switch back positions of cities, restoring previus route.
                route[i], route[j] = route[j], route[i] # Remove movement
        return best_i, best_j, fo_best_neighbour

    def adjacent_neighbour(self):
        n=self.n_cities
        print('best_neighbour', n)
        route=self.solution.route
        fo_best_neighbour=fo=self.fo
        best_i = best_j = None

        # For each city i
        for i in range(1,n-1):
            j = i+1
            # Verify total value with edges formed with selecteds cities and respectives neighbours. Called delta value.
            delta1 = self.delta(i, j)
            # Apply movement. Switch allocation of cities i and j on the route.
            route[i], route[j] = route[j], route[i]
            # Verify new delta value.
            delta2 = self.delta(i, j)
            # Calculate new Objective Function formed by switch.
            fo_neighbour = fo - delta1 + delta2
            # Verify if this new Objective Function is better.
            if fo_neighbour < fo_best_neighbour:
                # Store current best positions.
                best_i, best_j = i, j
                # Store new best Objective Function.
                fo_best_neighbour = fo_neighbour
            # Switch back positions of cities, restoring previus route.
            route[i], route[j] = route[j], route[i] # Remove movement
        return best_i, best_j, fo_best_neighbour

    def first_improvement_neighbour(self):
        n=self.n_cities
        route=self.solution.route
        improved=False
        fo_best_neighbour=fo=self.fo
        positions=range(1,n)
        random.shuffle(positions)
        best_i = best_j = None

        for i in range(len(positions)-1):
            for j in range(i+1, len(positions)):
                # print(i, j)
                # print(positions[i], positions[j])
                delta1 = self.delta(positions[i], positions[j])
                route[positions[i]], route[positions[j]] = route[positions[j]], route[positions[i]] # Apply movement
                delta2 = self.delta(positions[i], positions[j])
                fo_neighbour = fo - delta1 + delta2
                if fo_neighbour < fo_best_neighbour:
                    best_i, best_j = positions[i], positions[j]
                    fo_best_neighbour = fo_neighbour
                    improved = True
                route[positions[i]], route[positions[j]] = route[positions[j]], route[positions[i]] # Remove movement
                if improved:
                    break
            if improved:
                break
        return best_i, best_j, fo_best_neighbour

    def random_neighbour(self):
        n=self.n_cities-1
        route=self.solution.route
        fo_new_neighbour = fo = self.fo = self.solution.fo

        # Select two diferent cities i, j
        i = j = random.randint(1,n)
        while j==i:
            j = random.randint(1,n)
        # Verify total value with edges formed with selecteds cities and respectives neighbours. Called delta value.
        delta1 = self.delta(i, j)
        # Apply movement. Switch allocation of cities i and j on the route.
        route[i], route[j] = route[j], route[i]
        # Verify new delta value.
        delta2 = self.delta(i, j)
        # Calculate new Objective Function formed by switch.
        fo_new_neighbour = fo - delta1 + delta2
        # Switch back positions of cities, restoring previus route.
        route[i], route[j] = route[j], route[i] # Remove movement
        return i, j, fo_new_neighbour

    def delta(self, i, j):
        n = self.n_cities-1
        i_before = n-1 if i==0   else i-1
        j_before = n-1 if j==0   else j-1
        i_after = i+1
        j_after = j+1
        # i_after  = 0   if i==n-1 else i+1
        # j_after  = 0   if j==n-1 else j+1
        R, D = self.solution.route, self.distances
        # if i_after >=50 or j_after >= 50:
        #     print(i_after, j_after)
        #     print([x for x in range(len(R))])
        #     print(R)
        return D[R[i_before], R[i]] + D[R[i], R[i_after]] + D[R[j_before], R[j]] + D[R[j], R[j_after]]