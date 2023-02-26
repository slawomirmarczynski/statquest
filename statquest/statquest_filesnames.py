#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileNames class as a Component subclass.

File:
    project: StatQuest
    name: statquest_filenames.py
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

import os
import re
import tkinter as tk
from tkinter import filedialog, ttk

from statquest_component import Component
from statquest_locale import setup_locale_translation_gettext

_ = setup_locale_translation_gettext()


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
        self.tests_csv = tk.StringVar()

        def callback_input(*args):
            """
            Reaction to changing the name of the input file - the name of
            the main output file is automatically changed accordingly.

            Args:
                *args: needed for tkinker callback
            """
            head, tail = os.path.split(self.input_csv.get())
            name, extension = os.path.splitext(tail)
            self.tests_dot.set(os.path.join(head, name + '_links.txt'))
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
            self.profi_htm.set(os.path.join(head, name + '_profile' + '.html'))
            self.tests_csv.set(os.path.join(head, name + '_tests' + '.csv'))
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
                '.html': 'HTML', }
            filetypes = (known_types[req_ext], '*' + req_ext)
            name = filedialog.asksaveasfilename(filetypes=(filetypes,))
            if name:
                name = os.path.normpath(name)
                variable.set(name)

        # Add observers/listeners to handle changes in entry fields models.
        #
        self.input_csv.trace_add('write', callback_input)
        self.tests_dot.trace_add('write', callback_output)
        self.profi_htm.trace_add('write', self.callback)
        self.tests_csv.trace_add('write', self.callback)

        # An abbreviation of self._frame.
        #
        frame = self._frame

        # Create widgets: labels.
        #
        label_input = ttk.Label(frame, text=_('Dane wejściowe'))
        label_output = ttk.Label(frame, text=_('Wyniki obliczeń'))
        label_input_csv = ttk.Label(frame, text=_('Dane (CSV lub XSLX):'))
        label_tests_dot = ttk.Label(frame, text=_('Graf zależności:'))
        label_profi_htm = ttk.Label(frame, text=_('Profil:'))
        label_tests_csv = ttk.Label(frame, text=_('Wyniki testów:'))

        # Create widgets: entry fields with models (i.e. traced variables).
        #
        entry_input_csv = ttk.Entry(frame, textvariable=self.input_csv)
        entry_tests_dot = ttk.Entry(frame, textvariable=self.tests_dot)
        entry_profi_htm = ttk.Entry(frame, textvariable=self.profi_htm)
        entry_tests_csv = ttk.Entry(frame, textvariable=self.tests_csv)

        # Create widgets: buttons.
        #
        button_input_csv = ttk.Button(
            frame,
            text=_('zmień wszystko'),
            command=lambda: pick_open())
        button_tests_dot = ttk.Button(
            frame,
            text=_('zmień pozostałe'),
            command=lambda: pick_save(self.tests_dot, ".txt"))
        button_profi_htm = ttk.Button(
            frame,
            text=_('zmień'),
            command=lambda: pick_save(self.profi_htm, ".csv"))
        button_tests_csv = ttk.Button(
            frame,
            text=_('zmień'),
            command=lambda: pick_save(self.tests_csv, ".csv"))

        # TL;DR - all elements are placed by the grid manager
        # - entry fields are resizable - may expand horizontally.

        label_input.grid(row=0, column=0, sticky='w')
        label_output.grid(row=2, column=0, sticky='w')
        label_input_csv.grid(row=1, column=1, sticky='e')
        label_tests_dot.grid(row=3, column=1, sticky='e')
        label_profi_htm.grid(row=4, column=1, sticky='e')
        label_tests_csv.grid(row=5, column=1, sticky='e')

        entry_input_csv.grid(row=1, column=2, sticky='we')
        entry_tests_dot.grid(row=3, column=2, sticky='we')
        entry_profi_htm.grid(row=4, column=2, sticky='we')
        entry_tests_csv.grid(row=5, column=2, sticky='we')

        button_input_csv.grid(row=1, column=3, sticky='ew')
        button_tests_dot.grid(row=3, column=3, sticky='ew')
        button_profi_htm.grid(row=4, column=3, sticky='ew')
        button_tests_csv.grid(row=5, column=3, sticky='ew')

        frame.columnconfigure(2, weight=1)

        # Set uniform/standard padding for all widgets in the frame.
        #
        for widget in frame.winfo_children():
            widget.grid_configure(padx=5, pady=5)
