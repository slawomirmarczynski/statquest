#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The global variables to hold the configuration and defaults.

File:
    project: StatQuest
    name: statquest_globals.py
    version: 0.4.0.0
    date: 19.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl

Copyright (c) 2022 Sławomir Marczyński, slawek@zut.edu.pl.
"""

# Setup output files names. The program will use them without any warning
# i.e. it will not check whether any files already exist or not.
# Therefore, the program should be run in the appropriate working directory.

# @todo: The overwrite protection, definition of working (sub)directory,
#        better options to choose file names.
#
FREQS_CSV_FILE_NAME = 'freqs.csv'  # for the frequency statistics
STATS_CSV_FILE_NAME = 'stats.csv'  # for means, variances, medians etc.
TESTS_CSV_FILE_NAME = 'tests.csv'  # for detailed output of test results
TESTS_DOT_FILE_NAME = 'tests.gv'   # for a graph in DOT language (GraphViz)
TESTS_TXT_FILE_NAME = 'tests.txt'  # for write-ups of tests docs

# Default importance level alpha, it is a probability as a float number.
#
DEFAULT_ALPHA_LEVEL = 0.05
assert 0 <= DEFAULT_ALPHA_LEVEL <= 1.0
