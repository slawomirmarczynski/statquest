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

from statquest_globals import ALPHA_LEVEL
from statquest_globals import STATS_CSV_FILE_NAME, FREQS_CSV_FILE_NAME
from statuest_globals import TESTS_TXT_FILE_NAME, TESTS_CSV_FILE_NAME, \
    TESTS_DOT_FILE_NAME
from statquest_data import OBSERVABLES
from statquest_observable import Observable
from statquest_statistics import Test, TESTS_SUITE
from statquest_relation import Relation
from statquest_view import *
import statquest_locale
import itertools


def print_to_file(description, file_name, writer, iterable, **kwargs):
    print(description, _('są zapisywane do pliku'), file_name)
    with open(file_name, 'wt', encoding='utf-8') as file:
        writer(iterable, file=file, **kwargs)


_ = statquest_locale.setup_locale()
if __name__ == '__main__':

    tests = create_tests_suite()
    with open(TESTS_TXT_FILE_NAME, 'wt') as file:
        write_tests_descriptions(tests, file)

    observables = import_observables()
    with open(STATS_CSV_FILE_NAME, 'wt') as file:
        write_descriptive_statistics(observables, file)
    with open(FREQS_CSV_FILE_NAME, 'wt') as file:
        write_elements_freq(observables, file)

    relations = Relation.create_relations(observables, tests)
    with open(TESTS_CSV_FILE_NAME, 'wt') as file:
        write_relations_csv(relations, file)

    significant_relations = relations.filter(alpha)
    with open(TESTS_DOT_FILE_NAME, 'wt') as file:
        write_relations_dot(significant_relations, file)
