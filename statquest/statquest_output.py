#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Output routines.

File:
    project: StatQuest
    name: statquest_output.py
    version: 0.4.0.0
    date: 19.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl

Copyright (c) 2022 Sławomir Marczyński, slawek@zut.edu.pl.
"""

from itertools import chain

import statquest_locale

CSV_SEPARATOR = ';'


def output(file_name, writer, content, *args, **kwargs):
    """
    Use a writer to output a content to a text file.

    Args:
        file_name (str): file name.
        writer (function): a function like fun(content, file).
        content: a content to write.
        args: extra arguments to pass to writer
        kwargs: extra arguments to pass to writer
    """
    with open(file_name, "wt") as file:
        # writer(content, sys.stdout)  # uncomment to echo on sys.stdout
        writer(content, file, *args, **kwargs)


def print_csv(*args, **kwargs):
    """
    Print in CSV format.

    Generally print_cvs(...) behave like print(...), but use delimiters
    to separate fields.

    Args:
        *args: any args that con be forwarded to print
        **kwargs: any kwargs that con be forwarded to print.
    """
    print(*args, sep=CSV_SEPARATOR, **kwargs)


def write_tests_doc(tests, file):
    """
    Print the descriptions of the tests to a file/console.

    Args:
        tests (iterable): a collection of test objects.
        file (file): a text file; None redirects to a console.
    """
    if tests:
        for test in tests:
            print('=' * 80, file=file)
            print(test.__doc__, file=file)
        print('=' * 80, file=file)


def write_descriptive_statistics_csv(observables, file):
    """
    Print descriptive statistics.

    Prints descriptive statistics of given observables collection
    in CSV format.

    Args:
        observables (iterable): a collection of observables whose
            statistics should be printed/exported to file.
        file: file for exported data or None for console output.
    """

    for obs in observables:
        if obs.IS_CONTINUOUS or obs.IS_ORDINAL:
            keys = obs.descriptive_statistics().keys()
            break
    else:
        return  # there is no key, nothing to print
    print_csv(_('variable'), *keys, file=file)
    for obs in observables:
        if obs.IS_CONTINUOUS or obs.IS_ORDINAL:
            print_csv(obs, *obs.descriptive_statistics().values(), file=file)


def write_elements_freq_csv(observables, file):
    """
    Write how many times the specified values have appeared in the data.

    Args:
        observables (iterable): a collection of observables
        file (file): output file.
    """
    for obs in observables:
        if obs.IS_ORDINAL or obs.IS_NOMINAL:
            print_csv(obs, file=file)
            for key, value in obs.frequency_table().items():
                print_csv(key, value, file=file)
            print_csv(file=file)


def write_relations_csv(relations, file, alpha):
    """
    Write all given relations in CSV format.

    Note:
        We assume that relation names have no sep character inside.

    Args:
        relations (iterable): a collection of relations.
        file (file): file or null for console write.
        alpha (float): the alpha level
    """
    print_csv(
        _('data1'), _('data2'), _('test'),
        _('stat'), _('value'), _('p_value'),
        _('thesis'), _('related?'), file=file)

    relations_list = list(chain.from_iterable(relations.values()))

    for relation in relations_list:
        if relation.p_value < alpha:
            thesis = relation.test.h1_thesis
        else:
            thesis = relation.test.h0_thesis
        print_csv(
            relation.observable1, relation.observable2, relation.test.name,
            relation.test.stat_name, relation.value, relation.p_value,
            thesis, relation.plausible(alpha), file=file)


def write_relations_dot(relations, file):
    """
    Write graph of relations.

    Relations are written as graph data described in DOT language::

        graph {
                "obs1" -- "obs2"
                ...
        }

    Note:
        Function write_relations_dot writes all relations given as
        a parameter. However, it can be applied selectively to a subset
        of relations. We can segregate relationships according to
        established criteria before call write_dot and then use
        write_dot to show only specifically selected relations.

    Args:
        relations (dict(Relations)): an dictionary where keys are
            pair of relations (a, b) and values are Relations.
            Notice that Relations are containers for Relation objects.
        file (file):  output file.
    """
    if relations:
        print('graph {', file=file)
        for (a, b), rlist in relations.items():
            label = []
            for r in rlist:
                s = f'{r.test.name} (p = {r.p_value:#.4})'
                s = s.replace('Test ', '')
                label.append(s)
            label = '\\n'.join(label)
            print(f'"{a}" -- "{b}" [ label="{label}" ]', file=file)
        print('}', file=file)


_ = statquest_locale.setup_locale()
if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
