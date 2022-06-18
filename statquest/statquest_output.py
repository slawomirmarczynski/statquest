#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Output routines.

File:
    project: StatQuest
    name: statquest_output.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""
import sys
from itertools import chain

import statquest_locale
from statquest_globals import DEFAULT_ALPHA_LEVEL

CSV_SEPARATOR = ';'


def output(file_name, writer, iterable):
    with open(file_name, "wt") as file:
        writer(iterable, sys.stdout)
        writer(iterable, file)


def write_tests_doc(tests, file):
    """
    Print the description of the test to a file/console.

    Args:
        tests (iterable): a collection of test objects.
        file (file): a text file; None redirects to a console.
    """
    if tests:
        for test in tests:
            print('=' * 80, file=file)
            print(test.__doc__, file=file)
        print('=' * 80, file=file)


def write_descriptive_statistics(observables, file=None):
    """
    Print descriptive statistics.

    Prints descriptive statistics of given observables collection
    in a human readable format.

    Args:
        observables (iterable): a collection of observables whose
            statistics should be printed/exported to file.
        sep: separator, may be set for a CSV-like format.
        file: file for exported data or None for console output.

    Examples:
        @todo - examples/unit tests.
    """

    for obs in observables:
        if obs.IS_CONTINUOUS or obs.IS_ORDINAL:
            keys = obs.descriptive_statistics().keys()
            break
    else:
        return  # there is no key, nothing to print
    print(_('variable'), *keys, sep=CSV_SEPARATOR, file=file)
    for obs in observables:
        if obs.IS_CONTINUOUS or obs.IS_ORDINAL:
            print(obs, *obs.descriptive_statistics().values(),
                  sep=CSV_SEPARATOR, file=file)


def write_elements_freq(observables, file):
    for obs in observables:
        if obs.IS_ORDINAL or obs.IS_NOMINAL:
            print(obs)
            for key, value in obs.frequency_table().items():
                print(key, value, sep=CSV_SEPARATOR, file=file)
            print(file=file)


def write_relations_csv(relations, file):
    """
    Write all given relations in CSV format.

    Note:
        We assume that relation names have no sep character inside.

    Args:
        relations (iterable): a collection of relations.
        alpha (float):
        sep (str): CSV file separator.
        file (file): file or null for console write.
    """

    fmt = '{:40}\t{:40}\t{:20}\t{:20}\t{:20}\t{:40}'
    print(fmt.format(
        _('dane1'), _('dane2'), _('test'),
        _('p_value'), _('statystyka'), _('wartość'), _('teza')),
        file=file)

    relations_list = list(chain.from_iterable(relations.values()))

        # key=lambda r:
        # r.p_value if r.test.prove_relationship else 1 - r.p_value)

    for r in relations_list:
        print(fmt.format(
            r, r.plausible()),
            file=file)


def write_relations_dot(relations, file=None):
    """
    Zapis danych w języku DOT - opisującym zależności jako graf.

        graph {
                "obs1" -- "obs2"
                ...
        }

    Dane:
        relations -- relacje do zapisania jako iterable;
        file      -- plik w którym mają być zapisane relacje.

    Uwaga: write_dot zapisuje wszystkie relacje podane jako parametr,
    nie oznacza to jednak że musi być używane do wypisywania nieselektywnie
    wszystkich relacji jakie są w programie. Logika "piętro wyżej" może
    dzielić/segregować relacje według założonych kryteriów i potem używać
    write_dot() do wypisywania tylko określonych relacji, np. takich które
    obejmują z góry wybrane obserwable.
    """
    print('graph {', file=file)
    for r in relations:
        if r.p_value <= ALPHA_LEVEL:
            print('"', r.observable1.name, '"', ' -- ',
                  '"', r.observable2.name, '"', sep='', file=file)
    print('}', file=file)


_ = statquest_locale.setup_locale()
if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
