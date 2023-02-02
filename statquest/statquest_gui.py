#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tkinter GUI for StatQuest.

File:
    project: StatQuest
    name: statquest_gui.py
    version: 0.4.1.0
    date: 01.02.2023

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
from tkinter import filedialog, ttk

from statquest import statquest_locale


class ScrollableFrame(ttk.Frame):
    """
    Umożliwia pionowe przewijanie zawartości.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        canvas = tk.Canvas(self, width=0)
        sb = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            '<Configure>',
            lambda event: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')


class BorderedFrame(ttk.Frame):
    """
    Klasa ubogacająca zwykłe ttk.Frame o widoczną ramkę.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, relief='solid', borderwidth=5, **kwargs)


class IntroFrame(ttk.Frame):
    """
    Krótki opis co program robi.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = ttk.Label(self, text=_('Program do analizy danych'))
        label.pack(fill='x', expand=True)


class ParametersFrame(BorderedFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def callback(*args):
            if columns_frame:
                columns_frame.parameters_frame_observer(self.locale_code.get())

        self.alpha = tk.DoubleVar(value=0.95)
        self.profile = tk.BooleanVar(value=False)
        self.locale_code = tk.StringVar()
        self.locale_code.trace('w', callback)

        label = ttk.Label(self, text='Parametry')
        label.grid(row=0, column=0, sticky='w')

        label_alpha = ttk.Label(
            self, text='α jako krytyczna wartość dla p-value: ')
        label_alpha.grid(row=1, column=0, sticky='e')
        entry_alpha = ttk.Entry(self, width=20, textvariable=self.alpha)
        entry_alpha.grid(row=1, column=1, sticky='w')

        checkbox_profile = ttk.Checkbutton(
            self, text='generowanie raportu Pandas Profile',
            variable=self.profile, onvalue=True, offvalue=False)
        checkbox_profile.grid(row=2, column=0, sticky='w')

        label_locale = ttk.Label(self, text='Ustawienia regionalne:')
        label_locale.grid(row=3, column=0, sticky='e')
        combobox_locale = ttk.Combobox(self, width=8,
                                       textvariable=self.locale_code)
        combobox_locale.grid(row=3, column=1, sticky='w')
        combobox_locale['values'] = ('pl_PL', 'en_US')
        combobox_locale.current(0)

        for w in self.winfo_children():
            w.grid_configure(padx=5, pady=5)

    def export_data_to_object(self, obj):
        obj.alpha = self.alpha.get()
        obj.should_compute_pandas_profile = self.profile.get()
        obj.locale_code = self.locale_code.get()


class FileFrame(BorderedFrame):
    """
    Wybór plików.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label_input = ttk.Label(self, text="Dane wejściowe")
        label_output = ttk.Label(self, text="Wyniki obliczeń")
        label_input_csv = ttk.Label(self, text="Dane (CSV lub XSLX):")
        label_profi_htm = ttk.Label(self, text="Profil (HTML):")
        label_freqs_csv = ttk.Label(self, text="Tablica częstości (CSV):")
        label_stats_csv = ttk.Label(self, text="Statystyki (CSV):")
        label_tests_csv = ttk.Label(self, text="Wyniki testów (CSV):")
        label_tests_dot = ttk.Label(self, text="Graf zależności (GV):")
        label_tests_txt = ttk.Label(self, text="Opis testów (TXT):")

        self.input_csv = tk.StringVar()
        self.profi_htm = tk.StringVar()
        self.freqs_csv = tk.StringVar()
        self.stats_csv = tk.StringVar()
        self.tests_csv = tk.StringVar()
        self.tests_dot = tk.StringVar()
        self.tests_txt = tk.StringVar()

        def callback(*args):
            head, tail = os.path.split(self.input_csv.get())
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
            if columns_frame:
                columns_frame.file_frame_observer(self.input_csv.get())

        self.input_csv.trace('w', callback)

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

        def pick_open():
            full_name = filedialog.askopenfilename(
                filetypes=(('CSV', '*.csv'), ("Excel", "*.xlsx")))
            if full_name:
                full_name = os.path.normpath(full_name)
                self.input_csv.set(full_name)

        def pick_save(variable, file_type):
            known_types = {'.txt': 'text', '.csv': 'CSV', '.xlmx': 'Excel',
                           '.html': 'HTML', '.gv': 'DOT', }
            ft = (known_types[file_type], '*' + file_type)
            name = filedialog.asksaveasfilename(filetypes=(ft,))
            if name:
                name = os.path.normpath(name)
                variable.set(name)

        button_input_csv = ttk.Button(self, text='zmień wszystko',
                                      command=lambda: pick_open())
        button_profi_htm = ttk.Button(self, text='zmień',
                                      command=lambda: pick_save(self.profi_htm,
                                                                ".html"))
        button_freqs_csv = ttk.Button(self, text='zmień',
                                      command=lambda: pick_save(self.freqs_csv,
                                                                ".csv"))
        button_stats_csv = ttk.Button(self, text='zmień',
                                      command=lambda: pick_save(self.stats_csv,
                                                                ".csv"))
        button_tests_csv = ttk.Button(self, text='zmień',
                                      command=lambda: pick_save(self.tests_csv,
                                                                ".csv"))
        button_tests_dot = ttk.Button(self, text='zmień',
                                      command=lambda: pick_save(self.tests_dot,
                                                                ".gv"))
        button_tests_txt = ttk.Button(self, text='zmień',
                                      command=lambda: pick_save(self.tests_txt,
                                                                ".txt"))
        label_input.grid(row=0, column=0, sticky='w')
        label_output.grid(row=2, column=0, sticky='w')
        label_input_csv.grid(row=1, column=1, sticky='e')
        label_profi_htm.grid(row=3, column=1, sticky='e')
        label_freqs_csv.grid(row=4, column=1, sticky='e')
        label_stats_csv.grid(row=5, column=1, sticky='e')
        label_tests_csv.grid(row=6, column=1, sticky='e')
        label_tests_dot.grid(row=7, column=1, sticky='e')
        label_tests_txt.grid(row=8, column=1, sticky='e')

        entry_input_csv.grid(row=1, column=2, sticky='w')
        entry_profi_htm.grid(row=3, column=2, sticky='w')
        entry_freqs_csv.grid(row=4, column=2, sticky='w')
        entry_stats_csv.grid(row=5, column=2, sticky='w')
        entry_tests_csv.grid(row=6, column=2, sticky='w')
        entry_tests_dot.grid(row=7, column=2, sticky='w')
        entry_tests_txt.grid(row=8, column=2, sticky='w')

        button_input_csv.grid(row=1, column=3, sticky='ew')
        button_profi_htm.grid(row=3, column=3, sticky='ew')
        button_freqs_csv.grid(row=4, column=3, sticky='ew')
        button_stats_csv.grid(row=5, column=3, sticky='ew')
        button_tests_csv.grid(row=6, column=3, sticky='ew')
        button_tests_dot.grid(row=7, column=3, sticky='ew')
        button_tests_txt.grid(row=8, column=3, sticky='ew')

        for w in self.winfo_children():
            w.grid_configure(padx=5, pady=5)

    def export_data_to_object(self, obj):
        obj.input_csv_file_name = self.input_csv.get()
        obj.profi_htm_file_name = self.profi_htm.get()
        obj.freqs_csv_file_name = self.freqs_csv.get()
        obj.stats_csv_file_name = self.stats_csv.get()
        obj.tests_csv_file_name = self.tests_csv.get()
        obj.tests_dot_file_name = self.tests_dot.get()
        obj.tests_txt_file_name = self.tests_txt.get()


