#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tkinter GUI for StatQuest.

File:
    project: StatQuest
    name: statquest_intro.py
    version: 0.5.1.2
    date: 21.03.2024

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński
"""
import os
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


import re
import sys
import textwrap
from tkinter import ttk

from statquest_component import Component
from statquest_locale import get_default_locale_code


def dedentln(string):
    """
    Funkcja pomocna do przygotowywania do wstawiania do kontrolek
    tkinter tekstu zapisanego jako literał w wielu liniach.

    Args:
        string (str): łańcuch znaków z niepotrzebnymi wcięciami i nadmiarem
            znaków nowej linii.

    Returns:
        łańcuch znaków lepiej sformatowany, znaki nowej linii są usunięte
        jeżeli występowały pojedynczo.
    """
    pattern = '(?<!\n)\n(?!\n)'
    return re.sub(pattern, ' ', textwrap.dedent(string)).strip()


class Intro(Component):
    def __init__(self, parent_component, parent_frame, *args, **kwargs):
        super().__init__(parent_component, parent_frame, *args, **kwargs)

        text = (
            '''
            StatQuest - statistical methods for data analysis.
    
            The StatQuest program is intended for to statistical analysis
            of nominal, ordinal and continuous data. 
    
            An example of continuous data can be AAA cell voltage values 
            measured in volts. These will be values expressed in floating 
            point numbers like 1.45, 1.39, 1.52. In this case, we have
            values for which the calculation makes sense arithmetic mean,
            standard deviation, etc.
    
            Ordinal data is understood in StatQuest as data that can be
            described with integers. Does it make sense to calculate the 
            average for such data? Might have, might not have. For example if
            we will assign 1 as code to tall people and 0 to short people,
            then it is calculated for a given population, the mean says
            something about what percentage of people there are high in this
            population. If we add code 2 for big city and code 3 for small
            town... then the average makes no sense.
            
            Categorical data is data that cannot be expressed in numbers.
            A good example would be the color of the eyes: blue, green, ...
            Each value is expressed non-numerically, cannot be calculated
            mean or standard deviation.
            '''
        )

        try:
            code = get_default_locale_code()
            file_name = os.path.join('locale', code, 'intro.txt')
            with open(file_name, encoding='utf-8') as file:
                text = file.read()
        except:
            pass

        text = dedentln(text)
        label = ttk.Label(self._frame, text=text)
        label.bind('<Configure>',
                   lambda event: label.config(wraplength=label.winfo_width()))
        label.pack(fill='x', expand=True)
