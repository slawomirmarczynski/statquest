#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
StatQuest - the automatic detection statistically significant relations.

The Observable class and the factory of Observable objects.

File:
    name: statquest_observable.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""

from collections import defaultdict

import numpy as np
from scipy import stats


class Observable:
    """
    Observable is the class whose objects hold data.

    Observable types can be nominal, ordinal, or continuous.
    An observable is continuous type if its values are float point numbers.
    An observable is ordinal type if its values are int numbers.
    An observable is nominal type if its values are strings of characters.

    Future versions of the program may also introduce the interval type.
    The interval observables will be pairs of floating point numbers.

    Attributes:
        name (str): the observable name.
        data (dict): the observable data.
        dependencies (set): known trivial dependencies.
        IS_CONTINUOUS (bool): read-only, True for a continous scale
        IS_NOMINAL (bool): read-only, True for a nominal scale
        IS_ORDINAL (bool): read-only, True for an ordinal scale
    """

    def __init__(self, name, data, dependencies=None):
        """
        Observable initializer.

        The observable initializer link a name with given data.
        Optionaly is possible to describe "trival dependences",
        i.e. a collection of observables that should not be tested
        against this one.

        Args:
            name (str): the observable name as a string of characters, should
                be unique, should not be None.
            data (dict): an dictionary or something that may be casted to dict.
            dependencies (iterable): a set of observables (or something that
                may be cast to set) which should be excluded from tests with
                this observable. For example: weights in pounds should not be
                tested against the same weights expressed in kg; these data
                are obviously linear depended and there is no need to employ
                statistical tests for prove that are correlated.
        """
        assert name is not None
        self.name = name
        self.data = dict(data)
        self.dependencies = set(dependencies) if dependencies else set()
        self.dependencies.add(self)
        self._propagate_dependencies(self.dependencies)
        self.IS_CONTINUOUS = self._is_continuous()
        self.IS_NOMINAL = self._is_nominal()
        self.IS_ORDINAL = self._is_ordinal()

    def __getitem__(self, key):
        """
        Return a value for the given key.

        Returns a value for the given key, thus an object of the class
        Observable will behave in a "transparent" way.

        Args:
            key: a key to obtain requested value from self.data dict.

        Return:
            requested value from self.data dict.

        Example::

            >>> obs = Observable('example', {1: 'A', 2: 'B', 3: 'AB'})
            >>> obs[2]
            'B'
        """
        return self.data[key]

    def __len__(self):
        """
        Observable size.

        Return:
            number of elements stored inside the observable.

        Example::

            >>> obs = Observable('example', {1: 'A', 2: 'B', 3: 'AB'})
            >>> len(obs)
            3
            >>> empty = Observable('empty observable', {})
            >>> len(empty)
            0
        """
        return len(self.data)

    def __str__(self):
        """
        Get the name of the observable for printing, labelling etc.

        Return:
            the name given to observable.

        Example::

            >>> obs = Observable('example', {1: 'A', 2: 'B', 3: 'AB'})
            >>> print(obs)
            example
        """
        return self.name

    def is_dependent_by_assumption(self, observable):
        """
        Check for trivial dependencies.

        Some relation are trivial/obvious. They should not be checked because
        we already have known the direct dependency. For example the observable is
        always corelated to self (i.e. A is corelated with A).

        Args:
            observable (Observable): the observable to check with self.

        Return:
            True if an trivial dependency was found in in self.dependencies.

        Example::

            >>> obs1 = Observable('X', {1: 1, 2: 2, 3: 3})
            >>> obs2 = Observable('Y', {1: 1, 2: 4, 3: 9}, dependencies={obs1})
            >>> obs3 = Observable('Z', {1: 1, 2: 8, 3: 27}, dependencies={obs2})
            >>> obs4 = Observable('T', {1: 'A', 2: 'B', 3: 'C'})
            >>> Observable._propagate_dependencies((obs1, obs2, obs3, obs4))
            >>> obs1.is_dependent_by_assumption(obs1)
            True
            >>> obs1.is_dependent_by_assumption(obs2)
            True
            >>> obs1.is_dependent_by_assumption(obs3)
            True
            >>> obs1.is_dependent_by_assumption(obs4)
            False
        """
        return observable in self.dependencies

    def nominals(self):
        """
        Zwraca skalę nominalną jako listę, tj. listę łancuchów znaków.
        Skala ta jest zbudowana na wartościach (nie kluczach) z self.data.

        Uwaga: wszystkie wartości powinny być jednego typu, w przeciwnym razie
               nie będzie możliwe sortowanie, co skończy się wyjątkiem.

        Przykłady:

            >>> x = Observable('X', {'C': 'Celina', 'B': 'Basia', 'A': 'Ala'})
            >>> x.nominals()
            ['Ala', 'Basia', 'Celina']

            >>> y = Observable('Y', {'C': 1, 'B': 31, 'A': 2})
            >>> y.nominals()
            ['1', '2', '31']
        """
        return list(map(str, self.values_as_sorted_list()))

    def ordinals(self):
        """
        Zwraca skalę porządkową jako listę, tj. listę liczb całkowitych.
        Skala ta jest zbudowana na wartościach (nie kluczach) z self.data.

        Uwaga: wszystkie wartości powinny być jednego typu, w przeciwnym razie
               nie będzie możliwe sortowanie, co skończy się wyjątkiem.

        Przykłady:

            >>> x = Observable('X', {'C': 111, 'B': 777, 'A': -5})
            >>> x.ordinals()
            [-5, 111, 777]

            >>> y = Observable('Y', {'C': '1', 'B': '5', 'A': '2'})
            >>> y.ordinals()
            [1, 2, 5]
        """
        return list(map(int, self.values_as_sorted_list()))

    def values_as_sorted_list(self):
        """
        Return the sorted list of values from self.data dictionary.

        Return:
            sorted list of values.

        Example::

            >>> x = Observable('X', {'C': 'Celina', 'B': 'Basia', 'A': 'Ala'})
            >>> x.values_as_sorted_list()
            ['Ala', 'Basia', 'Celina']
        """
        return sorted(list(self.frequency_table().keys()))

    def values_to_indices_dict(self):
        """
        Return values-to-indices mapping, where indices are indices of values
        on list returned by values_as_sorted_list().

        Return:
            dictionary

        Example::

            >>> x = Observable('X', {'C': 'Celina', 'B': 'Basia', 'A': 'Ala'})
            >>> x.values_to_indices_dict()
            {'Ala': 0, 'Basia': 1, 'Celina': 2}
        """
        values_as_keys = self.values_as_sorted_list()
        return {values_as_keys[i]: i for i in range(len(values_as_keys))}

    def frequency_table(self):
        """
        Compute frequency table for the observable.

        Compute numbers of individual values occurrences for non-continuous
        variables. This way converts from the nominal scale to ordinal
        or continuous scale.

        Return:
            frequency table as a dictionary.

        Note:
            works best with nominal or ordinal data.

        Example::

            >>> obs = Observable('example', {1: 'A', 2: 'B', 3: 'A'})
            >>> print(obs.frequency_table())
            {'A': 2, 'B': 1}
        """
        # @todo: check if removing this assertion make no problems
        # assert self.is_ordinal() or self.is_nominal()
        freq = defaultdict(int)
        for item in self.data.values():
            freq[item] += 1
        freq = dict(sorted(tuple(freq.items())))
        return freq

    def descriptive_statistics(self):
        """
        Obliczanie statystyk opisowych.

        Zwraca:
            słownik, kluczami są nazwy statystyk, wartościami sa wartości
            statystyk.

            if observable.is_ordinal() or observable.is_continuous():
        data = list(data.values())

        Przykład:
            >>> obs = Observable('example', {1: 10.5, 2: 10.2, 3: 10.9})
            >>> obs.descriptive_statistics()
            {'średnia': 10.533333333333333, 'mediana': 10.5, ...
        """
        if self.IS_CONTINUOUS or self.IS_ORDINAL:
            data = tuple(self.data.values())
            return {'średnia': np.mean(data),
                    'mediana': np.median(data),
                    'dolny kwartyl': np.percentile(data, 25),
                    'górny kwartyl': np.percentile(data, 75),
                    'wartość najmniejsza': np.min(data),
                    'wartość największa': np.max(data),
                    'odchylenie standardowe': np.std(data),
                    'wariancja': np.var(data),
                    'asymetria': stats.skew(data),
                    'kurtoza': stats.kurtosis(data)}
        return None  # @todo - może lepiej raise TypeError lub coś takiego?!

    @staticmethod
    def print_descriptive_statistics(observables, sep='\t', file=None):
        """
        Print descriptive statistics.

        Print descriptive statistics of given observables in a human readable
        format.

        Args:
            observables (iterable): a collection of observables whose
                statistics should be printed/exported to file.
            sep: separator, may be set for a CSV-like format.
            file: file for exported data or None for console output.

        Examples::
            @todo - examples/unit tests.
        """
        for obs in observables:
            if obs.is_continuous() or obs.is_ordinal():
                keys = obs.stat().keys()
                break

        print('dane', *keys, sep=sep, file=file)
        for obs in observables:
            if obs.is_continuous() or obs.is_ordinal():
                print(obs, *obs.stat().values(), sep=sep, file=file)

    def _is_continuous(self):
        """
        Check self if it is a countinuous variable.

        It is assumed that an observable is countinuous if and only if values
        stored in self.data are float numbers.

        Args:
            verify: if it is True then all data is checked, whereas if
                it is False then only the very first item is investigated.

        Returns:
            True remarks that the observable represent a continuous variable.

        Examples::

            >>> obs1 = Observable('example', {1: 10.5, 2: 10.2, 3: 11.5})
            >>> obs1.IS_CONTINUOUS
            True
            >>> obs2 = Observable('example', {1: 10.5, 2: 10.2, 3: '11.5'})
            >>> obs2.IS_CONTINUOUS
            False
            >>> obs3 = Observable('example', {1: 'nie', 2: 'tak'})
            >>> obs3.IS_CONTINUOUS
            False
            >>> obs4 = Observable('example', {1: 3.1, 2: 'not float'})
            >>> obs4.IS_CONTINUOUS
            False
        """
        return self._check_data_kind(float)

    def _is_nominal(self):
        """
        Check self if it is a nominal variable.

        It is assumed that an observable is nominal if and only if values
        stored in self.data are strings.

        Args:
            verify: if it is True then all data is checked, whereas if
                it is False then only the very first item is investigated.

        Returns:
            True remarks that the observable represent a nominal variable.

        Examples::

            >>> obs1 = Observable('example', {1: 'A', 2: 'B', 3: 'ABC'})
            >>> obs1.IS_NOMINAL
            True
            >>> obs2 = Observable('example', {1: 3.1, 2: 3.2})
            >>> obs2.IS_NOMINAL
            False
            >>> obs3 = Observable('example', {1: 31, 2: 32})
            >>> obs3.IS_NOMINAL
            False
            >>> obs4 = Observable('example', {1: 'A', 2: 'B', 3: 3.142})
            >>> obs4.IS_NOMINAL
            False
        """
        return self._check_data_kind(str)

    def _is_ordinal(self):
        """
        Sprawdza, czy obserwabla jest ordinal, czyli czy przedstawia zmienną
        porządkową. Zakłada się, że obserwabla jest porządkową jeżeli jej
        wartości są zapisane jako liczby całkowite.

        Dane:
            verify -- jeżeli jest True, to sprawdzane są wszystkie dane
                      zapisane w obserwabli; jeżeli False to sprawdzany
                      jest tylko pierwsza pozycja w słowniku self.data.

        Zwraca:
            True jeżeli obserwabla jest typu ordinal, False jeżeli nie.

        Przykłady:

            >>> obs1 = Observable('example', {1: 100, 2: 105, 3: 200})
            >>> obs1.IS_ORDINAL
            True
            >>> obs2 = Observable('example', {1: 3.1, 2: 3.2})
            >>> obs2.IS_ORDINAL
            False
            >>> obs3 = Observable('example', {1: '1', 2: '2'})
            >>> obs3.IS_ORDINAL
            False
            >>> obs4 = Observable('example', {1: 1, 2: 2, 3: 'ABC'})
            >>> obs4.IS_ORDINAL
            False
        """
        return self._check_data_kind(int)

    def _check_data_kind(self, T):
        """
        Metoda chroniona klasy Observable: implementacja sprawdzania typu
        zmiennych jakie mają wartości ze słownika self.data.

        Dane:
            T      -- typ, np. int, float, str
            verify -- jeżeli jest True, to szczegółowo sprawdzane są wszystkie
                      elementy słownika self.data, jeżeli False to sprawdzany
                      jest tylko jeden element (jako reprezentatywny dla całego
                      słownika).

        Zwraca:
            True lub False, zależnie od tego czy słownik zawiera zmienne tego
            typu jaki został podany jako parametr T.

        Przykłady:

            >>> obs1 = Observable('example', {1: 10.5, 2: 10.2, 3: -5.0})
            >>> obs1._check_data_kind(float)
            True
            >>> obs2 = Observable('example', {1: 10, 2: 11, 3: 12})
            >>> obs2._check_data_kind(float)
            False
            >>> obs3 = Observable('example', {1: 'A', 2: 'AB', 3: 'ABC'})
            >>> obs3._check_data_kind(float)
            False
        """
        assert isinstance(self.data, dict)

        if not self.data:
            return False

        # @todo: filter/map coś w stylu any/each

        for v in self.data.values():
            if not isinstance(v, T):
                return False
        return True

    @staticmethod
    def _propagate_dependencies(observables):
        """
        Propagate trivial dependencies between observables.

        Some relations between observables are trivial and should not
        be tested because there is no sense to test H0/H1 hypothesis
        already knowing that probability of H0 is 100%. This kind of
        relationship can be described by dependencies parameter during
        initialization of an observable (an instance of Observable).

        Having observables a, b, c may happen that a is depended on b,
        b is depended on c, but neither b nor c is not depended on a.
        Simply speaking, there is no guarantee that "dependency" will
        be a symmetric relation as should be.

        This method, propagate_dependencies, enforce symmetry of these
        relations.

        Args:
            observables (iterable): an collection of observables,
                they would be modified/updated (if necessary) by the
                call of propagate_dependencies.
        """
        # The algorithm below is rather simple and perhaps doesn't have
        # the best performance. We just iterate over the observables
        # pool. For each observable, it is checked whether other
        # observables that are described as dependent on observable a
        # (and due to the transitivity of these relations also on other
        # observables described inside a as dependent) know themselves
        # that they depend on observable a.
        # This is updated in subsequent cycles until the cycle that
        # changes nothing , i.e. all relations are already symmetric.
        #
        need_update = True
        while need_update:
            need_update = False
            for a in observables:
                for b in a.dependencies:
                    if b is not a:
                        d = b.dependencies | a.dependencies
                        if d != b.dependencies:
                            need_update = True
                            b.dependencies = d


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
