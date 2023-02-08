from unittest import TestCase

import pandas

from statquest_dataframe import *

class TestDataFrameProvider(TestCase):

    def test___init__(self):
        """create empty"""
        data_frame_provider = DataFrameProvider()
        self.assertIsNotNone(data_frame_provider)

    def test_set_locale_1(self):
        """default locale"""
        data_frame_provider = DataFrameProvider()
        data_frame_provider.set_locale()

    def test_set_locale_2(self):
        """default locale"""
        data_frame_provider = DataFrameProvider()
        data_frame_provider.set_locale('')
        data_frame_provider.set_locale(None)
        data_frame_provider.set_locale(False)

    def test_set_file_name(self):
        """empty for missing"""
        data_frame_provider = DataFrameProvider()
        data_frame_provider.set_file_name('random_784717643963_non_exist.file')

    def test_get(self):
        data_frame_provider = DataFrameProvider()
        result = data_frame_provider.get()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pandas.DataFrame)

