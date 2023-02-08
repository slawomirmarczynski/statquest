#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_tests.py
    version: 4.2.0.1
    date: 07.02.2022

Authors:
    Sławomir Marczyński

Copyright (c) 2022 Sławomir Marczyński.
"""
from unittest import TestCase

from statquest_observable import Observable
from statquest_tests import *


class TestTest(TestCase):

    def setUp(self):
        n = 100
        data_int = {1: 1, 2: 2, 3: 4, 4: 5, 5: 66, 6: 34, 7: -2}
        data_float = {1: 1.5, 2.3: 2, 3: 4, 4: 5, 5: 66, 6: 34, 7: -2.5}
        data_str = {1: 'a', 2: 'b', 3: 'c', 4: 'cc', 5: 'abc'}
        self.obs_ordinal = Observable('ord obs', data_int)
        self.obs_continuous = Observable('cont obs', data_float)
        self.obs_nominal = Observable('nom obs', data_str)

    def test___init__(self):
        # with self.assertRaises(TypeError):
        #     test = Test()
        self.assertIsInstance(self.test, Test)
        self.assertIsInstance(self.test.name, str)
        self.assertIsInstance(self.test.name_short, str)
        self.assertIsInstance(self.test.stat_name, str)
        self.assertIsInstance(self.test.h0_thesis, str)
        self.assertIsInstance(self.test.h1_thesis, str)
        self.assertIsInstance(self.test.prove_relationship, bool)
        self.assertTrue(self.test.name)
        self.assertTrue(self.test.name_short)
        self.assertTrue(self.test.stat_name)
        self.assertTrue(self.test.h0_thesis)
        self.assertTrue(self.test.h1_thesis)
        self.assertTrue(self.test.h0_thesis != self.test.h1_thesis)

    def test___call__(self):
        carried = 0
        skipped = 0
        for a in self.obs_ordinal, self.obs_continuous, self.obs_nominal:
            for b in self.obs_ordinal, self.obs_continuous, self.obs_nominal:
                if self.test.can_be_carried_out(a, b):
                    result = self.test(a, b)
                    self.assertIsInstance(result, Relation)
                    carried += 1
                else:
                    skipped += 1
        self.assertTrue(carried > 0)
        self.assertTrue(carried + skipped == 9)

    def test_can_be_carried_out(self):
        carried = 0
        for a in self.obs_ordinal, self.obs_continuous, self.obs_nominal:
            for b in self.obs_ordinal, self.obs_continuous, self.obs_nominal:
                result = self.test.can_be_carried_out(a, b)
                self.assertIsInstance(result, bool)
                if result:
                    carried += 1
        self.assertTrue(carried > 0)


class TestChiSquareIndependenceTest(TestTest):
    def setUp(self):
        super().setUp()
        self.test = ChiSquareIndependenceTest()


class TestKruskalWallisTest(TestTest):
    def setUp(self):
        super().setUp()
        self.test = KruskalWallisTest()


class TestPearsonCorrelationTest(TestTest):
    def setUp(self):
        super().setUp()
        self.test = PearsonCorrelationTest()


# Dirty trick that makes the base class invisible for unittest auto discovery.
#
del TestTest
