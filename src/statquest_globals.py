# -*- coding: utf-8 -*-
"""
Program do analizy danych z bazy danych SQLite ProQuest.db.

Stałe globalne, używane w różnych miejscach programu.

Z założenia żaden moduł nie importuje głównego modułu proquest. Przeniesienie
stałych z proquest_globals do proquest spowodowałoby konieczność importowania
jakiego nie chcemy. Dlatego istnieje proquest_globals - tu wrzucane są te dane
które mają być dostępne "wszędzie" (tj. tam gdzie zostaną zaimportowane).

@file: proquest_globals.py
@version: 0.3.2.2
@date: 10.07.2018
@author: dr Sławomir Marczyński, slawek@zut.edu.pl
"""


# Uwaga: baza danych (w obecnej wersji programu) jest w tym samym katalogu
# w ktorym jest program. Podobnie inne pliki i zasoby. Nazwy plików są więc
# względne - odnoszą się do katalogu roboczego.
#
DATA_BASE_NAME = 'proquest.db'  # nazwa bazy danych SQLite3

# Nazwy plików wyjściowych, program tworzyć będzie je bez ostrzeżenia,
# czyli nie będzie sprawdzał czy już istnieją czy nie. Dlatego, co oczywiste,
# program powinien być uruchamiany w wyodrębnionym katalogu roboczym.
#
# @todo Weryfikacja run-time czy nie nadpisuje się plików, wybór nazw plików,
# wybór katalogu roboczego itp. itd. - z pewnością są do zrobienia, ale jest
# kwestią wątpliwą czy to bardzo potrzebne (na obecnym etapie).

FREQS_CSV_FILE_NAME = 'freqs.csv'  # nazwa pliku dla statystyk częstości
TESTS_CSV_FILE_NAME = 'tests.csv'  # nazwa pliku dla wyników testów
TESTS_DOT_FILE_NAME = 'tests.gv'   # nazwa pliku dla zapisów w języku DOT
TESTS_TXT_FILE_NAME = 'tests.txt'  # nazwa pliku dla opisu testów
STATS_CSV_FILE_NAME = 'stats.csv'  # nazwa pliku dla statystyk opisowych

# Poziom istotności przyjmowany w obliczeniach.
#
# @todo Globalnie ustalony poziom istotności być może nie jest najlepszym
# pomysłem. Być może należałoby przekazywać poziom istotności jako parametr.
#
ALPHA_LEVEL = 0.05             # poziom istotności alpha, musi być od 0 do 1.0

# Stałe: średnia ilość tygodni na miesiąc, liczba tygodni rocznie.
#
WEEKS_PER_MONTH = 4.33
WEEKS_PER_YEAR = 52
