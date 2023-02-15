#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: scrollableframe.py
    version: 0.4.2.1
    date: 07.02.2023

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


import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """
    Umożliwia pionowe przewijanie wstawionych do scrollable_frame widgetów.
    """

    def __init__(self, *args, **kwargs):
        """
        Tworzenie subklasy tkinter.ttk.Frame umożliwiającej przewijanie
        pionowe.

        Args:
            *args: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
            **kwargs: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
        """
        super().__init__(*args, **kwargs)

        # Obiekt klasy Canvas, w odróżnieniu od obiektu Frame, może być
        # przewijany. Jednak wygodniej jest zagnieżdżać obiekty wewnątrz
        # Frame niż wewnątrz Canvas. Dlatego tworzone są (obiekty) Frame
        # wewnątrz Canvas wewnątrz Frame. W ten sposób z zewnątrz widać
        # obiekty Frame, a obiekty Canvas (i ScrollBar) są ukryte w obiekcie
        # ScrollableFrame.

        # Tworzenie pustego canvas, czyli czegoś co można przewijać.
        # Na razie canvas jest puste, bez żadnej zawartości.
        #
        # bd=0 oznacza że nie chcemy marginesu wokół kanwy
        # highlightthickness=0 oznacza że nie chcemy pokazywać fokusu
        #
        canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        canvas.pack(side='left', fill='both', expand=True)

        # Tworzenie obiektu ScrollBar, czyli kontrolera przewijania.
        sb = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        sb.pack(side='right', fill='y')

        # Tworzenie kontenera (obiektu klasy ttk.Frame), który użytkownik
        # będzie mógł przewijać.
        #
        # Obserwator zdarzenia <Configure> jest potrzebny na wypadek gdyby
        # trzeba było na nowo określić zakres przewijania. Ten bowiem jest
        # ustalany na poziomie canvas i wymaga w takiej sytuacji odświeżenia.
        #
        self._scrollable_frame = ttk.Frame(canvas)
        self._scrollable_frame.bind(
            '<Configure>',
            lambda event: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        # Dodawanie do canvas zawartości - innego widgetu - wykonywane jest
        # metodą create_window. Nazwa może kojarzyć się z jakąś fabryką lub
        # funkcjami/metodami tworzącymi okna (CreateWindow jest np. Windows
        # API Microsoftu), ale w tkinter ma trochę inny sens.
        #
        # Po wstawieniu zyskujemy identyfikator wstawionego elementu, który
        # wkrótce nam się bardzo przyda.
        #
        scrollable_frame_canvas_id = canvas.create_window(
            (0, 0), window=self._scrollable_frame, anchor='nw')

        # Teraz trudniejsza część - dodajemy obserwatora pilnującego aby
        # szerokość obiektu canvas dopasowywała się do szerokości obszaru
        # jaki jest dostępny. Jeżeli tego nie zrobimy, to canvas będą (zwykle)
        # miały zły rozmiar. I choć nadal elementy doń wstawione mogłyby być
        # widoczne, to menadżer geometrii nie potrafiłby działać zgodnie
        # z naszymi oczekiwaniami.
        #
        # noinspection PyUnusedLocal
        def update_scrollable_frame_width(event):
            if self._scrollable_frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(
                    scrollable_frame_canvas_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', update_scrollable_frame_width)

        # Moglibyśmy to zrobić nieco wcześniej, ale robimy to na koniec:
        # podpinamy przewijanie kanwy z tym co ustawine jest przez belkę
        # przewijania (czyli przez scroll bar).
        #
        canvas.configure(yscrollcommand=sb.set)

        # Jeszcze dodajemy przewijanie kółkiem myszy.
        #
        canvas.bind_all(
            "<MouseWheel>",
            lambda event:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        )

    @property
    def scrollable_frame(self):
        """
        Okno przewijane jako read-only property.

        Returns:
            obiekt klasy tinter.ttk.Frame w którym można osadzać widgety.
        """
        return self._scrollable_frame

