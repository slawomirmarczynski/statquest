#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_input.py
    version: 0.4.0.0
    date: 19.06.2022

Authors:
    Sławomir Marczyński

Copyright (c) 2022 Sławomir Marczyński.
"""

from unittest import TestCase

import pandas as pd

from typing import Container

from statquest_input import *


class TestInput(TestCase):

    def test_input_observables(self):
        df = pd.DataFrame()
        observables = input_observables(df)
        self.assertIsNotNone(observables)
        # self.assertIsInstance(observables, Container)
        # self.assertTrue(observables)

    def test_input_observables1(self):
        df = pd.DataFrame()
        observables = input_observables(df)
        self.assertIsNotNone(observables)
        self.assertIsInstance(observables, Container)
        self.assertTrue(observables)
        for obs in observables:
            self.assertIsInstance(obs, Observable)
