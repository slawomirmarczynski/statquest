#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example/template for statquest_input() function.

File:
    project: StatQuest
    name: statquest_input.py
    version: 0.4.0.2
    date: 19.10.2022

Authors:
    Sławomir Marczyński

Copyright (c) 2022 Sławomir Marczyński.
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

from statquest_observable import Observable


def input_observables(data_frame):
    """

    Args:
        data_frame (pandas.DataFrame): input data as a Pandas Dataframe.

    Returns:
        observables (list): the list of observables.
    """
    # Observables can be created with calls Observable initializer with
    # name and dictionary, see example below:
    #
    #   obs1 = Observable('Observable1', {1: 1, 2: 3, 3: 1, 4: 2, 5: 6})
    #   obs2 = Observable('Observable2', {1: 1.0, 2: 3.2, 4: 2.1, 5: 6.1})
    #   obs3 = Observable('Observable3', {1: 'red', 2: 'blue', 3: 'pink'})
    #   return obs1, obs2, obs3
    #
    # but the implementation below construct them from pandas dataframe.

    observables = []
    for index in data_frame:
        name = str(index)
        series = data_frame[index]
        series = series.dropna()
        try:
            obs = Observable(name, dict(series));
            if len(obs) > 2:
                observables.append(obs)
                print(f"{name} ok")
            else:
                print(f"{name} too short")
        except:
            print(f"{name} fail")
    return observables
