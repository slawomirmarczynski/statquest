#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The definition of Relation and Relations classes.

File:
    project: StatQuest
    name: statquest_relations.py
    version: 0.5.1.1
    date: 25.02.2023

Authors:
    Sławomir Marczyński
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

import sys

import statquest_locale

_ = statquest_locale.setup_locale_translation_gettext()


class Relation:
    """
    The Relation class represents the result of a statistical test,
    with given confidence, on two different observables.
    For example, we have two observables (two data sets) and Anova test.
    The Relation object will contain references to observables, the test
    and alpha level and also the computed p_value.

    Attributes:
        observable1 (Observable): an observable
        observable2 (Observable): an observable
        test (Test): an statistical test (IT IS NOT UNIT-TEST)
        value: the value of the test statistics.
        p_value: the p-value, see above.
    """

    def __init__(self, observable1, observable2, test, value, p_value):
        """
        Initialize relation.

        Args:
            observable1 (Observable): an observable.
            observable2 (Observable): an observable.
            test (Test): the statistical test which has been proceeded.
            value (float): a statistics value, for example chi-square.
            p_value (float): probability of H0 thesis.
        """
        self.observable1 = observable1
        self.observable2 = observable2
        self.test = test
        self.value = value
        self.p_value = p_value

    def credible(self, alpha):
        """
        Check if relation is credible.

        Args:
            alpha (float) : significance level.

        Returns:
            bool: True if H0 is rejected and H0 states that the relation is
                not credible; False if H0 is rejected and H0 states that the
                relation is not credible; True if H0 is accepted and H0 states
                that the relation is credible; False if H0 is accepted and H0
                states that the relation is not credible.
        """
        if self.test.prove_relationship:
            return self.p_value < alpha
        return self.p_value > 1.0 - alpha

    @staticmethod
    def create_relations(observables, tests, progress=None):
        """
        Relationship factory. All possible relationships are created.

        Args:
            observables (iterable): a collection of Observables.
            tests (iterable): a collection of Tests.
            progress (progress.Progress): an optional Progress object.

        Returns:
            dict: the mapping of tuples (a, b) to relations.
        """
        # pylint: disable=invalid-name  # short names a, b are ok
        relations = {}
        if not observables or not tests:
            return relations
        known_pairs = set((a, a) for a in observables)
        known_triplets = set()
        if progress:
            progress.range(len(observables))
        for a in observables:
            if progress:
                progress.step()
            for b in observables:
                if (a, b) in known_pairs:
                    continue
                known_pairs.add((a, b))
                # known_pairs.add((b, a))
                rel = []
                for test in tests:
                    if test in known_triplets:
                        print('$', end='')
                        continue
                    known_triplets.add((a, b, test))
                    if test.is_symetric:
                        known_triplets.add((b, a, test))
                    if len(set(a.data.keys()) & set(b.data.keys())) < 2:
                        print(f'{a} nietestowalne z {b}.', file=sys.stderr)
                        continue
                    if test.can_be_carried_out(a, b):
                        # @todo: remove can_be_... - use exceptions
                        #        instead
                        try:
                            rel.append(test(a, b))
                        except:
                            print(f'Nieudany {test} dla {a} vs. {b}',
                                  file=sys.stderr)
                relations[(a, b)] = rel

        # For symmetric relations remove (b, a) relation
        # when is known (a, b) relation.
        #
        if progress:
            progress.range(len(observables))
        for a in observables:
            if progress:
                progress.step()
            for b in observables:
                try:
                    relations_a_b = relations[(a, b)]
                    relations_b_a = relations[(b, a)]
                except KeyError:
                    continue
                for ab in relations_a_b:
                    to_remove = []
                    for ba in relations_b_a:
                        if ab.test == ba.test and ab.test.is_symetric:
                            to_remove.append(ba)
                    for r in to_remove:
                        relations_b_a.remove(r)

        # Remove empty entries in relations.
        #
        if progress:
            progress.range(len(observables))
        for a in observables:
            if progress:
                progress.step()
            for b in observables:
                if (a, b) in relations and not relations[(a, b)]:
                    del relations[(a, b)]
        return relations

    @staticmethod
    def credible_only(relations, alpha):
        """
        Filter relations by significance.

        Args:
            relations (dict[Relations]): an dictionary with Relations
            alpha (float): significance level.

        Returns:
            dict[Relations]: the filtered dictionary of Relations
        """
        result = {}
        for key, rel in relations.items():
            list_ = [r for r in rel if r.credible(alpha)]
            if list_:
                result[key] = list_
        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
