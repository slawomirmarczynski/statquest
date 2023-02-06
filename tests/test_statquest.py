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

from statquest.statquest import ComputationEngine


class TestComputationEngine(TestCase):
    def test_init(self):
        computation_engine = ComputationEngine()
        self.assertIsNotNone(computation_engine)
