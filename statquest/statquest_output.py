#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Output routines.

File:
    project: StatQuest
    name: statquest_output.py
    version: 0.4.0.1
    date: 19.06.2022

Authors:
    Sławomir Marczyński

Copyright (c) 2022 Sławomir Marczyński.
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

import csv
from itertools import chain

import networkx as nx
import matplotlib.pyplot as plt

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
    with open(file_name, "wt", encoding='utf-8', newline='') as file:
        # writer(content, sys.stdout)  # uncomment to echo on sys.stdout
        writer(content, file, *args, **kwargs)


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
    data_title = _('data')
    entitled_keys = [data_title] + list(keys)
    csv_writer = csv.DictWriter(file, entitled_keys, delimiter=CSV_SEPARATOR)
    csv_writer.writeheader()
    for obs in observables:
        if obs.IS_CONTINUOUS or obs.IS_ORDINAL:
            descriptive_statistics = obs.descriptive_statistics()
            descriptive_statistics[data_title] = str(obs)  # the name of obs
            csv_writer.writerow(descriptive_statistics)


def write_elements_freq_csv(observables, file):
    """
    Write how many times the specified values have appeared in the data.

    Args:
        observables (iterable): a collection of observables
        file (file): output file.
    """
    csv_writer = csv.writer(file, delimiter=CSV_SEPARATOR)
    for obs in sorted(observables, key=lambda observable: str(observable)):
        if obs.IS_ORDINAL or obs.IS_NOMINAL:
            csv_writer.writerow((obs,))
            csv_writer.writerows(obs.frequency_table().items())
            print(file=file)


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
    csv_writer = csv.writer(file, delimiter=CSV_SEPARATOR)
    csv_writer.writerow((
        _('data1'), _('data2'),
        _('related?'),
        _('test'), _('stat'),
        _('value'), _('p_value'), _('thesis')))
    relations_list = list(chain.from_iterable(relations.values()))
    for relation in relations_list:
        if relation.p_value < alpha:
            thesis = relation.test.h1_thesis
        else:
            thesis = relation.test.h0_thesis
        csv_writer.writerow((
            relation.observable1, relation.observable2,
            relation.credible(alpha),
            relation.test.name, relation.test.stat_name,
            relation.value, relation.p_value, thesis))


def write_relations_dot(relations, file):
    """
    Write graph of relations.

    Relations are written as graph data described in DOT language::

        graph {
                "obs1" -- "obs2" [ label= "Student (p = 0.0754)" ]
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
            pairs of relations (a, b) and values are Relations.
            Notice that Relations are containers for Relation objects.
        file (file):  output file.
    """
    # pylint: disable=invalid-name  # (a, b) are ok
    if relations:
        print('graph {', file=file)
        for (a, b), rlist in relations.items():
            label = []
            for r in rlist:
                if r.test.prove_relationship:
                    s = f'{r.test.name_short}  p = {r.p_value:#.4}'
                else:
                    s = f'{r.test.name_short}* p = {r.p_value:#.4}'
                label.append(s)
            label = '\\n'.join(label)
            print(f'"{a}" -- "{b}" [ label="{label}" ]', file=file)
        print('}', file=file)


def write_relations_nx(relations, file):
    """
    """
    # pylint: disable=invalid-name  # (a, b) are ok
    if relations:
        graph = nx.Graph()  # todo: DiGraph?
        for (a, b), rlist in relations.items():
            label = []
            for r in rlist:
                if r.test.prove_relationship:
                    s = f'{r.test.name_short}  p = {r.p_value:#.4}'
                else:
                    s = f'{r.test.name_short}* p = {r.p_value:#.4}'
                label.append(s)
            label = '\\n'.join(label)
            graph.add_node(a)
            graph.add_node(b)
            graph.add_edge(a, b)
    options = {
        "font_size": 8,
        "node_size": 1500,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1,
    }
    nx.draw_networkx(graph, **options)
    #nx.draw(graph)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()



_ = statquest_locale.setup_locale()
if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
