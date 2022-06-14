#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program do analizy danych z bazy danych SQLite ProQuest.db.

Główna część programu - po uruchomieniu wykonuje wszystkie analizy.

Baza ta zawiera różne dane, w wielu tabelach, zawierające wyniki ankiet osób
chorych na nowotwory prostaty. Dane są anonimowe - nie ma nazwisk, imion itp.
danych osobowych. Baza ta powinna być w tym samym katalogu/folderze w którym
jest też program proquest.

@file: proquest.py
@version: 0.3.2.2
@date: 10.07.2018
@author: dr Sławomir Marczyński, slawek@zut.edu.pl
"""

from proquest_globals import ALPHA_LEVEL
from proquest_globals import STATS_CSV_FILE_NAME, FREQS_CSV_FILE_NAME
from proquest_globals import TESTS_TXT_FILE_NAME, TESTS_CSV_FILE_NAME, TESTS_DOT_FILE_NAME
from proquest_data import OBSERVABLES
from proquest_observable import Observable
from proquest_statistics import Test, TESTS_SUITE
from proquest_relation import Relation


def store(title, file_name, fun, iterable, **kwargs):
    print(title, 'są zapisywane do pliku:', file_name)
#    with open(file_name, 'w', encoding="utf-8") as file:
    with open(file_name, 'w') as file:
        fun(iterable, file=file, **kwargs)


if __name__ == '__main__':

    # BTW, dane zostały już wczytane przez moduł proquest_data i zaimportowane
    # przez form proquest_data import OBSERVABLES.

    store('Statystyki opisowe są zapisywane do pliku:',
          STATS_CSV_FILE_NAME, Observable.print_stat, OBSERVABLES, sep=';')

    store('Tablice częstości są zapisywane do pliku:',
          FREQS_CSV_FILE_NAME, Observable.print_freq, OBSERVABLES, sep=';')

    store('Opisy testów są zapisywane do pliku:',
          TESTS_TXT_FILE_NAME, Test.print_descriptions, TESTS_SUITE)

    # Przeprowadzanie testów statystycznych

    relations = Relation.create_relations(OBSERVABLES, TESTS_SUITE)
    relations = sorted(relations, key=lambda relation: relation.p_value)

    store('Zapis wyników testów do pliku',
          TESTS_CSV_FILE_NAME, Relation.write_csv, relations, sep=';')

    store('Zapis wyników testów jako grafu',
          TESTS_DOT_FILE_NAME, Relation.write_dot,
          [r for r in relations if r.p_value <= ALPHA_LEVEL])

    # Teraz coś ciekawszego

    ALPHA_LEVEL = 0.005

    def put(a, deep=0, symetric=True):
        group.add(a)
        graph.remove(a)
        for b in graph:
            if b in group:
                graph.remove(b)
            else:
                if deep < 3:
                    for r in relations:
                        if r(a, b, symetric=symetric) and b in graph:
                            rel.add(r)
                            put(b, deep + 1)

    i = 0
    graph = OBSERVABLES.copy()
    while len(graph) > 1:
        group = set()
        rel = set()
        put(graph[0])
        if rel:
            i += 1
#            rel = sorted(list(rel), key=lambda relation: relation.p_value)
            store('Zapis grupy jako grafu',
                  'group-' + str(i) + '.gv', Relation.write_dot, rel)
