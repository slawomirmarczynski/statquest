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


import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog

import os


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

            self.__files_collection= set()
            self.profi_htm_file_name = self.__make_name('_profi', '.html')
            self.freqs_csv_file_name = self.__make_name('_freqs', '.csv')
            self.stats_csv_file_name = self.__make_name('_stats', '.csv')
            self.tests_csv_file_name = self.__make_name('_tests', '.csv')
            self.tests_dot_file_name = self.__make_name('_links', '.gv')
            self.tests_txt_file_name = self.__make_name('_tests', '.txt')
            if any(map(os.path.exists, self.__files_collection)):
                overwrite = tkinter.messagebox.askokcancel(
                    parent=root,
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
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

if __name__ == '__main__':

    # files = FileNamesFromGUI()

    root = tk.Tk()
    frame = ScrollableFrame(root)
    frame.grid()
    inter = tk.Frame(frame.scrollable_frame)
    inter.grid()
    for i in range(30):
        b = ttk.Button(inter, text='button ' + str(i))
        b.grid(row=i, column=0)

    root.mainloop()
