#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_globals.py
    version: 0.4.0.0
    date: 19.6.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl

Copyright (c) 2022 Sławomir Marczyński, slawek@zut.edu.pl.
"""

from unittest import TestCase

from statquest_globals import *


class TestGlobals(TestCase):
    def test_DEFAULT_ALPHA_LEVEL(self):
        """default alpha level"""
        self.assertLessEqual(0.0, DEFAULT_ALPHA_LEVEL)
        self.assertGreaterEqual(1.0, DEFAULT_ALPHA_LEVEL)

    TESTS_CSV_FILE_NAME = 'tests.csv'  # for detailed output of test results
    TESTS_DOT_FILE_NAME = 'tests.gv'  # for a graph in DOT language (GraphViz)
    TESTS_TXT_FILE_NAME = 'tests.txt'  # for write-ups of tests docs
    STATS_CSV_FILE_NAME = 'stats.csv'  # for means, variances, medians etc.

    def test_FREQS_CSV_FILE_NAME(self):
        self.assertIsNotNone(FREQS_CSV_FILE_NAME)
        self.assertIsInstance(FREQS_CSV_FILE_NAME, str)
        self.assertGreater(len(FREQS_CSV_FILE_NAME), 0)

    def test_STATS_CSV_FILE_NAME(self):
        self.assertIsNotNone(STATS_CSV_FILE_NAME)
        self.assertIsInstance(STATS_CSV_FILE_NAME, str)
        self.assertGreater(len(STATS_CSV_FILE_NAME), 0)

    def test_TESTS_CSV_FILE_NAME(self):
        self.assertIsNotNone(TESTS_CSV_FILE_NAME)
        self.assertIsInstance(TESTS_CSV_FILE_NAME, str)
        self.assertGreater(len(TESTS_CSV_FILE_NAME), 0)

    def test_TESTS_DOT_FILE_NAME(self):
        self.assertIsNotNone(TESTS_DOT_FILE_NAME)
        self.assertIsInstance(TESTS_DOT_FILE_NAME, str)
        self.assertGreater(len(TESTS_DOT_FILE_NAME), 0)

    def test_TESTS_TXT_FILE_NAME(self):
        self.assertIsNotNone(TESTS_TXT_FILE_NAME)
        self.assertIsInstance(TESTS_TXT_FILE_NAME, str)
        self.assertGreater(len(TESTS_TXT_FILE_NAME), 0)
