#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Problem import *
from Menu import *

def main():
    info_path='./inputs/C50INFO.TXT'
    cities_path='./inputs/C50.TXT'
    P=Problem('TSP', info_path, cities_path)
    menu=Menu(P)
    menu.run()


if __name__ == "__main__":
    main()
    print(' END '.center(50, '='))