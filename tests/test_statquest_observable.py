#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_observable.py
    version: 0.5.1.1
    date: 25.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""

import pandas as pd

import math
import random
from unittest import TestCase

from statquest_observable import Observable


class TestObservable(TestCase):

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

    def tearDown(self):
        pass

    def test___init__1(self):
        """create ordinal"""
        self.assertIsInstance(self.observable_ordinal, Observable)
        self.assertIsNotNone(self.observable_ordinal.data)
        self.assertIsNotNone(self.observable_ordinal.data.name)
        self.assertTrue(self.observable_ordinal.IS_ORDINAL)
        self.assertTrue(self.observable_ordinal.IS_CONTINUOUS)
        self.assertFalse(self.observable_ordinal.IS_NOMINAL)

    def test___init__2(self):
        """create continuous"""
        self.assertIsInstance(self.observable_continuous, Observable)
        self.assertIsNotNone(self.observable_continuous.data)
        self.assertIsNotNone(self.observable_continuous.data.name)
        self.assertEqual(False, self.observable_continuous.IS_ORDINAL)
        self.assertEqual(True, self.observable_continuous.IS_CONTINUOUS)
        self.assertEqual(False, self.observable_continuous.IS_NOMINAL)

    def test___init__3(self):
        """create nominal"""
        self.assertIsInstance(self.observable_nominal, Observable)
        self.assertIsNotNone(self.observable_nominal.data)
        self.assertIsNotNone(self.observable_nominal.data.name)
        self.assertEqual(False, self.observable_nominal.IS_ORDINAL)
        self.assertEqual(False, self.observable_nominal.IS_CONTINUOUS)
        self.assertEqual(True, self.observable_nominal.IS_NOMINAL)

    def test___init__4(self):
        """create buggy"""
        with self.assertRaises(TypeError):
            obs = Observable('O', {1: 1, 2: 2.0, 3: 'bug'})

    def test___init__5(self):
        """create empty"""
        with self.assertRaises(TypeError):
            obs = Observable('O', {})
            self.assertIsNone(obs)

    def test___getitem__1(self):
        """Access to observable data"""
        for i in range(1, self.N + 1):
            vo = self.observable_ordinal[i]
            vc = self.observable_continuous[i]
            vn = self.observable_nominal[i]
            self.assertEqual(int(100 * i), vo)
            self.assertEqual(float(100 * i + 0.5), vc)
            self.assertEqual(str(100 * i), vn)

    def test___getitem__2(self):
        """Access to observable data"""
        for i in range(self.N, 0, -1):
            vo = self.observable_ordinal[i]
            vc = self.observable_continuous[i]
            vn = self.observable_nominal[i]
            self.assertEqual(int(100 * i), vo)
            self.assertEqual(float(100 * i + 0.5), vc)
            self.assertEqual(str(100 * i), vn)

    def test___getitem__3(self):
        """Access to observable data"""
        for j in range(self.N):
            i = random.randint(1, self.N)
            vo = self.observable_ordinal[i]
            vc = self.observable_continuous[i]
            vn = self.observable_nominal[i]
            self.assertEqual(int(100 * i), vo)
            self.assertEqual(float(100 * i + 0.5), vc)
            self.assertEqual(str(100 * i), vn)

    def test___len__1(self):
        """Length of data"""
        lo = len(self.observable_ordinal)
        lc = len(self.observable_continuous)
        ln = len(self.observable_nominal)
        self.assertEqual(self.N, lo)
        self.assertEqual(self.N, lc)
        self.assertEqual(self.N, ln)

    def test___str__1(self):
        """Casting to str"""
        self.assertEqual('di', str(self.observable_ordinal))
        self.assertEqual('df', str(self.observable_continuous))
        self.assertEqual('ds', str(self.observable_nominal))
