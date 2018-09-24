#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from Problem import *

class Menu(object):
    def __init__(self, problem):
        self.exec_flag=True
        self.problem=problem

    def run(self):
        while self.exec_flag:
            opt=self.screen_main()
            self.exec_operation(opt)

    def input_data(self):
        try:
            opt=int(raw_input('Choice: '))
        except Exception as e:
            print('> ERROR: invalid input character!')
            time.sleep(1)
            opt=-1
        finally:
            return opt

    def screen_main(self):
        opt=-1
        while opt<0 or opt>14:
            # os.system('cls' if os.name == 'nt' else 'clear')
            print(' {} '.format(self.problem.name).center(50, '='))
            print(' Main Menu '.center(50,'*'))
            if self.problem.solution==None:
                print('\t*** Need to create initial solution!')
            print('\t1. Initial Solution')
            print('\t2. Best Improvement Descent')
            print('\t3. First Improvement Descent')
            print('\t4. Simulated Annealing')
            print('\t5. Multi Start')
            print('\t0. Quit')
            print('*'*50)
            if self.problem.solution!=None:
                print('\t* FO of current solution: {}'.format(self.problem.solution.fo))
            opt=self.input_data()
        return opt

    def screen_construction(self):
        opt=-1
        while opt<1 or opt>5:
            # os.system('cls' if os.name == 'nt' else 'clear')
            print(' {} '.format(self.problem.name).center(50, '='))
            print(' Initial Solution '.center(50,'*'))
            print('\t1. Random Solution')
            print('\t2. Greed Solution (nearest neighbor)')
            print('\t3. Partially Greed Solution (nearest neighbor)')
            print('\t4. Greed Solution (cheapest insertion)')
            print('\t5. Partially Greed Solution (cheapest insertion)')
            print('*'*50)
            opt=self.input_data()
            self.problem.create_solution(opt)
        return opt

    def quit(self):
        self.exec_flag=False
        print('\nBye Bye!\n')
        time.sleep(.5)

    def exec_operation(self, opt):
        import time
        ini_time = time.clock()
        if opt==0:
            self.quit()
        elif opt==1:
            self.screen_construction()
        elif opt==2:
            print('\t* Best Improvement Descent')
            self.problem.apply_method('BestImproventDescent')
        elif opt==3:
            print('\t* First Improvement Descent')
            self.problem.apply_method('FirstImproventDescent')
        elif opt==4:
            print('\t* Simulated Annealing')
            self.problem.apply_method('SimulatedAnnealing')
        elif opt==5:
            print('\t* Multi Start')
            self.problem.apply_method('MultiStart')
        else:
            print('ERROR: invalid option ({})'.format(opt))
        print(self.problem.solution)
        print('Time {}'.format(time.clock()-ini_time))
        raw_input('\nPress ENTER to continue...')

