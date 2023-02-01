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
import gettext
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



import pandas as pd
import pandas_profiling

import statquest_dataframe
from statquest_gui import *
from statquest_input import input_observables
from statquest_output import *
from statquest_relations import Relations
from statquest_tests import ALL_STATISTICAL_TESTS
import statquest_gui


# Default importance level alpha, it is a probability as a float number.
#
DEFAULT_ALPHA_LEVEL = 0.99
assert 0 <= DEFAULT_ALPHA_LEVEL <= 1.0


class ComputationEngine:
    def run(self):
        tests = ALL_STATISTICAL_TESTS
        output(self.tests_txt_file_name,
               write_tests_doc,
               tests)

        data_frame = data_frame_provider.get_selected(self.selected_columns)
        if not data_frame.empty:
            data_frame = data_frame.copy()  # should defrag data_frame

        if self.should_compute_pandas_profile:
            profile_report = pandas_profiling.ProfileReport(data_frame)
            profile_report.to_file(self.profi_htm_file_name)

        # plot={"dpi": 200, "image_format": "png"} ???

        print(data_frame)

        observables = input_observables(data_frame)
        output(self.stats_csv_file_name,
               write_descriptive_statistics_csv,
               observables)
        output(self.freqs_csv_file_name,
               write_elements_freq_csv,
               observables)

        relations = Relations.create_relations(observables, tests)
        output(self.tests_csv_file_name,
               write_relations_csv,
               relations,
               self.alpha)

        significant_relations = Relations.credible_only(relations, self.alpha)
        output(self.tests_dot_file_name,
               write_relations_nx,
               significant_relations)
        output(self.tests_dot_file_name,
               write_relations_dot,
               significant_relations)


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('TkAgg')
    data_frame_provider = statquest_dataframe.DataFrameProvider()
    computation_engine = ComputationEngine()
    statquest_gui.run(data_frame_provider, computation_engine)
