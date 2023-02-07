#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The definition of Relation and Relations classes.

File:
    project: StatQuest
    name: statquest_relations.py
    version: 4.2.0.1
    date: 07.02.2022

Authors:
    Sławomir Marczyński
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
            bool: True if H0 is true and H0 states that the relation is
                credible; True if H0 is false and H0 states that the relation
                is not credible; False if H0 is False and H0 states that the
                relation is credible; False if H0 is True and H0 states that
                the relation is not credible;
        """
        if self.test.prove_relationship:
            return self.p_value >= alpha
        return self.p_value < alpha


class Relations:
    """
    Relations is a collection contain relations.
    """

    def __init__(self):
        """
        Create an empty object of class Relation.
        """
        self.relations = []

    @staticmethod
    def create_relations(observables, tests):
        """
        Relationship factory. All possible relationships are created.

        Args:
            observables (iterable): a collection of Observables
            tests (iterable): a collection of Tests

        Returns:
            dict: the mapping of tuples (a, b) to relations.
        """
        # pylint: disable=invalid-name  # short names a, b are ok
        observables_relations = {}
        known_pairs = set((a, a) for a in observables)
        for a in observables:
            for b in observables:
                if (a, b) not in known_pairs and (b, a) not in known_pairs:
                    known_pairs.add((a, b))
                    known_pairs.add((b, a))
                    observable_relations = Relations()
                    for test in tests:
                        if test.can_be_carried_out(a, b):
                            try:
                                observable_relations.relations.append(test(a, b))
                            except:
                                print('ups... something goes wrong')
                    observables_relations[(a, b)] = observable_relations
        return observables_relations

    def __len__(self):
        """
        Make relations transparent for len.

        Returns:
            Number of relations stored in Relations class object.
        """
        return len(self.relations)

    def __getitem__(self, item):
        """
        Make relations transparent for __getitem__
        .
        Args:
            item: selector of relation.

        Returns:
            Relation: relation selected by item.
        """
        return self.relations[item]

    def credible(self, alpha):
        """
        Cast to bool.

        Args:
            alpha (float): alpha probability level, from 0.0 to 1.0.

        Returns:
            bool: True if any relation is significant, False otherwise.
        """
        for relation in self.relations:
            if relation.credible(alpha):
                return True
        return False

    @staticmethod
    def credible_only(indexed_relations, alpha):
        """
        Filter relation by significance

        Args:
            indexed_relations (dict[Relations]): an dictionary with Relations
            alpha (float): significance level.

        Returns:
            dict[Relations]: the filtered dictionary of Relations
        """
        result = {}
        for key, relations in indexed_relations.items():
            if relations.credible(alpha):
                result[key] = [r for r in relations if r.credible(alpha)]
        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