class ColumnsFrame(BorderedFrame):
    """
    Wybór plików.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def select_all(*args):
            for name, variable, checkbox in self.__cbs:
                variable.set(True)

        def select_none(*args):
            for name, variable, checkbox in self.__cbs:
                variable.set(False)

        label = ttk.Label(self, text='Wybór kolumn')
        button_all = ttk.Button(self, text='wszystkie', command=select_all)
        button_none = ttk.Button(self, text='żadna', command=select_none)
        label.grid(row=0, column=0, sticky='w', pady=5)
        button_all.grid(row=0, column=2, padx=20)
        button_none.grid(row=0, column=3, padx=20)

        self.__cbs = []

    def populate(self, column_headers_list):
        for name, variable, checkbox in self.__cbs:
            checkbox.destroy()
            del variable
        i = 0
        for name in column_headers_list:
            i += 1
            variable = tk.BooleanVar()
            variable.set(True)
            print(name)
            checkbox = ttk.Checkbutton(self, text=name, variable=variable,
                                       onvalue=True, offvalue=False)
            checkbox.grid(row=i, column=1, sticky='we')
            self.__cbs.append((name, variable, checkbox))

    def parameters_frame_observer(self, locale_code):
        data_frame_provider.set_locale(locale_code)
        df = tuple(data_frame_provider.get())
        self.populate(df)

    def file_frame_observer(self, file_name):
        data_frame_provider.set_file_name(file_name)
        df = tuple(data_frame_provider.get())
        self.populate(df)

    def export_data_to_object(self, obj):
        selected = []
        for name, variable, checkbox in self.__cbs:
            if variable.get():
                print(name)
                selected.append(name)
        obj.selected_columns = selected


class LauncherFrame(ttk.Frame):
    """
    Wybór plików.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def callback(*args):
            parameters_frame.export_data_to_object(computation_engine)
            file_frame.export_data_to_object(computation_engine)
            columns_frame.export_data_to_object(computation_engine)
            computation_engine.run()

        button = ttk.Button(self, text="Uruchom obliczenia", command=callback)
        button.pack(side='left', pady=(10, 50))


data_frame_provider = None
computation_engine = None

intro = None
parameters_frame = None
file_frame = None
columns_frame = None
launcher_frame = None


def run(data_frame_provider_arg, computation_engine_arg):
    global data_frame_provider, computation_engine

    data_frame_provider = data_frame_provider_arg
    computation_engine = computation_engine_arg

    root = tk.Tk()
    root.title('StatQuest')

    global intro, parameters_frame, file_frame, columns_frame, launcher_frame

    frame = ScrollableFrame(root)
    intro = IntroFrame(frame.scrollable_frame)
    parameters_frame = ParametersFrame(frame.scrollable_frame)
    file_frame = FileFrame(frame.scrollable_frame)
    columns_frame = ColumnsFrame(frame.scrollable_frame)
    launcher_frame = LauncherFrame(frame.scrollable_frame)

    frame.pack(fill='both', expand=True)
    intro.pack(fill='x')
    parameters_frame.pack(fill='x')
    file_frame.pack(fill='x')
    columns_frame.pack(fill='x')
    launcher_frame.pack(fill='x')

    for w in frame.scrollable_frame.winfo_children():
        w.pack_configure(padx=10, pady=10)

    parameters_frame.export_data_to_object(computation_engine)
    file_frame.export_data_to_object(computation_engine)

    root.mainloop()


_ = statquest_locale.setup_locale_translation_gettext()
# directory = os.path.dirname(__file__)
# localedir = os.path.join(directory, 'locale')
# gettext.bindtextdomain('argparse', localedir)
# gettext.textdomain('argparse')
