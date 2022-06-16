#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The definition of Observable class.

File:
    project: StatQuest
    name: statquest_observable.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""

from collections import defaultdict

import numpy as np
from scipy import stats

import statquest_locale


class Observable:
    """
    Observable is the class whose objects hold labelled data.

    Lets a database contain some values indexed by a primary key.
    The Observable object encapsulate mapping (in fact a dict object)
    between keys (some id) and values (for example height or most
    favourite colour or number of children). Additionally, Observable
    provide means to distinguish (and convert) nominal, ordinal and
    continuous data, to compute frequency tables, means, variations etc.
    And last but not least: observables are labelled objects, i.e. each
    observable has got a name.

    Observable types can be nominal, ordinal, or continuous.
    An observable is continuous if its values are float point numbers.
    An observable is ordinal if its values are int numbers.
    An observable is nominal if its values are strings of characters.

    Attributes:
        name (str): the observable name.
        data (dict): the observable data.
        IS_CONTINUOUS (bool): read-only, True for a continuous scale
        IS_NOMINAL (bool): read-only, True for a nominal scale
        IS_ORDINAL (bool): read-only, True for an ordinal scale
    """

    def __init__(self, name, data):
        """
        Initialize observable.

        The observable initializer link a name with given data
        and initalize attributes.

        Args:
            name (str): the observable name as a string of characters.
            data (dict): an dictionary or something that may be cast to dict.

        Examples:
            Create observables and check their names and types.

            >>> o1 = Observable('example1', {1: 10, 2: 20, 3: 30})
            >>> print(o1, o1.IS_ORDINAL, o1.IS_CONTINUOUS, o1.IS_NOMINAL)
            example1 True False False

            >>> o2 = Observable('example2', {1: 10.5, 2: 10.2, 3: 11.5})
            >>> print(o2, o2.IS_ORDINAL, o2.IS_CONTINUOUS, o2.IS_NOMINAL)
            example2 False True False

            >>> o3 = Observable('example3', {1: 'yes', 2: 'maybe', 3: 'no'})
            >>> print(o3, o3.IS_ORDINAL, o3.IS_CONTINUOUS, o3.IS_NOMINAL)
            example3 False False True
        """
        self.name = name
        self.data = dict(data)
        self.IS_CONTINUOUS = self._check_data_kind(float)
        self.IS_NOMINAL = self._check_data_kind(str)
        self.IS_ORDINAL = self._check_data_kind(int)

    def __getitem__(self, key):
        """
        Return a value for the given key.

        Returns a value for the given key, thus an object of the class
        Observable will behave in a "transparent" way.

        Args:
            key: a key to obtain requested value from self.data dict.

        Returns:
            requested value from self.data dict.

        Examples:
            >>> obs = Observable('example', {1: 'A', 2: 'B', 3: 'AB'})
            >>> obs[2]
            'B'
        """
        return self.data[key]

    def __len__(self):
        """
        Get observable size.

        Returns:
            int: number of elements stored inside the observable.

        Examples:
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
        Get the name (label) of the observable.

        Returns:
            str: the name given to observable.

        Examples:
            >>> obs = Observable('example name', {1: 'A', 2: 'B', 3: 'AB'})
            >>> print(obs)
            example name
        """
        return self.name

    def nominals(self):
        """
        Construct a nominal scale.

        Constructs a nominal scale from the values stored in observable.

        Returns:
             list: the nominal scale as a list of strings.

        Note:
            All values should be of one type.

        Examples:
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
        Construct an ordinal scale.

        Constructs an ordinal scale from the values stored in observable.

        Returns:
            list: an ordinal scale as a list of integers.

        Note:
            All values should be of one type.

        Examples:
            >>> x = Observable('X', {'C': 111, 'B': 777, 'A': -5})
            >>> x.ordinals()
            [-5, 111, 777]

            >>> y = Observable('Y', {'C': '1', 'B': '5', 'A': '2'})
            >>> y.ordinals()
            [1, 2, 5]
        """
        return sorted(list(map(int, self.values_as_sorted_list())))

    def values_as_sorted_list(self):
        """
        Return the sorted list of unique values from self.data dictionary.

        Returns:
            list: sorted list of values.

        Example:
            >>> x = Observable('X', {'C': 'Celina', 'B': 'Basia', 'A': 'Ala'})
            >>> x.values_as_sorted_list()
            ['Ala', 'Basia', 'Celina']
        """
        return sorted(set(self.data.values()))

    def values_to_indices_dict(self):
        """
        Return values-to-indices mapping, where indices are indices of values
        on list returned by values_as_sorted_list().

        Returns:
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

        Returns:
            frequency table as a dictionary.

        Note:
            works best with nominal or ordinal data.

        Examples:
            >>> obs = Observable('example', {1: 'A', 2: 'B', 3: 'A'})
            >>> print(obs.frequency_table())
            {'A': 2, 'B': 1}
        """
        # @todo: check if removing this assertion make no problems
        # assert self.is_ordinal() or self.is_nominal()
        freq = defaultdict(int)
        for item in self.data.values():
            freq[item] += 1
        try:
            freq = dict(sorted(tuple(freq.items())))
        except TypeError:
            pass  # simply freq is unchanged, i.e. freq = freq
        return freq

    def descriptive_statistics(self):
        """
        Compute descriptive statistics.

        Returns:
            dict: dictionary where statistics names are keys and
                computed values are numerical values described by names.

        @todo i18n, l10n

        Examples:
            >>> obs = Observable('example', {1: 10.5, 2: 10.2, 3: 10.9})
            >>> obs.descriptive_statistics()        # doctest: +ELLIPSIS
            {'średnia': 10.533333333333333, 'mediana': 10.5, ...
        """
        if self.IS_CONTINUOUS or self.IS_ORDINAL:
            data = tuple(self.data.values())
            return {_('średnia'): np.mean(data),
                    _('mediana'): np.median(data),
                    _('dolny kwartyl'): np.percentile(data, 25),
                    _('górny kwartyl'): np.percentile(data, 75),
                    _('wartość najmniejsza'): np.min(data),
                    _('wartość największa'): np.max(data),
                    _('odchylenie standardowe'): np.std(data),
                    _('wariancja'): np.var(data),
                    _('asymetria'): stats.skew(data),
                    _('kurtoza'): stats.kurtosis(data)}
        return None  # @todo - może lepiej raise TypeError lub coś takiego?!

    @staticmethod
    def print_descriptive_statistics(observables, sep='\t', file=None):
        """
        Print descriptive statistics.

        Prints descriptive statistics of given observables
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
        print('dane', *keys, sep=sep, file=file)  # @todo i18n/l10n
        for obs in observables:
            if obs.IS_CONTINUOUS or obs.IS_ORDINAL:
                print(obs, *obs.descriptive_statistics().values(), sep=sep, file=file)

    def _check_data_kind(self, T):
        """
        Check if all values in self.data are type T.

        Args:
            T (type): int, float, str or other type

        Returns:
            bool: True if all values in dictionary self.data is type T,
                False if at least one value is not type T.

        Examples:
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
        # Notice that empty data (without elements) can not be checked for
        # type of all elements, because "all" in this case mean "none".
        #
        return (len(self.data) > 0
                and all(isinstance(v, T) for v in self.data.values()))


_ = statquest_locale.setup_locale()
if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
