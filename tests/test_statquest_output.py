#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_output.py
    version: 0.5.0.5
    date: 19.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""

import os
from unittest import TestCase
from unittest.mock import ANY, MagicMock, Mock

from statquest_output import *


class TestOutput(TestCase):

    def test_output(self):
        """Args transmission"""
        file_name = os.devnull
        writer = Mock()
        content = Mock()
        output(file_name, writer, content, 'param', key1=1)
        writer.assert_any_call(content, ANY, 'param', key1=1)

    def test_write_tests_doc(self):
        """Writing from docstring to file"""
        content = "Something important"
        spamer = MagicMock()
        spamer.__doc__ = content
        sink = Mock()
        write_tests_doc((spamer,), sink)
        sink.write.assert_any_call(content)

    def test_write_descriptive_statistics_csv(self):
        obs = Mock()
        obs.IS_CONTINUOUS = True
        obs.descriptive_statistics.return_value = {'A': 123.45, 'B': 777.89}
        sink = Mock()
        write_descriptive_statistics_csv((obs,), sink)

    def test_write_elements_freq_csv(self):
        obs = Mock()
        obs.IS_ORDINAL = True
        obs.frequency_table.return_value = {1: 10, 2: 20, 3: 1}
        sink = Mock()
        write_elements_freq_csv((obs,), sink)
        sink.write.assert_called()

    # @todo: Unit tests for writers of relation/relations.
    #
    # def test_write_relations_csv(self):
    #     self.fail()
    #
    # def test_write_relations_dot(self):
    #     self.fail()
