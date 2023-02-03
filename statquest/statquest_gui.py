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
import re
import textwrap
import tkinter as tk
from tkinter import filedialog, ttk

from statquest import statquest_locale


class ScrollableFrame(ttk.Frame):
    """
    Umożliwia pionowe przewijanie wstawionych do scrollable_frame widgetów.

    Attributes:
        scrollable_frame (tk.ttk.Frame): ramka będąca kontenerem na elementy;
            ta właśnie ramka jest przewijana.
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

    @property
    def scrollable_frame(self):
        """
        Okno przewijane jako read-only property.

        Returns:
            obiekt klasy tinter.ttk.Frame w którym można osadzać widgety.
        """
        return self._scrollable_frame


class BorderedFrame(ttk.Frame):
    """
    Klasa ubogacająca zwykłe ttk.Frame o widoczną ramkę.
    """

    def __init__(self, *args, **kwargs):
        """
        Tworzenie ramki tkinter.ttk.Frame mającej widoczną ramkę.

        Args:
            *args: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
            **kwargs: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
        """
        super().__init__(*args, relief='solid', borderwidth=5, **kwargs)


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


class IntroFrame(BorderedFrame):
    """
    Krótki opis co program robi.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicjalizator.

        Args:
            *args: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
            **kwargs: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
        """
        super().__init__(*args, **kwargs)
        self.pack(side='top', fill='x', expand=True)

        text = dedentln(
        '''
        StatQuest, aplikacja metod statystycznych do analizy danych.
        
        Program StatQuest służy do analizy danych wskaźnikowych, porządkowych
        i kategorycznych. Nie obsługiwane są w nim dane przedziałowe.

        Przykładem danych wskaźnikowych może być wartości napięcia ogniw AAA 
        mierzone w woltach. Będą to wartości wyrażone liczbami 
        zmiennoprzecinkowymi takimi jak 1.45, 1.39, 1.52. W takim przypadku
        mamy wartości dla których sens ma obliczanie średniej arytmetycznej,
        odchylenia standardowego itp.
        
        Dane porządkowe są w programie StatQuest rozumiane jako takie które
        można opisać liczbami całkowitymi. Czy ma sens obliczanie średniej
        dla takich danych? Może mieć, może nie mieć. Przykładowo jeżeli 
        osobom wysokim przypiszemy jako kod 1, a niskim 0, to obliczona
        dla danej populacji średnia coś mówi o tym jaki procent ludzi jest
        wysokich w tej populacji. Jeżeli dodamy jeszcze kod 2 dla rudych
        oraz kod 3 dla mieszkańców małych miasteczek... to obliczona technikami
        statystycznymi średnia nie ma sensu. Choć same obliczenia są/byłyby
        dość proste.
        
        Dane kategoryczne to takie dane które nie są wyrażalne liczbami.
        Dobrym przykładem może być kolor oczu: niebieskie, brązowe, zielone...
        Każda wartość jest wyrażona nie-liczbowo, nie da się obliczyć
        średniej czy odchylenia standardowego.
        '''
        )

        label = ttk.Label(self, text=text)
        label.bind('<Configure>',
                   lambda event: label.config(wraplength=label.winfo_width()))
        label.pack(fill='x', expand=True)


class ParametersFrame(BorderedFrame):
    """
    Konfigurowanie parametrów pracy programu.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicjalizator.

        Args:
            *args: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
            **kwargs: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
        """
        super().__init__(*args, **kwargs)

        def validator(string):
            """
            Sprawdza czy wartość wpisana w kontrolkę jest liczbą z przedziału
            od 0 do 1, czyli mogącą określać prawdopodobieństwo.

            Args:
                string (str): wpisana liczba jako napis.

            Returns:
                True jeżeli walidacja zakończyła się pomyślnie, False jeżeli
                nie powiodła się.
            """

            try:
                value = float(string)
                return 0 <= value <= 1
            except:
                return False

        # Rejestracja, dla potrzeb tkinker, funkcji walidującej.
        #
        registred_validator = self.register(validator)

        def callback(*args):
            """
            Informowanie computation_engine o aktualnych wartościach
            parametrów jakie mają być użyte w obliczeniach.

            Args:
                *args: argumenty są określane przez tkinker.tk.StrValue.
            """

            # Nawet jeżeli zmienia się tylko jeden parametr, to nie zaszkodzi
            # aktualizacja wszystkich innych. Owszem, nie jest to potrzebne,
            # jednak zyskujemy na prostocie. Obiekt computation_engine używa
            # zwykłych zmiennych do przechowywania wartości parametrów.
            #
            computation_engine.alpha = self.alpha.get()
            computation_engine.should_compute_pandas_profile = self.profile.get()
            computation_engine.locale_code = self.locale_code.get()
            data_frame_provider.set_locale(self.locale_code.get())
            columns_frame.update()


        # tkinker wymaga aby wartości początkowe dla obiektów takich jak
        # tk.StringVar itp. były jawnie określane. Sam z siebie nie gwarantuje
        # że początkowa zawartość pól Entry będzie skopiowana do takich
        # zmiennych.
        #
        self.alpha = tk.DoubleVar(value=0.95)
        self.profile = tk.BooleanVar(value=False)
        self.locale_code = tk.StringVar(value='pl_PL')
        self.locale_code.trace_add('write', callback)

        # Ogólny opis dla tej sekcji.
        #
        label = ttk.Label(self, text=_('Parametry'))
        label.grid(row=0, column=0, columnspan=4, sticky='w')

        # Parametr alpha
        #
        label_alpha = ttk.Label(
            self, text=_('α jako krytyczna wartość dla p-value:'))
        label_alpha.grid(row=1, column=0, sticky='e')
        entry_alpha = ttk.Entry(self, width=20, textvariable=self.alpha,
                                validate='all',
                                validatecommand=(registred_validator, '%P'))
        entry_alpha.grid(row=1, column=1, sticky='w')
        label_alpha_comment = ttk.Label(
            self,
            text=_('Wartość parametru α musi spełniać warunek 0 ⩽ α ⩽ 1.'))
        label_alpha_comment.grid(row=1, column=2, sticky='w')

        # Czy ma być użyte pandas_profiling (tj. ydata_profiling)?
        #
        checkbox_profile = ttk.Checkbutton(
            self, text=_('generowanie raportu Ydata Profile'),
            variable=self.profile, onvalue=True, offvalue=False)
        checkbox_profile.grid(row=2, column=0, sticky='w')
        label_profile_comment = ttk.Label(self, text=_(
            'Oblicza podstawowe statystyki i korelacje. Nie wpływa na testy.'))
        label_profile_comment.grid(row=2, column=2, sticky='w')

        label_locale = ttk.Label(self, text=_('ustawienia regionalne:'))
        label_locale.grid(row=3, column=0, sticky='e')
        combobox_locale = ttk.Combobox(self, width=8,
                                       textvariable=self.locale_code)
        combobox_locale.grid(row=3, column=1, sticky='w')
        combobox_locale['values'] = ('pl_PL', 'en_US')
        combobox_locale.current(0)
        label_locale_comment = ttk.Label(
            self,
            text='Ustala szczegóły takie jak znak przecinka dziesiętnego.')
        label_locale_comment.grid(row=3, column=2, sticky='w')

        for widget in self.winfo_children():
            widget.grid_configure(padx=5, pady=5)  # todo: piksele -> punkty



class FileFrame(BorderedFrame):
    """
    Wybór plików.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicjalizator.

        Args:
            *args: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
            **kwargs: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
        """

        super().__init__(*args, **kwargs)

        label_input = ttk.Label(self, text="Dane wejściowe")
        label_output = ttk.Label(self, text="Wyniki obliczeń")
        label_input_csv = ttk.Label(self, text="Dane (CSV lub XSLX):")
        label_tests_dot = ttk.Label(self, text="Graf zależności (DOT):")
        label_profi_htm = ttk.Label(self, text="Profil (HTML):")
        label_freqs_csv = ttk.Label(self, text="Tablica częstości (CSV):")
        label_stats_csv = ttk.Label(self, text="Statystyki (CSV):")
        label_tests_csv = ttk.Label(self, text="Wyniki testów (CSV):")
        label_tests_txt = ttk.Label(self, text="Opis testów (TXT):")

        self.input_csv = tk.StringVar()
        self.tests_dot = tk.StringVar()
        self.profi_htm = tk.StringVar()
        self.freqs_csv = tk.StringVar()
        self.stats_csv = tk.StringVar()
        self.tests_csv = tk.StringVar()
        self.tests_txt = tk.StringVar()

        def callback(*args):
            computation_engine.input_csv_file_name = self.input_csv.get()
            computation_engine.tests_dot_file_name = self.tests_dot.get()
            computation_engine.profi_htm_file_name = self.profi_htm.get()
            computation_engine.freqs_csv_file_name = self.freqs_csv.get()
            computation_engine.stats_csv_file_name = self.stats_csv.get()
            computation_engine.tests_csv_file_name = self.tests_csv.get()
            computation_engine.tests_txt_file_name = self.tests_txt.get()
            columns_frame.update()

        def callback_input(*args):
            head, tail = os.path.split(self.input_csv.get())
            name, extension = os.path.splitext(tail)
            self.tests_dot.set(os.path.join(head, name + '_links' + '.dot'))
            # self.profi_htm.set(os.path.join(head, name + '_profi' + '.html'))
            # self.freqs_csv.set(os.path.join(head, name + '_freqs' + '.csv'))
            # self.stats_csv.set(os.path.join(head, name + '_stats' + '.csv'))
            # self.tests_csv.set(os.path.join(head, name + '_tests' + '.csv'))
            # self.tests_txt.set(os.path.join(head, name + '_tests' + '.txt'))
            callback(*args)
            data_frame_provider.set_file_name(self.input_csv.get())
            columns_frame.update()


        def callback_output(*args):
            head, tail = os.path.split(self.tests_dot.get())
            name, extension = os.path.splitext(tail)
            self.profi_htm.set(os.path.join(head, name + '_profi' + '.html'))
            self.freqs_csv.set(os.path.join(head, name + '_freqs' + '.csv'))
            self.stats_csv.set(os.path.join(head, name + '_stats' + '.csv'))
            self.tests_csv.set(os.path.join(head, name + '_tests' + '.csv'))
            self.tests_txt.set(os.path.join(head, name + '_tests' + '.txt'))
            callback(*args)

        # Ponieważ śledzenie (trace) jest dodawane do wielu kontrolek, których
        # zawartość jest generowane także przez kontrolki, to call-back'i
        # niepotrzebnie będą się wywoływać nadmierną liczbę razy. Nie jest to
        # jednak istotnym problemem - nawet kilkanaście wywołań nie będzie
        # zauważalne.
        #
        self.input_csv.trace_add('write', callback_input)
        self.tests_dot.trace_add('write', callback_output)
        self.profi_htm.trace_add('write', callback)
        self.freqs_csv.trace_add('write', callback)
        self.stats_csv.trace_add('write', callback)
        self.tests_csv.trace_add('write', callback)
        self.tests_txt.trace_add('write', callback)

        entry_input_csv = ttk.Entry(self, width=80, textvariable=self.input_csv)
        entry_profi_htm = ttk.Entry(self, width=80, textvariable=self.profi_htm)
        entry_freqs_csv = ttk.Entry(self, width=80, textvariable=self.freqs_csv)
        entry_stats_csv = ttk.Entry(self, width=80, textvariable=self.stats_csv)
        entry_tests_csv = ttk.Entry(self, width=80, textvariable=self.tests_csv)
        entry_tests_dot = ttk.Entry(self, width=80, textvariable=self.tests_dot)
        entry_tests_txt = ttk.Entry(self, width=80, textvariable=self.tests_txt)

        def pick_open():
            full_name = filedialog.askopenfilename(
                filetypes=(('CSV', '*.csv'), ("Excel", "*.xlsx")))
            if full_name:
                full_name = os.path.normpath(full_name)
                self.input_csv.set(full_name)

        def pick_save(variable, file_type):
            known_types = {'.txt': 'text', '.csv': 'CSV', '.xlmx': 'Excel',
                           '.html': 'HTML', '.dot': 'DOT', }
            ft = (known_types[file_type], '*' + file_type)
            name = filedialog.asksaveasfilename(filetypes=(ft,))
            if name:
                name = os.path.normpath(name)
                variable.set(name)

        button_input_csv = ttk.Button(
            self, text='zmień wszystko',
            command=lambda: pick_open())
        button_tests_dot = ttk.Button(
            self, text='zmień pozostałe',
            command=lambda: pick_save(self.tests_dot, ".gv"))
        button_profi_htm = ttk.Button(
            self, text='zmień',
            command=lambda: pick_save(self.profi_htm, ".csv"))
        button_freqs_csv = ttk.Button(
            self, text='zmień',
            command=lambda: pick_save(self.freqs_csv, ".csv"))
        button_stats_csv = ttk.Button(
            self, text='zmień',
            command=lambda: pick_save(self.stats_csv, ".csv"))
        button_tests_csv = ttk.Button(
            self, text='zmień',
            command=lambda: pick_save(self.tests_csv, ".csv"))
        button_tests_txt = ttk.Button(
            self, text='zmień',
            command=lambda: pick_save(self.tests_txt, ".txt"))

        label_input.grid(row=0, column=0, sticky='w')
        label_output.grid(row=2, column=0, sticky='w')

        label_input_csv.grid(row=1, column=1, sticky='e')
        label_tests_dot.grid(row=2, column=1, sticky='e')
        label_profi_htm.grid(row=3, column=1, sticky='e')
        label_freqs_csv.grid(row=4, column=1, sticky='e')
        label_stats_csv.grid(row=5, column=1, sticky='e')
        label_tests_csv.grid(row=6, column=1, sticky='e')
        label_tests_txt.grid(row=7, column=1, sticky='e')

        entry_input_csv.grid(row=1, column=2, sticky='we')
        entry_tests_dot.grid(row=2, column=2, sticky='we')
        entry_profi_htm.grid(row=3, column=2, sticky='we')
        entry_freqs_csv.grid(row=4, column=2, sticky='we')
        entry_stats_csv.grid(row=5, column=2, sticky='we')
        entry_tests_csv.grid(row=6, column=2, sticky='we')
        entry_tests_txt.grid(row=7, column=2, sticky='we')

        button_input_csv.grid(row=1, column=3, sticky='ew')
        button_tests_dot.grid(row=2, column=3, sticky='ew')
        button_profi_htm.grid(row=3, column=3, sticky='ew')
        button_freqs_csv.grid(row=4, column=3, sticky='ew')
        button_stats_csv.grid(row=5, column=3, sticky='ew')
        button_tests_csv.grid(row=6, column=3, sticky='ew')
        button_tests_txt.grid(row=7, column=3, sticky='ew')

        self.columnconfigure(2, weight=1)

        for widget in self.winfo_children():
            widget.grid_configure(padx=5, pady=5)


class ColumnsFrame(BorderedFrame):
    """
    Wybór plików.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicjalizator.

        Args:
            *args: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
            **kwargs: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
        """

        super().__init__(*args, **kwargs)

        def select_all(*args):
            for name, variable, checkbox in self.__cbs:
                variable.set(True)

        def select_none(*args):
            for name, variable, checkbox in self.__cbs:
                variable.set(False)

        label = ttk.Label(self, text=_('Wybór kolumn'))
        button_all = ttk.Button(self, text=_('wszystkie'), command=select_all)
        button_none = ttk.Button(self, text=_('żadna'), command=select_none)
        label.grid(row=0, column=0, sticky='w', pady=5)
        button_all.grid(row=0, column=2, padx=20)
        button_none.grid(row=0, column=3, padx=20)

        self.__cbs = []

    def populate(self, column_headers_list):

        def callback():
            selected = []
            for name, variable, checkbox in self.__cbs:
                if variable.get():
                    print(name)
                    selected.append(name)
            computation_engine.selected_columns = selected

        for name, variable, checkbox in self.__cbs:
            checkbox.destroy()
            del variable
        self.__cbs.clear()
        i = 0
        for name in column_headers_list:
            i += 1
            variable = tk.BooleanVar()
            variable.set(True)
            checkbox = ttk.Checkbutton(self, text=name, variable=variable,
                                       onvalue=True, offvalue=False,
                                       command=callback)
            checkbox.grid(row=i, column=1, sticky='we')
            self.__cbs.append((name, variable, checkbox))
        callback()

    def update(self):
        pandas_data_frame = tuple(data_frame_provider.get())
        self.populate(pandas_data_frame)


class LauncherFrame(ttk.Frame):
    """
    Wybór plików.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicjalizator.

        Args:
            *args: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
            **kwargs: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
        """

        super().__init__(*args, **kwargs)

        def callback(*args):
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
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root_width = int(screen_width * 0.75)
    root_height = int(screen_height * 0.75)
    root.geometry(f'{root_width}x{root_height}')

    global intro, parameters_frame, file_frame, columns_frame, launcher_frame

    frame = ScrollableFrame(root)
    frame.pack(fill='both', expand=True)
    intro = IntroFrame(frame.scrollable_frame)
    parameters_frame = ParametersFrame(frame.scrollable_frame)
    file_frame = FileFrame(frame.scrollable_frame)
    columns_frame = ColumnsFrame(frame.scrollable_frame)
    launcher_frame = LauncherFrame(frame.scrollable_frame)

    parameters_frame.pack(fill='x')
    file_frame.pack(fill='x')
    columns_frame.pack(fill='x')
    launcher_frame.pack(fill='x')

    for w in frame.scrollable_frame.winfo_children():
        w.pack_configure(padx=10, pady=10)

    root.mainloop()


_ = statquest_locale.setup_locale_translation_gettext()
# directory = os.path.dirname(__file__)
# localedir = os.path.join(directory, 'locale')
# gettext.bindtextdomain('argparse', localedir)
# gettext.textdomain('argparse')
