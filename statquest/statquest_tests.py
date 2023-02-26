#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The definition of statistical tests.

There are definitions of three statistical tests: the chi-square
independence test, the Kruskal-Wallis test, the Pearson correlation
test. These tests are provided as a tuple ALL_STATISTICAL_TESTS.

File:
    project: StatQuest
    name: statquest_tests.py
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

import warnings
from abc import ABC, abstractmethod
from collections import defaultdict

import pandas as pd
from scipy import stats

import statquest_locale
from statquest_relation import Relation

_ = statquest_locale.setup_locale_translation_gettext()


class Test(ABC):
    """
    Abstract Statistical Test.

    Here, in derived classes, should be a description of the test
    procedure, with reference to sources etc.

    Attributes:
        name (str): test name.
        h0_thesis (str): short name for the null hypothesis.
        h1_thesis (str): short name for the alternative hypothesis.
        prove_relationship (bool): True if true h0_thesis prove
            observables relationship; False if true h0_thesis mean
            that observables are independent.
    """

    @abstractmethod
    def __init__(self):
        """
        Init test.

        Note:
            Why this initializer has no parameters (except self)? Each
            test have completely different logic and must be hard-coded
            from a scratch. It is useless call parametrized initializer.
        """
        self.name = _('test')
        self.name_short = _('test')  # should not exceed n chars
        self.stat_name = 'unknown'
        self.h0_thesis = _('H0: null hypothesis')  # p_value > alpha
        self.h1_thesis = _('H1: alternative hypothesis')  # p_value < alpha
        self.prove_relationship = True
        self.is_symetric = True  # test(a, b) is the same as test(b, a)

    def __str__(self):
        """
        Return the name.

        Return:
            str: the name of this test.
        """
        return self.name

    @abstractmethod
    def __call__(self, a, b):
        """
        Relation factory.

        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object
            b (Observable): an object of class Observable

        Throws:
            TypeError: when observables aren't compatible with the test.

        Returns:
            Relation: the result of the test.
        """
        if not self.can_be_carried_out(a, b):
            raise TypeError
        value = 0
        p_value = 0
        return Relation(a, b, self, value, p_value)

    @abstractmethod
    def can_be_carried_out(self, a, b):  # pylint: disable=unused-argument
        """
        Can test be carried out?

        Args:
            a (Observable): observable class object
            b (Observable): an object of class Observable

        Returns:
            bool: True if the test can be applied to data a and b,
                False if the test cannot be used (e.g. the test requires
                NOMINAL variables, but data is CONTINUOUS type).
        """
        return False  # Should/must be overridden in subclasses.


class ChiSquareIndependenceTest(Test):  # pylint: disable=C0111
    """
    Pearson's Chi-Square Test of Independence.

    We have got cases that are described using two categorical variables
    using appropriate nominal scales. We want to find out if these
    variables are independent, i.e. whether the features described by
    the scales are significantly different.

    We formulate the null hypothesis and the alternative hypothesis:

        H0: There is no relationship between the categorical variables.
        H1: Categorical variables are not independent.

    We calculate the chi-square statistic for the corresponding crosstab,
    then we compare the p-value with the alpha significance level.
    Customary the alpha significance level is assumed to be 0.05
    (i.e. 5%), specifying it as "significant". A significance level of
    0.001 is sometimes referred to as "highly significant".

    If p-value is too small, the test reject the null hypothesis.

    If p-value is  big - "we have no grounds to reject the null
    hypothesis" - de facto we just take the null hypothesis.

    In the table form it looks like this:

                                  H0    H1
                -----------------------------------------------
                p_value < alpha:  no    yes   are dependent
                p_value > alpha:  yes   no    are NOT dependent

    See also:
        https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
        https://online.stat.psu.edu/stat500/lesson/8
    """

    def __init__(self):
        """
        Init test.

        Note:
            Why this initializer has no parameters (except self)? Each
            test have completely different logic and must be hard-coded
            from a scratch. It is useless call parametrized initializer.
        """
        super().__init__()  # not necessary, but it is safer

        self.name = _("Pearson's Chi-Square Test of Independence")
        self.name_short = _("chi-square")  # should not exceed n chars
        self.stat_name = 'chi-square'
        self.h0_thesis = _('H0: variables are independent')
        self.h1_thesis = _('H1: variables are not independent')
        self.prove_relationship = True

    def __call__(self, a, b):
        """
        Relation factory.

        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object
            b (Observable): an object of class Observable

        Throws:
            TypeError: when observables aren't compatible with the test.

        Returns:
            tuple:
                q_value (float): q_value value
                p_value (float): p_value value
                stat_name (str): the name of the statistic
                stat_value (float): the value of the statistic
        """
        if not self.can_be_carried_out(a, b):
            raise TypeError
        ctab = pd.crosstab(a.data, b.data)
        chisq, p_value, dof, expected = stats.chi2_contingency(ctab)
        return Relation(a, b, self, chisq, p_value)

    def can_be_carried_out(self, a, b):
        """
        Can test be preformed?

        Checks whether the test can be performed on observations a and b.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object.
            b (Observable): an object of class Observable.

        Returns:
            bool: True if the test can be applied to data a and b,
                False if the test cannot be used (e.g. the test requires
                NOMINAL variables, but data is CONTINUOUS type).
        """
        if a and b:
            good_a = a.IS_NOMINAL or a.IS_ORDINAL
            good_b = b.IS_NOMINAL or b.IS_ORDINAL
            if good_a and good_b:
                return True
        return False


