#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest.py
    version: 0.4.0.0
    date: 19.06.2022

Authors:
    Sławomir Marczyński

Copyright (c) 2022 Sławomir Marczyński.
"""

from unittest import TestCase

from statquest import *


class TestGlobals(TestCase):
    def test_DEFAULT_ALPHA_LEVEL(self):
        """default alpha level"""
        self.assertLessEqual(0.0, DEFAULT_ALPHA_LEVEL)
        self.assertGreaterEqual(1.0, DEFAULT_ALPHA_LEVEL)

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
