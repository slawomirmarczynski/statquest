#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest.py
    version: 0.4.0.2
    date: 19.10.2022

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
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog, ttk
import pandas as pd


class FileNamesFromGUI:
    def __init__(self):
        print("Swimming")
        root = tk.Tk()
        root.withdraw()
        self.input_file_name = filedialog.askopenfilename(
            filetypes=(('CSV', '*.csv'), ("Excel", "*.xlsx")))
        if self.input_file_name:
            self.input_file_name = os.path.normpath(self.input_file_name)
            self.__head, self.__tail = os.path.split(self.input_file_name)
            self.__name, self.__extension = os.path.splitext(self.__tail)
            if self.__extension not in ('.csv', '.xlsx'):
                raise ValueError

            # File names for the input file, panda profiles, the frequency
            # statistics, means-variances-medians-etc., the detailed output of
            # test results, the graph in DOT language (GraphViz) and write-ups
            # of tests docs.

            self.__files_collection = set()
            self.profi_htm_file_name = self.__make_name('_profi', '.html')
            self.freqs_csv_file_name = self.__make_name('_freqs', '.csv')
            self.stats_csv_file_name = self.__make_name('_stats', '.csv')
            self.tests_csv_file_name = self.__make_name('_tests', '.csv')
            self.tests_dot_file_name = self.__make_name('_links', '.gv')
            self.tests_txt_file_name = self.__make_name('_tests', '.txt')
            if any(map(os.path.exists, self.__files_collection)):
                overwrite = tkinter.messagebox.askokcancel(parent=root,
                                                           title='StatQuest',
                                                           message='Czy można nadpisać istniejące wyniki?')
                if not overwrite:
                    raise FileExistsError

            print(self.__files_collection)
        else:
            raise FileNotFoundError

    def input_file_is_csv_file(self):
        return self.__extension == '.csv'

    def input_file_is_excel_file(self):
        return self.__extension == '.xlsx'

    def __make_name(self, postfix, extension):
        name = os.path.join(self.__head, self.__name + postfix + extension)
        if name in self.__files_collection:
            raise RuntimeError
        self.__files_collection.add(name)
        return name


class ScrollableFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        canvas = tk.Canvas(self, width=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical',
                                  command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind('<Configure>',
                                   lambda event: canvas.configure(
                                       scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')


class BorderedFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, relief='solid', borderwidth=5, **kwargs)


class IntroFrame(BorderedFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = ttk.Label(self, text='Program do analizy danych')
        label.pack(fill='x', expand=True)


class FileFrame(BorderedFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label_input_csv = ttk.Label(self, text="Input file name:")
        label_profi_htm = ttk.Label(self, text="Output profile:")
        label_freqs_csv = ttk.Label(self, text="Output frequency table:")
        label_stats_csv = ttk.Label(self, text="Output statistics:")
        label_tests_csv = ttk.Label(self, text="Output test results:")
        label_tests_dot = ttk.Label(self, text="Output graph:")
        label_tests_txt = ttk.Label(self, text="Output documentation:")

        self.input_csv = tk.StringVar()
        self.profi_htm = tk.StringVar()
        self.freqs_csv = tk.StringVar()
        self.stats_csv = tk.StringVar()
        self.tests_csv = tk.StringVar()
        self.tests_dot = tk.StringVar()
        self.tests_txt = tk.StringVar()

        entry_input_csv = ttk.Entry(self, width=80,
                                    textvariable=self.input_csv)
        entry_profi_htm = ttk.Entry(self, width=80,
                                    textvariable=self.profi_htm)
        entry_freqs_csv = ttk.Entry(self, width=80,
                                    textvariable=self.freqs_csv)
        entry_stats_csv = ttk.Entry(self, width=80,
                                    textvariable=self.stats_csv)
        entry_tests_csv = ttk.Entry(self, width=80,
                                    textvariable=self.tests_csv)
        entry_tests_dot = ttk.Entry(self, width=80,
                                    textvariable=self.tests_dot)
        entry_tests_txt = ttk.Entry(self, width=80,
                                    textvariable=self.tests_txt)

        def setup_all():
            full_name = filedialog.askopenfilename(
                filetypes=(('CSV', '*.csv'), ("Excel", "*.xlsx")))
            if full_name:
                full_name = os.path.normpath(full_name)
                self.input_csv.set(full_name)
                head, tail = os.path.split(full_name)
                name, extension = os.path.splitext(tail)
                self.profi_htm.set(
                    os.path.join(head, name + '_profi' + '.html'))
                self.freqs_csv.set(
                    os.path.join(head, name + '_freqs' + '.csv'))
                self.stats_csv.set(
                    os.path.join(head, name + '_stats' + '.csv'))
                self.tests_csv.set(
                    os.path.join(head, name + '_tests' + '.csv'))
                self.tests_dot.set(os.path.join(head, name + '_links' + '.gv'))
                self.tests_txt.set(
                    os.path.join(head, name + '_tests' + '.txt'))

                data_frame = pd.read_csv(files_names.input_file_name,
                                         encoding='cp1250', sep=';',
                                         decimal=',')

        def pick_save(variable, file_type):
            known_types = {'.txt': 'text', '.csv': 'CSV', '.xlmx': 'Excel',
                           '.html': 'HTML', '.gv': 'DOT', }
            ft = (known_types[file_type], '*' + file_type)
            name = filedialog.asksaveasfilename(filetypes=(ft,))
            if name:
                name = os.path.normpath(name)
                variable.set(name)

        button_input_csv = ttk.Button(self, text='change all',
                                      command=lambda: setup_all())
        button_profi_htm = ttk.Button(self, text='change',
                                      command=lambda: pick_save(self.profi_htm,
                                                                ".html"))
        button_freqs_csv = ttk.Button(self, text='change',
                                      command=lambda: pick_save(self.freqs_csv,
                                                                ".csv"))
        button_stats_csv = ttk.Button(self, text='change',
                                      command=lambda: pick_save(self.stats_csv,
                                                                ".csv"))
        button_tests_csv = ttk.Button(self, text='change',
                                      command=lambda: pick_save(self.tests_csv,
                                                                ".csv"))
        button_tests_dot = ttk.Button(self, text='change',
                                      command=lambda: pick_save(self.tests_dot,
                                                                ".gv"))
        button_tests_txt = ttk.Button(self, text='change',
                                      command=lambda: pick_save(self.tests_txt,
                                                                ".txt"))

        label_input_csv.grid(row=0, column=0, sticky='e')
        label_profi_htm.grid(row=1, column=0, sticky='e')
        label_freqs_csv.grid(row=2, column=0, sticky='e')
        label_stats_csv.grid(row=3, column=0, sticky='e')
        label_tests_csv.grid(row=4, column=0, sticky='e')
        label_tests_dot.grid(row=5, column=0, sticky='e')
        label_tests_txt.grid(row=6, column=0, sticky='e')

        entry_input_csv.grid(row=0, column=1, sticky='w')
        entry_profi_htm.grid(row=1, column=1, sticky='w')
        entry_freqs_csv.grid(row=2, column=1, sticky='w')
        entry_stats_csv.grid(row=3, column=1, sticky='w')
        entry_tests_csv.grid(row=4, column=1, sticky='w')
        entry_tests_dot.grid(row=5, column=1, sticky='w')
        entry_tests_txt.grid(row=6, column=1, sticky='w')

        button_input_csv.grid(row=0, column=2, sticky='ew')
        button_profi_htm.grid(row=1, column=2, sticky='ew')
        button_freqs_csv.grid(row=2, column=2, sticky='ew')
        button_stats_csv.grid(row=3, column=2, sticky='ew')
        button_tests_csv.grid(row=4, column=2, sticky='ew')
        button_tests_dot.grid(row=5, column=2, sticky='ew')
        button_tests_txt.grid(row=6, column=2, sticky='ew')

        for w in self.winfo_children():
            w.grid_configure(padx=2, pady=2)


class ParametersFrame(BorderedFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.alpha = tk.DoubleVar(value=0.95)
        self.profile = tk.BooleanVar(value=False)

        label_alpha = ttk.Label(self, text='alpha:')
        label_alpha.grid(row=0, column=0, sticky="e")
        entry_alpha = ttk.Entry(self, width=20, textvariable=self.alpha)
        entry_alpha.grid(row=0, column=1, sticky='w')

        spacer = ttk.Label(self, width=20)
        spacer.grid(row=0, column=2)

        checkbox_profile = ttk.Checkbutton(
            self, text='profile',
            variable=self.profile, onvalue=True, offvalue=False)
        checkbox_profile.grid(row=0, column=3)


if __name__ == '__main__':

    root = tk.Tk()
    root.title('StatQuest')
    frame = ScrollableFrame(root)
    frame.pack(fill='both', expand=True)
    intro = IntroFrame(frame.scrollable_frame)
    intro.pack(fill='both', expand=True)
    file_frame = FileFrame(frame.scrollable_frame)
    file_frame.pack(fill='x', expand=True)
    parameters_frame = ParametersFrame(frame.scrollable_frame)
    parameters_frame.pack(fill='x', expand=True)

    for w in frame.scrollable_frame.winfo_children():
        w.pack_configure(padx=5, pady=5)

    root.mainloop()