class KruskalWallisTest(Test):  # pylint: disable=C0111
    """
    Kruskal-Wallis test.

    We have data that can be classified using the nominal scale and
    numerical values (floating point numbers, integers). We want to find
    out if the distributions of a continuous variable are significantly
    different for each group formed by values having the same nominal
    value. We don't know if the data is normally distributed.
    We formulate null hypothesis and alternative hypothesis:

        H0: Distribution functions are equal.
        H1: Distribution functions are not equal.

    If p-value is too small, reject the null hypothesis.

    If p-value it is big, "we have no grounds to reject the null
    hypothesis" (de facto we just take the null hypothesis.)

    In the table it looks like this:

                          H0   H1    application
        -------------------------------------------------- --------
        p_value < alpha:  no   yes   the distributions are NOT the same
        p_value > alpha:  yes  no    the distributions are the same

    For example, such a test could be used to test whether the height of
    patients (in centimeters) is related to be right or left-handed.

    See also:
      https://en.wikipedia.org/wiki/Kruskal-Wallis_one-way_analysis_of_variance
      http://www.biostathandbook.com/kruskalwallis.html
    """

    def __init__(self):
        """
        Init test.

        Note:
            Why this initializer has no parameters (except self)? Each
            test have completely different logic and must be hard-coded
            from a scratch. It is useless call parametrized initializer.
        """
        super().__init__()
        self.name = _('Kruskal-Wallis Test')
        self.name_short = _("Kruskal-Wallis")  # should not exceed n chars
        self.stat_name = 'H'
        self.h0_thesis = _('H0: distributions are equal')
        self.h1_thesis = _('H1: distributions are not equal')
        self.prove_relationship = False
        self.is_symetric = False

    def __call__(self, a, b):
        """
        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object.
            b (Observable): an object of class Observable.

        Throws:
            TypeError: when observables aren't compatible with the test.

        Returns:
            tuple: (p_value, stat_name, stat_value); in subclasses:
                p_value (float): p_value value
                stat_name (str): the name of the statistic
                stat_value (float): the value of the statistic
        """
        if not self.can_be_carried_out(a, b):
            raise TypeError

        # We have two observables, namely a and b. One of them should be
        # nominal or ordinal, one of them should be continuous. 
        # If the observable a is continuous and the observable b is nominal
        # (or ordinal) then we swap a and b. Since we can assume that
        # the observable a is nominal/ordinal and observable b is continuous.
        #
        # We don't check all details here, because the check was already
        # provided by self.can_be_carried_out(a, b).
        #
        on = a.IS_ORDINAL and b.IS_NOMINAL
        cn = a.IS_CONTINUOUS and b.IS_NOMINAL
        co = a.IS_CONTINUOUS and b.IS_ORDINAL
        if on or cn or co:
            a, b = b, a

        # We collect all keys common for both observables.
        # And construct a mapping (dictionary) from a-values to b-values.
        #
        keys = set(a.data.keys()) & set(b.data.keys())
        observed = defaultdict(list)
        for k in keys:
            observed[a[k]].append(b[k])

        h, p_value = stats.kruskal(*list(observed.values()))
        return Relation(a, b, self, h, p_value)

    def can_be_carried_out(self, a, b):
        """
        Check can test be preformed.

        Checks whether the test can be performed on observations a and b.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object
            b (Observable): an object of class Observable.

        Returns:
            bool: True if the test can be applied to data a and b,
                False if the test cannot be used (e.g. the test requires
                NOMINAL variables, but data is CONTINUOUS type).
        """
        if a and b:
            if (a.IS_NOMINAL or a.IS_ORDINAL) and b.IS_CONTINUOUS:
                return True
            if (b.IS_NOMINAL or b.IS_ORDINAL) and a.IS_CONTINUOUS:
                return True
        return False


