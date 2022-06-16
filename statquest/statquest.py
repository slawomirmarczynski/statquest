#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
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

def print_to_file(description, file_name, writer, iterable, **kwargs):
    print(description, _('są zapisywane do pliku'), file_name)
    with open(file_name, 'wt', encoding='utf-8') as file:
        writer(iterable, file=file, **kwargs)

import statquest_locale
_ = statquest_locale.setup_locale()
if __name__ == '__main__':

    observables = import_observables()
    observables = [Observable()]
    # tests = create_tests_suite()
    tests = TESTS_SUITE

    CSV_SEPARATOR = ';'

    print_to_file(
        _('statystyki opisowe'), STATS_CSV_FILE_NAME,
        Observable.print_stat, observables, sep=CSV_SEPARATOR)
    print_to_file(
        _('tablice częstości'), FREQS_CSV_FILE_NAME,
        Observable.print_freq, observables, sep=CSV_SEPARATOR)
    print_to_file(
        _('opisy testów'), TESTS_TXT_FILE_NAME,
        Test.print_descriptions, tests)

    relations = Relation.create_relations(observables, tests)

# problem - relacje zebrane jak lecą były sortowane po p-value

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