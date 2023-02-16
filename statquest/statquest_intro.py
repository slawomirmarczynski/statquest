#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tkinter GUI for StatQuest.

File:
    project: StatQuest
    name: statquest_intro.py
    version: 0.5.0.0
    date: 16.02.2023

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


import re
import textwrap
from tkinter import ttk

from statquest_component import Component


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

        text = dedentln(
            '''
            StatQuest, aplikacja metod statystycznych do analizy danych.

            Program StatQuest służy do analizy danych wskaźnikowych,
            porządkowych i kategorycznych. Nie obsługiwane są w nim dane
            przedziałowe.

            Przykładem danych wskaźnikowych może być wartości napięcia ogniw
            AAA mierzone w woltach. Będą to wartości wyrażone liczbami 
            zmiennoprzecinkowymi takimi jak 1.45, 1.39, 1.52. 
            W takim przypadku mamy wartości dla których sens ma obliczanie
            średniej arytmetycznej, odchylenia standardowego itp.

            Dane porządkowe są w programie StatQuest rozumiane jako takie które
            można opisać liczbami całkowitymi. Czy ma sens obliczanie średniej
            dla takich danych? Może mieć, może nie mieć. Przykładowo jeżeli 
            osobom wysokim przypiszemy jako kod 1, a niskim 0, to obliczona
            dla danej populacji średnia coś mówi o tym jaki procent ludzi jest
            wysokich w tej populacji. Jeżeli dodamy jeszcze kod 2 dla rudych
            oraz kod 3 dla mieszkańców małych miasteczek... to obliczona
            technikami statystycznymi średnia nie ma sensu. 
            Choć same obliczenia są/byłyby dość proste.

            Dane kategoryczne to takie dane które nie są wyrażalne liczbami.
            Dobrym przykładem może być kolor oczu: niebieskie, zielone, ...
            Każda wartość jest wyrażona nie-liczbowo, nie da się obliczyć
            średniej czy odchylenia standardowego.
            '''
        )

        label = ttk.Label(self._frame, text=text)
        label.bind('<Configure>',
                   lambda event: label.config(wraplength=label.winfo_width()))
        label.pack(fill='x', expand=True)
