#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""

from statquest_globals import *
from statquest_input import input_observables
from statquest_output import *
from statquest_relations import Relations
from statquest_statistics import ALL_STATISTICAL_TESTS

if __name__ == '__main__':
    tests = ALL_STATISTICAL_TESTS
    output(TESTS_TXT_FILE_NAME, write_tests_descriptions, tests)

    observables = input_observables()
    output(STATS_CSV_FILE_NAME, write_descriptive_statistics, observables)
    output(FREQS_CSV_FILE_NAME, write_elements_freq, observables)

    relations = Relations.create_relations(observables, tests)
    output(TESTS_CSV_FILE_NAME, write_relations_csv, relations)

    significant_relations = relations.filter(DEFAULT_ALPHA_LEVEL)
    output(TESTS_DOT_FILE_NAME, write_relations_dot, significant_relations)
