#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy
import random
from operator import itemgetter 
import multiprocess
import itertools
from contextlib import closing
import gc

from Method import Method
from SolutionFactory import SolutionFactory
from FirstImproventDescent import FirstImproventDescent
from BestImproventDescent import BestImproventDescent
from SimulatedAnnealing import SimulatedAnnealing


class GeneticAlgorithm(Method):
    def __init__(self, solution):
        self.pop_size = 200
        self.epoch = 0
        self.prob_cross = 0.85
        self.prob_mut = 0.03
        self.population = None
        self.fos = None
        self.solution_star = None
        self.fo_star = None
        super(GeneticAlgorithm, self).__init__(solution)

    def construct_solution(self, construct_type=3):
        if construct_type != 3 and construct_type != 5:
            print('ERROR: invalid option ({}) for construct method. Switch to "Partially Greed Nearest Solution.".'.format(construct_type))
        solution = self.factory.setup_solution(construct_type)
        return solution, solution.fo

    def setup_local_search(self, local_search_opt = 1):
        local_search_opts = ('RandomDescent', 'FirstImproventDescent', 'BestImproventDescent')
        method_type = local_search_opts[local_search_opt]
        self.local_search_class = getattr(__import__(method_type), method_type)
        # self.local_search_class = list()
        # for i in range(2):
        #     method_type = local_search_opts[i]
        #     self.local_search_class.append( getattr(__import__(method_type), method_type) )

    def stop_criteria(self):
        print('Epoch: {} | STD Fo: {} | Star: {}'.format(self.epoch, np.std(self.fos), self.fo_star))
        return False if np.std(self.fos) < 0.01 and self.epoch > 1000 else True

    def update_star(self, solution):
        upgraded = False
        if solution.fo < self.fo_star:
            self.fo_star = solution.fo
            self.solution_star = copy.deepcopy(solution)
            upgraded = True
        return upgraded, self.solution_star, self.fo_star

    def init_population(self):
        self.population = list()
        self.fos = list()
        self.fo_star = float('inf')
        for i in range(self.pop_size):
            # Construct a solution
            solution, constructed_fo = self.construct_solution(construct_type=3)
            self.population.append(solution)
            self.fos.append(constructed_fo)
            self.update_star(solution)
        self.fos = np.array(self.fos)
        return self.population, self.solution_star, self.fo_star

    def tournament(self):
        n = self.pop_size-1
        # Select father 1
        i = j = random.randint(0,n)
        while i==j:
            j = random.randint(0,n)
        f1 = i if self.fos[i] < self.fos[j] else j 
        # Select father 2
        i = j = f1
        while i==j or i==f1 or j==f1:
            i = random.randint(0,n)
            j = random.randint(0,n)
        f2 = i if self.fos[i] < self.fos[j] else j
        if f1 > f2:
            f1, f2 = f2, f1
        return f1, f2

    def cross_over_ox(self, parent_1, parent_2, child_1, child_2):
        n = parent_1.n_cities
        cut_point_1 = random.randint(2, int(n/2))
        cut_point_2 = random.randint(1+int(n/2), n-3)

        gene_1 = np.array([-1 for x in range(n)])
        gene_2 = np.array([-1 for x in range(n)])


        pool_child_1 = set()
        pool_child_2 = set()
        for i in range(cut_point_1, cut_point_2+1):
            gene_1[i] = parent_2.route[i]
            gene_2[i] = parent_1.route[i]
            pool_child_1.add(parent_2.route[i])
            pool_child_2.add(parent_1.route[i])

        i_child, i_parent = 0, 0
        while i_child < n and gene_1[i_child] < 0:
            if parent_1.route[i_parent] not in pool_child_1:
                gene_1[i_child] = parent_1.route[i_parent]
                i_child += 1
            i_parent += 1
        i_child = cut_point_2+1
        while i_child < n and gene_1[i_child] < 0:
            if parent_1.route[i_parent] not in pool_child_1:
                gene_1[i_child] = parent_1.route[i_parent]
                i_child += 1
            i_parent += 1

        i_child, i_parent = 0, 0
        while i_child < n and gene_2[i_child] < 0:
            if parent_2.route[i_parent] not in pool_child_2:
                gene_2[i_child] = parent_2.route[i_parent]
                i_child += 1
            i_parent += 1
        i_child = cut_point_2+1
        while i_child < n and gene_2[i_child] < 0:
            if parent_2.route[i_parent] not in pool_child_2:
                gene_2[i_child] = parent_2.route[i_parent]
                i_child += 1
            i_parent += 1



        child_1.route = gene_1
        child_2.route = gene_2  

        child_1.calc_fo()
        child_2.calc_fo()

        # print('*'*20)
        # print(cut_point_1, cut_point_2)
        # print('parent_1')
        # print(parent_1)
        # print('parent_2')
        # print(parent_2)
        # print('child_1')
        # print(child_1)
        # print('child_2')
        # print(child_2)
        # print('*'*20)

        # raise Exception('TESTE')

        return child_1, child_2


    def cross_over(self, index_parent_1, index_parent_2):
        parent_1 = self.population[index_parent_1]
        parent_2 = self.population[index_parent_2]

        child_1 = copy.deepcopy(parent_1)
        child_2 = copy.deepcopy(parent_2)

        child_1, child_2 = self.cross_over_ox(parent_1, parent_2, child_1, child_2)

        # print('*'*10)
        # print('parent_1', parent_1.route)
        # print('parent_2', parent_2.route)
        # print('child_1', child_1.route)
        # print('child_2', child_2.route)
        # print('*'*10)

        return child_1, child_2

    def mutation(self, child):
        if self.prob_mut > random.uniform(0, 1):
            mutation_type = random.randint(0,1)
            if mutation_type == 0:
                child.route, child.fo = child.insertion_perturbation()
            elif mutation_type == 1:
                child.route, child.fo = child.reciprocal_exchange_perturbation()
        return child

    def survive(self, population=None):
        if population == None:
            population = self.population
        cnt = 0
        selected_indexes = self.roulett_whell(population)
        new_pop = itemgetter(*selected_indexes)(population)
        new_fos = np.array([ s.fo for s in new_pop ])

        # new_pop, new_fos = list(), list()
        # while cnt < self.pop_size:
        #     selected_index = self.roulett_whell(population)
        #     selected_organism = population[selected_index]
        #     new_pop.append(selected_organism)
        #     new_fos.append(selected_organism.fo)
        #     population.pop(selected_index)
        #     cnt += 1
        # self.population = new_pop
        assert len(self.population) == self.pop_size
        return new_pop,  new_fos


    def roulett_whell(self, population):
        max_bound = sum([ i.fo for i in population ])
        seletion_probs = [ i.fo/max_bound for i in population ]
        # index = np.random.choice(len(population), p=seletion_probs)
        indexes = np.random.choice(len(population), self.pop_size, p=seletion_probs, replace=False)
        return indexes
        # return np.random.choice(len(population), p=seletion_probs)

    def reproduction(self, max_childs=None):
        # Setup local variables
        num_childs = 0
        new_pop = list()
        new_fos = list()

        if max_childs == None:
            max_childs = self.pop_size * 2

        # Iterate to form new population
        while num_childs < max_childs:

            # Select two indexes for parents
            index_parent_1, index_parent_2 = self.tournament()

            # Perform cross over
            if self.prob_cross > random.uniform(0, 1):
                child_1, child_2 = self.cross_over(index_parent_1, index_parent_2)

            # Clone parents
            else:
                child_1, child_2 = self.population[index_parent_1], self.population[index_parent_2]

            # Perform mutation to child 1
            child1 = self.mutation(child_1)

            # Perform mutation to child 2
            child1 = self.mutation(child_2)

            # Allocate new child 1
            new_pop.append(child_1)
            new_fos.append(child_1.fo)

            # Allocate new child 2
            new_pop.append(child_2)
            new_fos.append(child_2.fo)

            improve_prob = 0.1
            if random.uniform(0,1) < improve_prob:
                child_1 = self.local_search_class(child_1).solution
                # search_type = random.randint(0,1)
                # child_1 = self.local_search_class[search_type](child_1).solution
            if random.uniform(0,1) < improve_prob:
                child_2 = self.local_search_class(child_2).solution
                # search_type = random.randint(0,1)
                # child_2 = self.local_search_class[search_type](child_2).solution

            if self.update_star(child_1)[0]:
                print('Update Star: {}'.format(self.fo_star))
            if self.update_star(child_2)[0]:
                print('Update Star: {}'.format(self.fo_star))

            # Update counter
            num_childs += 2

        return new_pop, new_fos

    def evolve(self):

        while self.stop_criteria():
            self.epoch += 1
            new_pop, new_fos = self.reproduction()
            self.population, self.fos = self.survive(new_pop)


    def run(self):
        self.factory = SolutionFactory(self.distances)
        self.setup_local_search(local_search_opt=1)
        self.init_population()
        self.evolve()
        self.solution = copy.deepcopy(self.solution_star)
        return self.solution_star.fo