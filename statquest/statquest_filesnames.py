#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileNames class as a Component subclass.

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

import os
import re
import tkinter as tk
from tkinter import filedialog, ttk

from statquest_component import Component


class FilesNames(Component):
    """
    The choice of files names.
    """

    def __init__(self, parent_component, parent_frame, *args, **kwargs):
        super().__init__(parent_component, parent_frame, *args, **kwargs)

        # A better, theoretically, approach would be to abstract from the
        # specific GUI solution (ie from the tkinter library). However,
        # then the whole program becomes longer and more complicated.
        # Therefore, perhaps it is better to use objects like StringVar
        # instead of ordinary variables - the program is shorter,
        # you don't have to rewrite data from widgets to ordinary variables,
        # the number of necessary callbacks/observers is significantly
        # reduced.
        #
        self.input_csv = tk.StringVar()
        self.tests_dot = tk.StringVar()
        self.profi_htm = tk.StringVar()
        self.freqs_csv = tk.StringVar()
        self.stats_csv = tk.StringVar()
        self.tests_csv = tk.StringVar()
        self.tests_txt = tk.StringVar()

        def callback_input(*args):
            """
            Reaction to changing the name of the input file - the name of
            the main output file is automatically changed accordingly.

            Args:
                *args: needed for tkinker callback
            """
            head, tail = os.path.split(self.input_csv.get())
            name, extension = os.path.splitext(tail)
            self.tests_dot.set(os.path.join(head, name + '_links.dot'))
            self.callback(*args)

        def callback_output(*args):
            """
            Reaction to changing the name of the main output file -
            other output files are automatically changed accordingly.

            Args:
                *args: needed for tkinker callback
            """
            head, tail = os.path.split(self.tests_dot.get())
            name, extension = os.path.splitext(tail)
            name = re.sub(r'_links$', '', name)
            self.profi_htm.set(os.path.join(head, name + '_profi' + '.html'))
            self.freqs_csv.set(os.path.join(head, name + '_freqs' + '.csv'))
            self.stats_csv.set(os.path.join(head, name + '_stats' + '.csv'))
            self.tests_csv.set(os.path.join(head, name + '_tests' + '.csv'))
            self.tests_txt.set(os.path.join(head, name + '_tests' + '.txt'))
            self.callback(*args)

        def pick_open():
            """
            Reaction to pressing the input file selection button.
            """
            full_name = filedialog.askopenfilename(
                filetypes=(('CSV', '*.csv'), ("Excel", "*.xlsx")))
            if full_name:
                full_name = os.path.normpath(full_name)
                self.input_csv.set(full_name)

        def pick_save(variable, req_ext):
            """
            Reaction to pressing the output file selection button.

            Args:
                variable (tkinter.StringVar): file name as StringVar
                req_ext: an extension of the required file name.
            """
            known_types = {
                '.txt': 'text',
                '.csv': 'CSV',
                '.xlmx': 'Excel',
                '.html': 'HTML',
                '.dot': 'DOT', }
            filetypes = (known_types[req_ext], '*' + req_ext)
            name = filedialog.asksaveasfilename(filetypes=(filetypes,))
            if name:
                name = os.path.normpath(name)
                variable.set(name)

        self.input_csv.trace_add('write', callback_input)
        self.tests_dot.trace_add('write', callback_output)
        self.profi_htm.trace_add('write', self.callback)
        self.freqs_csv.trace_add('write', self.callback)
        self.stats_csv.trace_add('write', self.callback)
        self.tests_csv.trace_add('write', self.callback)
        self.tests_txt.trace_add('write', self.callback)

        label_input = ttk.Label(self._frame, text='Dane wejściowe')
        label_output = ttk.Label(self._frame, text='Wyniki obliczeń')
        label_input_csv = ttk.Label(self._frame, text='Dane (CSV lub XSLX):')
        label_tests_dot = ttk.Label(self._frame, text='Graf zależności:')
        label_profi_htm = ttk.Label(self._frame, text='Profil:')
        label_freqs_csv = ttk.Label(self._frame, text='Tablica częstości:')
        label_stats_csv = ttk.Label(self._frame, text='Statystyki:')
        label_tests_csv = ttk.Label(self._frame, text='Wyniki testów:')
        label_tests_txt = ttk.Label(self._frame, text='Opis testów:')

        entry_input_csv = ttk.Entry(self._frame, textvariable=self.input_csv)
        entry_tests_dot = ttk.Entry(self._frame, textvariable=self.tests_dot)
        entry_profi_htm = ttk.Entry(self._frame, textvariable=self.profi_htm)
        entry_freqs_csv = ttk.Entry(self._frame, textvariable=self.freqs_csv)
        entry_stats_csv = ttk.Entry(self._frame, textvariable=self.stats_csv)
        entry_tests_csv = ttk.Entry(self._frame, textvariable=self.tests_csv)
        entry_tests_txt = ttk.Entry(self._frame, textvariable=self.tests_txt)

        button_input_csv = ttk.Button(
            self._frame,
            text='zmień wszystko',
            command=lambda: pick_open())
        button_tests_dot = ttk.Button(
            self._frame,
            text='zmień pozostałe',
            command=lambda: pick_save(self.tests_dot, ".dot"))
        button_profi_htm = ttk.Button(
            self._frame,
            text='zmień',
            command=lambda: pick_save(self.profi_htm, ".csv"))
        button_freqs_csv = ttk.Button(
            self._frame,
            text='zmień',
            command=lambda: pick_save(self.freqs_csv, ".csv"))
        button_stats_csv = ttk.Button(
            self._frame,
            text='zmień',
            command=lambda: pick_save(self.stats_csv, ".csv"))
        button_tests_csv = ttk.Button(
            self._frame,
            text='zmień',
            command=lambda: pick_save(self.tests_csv, ".csv"))
        button_tests_txt = ttk.Button(
            self._frame,
            text='zmień',
            command=lambda: pick_save(self.tests_txt, ".txt"))

        label_input.grid(row=0, column=0, sticky='w')
        label_output.grid(row=2, column=0, sticky='w')
        label_input_csv.grid(row=1, column=1, sticky='e')
        label_tests_dot.grid(row=3, column=1, sticky='e')
        label_profi_htm.grid(row=4, column=1, sticky='e')
        label_freqs_csv.grid(row=5, column=1, sticky='e')
        label_stats_csv.grid(row=6, column=1, sticky='e')
        label_tests_csv.grid(row=7, column=1, sticky='e')
        label_tests_txt.grid(row=8, column=1, sticky='e')

        entry_input_csv.grid(row=1, column=2, sticky='we')
        entry_tests_dot.grid(row=3, column=2, sticky='we')
        entry_profi_htm.grid(row=4, column=2, sticky='we')
        entry_freqs_csv.grid(row=5, column=2, sticky='we')
        entry_stats_csv.grid(row=6, column=2, sticky='we')
        entry_tests_csv.grid(row=7, column=2, sticky='we')
        entry_tests_txt.grid(row=8, column=2, sticky='we')

        button_input_csv.grid(row=1, column=3, sticky='ew')
        button_tests_dot.grid(row=3, column=3, sticky='ew')
        button_profi_htm.grid(row=4, column=3, sticky='ew')
        button_freqs_csv.grid(row=5, column=3, sticky='ew')
        button_stats_csv.grid(row=6, column=3, sticky='ew')
        button_tests_csv.grid(row=7, column=3, sticky='ew')
        button_tests_txt.grid(row=8, column=3, sticky='ew')

        self._frame.columnconfigure(2, weight=1)

        for widget in self._frame.winfo_children():
            widget.grid_configure(padx=5, pady=5)
