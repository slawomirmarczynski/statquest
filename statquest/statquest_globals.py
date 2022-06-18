#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The global variables to hold the configuration and defaults.

File:
    project: StatQuest
    name: statquest_global.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""

# @todo: Przetłumaczyć komentarze z polskiego na angielski.

# Nazwy plików wyjściowych, program tworzyć będzie je bez ostrzeżenia,
# czyli nie będzie sprawdzał czy już istnieją czy nie. Dlatego, co oczywiste,
# program powinien być uruchamiany w wyodrębnionym katalogu roboczym.
#
# @todo Weryfikacja run-time czy nie nadpisuje się plików, wybór nazw plików,
#       wybór katalogu roboczego itp. itd. - z pewnością są do zrobienia,
#       ale jest kwestią wątpliwą czy to bardzo potrzebne (na obecnym etapie).

FREQS_CSV_FILE_NAME = 'freqs.csv'  # nazwa pliku dla statystyk częstości
TESTS_CSV_FILE_NAME = 'tests.csv'  # nazwa pliku dla wyników testów
TESTS_DOT_FILE_NAME = 'tests.gv'   # nazwa pliku dla zapisów w języku DOT
TESTS_TXT_FILE_NAME = 'tests.txt'  # nazwa pliku dla opisu testów
STATS_CSV_FILE_NAME = 'stats.csv'  # nazwa pliku dla statystyk opisowych

# Poziom istotności przyjmowany w obliczeniach.
#
# @todo Globalnie ustalony poziom istotności być może nie jest najlepszym
#        pomysłem. Być może należałoby przekazywać poziom istotności jako
#        parametr.
#
DEFAULT_ALPHA_LEVEL = 0.05  # poziom istotności alpha, musi być od 0 do 1.0

assert 0 <= DEFAULT_ALPHA_LEVEL <= 1.0
