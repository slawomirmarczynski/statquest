#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest_parameters.py
    version: 0.5.1.1
    date: 25.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński
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


import tkinter as tk
from tkinter import ttk

from statquest_component import Component
from statquest_locale import get_default_locale_code, get_supported_locales, \
    setup_locale_translation_gettext

_ = setup_locale_translation_gettext()


class Parameters(Component):
    """
    Konfigurowanie parametrów pracy programu.
    """

    def __init__(self, parent_component, parent_frame, *args, **kwargs):
        super().__init__(parent_component, parent_frame, *args, **kwargs)

        DEFAULT_ALPHA_LEVEL = 0.05
        assert 0 <= DEFAULT_ALPHA_LEVEL <= 1.0

        self.alpha = tk.DoubleVar(value=DEFAULT_ALPHA_LEVEL)
        self.need_profile = tk.BooleanVar(value=False)
        self.need_correlations = tk.BooleanVar(value=False)
        self.locale_code = tk.StringVar(value=get_default_locale_code())
        self.drop_too_short = tk.IntVar(value=2)

        def alpha_validator(string):
            """
            Sprawdza czy wartość wpisana w kontrolkę jest liczbą z przedziału
            od 0 do 1, czyli mogącą określać prawdopodobieństwo.

            Args:
                string (str): wpisana liczba jako napis.

            Returns:
                True jeżeli walidacja zakończyła się pomyślnie, False jeżeli
                nie powiodła się.
            """
            try:
                value = float(string)
                return 0 <= value <= 1
            except:
                return False

        registred_alpha_validator = self._frame.register(alpha_validator)

        def drop_too_short_validator(string):
            try:
                value = int(string)
                return value > 1
            except:
                return False

        registred_drop_to_short = self._frame.register(
            drop_too_short_validator)

        def callback_correlations(*args):
            checkbox_correlations['state'] = (
                'normal' if self.need_profile.get() else 'disabled')
            self.callback(*args)

        self.alpha.trace_add('write', self.callback)
        self.need_profile.trace_add('write', callback_correlations)
        self.need_correlations.trace_add('write', self.callback)
        self.locale_code.trace_add('write', self.callback)

        label = ttk.Label(self._frame, text=_('Parameters'))
        label.grid(row=0, column=0, columnspan=4, sticky='w')

        label_alpha = ttk.Label(
            self._frame,
            text=_('The significance level α for p-value:'))
        label_alpha.grid(row=1, column=0, sticky='e')

        spinbox_alpha = ttk.Spinbox(
            self._frame, from_=0, to=1, increment=0.01, format="%.2f",
            width=10,
            textvariable=self.alpha,
            validate='all', validatecommand=(registred_alpha_validator, '%P'))
        spinbox_alpha.grid(row=1, column=1, sticky='w')
        label_alpha_comment = ttk.Label(
            self._frame,
            text=_('The α value is a probability, therefore 0 ⩽ α ⩽ 1.'))
        label_alpha_comment.grid(row=1, column=2, sticky='w')

        checkbox_profile = ttk.Checkbutton(
            self._frame,
            text=_('should generate Ydata Profile'),
            variable=self.need_profile, onvalue=True, offvalue=False)
        checkbox_profile.grid(row=2, column=0, sticky='w')
        label_profile_comment = ttk.Label(
            self._frame,
            text=_('This option is not dependent on tests.'))
        label_profile_comment.grid(row=2, column=2, sticky='w')
        checkbox_correlations = ttk.Checkbutton(
            self._frame,
            text=_('should compute correlations in Ydata Profile '),
            variable=self.need_correlations,
            onvalue=True, offvalue=False)
        checkbox_correlations.grid(row=3, column=0, sticky='w')
        label_profile_comment_correlations = ttk.Label(
            self._frame,
            text=_('Turn on correlations in Ydata Profile.'))
        label_profile_comment_correlations.grid(row=3, column=2, sticky='w')

        label_locale = ttk.Label(self._frame, text=_('locale settings:'))
        label_locale.grid(row=4, column=0, sticky='e')
        combobox_locale = ttk.Combobox(self._frame, width=8,
                                       textvariable=self.locale_code)
        combobox_locale.grid(row=4, column=1, sticky='w')
        combobox_locale['values'] = get_supported_locales()
        label_locale_comment = ttk.Label(
            self._frame,
            text=_('The decimal separator, the CSV separator encodings.'))
        label_locale_comment.grid(row=4, column=2, sticky='w')

        label_drop = ttk.Label(
            self._frame,
            text=_('the data threshold:'))
        label_drop.grid(row=5, column=0, sticky='e')
        spinbox_drop = ttk.Spinbox(
            self._frame, from_=2, to=1000000, increment=1,
            width=10,
            textvariable=self.drop_too_short,
            validate='all', validatecommand=(registred_drop_to_short, '%P'))
        spinbox_drop.grid(row=5, column=1, sticky='w')
        leabel_drop_comment = ttk.Label(
            self._frame,
            text=_("If the amount of data in the column is less than the"
                   " threshold, then whole column will be rejected as not"
                   " representative of the data."))
        leabel_drop_comment.grid(row=5, column=2, sticky='w')

        for widget in self._frame.winfo_children():
            widget.grid_configure(padx=5, pady=5)

        callback_correlations()
        self.callback()