class PearsonCorrelationTest(Test):  # pylint: disable=C0111
    """
    Pearson Correlation Test.

    We have two continuous variables. We want to find out if these
    variables are correlated or not.

    We formulate the null hypothesis and the alternative hypothesis:

        H0: There is no correlation.
        H1: There is a correlation.

    If p-value is too small, reject the null hypothesis if p-value
    it is big, "we have no grounds to reject the null hypothesis" 
    (de facto we just take the null hypothesis).

    It can be presented in table form:

                                H0      H1      conclusion
            -----------------------------------------------------------
            p_value < alpha:    no      yes     there is a correlation
            p_value > alpha:    yes     no      there is no correlation

    For example, such a test could be used to check whether mass
    the patient's body depends on his height.

    In the case of the r correlation test, the problematic are: 
        - the requirement of the normality of the respondents schedules;
        - the possibility that dependency is not linear.
     
     You can quite easily create such datasets for which
     test correlation clearly produces erroneous results.
    """

    def __init__(self):
        """
        Init test.

        Note:
            Why this initializer has no parameters (except self)? Each
            test have completely different logic and must be hard-coded
            from a scratch. It is useless call parametrized initializer.
        """
        super().__init__()
        self.name = _('Pearson Correlation Test')
        self.name_short = _('Pearson Correlation')
        self.stat_name = _('r')
        self.h0_thesis = _('H0: data are not correlated')
        self.h1_thesis = _('H1: data are correlated')
        self.prove_relationship = True

    def can_be_carried_out(self, a, b):
        """
        Check can test be preformed.

        Checks whether the test can be performed on observations a and b.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object.
            b (Observable): an object of class Observable.

        Returns:
            bool: True if the test can be applied to data a and b,
                False if the test cannot be used (e.g. the test requires
                NOMINAL variables, but data is CONTINUOUS type).
        """
        if (a is not None) and (b is not None):
            good_a = a.IS_ORDINAL or a.IS_CONTINUOUS
            good_b = b.IS_ORDINAL or b.IS_CONTINUOUS
            if good_a and good_b:
                return True
        return False

    def __call__(self, a, b):
        """
        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object.
            b (Observable): an object of class Observable.

        Throws:
            TypeError: when observables aren't compatible with the test.

        Returns:
            tuple: (p_value, stat_name, stat_value); in subclasses:
                p_value (float): p_value value
                stat_name (str): the name of the statistic
                stat_value (float): the value of the statistic
        """

        df = pd.merge(a.data, b.data, left_index=True, right_index=True)
        df = df.dropna()
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            r, p_value = stats.pearsonr(x, y)
        return Relation(a, b, self, r, p_value)


