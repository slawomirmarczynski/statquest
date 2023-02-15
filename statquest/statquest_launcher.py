#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest.py
    version: 0.4.2.1
    date: 07.02.2023

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

import ydata_profiling as pandas_profiling

from progress import Progress
from statquest_component import Component

from statquest_relations import Relations

from statquest_locale import setup_locale_translation_gettext


_ = setup_locale_translation_gettext()


class Launcher(Component):
    def __init__(self, parent_component, parent_frame, *args, **kwargs):
        super().__init__(parent_component, parent_frame, *args, **kwargs)

        def enable_siblings(enable):
            stack = [self._frame.master]
            while stack:
                widget = stack.pop(0)
                stack.extend(widget.winfo_children())
                try:
                    widget['state'] = 'normal' if enable else 'disable'
                except tk.TclError:
                    pass

        def engine():
            if parent_component.parameters.need_profile.get():
                data_frame = parent_component.input.get_data_frame()
                if not data_frame.empty:
                    data_frame = data_frame.copy()  # should defrag data_frame
                    plot_parameters = {"dpi": 300, "image_format": "png"}
                    if parent_component.parameters.need_correlations.get():
                        profile_report = pandas_profiling.ProfileReport(
                            data_frame,
                            plot=plot_parameters)
                    else:
                        profile_report = pandas_profiling.ProfileReport(
                            data_frame,
                            correlations=None,
                            plot=plot_parameters)
                    file_name = parent_component.files_names.profi_htm.get()
                    profile_report.to_file(file_name)

            alpha = parent_component.parameters.alpha.get()
            tests = parent_component.suite.get_selected()
            observables = parent_component.input.get_observables()
            relations = Relations.create_relations(observables, tests,
                                                   progress=self.progress)
            significant_relations = Relations.credible_only(relations, alpha)

            parent_component.output.tests_txt(tests)
            parent_component.output.stats_csv(observables)
            parent_component.output.freqs_csv(observables)
            parent_component.output.tests_csv(relations, alpha)
            parent_component.output.tests_dot(significant_relations)
            parent_component.output.tests_nx(significant_relations)

        def callback(*args):
            enable_siblings(False)
            label['text'] = 'przeprowadzam obliczenia'
            label['state'] = 'normal'
            self._frame.master.update()
            try:
                engine()
            except Exception as ex:
                print(ex)
                tk.messagebox.showwarning(
                    title='StatQuest',
                    message='Coś nie tak, może po prostu brak danych?\n'
                            'Sprawdź i spróbuj ponownie')
            label['text'] = ''
            enable_siblings(True)
            self.progress.set(0)

        button = ttk.Button(self._frame,
                            text="Uruchom obliczenia",
                            command=callback)
        button.grid(row=0, column=0, padx=20)

        label = ttk.Label(self._frame,
                          width=30)
        label.grid(row=0, column=1, padx=20)

        self.progress = Progress(self._frame)
        self.progress.progress.grid(row=0, column=2, sticky='we')
        self._frame.grid_columnconfigure(2, weight=1)
        self._frame.grid_columnconfigure(3, weight=1)
