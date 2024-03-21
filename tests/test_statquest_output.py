#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_output.py
    version: 0.5.1.2
    date: 21.03.2024

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""

import os
from unittest import TestCase
from unittest.mock import ANY, MagicMock, Mock

from statquest_output import *


# class TestOutputX(TestCase):
#
#     def test_output(self):
#         """Args transmission"""
#         file_name = os.devnull
#         writer = Mock()
#         content = Mock()
#         output(file_name, writer, content, 'param', key1=1)
#         writer.assert_any_call(content, ANY, 'param', key1=1)


class TestOutput(TestCase):

    def test___init__1(self):
        with self.assertRaises(TypeError):
            output = Output()

    def test___init__2(self):
        parent_component = None
        output = Output(parent_component)
        self.assertIsNotNone(output)

    def test___init__3(self):
        parent_component = Mock()
        output = Output(parent_component)
        self.assertIsNotNone(output)

    def test_tests_csv(self):
        parent_component = Mock()
        parent_component.files_names.tests_csv.get.return_value = os.devnull
        output = Output(parent_component)
        relations = {(Mock(), Mock()): [Mock(), Mock(), Mock()]}
        alpha = 0.05
        output.tests_csv(relations, alpha)