class SpearmanRTest(Test):  # pylint: disable=C0111
    """
    Spearman r Test.

    We have two continuous variables. We want to find out if these
    variables are correlated or not.

    We formulate the null hypothesis and the alternative hypothesis:

        H0: There is no correlation.
        H1: There is a correlation.

    If p-value is too small, reject the null hypothesis if p-value
    it is big, "we have no grounds to reject the null hypothesis"
    (de facto we just take the null hypothesis).

    It can be presented in table form:

                                H0      H1      conclusion
            -----------------------------------------------------------
            p_value < alpha:    no      yes     there is a correlation
            p_value > alpha:    yes     no      there is no correlation

    For example, such a test could be used to check whether mass
    the patient's body depends on his height.
    """

    def __init__(self):
        """
        Init test.

        Note:
            Why this initializer has no parameters (except self)? Each
            test have completely different logic and must be hard-coded
            from a scratch. It is useless call parametrized initializer.
        """
        super().__init__()
        self.name = _('Spearman r test')
        self.name_short = _('Spearman r')
        self.stat_name = _('r')
        self.h0_thesis = _('H0: data are not correlated')
        self.h1_thesis = _('H1: data are correlated')
        self.prove_relationship = True

    def can_be_carried_out(self, a, b):
        """
        Check can test be preformed.

        Checks whether the test can be performed on observations a and b.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object.
            b (Observable): an object of class Observable.

        Returns:
            bool: True if the test can be applied to data a and b,
                False if the test cannot be used (e.g. the test requires
                NOMINAL variables, but data is CONTINUOUS type).
        """
        if (a is not None) and (b is not None):
            good_a = a.IS_ORDINAL or a.IS_CONTINUOUS
            good_b = b.IS_ORDINAL or b.IS_CONTINUOUS
            if good_a and good_b:
                return True
        return False

    def __call__(self, a, b):
        """
        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object.
            b (Observable): an object of class Observable.

        Throws:
            TypeError: when observables aren't compatible with the test.

        Returns:
            tuple: (p_value, stat_name, stat_value); in subclasses:
                p_value (float): p_value value
                stat_name (str): the name of the statistic
                stat_value (float): the value of the statistic
        """

        df = pd.merge(a.data, b.data, left_index=True, right_index=True)
        df = df.dropna()
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            r, p_value = stats.spearmanr(x, y)
        return Relation(a, b, self, r, p_value)


class KendallTauTest(Test):  # pylint: disable=C0111
    """
    Spearman r Test.

    We have two continuous variables. We want to find out if these
    variables are correlated or not.

    We formulate the null hypothesis and the alternative hypothesis:

        H0: There is no correlation.
        H1: There is a correlation.

    If p-value is too small, reject the null hypothesis if p-value
    it is big, "we have no grounds to reject the null hypothesis"
    (de facto we just take the null hypothesis).

    It can be presented in table form:

                                H0      H1      conclusion
            -----------------------------------------------------------
            p_value < alpha:    no      yes     there is a correlation
            p_value > alpha:    yes     no      there is no correlation

    For example, such a test could be used to check whether mass
    the patient's body depends on his height.
    """

    def __init__(self):
        """
        Init test.

        Note:
            Why this initializer has no parameters (except self)? Each
            test have completely different logic and must be hard-coded
            from a scratch. It is useless call parametrized initializer.
        """
        super().__init__()
        self.name = _('Kendall tau test')
        self.name_short = _('Kendall tau')
        self.stat_name = _('r')
        self.h0_thesis = _('H0: data are not correlated')
        self.h1_thesis = _('H1: data are correlated')
        self.prove_relationship = True

    def can_be_carried_out(self, a, b):
        """
        Check can test be preformed.

        Checks whether the test can be performed on observations a and b.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object.
            b (Observable): an object of class Observable.

        Returns:
            bool: True if the test can be applied to data a and b,
                False if the test cannot be used (e.g. the test requires
                NOMINAL variables, but data is CONTINUOUS type).
        """
        if (a is not None) and (b is not None):
            good_a = a.IS_ORDINAL or a.IS_CONTINUOUS
            good_b = b.IS_ORDINAL or b.IS_CONTINUOUS
            if good_a and good_b:
                return True
        return False

    def __call__(self, a, b):
        """
        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object.
            b (Observable): an object of class Observable.

        Throws:
            TypeError: when observables aren't compatible with the test.

        Returns:
            tuple: (p_value, stat_name, stat_value); in subclasses:
                p_value (float): p_value value
                stat_name (str): the name of the statistic
                stat_value (float): the value of the statistic
        """

        df = pd.merge(a.data, b.data, left_index=True, right_index=True)
        df = df.dropna()
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            r, p_value = stats.kendalltau(x, y)
        return Relation(a, b, self, r, p_value)


ALL_STATISTICAL_TESTS = (ChiSquareIndependenceTest(),
                         KruskalWallisTest(),
                         PearsonCorrelationTest(),
                         SpearmanRTest(),
                         KendallTauTest())

if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
