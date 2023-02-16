#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_locale.py
    version: 0.5.0.0
    date: 16.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""

from unittest import TestCase

from statquest_locale import *


class TestSetupLocaleTranslationGettext(TestCase):

    def test_1(self):
        """gettext interface"""
        result = setup_locale_translation_gettext()
        self.assertIsNotNone(result)

    def test_2(self):
        """gettext fallback"""
        translator = setup_locale_translation_gettext()
        source = 'This is random string 479207759234140750434371324893'
        translation = translator(source)
        self.assertEqual(source, translation)


class TestSetupLocaleCSV(TestCase):

    def test_1(self):
        """default locale argument"""
        result = setup_locale_csv_format()
        self.assertIsInstance(result, dict)
        self.assertTrue(result)

    def test_2(self):
        """pl_PL locale argument"""
        result = setup_locale_csv_format('pl_PL')
        self.assertIsInstance(result, dict)
        self.assertTrue(result)

    def test_3(self):
        """en_US locale argument"""
        result = setup_locale_csv_format('en_US')
        self.assertIsInstance(result, dict)
        self.assertTrue(result)

    def test_4(self):
        """bad locale argument"""
        with self.assertRaises(ValueError):
            setup_locale_csv_format('random_1283221634_unsuported_locale')

    def test_5(self):
        """bad locale argument"""
        with self.assertRaises(ValueError):
            setup_locale_csv_format(3.1415927)


class TestSetupLocaleExcel(TestCase):

    def test_1(self):
        """default locale argument"""
        result = setup_locale_excel_format()
        self.assertIsInstance(result, dict)
        self.assertTrue(result)
        result = setup_locale_excel_format('')
        self.assertIsInstance(result, dict)
        self.assertTrue(result)
        result = setup_locale_excel_format(None)
        self.assertIsInstance(result, dict)
        self.assertTrue(result)
        result = setup_locale_excel_format(False)
        self.assertIsInstance(result, dict)
        self.assertTrue(result)

    def test_2(self):
        """pl_PL locale argument"""
        result = setup_locale_excel_format('pl_PL')
        self.assertIsInstance(result, dict)
        self.assertTrue(result)

    def test_3(self):
        """en_US locale argument"""
        result = setup_locale_excel_format('en_US')
        self.assertIsInstance(result, dict)
        self.assertTrue(result)

    def test_4(self):
        """bad locale argument"""
        with self.assertRaises(ValueError):
            setup_locale_excel_format('random_1283221634_unsupported_locale')

    def test_5(self):
        """bad locale argument"""
        with self.assertRaises(ValueError):
            setup_locale_excel_format(3.1415927)
