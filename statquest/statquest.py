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

# import gettext
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog, ttk

import pandas as pd
import pandas_profiling

from statquest_gui import *
from statquest_input import input_observables
from statquest_output import *
from statquest_relations import Relations
from statquest_tests import ALL_STATISTICAL_TESTS
from statquest_gui import FileNamesFromGUI


# Default importance level alpha, it is a probability as a float number.
#
DEFAULT_ALPHA_LEVEL = 0.99
assert 0 <= DEFAULT_ALPHA_LEVEL <= 1.0




if __name__ == '__main__':

    _ = statquest_locale.setup_locale()
    directory = os.path.dirname(__file__)
    localedir = os.path.join(directory, 'locale')
    # gettext.bindtextdomain('argparse', localedir)
    # gettext.textdomain('argparse')

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

    tests = ALL_STATISTICAL_TESTS
    output(files_names.tests_txt_file_name, write_tests_doc, tests)

    if files_names.input_file_name_is_csv_file():
        data_frame = pd.read_csv(files_names.input_file_name,
                                 encoding='cp1250', sep=';', decimal=',')
    elif files_names.input_file_is_excel_file():
        raise NotImplementedError
    else:
        raise NotImplementedError

    alpha, can_profile, data_frame = SelectOptionsFromGUI()

    data_frame = data_frame.copy()  # should defrag data_frame
    # profile_report = pandas_profiling.ProfileReport(data_frame)
    # # plot={"dpi": 200, "image_format": "png"})
    # profile_report.to_file(PAPRO_HTM_FILE_NAME)

    print(data_frame)

    observables = input_observables(data_frame)
    output(STATS_CSV_FILE_NAME, write_descriptive_statistics_csv, observables)
    output(FREQS_CSV_FILE_NAME, write_elements_freq_csv, observables)

    relations = Relations.create_relations(observables, tests)
    output(TESTS_CSV_FILE_NAME, write_relations_csv, relations, alpha)

    significant_relations = Relations.credible_only(relations, alpha)
    output(TESTS_DOT_FILE_NAME, write_relations_nx, significant_relations)
    output(TESTS_DOT_FILE_NAME, write_relations_dot, significant_relations)


#    main()
