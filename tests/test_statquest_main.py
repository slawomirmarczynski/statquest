#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest.py
    version: 0.5.0.5
    date: 19.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""

from unittest import TestCase

from statquest_engine import ComputationEngine


class TestComputationEngine(TestCase):
    def test_init(self):
        """
        Creating non-null computation engine.
        """
        computation_engine = ComputationEngine()
        self.assertIsNotNone(computation_engine)
