#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest.py
    version: 0.4.0.2
    date: 07.02.2022

Authors:
    Sławomir Marczyński

Copyright (c) 2022 Sławomir Marczyński
"""

#  Copyright (c) 2022 Sławomir Marczyński. All rights reserved.
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met: 1. Redistributions of source code must retain the above
#  copyright notice, this list of conditions and the following
#  disclaimer. 2. Redistributions in binary form must reproduce the
#  above copyright notice, this list of conditions and the following
#  disclaimer in the documentation and/or other materials provided with
#  the distribution. 3. Neither the name of the copyright holder nor
#  the names of its contributors may be used to endorse or promote
#  products derived from this software without specific prior written
#  permission. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
#  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
#  BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
#  THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#  STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#  OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import pandas as pd
import statquest_locale


class DataFrameProvider:
    def __init__(self):
        self.__empty_data_frame = pd.DataFrame()
        self.__data_frame = self.__empty_data_frame
        self.__file_name = None
        self.__csv_format = statquest_locale.setup_locale_csv_format()
        self.is_csv_file = False
        self.is_excel_file = False

    def set_locale(self, locale_='default'):
        self.__csv_format = statquest_locale.setup_locale_csv_format(locale_)
        self.reload()

    def set_file_name(self, file_name):
        self.__file_name = file_name
        self.reload()

    def reload(self):
        self.is_csv_file = False
        self.is_excel_file = False
        try:
            if self.__file_name and os.path.exists(self.__file_name):
                __, extension = os.path.splitext(self.__file_name)
                if extension.lower() == '.xlsx':
                    decimal = self.__csv_format['decimal']
                    df = pd.read_excel(self.__file_name, decimal=decimal)
                    self.__data_frame = df
                    self.is_excel_file = True
                else:
                    df = pd.read_csv(self.__file_name, **self.__csv_format)
                    self.__data_frame = df
                    self.is_csv_file = True
        except:
            self.__data_frame = self.__empty_data_frame


    def get(self):
        return self.__data_frame

    def get_selected(self, headers):
        try:
            df = self.__data_frame.loc[:, headers]
        except:
            df = self.__empty_data_frame
        return df
