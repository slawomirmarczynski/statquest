#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The definition of Observable class.

File:
    project: StatQuest
    name: statquest_observable.py
    version: 0.5.1.1
    date: 25.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
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

from numpy import float32, float64, int32, int64

import statquest_locale

_ = statquest_locale.setup_locale_translation_gettext()


class Observable:
    """
    Observable is the class whose objects hold data as Pandas Series.

    Observable types can be nominal, ordinal, or continuous. An observable
    is continuous if its values can be used as float point numbers. It is
    ordinal if its values can be used as integer numbers. It is nominal if
    its values can be used as strings of characters.
    """

    # Integer types are promoted to float-point in computations,
    # therefore CONTINUOUS_TYPES includes these types.
    # Actually we would check if a type is cast-able to the desired
    # type.
    #
    ORDINAL_TYPES = (int, int32, int64, int32, int64,)
    CONTINUOUS_TYPES = (float, float32, float64, int, int32, int64)
    NOMINAL_TYPES = (str, object)

    def __init__(self, pandas_series):
        """
        Initialize observable.

        The observable initializer link a name with given data
        and initalize attributes.

        Args:
            pandas_series (pandas.Series): an object of pandas.Serie type.

        Raises:
            TypeError: the observable cannot be created due unknown type
                of data values.
        """
        self.data = pandas_series.dropna()
        # self.data = self.data[self.data.str.strip().astype(bool)]
        self.IS_ORDINAL = False
        self.IS_CONTINUOUS = False
        self.IS_NOMINAL = False
        self.__classify_data_kind()

    def __classify_data_kind(self):
        # Kacze badanie typu. Założenie - nie mamy brakujących wartości (NaN),
        # te bowiem zostały już usunięte wcześniej.
        #
        score_ordinal = 0
        score_continuous = 0
        score_nominal = 0
        values = self.data.to_list()
        for v in values:
            try:
                i = int(v)
                if i == v:
                    score_ordinal += 1
            except:
                pass
            try:
                f = float(v)
                if f == v:
                    score_continuous += 1
            except:
                pass
            try:
                s = str(v)
                if s == v:
                    score_nominal += 1
            except:
                pass
        length = len(values)
        self.IS_ORDINAL = (score_ordinal == length)
        self.IS_CONTINUOUS = (score_continuous == length)
        self.IS_NOMINAL = (score_nominal == length)
        if self.IS_ORDINAL or self.IS_CONTINUOUS:
            self.IS_NOMINAL = False
        if not (self.IS_ORDINAL or self.IS_CONTINUOUS or self.IS_NOMINAL):
            raise TypeError

    def __getitem__(self, key):
        """
        Return a value for the given key.

        Returns a value for the given key, thus an object of the class
        Observable will behave in a "transparent" way.

        Args:
            key: a key to obtain requested value from self.data dict.

        Returns:
            requested value from self.data dict.
        """
        return self.data[key]

    def __len__(self):
        """
        Get observable size.

        Returns:
            int: number of elements stored inside the observable.
        """
        return len(self.data)

    def __str__(self):
        """
        Get the name (label) of the observable.

        Returns:
            str: the name given to observable.
        """
        return self.data.name
