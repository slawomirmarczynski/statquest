#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The definition of Relation and Relations classes.

File:
    project: StatQuest
    name: statquest_relations.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""

from statquest_globals import DEFAULT_ALPHA_LEVEL
import statquest_locale
_ = statquest_locale.setup_locale()


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
        observables_relations = dict()
        known_pairs = set((a, a) for a in observables)
        for a in observables:
            for b in observables:
                if (a, b) not in known_pairs and (b, a) not in known_pairs:
                    known_pairs.add((a, b))
                    known_pairs.add((b, a))
                    observable_relations = Relations()
                    for test in tests:
                        if test.can_be_carried_out(a, b):
                            observable_relations.relations.append(test(a, b))
                    observables_relations[(a, b)] = observable_relations
        return observables_relations

    # def __len__(self):
    #     """
    #     Make relations transparent for len.
    #
    #     Returns:
    #         Number of relations stored in Relations class object.
    #     """
    #     return len(self.relations)
    #
    # def __getitem__(self, item):
    #     """
    #     Make relations transparent for __getitem__
    #     .
    #     Args:
    #         item: selector of relation.
    #
    #     Returns:
    #         Relation: relation selected by item.
    #     """
    #     return self.relations[item]

    def plausible(self, alpha=DEFAULT_ALPHA_LEVEL):
        """
        Cast to bool.

        Args:
            alpha (float): alpha probability level, from 0.0 to 1.0.

        Returns:
            bool: True if any relation is significant, False otherwise.
        """
        for relation in self.relations:
            if relation.plausible(alpha):
                return True
        return False


class Relation:
    """
    The Relation class represents the result of a statistical test,
    with given confidence, on two different observables.
    For example, we have two observables (two data sets) and Anova test.
    The Relation object will contain references to observables, the test
    and alpha level and also the computed p_value.
    """

    def __init__(self, observable1, observable2,
                 test, value, p_value, q_value):
        """
        Initialize relation.

        Args:
            observable1 (Observable): an observable.
            observable2 (Observable): an observable.
            test (Test): the statistical test which has been proceeded.
            value (float): a statistics value, for example chi-square.
            p_value (float): probability of H0 thesis.
            q_value (float): probability of the dependency; dependency
                may be defined as true H0 or true H1, thus q_value may
                be equal p_value or q_value may be equal 1.0 - p_value.

        Attributes:
            self.observable1 (Observable): an observable
            self.observable2 (Observable): an observable
            self.test (Test): an statistical test (IT IS NOT UNIT-TEST)
            self.value: the value of the test statistics.
            self.p_value: the p-value, see above.
            self.q_value: the q-value, see above.
        """
        self.observable1 = observable1
        self.observable2 = observable2
        self.test = test
        self.value = value
        self.q_value = q_value
        self.p_value = p_value

    # def is_H0_true(self, alpha=DEFAULT_ALPHA_LEVEL):
    #     return self.p_value > alpha
    #
    # def is_H1_true(self, alpha=DEFAULT_ALPHA_LEVEL):
    #     return self.p_value <= alpha

    def plausible(self, alpha=DEFAULT_ALPHA_LEVEL):
        if self.test.prove_relationship:
            return self.p_value >= alpha
        else:
            return self.p_value < alpha


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
