#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest.py
    version: 4.2.0.1
    date: 07.02.2022

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

import ydata_profiling as pandas_profiling

from statquest_gui import *
from statquest_input import input_observables
from statquest_output import *
from statquest_relations import Relations
from statquest_tests import ALL_STATISTICAL_TESTS


class ComputationEngine:
    def run(self, data_frame_provider, computation_engine):
        tests = ALL_STATISTICAL_TESTS
        output(self.tests_txt_file_name, write_tests_doc, tests)

        data_frame = data_frame_provider.get_selected(self.selected_columns)
        if not data_frame.empty:
            data_frame = data_frame.copy()  # should defrag data_frame

        if self.need_pandas_profile:
            progress_bar = False
            plot_parameters = {"dpi": 300, "image_format": "png"}
            if self.need_pandas_profile_correlations:
                profile_report = pandas_profiling.ProfileReport(
                    data_frame,
                    plot=plot_parameters,
                    progress_bar=progress_bar)
                profile_report.to_file(self.profi_htm_file_name)
            else:
                profile_report = pandas_profiling.ProfileReport(
                    data_frame,
                    correlations=None,
                    plot=plot_parameters,
                    progress_bar=progress_bar)
                profile_report.to_file(self.profi_htm_file_name)

        # print(data_frame)

        observables = input_observables(data_frame)
        output(self.stats_csv_file_name, write_descriptive_statistics_csv,
               observables)
        output(self.freqs_csv_file_name, write_elements_freq_csv,
               observables)

        relations = Relations.create_relations(observables, tests)
        output(self.tests_csv_file_name, write_relations_csv,
               relations, self.alpha)

        significant_relations = Relations.credible_only(relations, self.alpha)
        output(self.tests_dot_file_name, write_relations_nx,
               significant_relations)
        output(self.tests_dot_file_name, write_relations_dot,
               significant_relations)


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
