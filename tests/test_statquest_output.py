#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_output.py
    version: 0.4.0.0
    date: 19.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl

Copyright (c) 2022 Sławomir Marczyński, slawek@zut.edu.pl.
"""
import os
from unittest import TestCase
import io

from statquest_output import *
from statquest_output import _print_csv


class TestOutput(TestCase):

    def test_output(self):
        """Parameter transmission"""
        test_args = tuple(k for k in range(10))
        test_kwargs = {('p' + str(k)): k for k in range(10)}
        test_content = ['test', 'content']

        def test_writer(content, file_name, *args, **kwargs):
            self.assertIsNotNone(file_name)
            self.assertIsNotNone(content)
            self.assertIsNotNone(args)
            self.assertIsNotNone(kwargs)
            self.assertListEqual(test_content, content)
            self.assertTupleEqual(test_args, args)
            self.assertDictEqual(test_kwargs, kwargs)

        file_name = os.devnull
        output(file_name, test_writer, test_content, *test_args, **test_kwargs)

    def test__print_csv_1(self):
        string = 'anything'
        sink = io.StringIO()
        _print_csv(string, end='', file=sink)
        self.assertEqual(string, sink.getvalue())

    def test__print_csv_2(self):
        string1 = 'anything1'
        string2 = 'anything2'
        sink = io.StringIO()
        _print_csv(string1, string2, file=sink)
        self.assertNotEqual(string1 + string2, sink.getvalue())

    def test_write_tests_doc(self):
        class spam():
            """Something important"""
        sink = io.StringIO()
        write_tests_doc((spam,), sink)
        result = sink.getvalue()
        self.assertNotEqual(-1, result.find("Something important"))

    def test_write_descriptive_statistics_csv(self):
        self.fail()

    def test_write_elements_freq_csv(self):
        self.fail()

    def test_write_relations_csv(self):
        self.fail()

    def test_write_relations_dot(self):
        self.fail()
