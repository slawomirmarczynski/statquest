#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_tests.py
    version: 0.5.1.1
    date: 25.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""
from unittest import TestCase

from statquest_observable import Observable
from statquest_tests import *


class TestTest(TestCase):

    def setUp(self):
        self.N = 100
        data_int = pd.Series(
            {i: int(100 * i) for i in range(1, self.N + 1)}, name='di')
        data_float = pd.Series(
            {i: float(100 * i + 0.5) for i in range(1, self.N + 1)}, name='df')
        data_str = pd.Series(
            {i: str(100 * i) for i in range(1, self.N + 1)}, name='ds')
        self.observable_ordinal = Observable(data_int)
        self.observable_continuous = Observable(data_float)
        self.observable_nominal = Observable(data_str)
        del data_int
        del data_float
        del data_str

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
