#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest.py
    version: 4.2.0.1
    date: 07.02.2022

Authors:
    Sławomir Marczyński

Copyright (c) 2022 Sławomir Marczyński.
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

    def test_run_1(self):
        """
        Empty run should fail.
        """
        computation_engine = ComputationEngine()
        with self.assertRaises(TypeError):
            computation_engine.run()


