#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest_filenames.py
    version: 0.5.0.5
    date: 19.02.2023

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
from tkinter import filedialog, ttk

from statquest_component import Component
from statquest_locale import setup_locale_translation_gettext
from statquest_tests import ALL_STATISTICAL_TESTS

_ = setup_locale_translation_gettext()


class Suite(Component):

    def __init__(self, parent_component, parent_frame, *args, **kwargs):
        super().__init__(parent_component, parent_frame, *args, **kwargs)

        self.tests_to_proceed = []

        def callback(*args):
            self.tests_to_proceed.clear()
            for t in self.switches:
                v, cb = self.switches[t]
                if v.get():
                    self.tests_to_proceed.append(t)

        label = ttk.Label(self._frame, text='Uruchamiane testy')
        label.grid(row=0, column=0, pady=(5, 20), sticky='w')

        self.switches = {}
        for i, t in enumerate(ALL_STATISTICAL_TESTS):
            v = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(self._frame, text=str(t), variable=v,
                                 onvalue=True, offvalue=False)
            cb.grid(row=i + 1, column=0, sticky='w')
            v.trace_add('write', callback=callback)
            self.switches[t] = v, cb
        callback()

    def get_selected(self):
        result = []
        for t in self.switches:
            v, cb = self.switches[t]
            if v.get():
                result.append(t)
        return result
