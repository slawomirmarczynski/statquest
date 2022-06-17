#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
An example/template for statquest_input() function.

File:
    project: StatQuest
    name: statquest_input.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""


from statquest_observable import Observable


def input_observables():
    obs1 = Observable('Observable1', {1: 1, 2: 3, 3: 1, 4: 2, 5: 6})
    obs2 = Observable('Observable1', {1: 1.0, 2: 3.2, 3: 1.1, 4: 2.1, 5: 6.1})
    obs3 = Observable('Observable1',
                      {1: 'red', 2: 'blue', 3: 'x', 4: 'y', 5: 'z', 6: 't'})
    return obs1, obs2, obs3
