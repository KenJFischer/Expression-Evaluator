# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 19:59:52 2022

@author: Ken

Run this file to use the calculator

"""

import Calculator

calc = Calculator.Calculator()

while True:
    print(calc.evaluate(input()))