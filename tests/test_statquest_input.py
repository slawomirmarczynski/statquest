#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_input.py
    version: 0.5.0.0
    date: 16.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""

from unittest import TestCase

import pandas as pd

from typing import Container

from statquest_input import *


class TestInput(TestCase):

    def test_input_observables_1(self):
        """empty"""
        df = pd.DataFrame()
        observables = input_observables(df)
        self.assertIsInstance(observables, Container)
        self.assertFalse(observables)

    def test_input_observables_2(self):
        """too short"""
        df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        observables = input_observables(df)
        self.assertIsInstance(observables, Container)
        self.assertFalse(observables)

    def test_input_observables_3(self):
        """good"""
        df = pd.DataFrame(data={'col1': [-1, 3, 5, 17]})
        observables = input_observables(df)
        self.assertIsInstance(observables, Container)
        self.assertTrue(observables)
        for obs in observables:
            self.assertIsInstance(obs, Observable)
