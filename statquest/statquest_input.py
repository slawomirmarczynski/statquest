#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Component.

File:
    project: StatQuest
    name: statquest_input.py
    version: 0.5.1.1
    date: 25.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""

#  Copyright (c) 2023 Sławomir Marczyński. All rights reserved.
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
import tkinter as tk
from tkinter import ttk

import pandas as pd

import statquest_locale
from statquest_component import Component
from statquest_locale import setup_locale_translation_gettext
from statquest_observable import Observable

_ = setup_locale_translation_gettext()


class Input(Component):

    def __init__(self, parent_component, parent_frame, *args, **kwargs):
        super().__init__(parent_component, parent_frame, *args, **kwargs)

        self._empty_data_frame = pd.DataFrame()
        self._data_frame = self._empty_data_frame
        self._file_name = None
        self._code = None
        self.is_csv_file = False
        self.is_excel_file = False
        self._cbs = []

        def select_all(*args):
            for name, variable, checkbox in self._cbs:
                variable.set(True)

        def select_none(*args):
            for name, variable, checkbox in self._cbs:
                variable.set(False)

        label = ttk.Label(
            self._frame,
            text=_('Wybór kolumn'))
        button_all = ttk.Button(
            self._frame,
            text=_('wszystkie'),
            command=select_all)
        button_none = ttk.Button(
            self._frame, text=_('żadna'),
            command=select_none)
        label_spacer = ttk.Label(self._frame)

        label.grid(row=0, column=0, sticky='w', pady=5)
        button_all.grid(row=0, column=5, padx=20)
        button_none.grid(row=0, column=6, padx=20)
        label_spacer.grid(row=1, column=0)

    def update(self, *args):
        try:
            file_name = self._parent_component.files_names.input_csv.get()
            code = self._parent_component.parameters.locale_code.get()
            if file_name != self._file_name or code != self._code:
                self._data_frame = self._empty_data_frame
                self._file_name = file_name
                self._code = code
                self.is_csv_file = False
                self.is_excel_file = False
                for name, variable, checkbox in self._cbs:
                    checkbox.destroy()
                    del variable
                self._cbs.clear()
                if self._file_name and os.path.exists(self._file_name):
                    __, extension = os.path.splitext(self._file_name)
                    if extension.lower() == '.xlsx':
                        fmt = statquest_locale.setup_locale_excel_format(code)
                        df = pd.read_excel(self._file_name, **fmt)
                        self._data_frame = df
                        self.is_excel_file = True
                    else:
                        fmt = statquest_locale.setup_locale_csv_format(code)
                        df = pd.read_csv(self._file_name, **fmt)
                        self._data_frame = df
                        self.is_csv_file = True
                    i = 1
                    for name in self._data_frame:
                        i += 1
                        variable = tk.BooleanVar()
                        variable.set(True)
                        checkbox = ttk.Checkbutton(
                            self._frame,
                            text=name,
                            variable=variable,
                            onvalue=True,
                            offvalue=False)
                        checkbox.grid(row=i, column=1, sticky='we')
                        self._cbs.append((name, variable, checkbox))

                        try:
                            serie = self._data_frame[name].dropna()
                            obs = Observable(name, serie)
                            tn = 'nominal' if obs.IS_NOMINAL else '--'
                            to = 'ordinal' if obs.IS_ORDINAL else '--'
                            tc = 'continuous' if obs.IS_CONTINUOUS else '--'
                            ln = ttk.Label(self._frame, text=tn, width=10)
                            lo = ttk.Label(self._frame, text=to, width=10)
                            lc = ttk.Label(self._frame, text=tc, width=10)
                            ln.grid(row=i, column=2, sticky='w', padx=10)
                            lo.grid(row=i, column=3, sticky='w', padx=10)
                            lc.grid(row=i, column=4, sticky='w', padx=10)
                        except:
                            pass
        except:
            pass

    def set_locale(self, locale_code=None):
        self._code = locale_code
        self.update(self)

    def set_file_name(self, file_name):
        self._file_name = file_name
        self.update(self)

    def get_data_frame(self):
        headers = []
        for name, variable, checkbox in self._cbs:
            if variable.get():
                headers.append(name)
        try:
            df = self._data_frame.loc[:, headers]
        except:
            df = self._empty_data_frame
        return df

    def get_observables(self):
        data_frame = self.get_data_frame()
        observables = []
        drop_threshold = self._parent_component.parameters.drop_too_short.get()
        for index in data_frame:
            series = data_frame[index]
            try:
                obs = Observable(series)
                if len(obs) >= drop_threshold:
                    observables.append(obs)
            except:
                pass
        return observables


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
