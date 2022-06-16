#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The definition of statistical tests.

There are defined three statistical tests: the chi-square independence test, 
the Kruskal-Wallis test, the Pearson correlation test.

File:
    project: StatQuest
    name: statquest_statistics.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""

from collections import defaultdict

import numpy as np
from scipy import stats

import statquest_locale


class Test:
    """
    Abstract base class for statistical tests.

    Here, in derived classes, should be a description of the test
    procedure, with reference to sources etc.

    The null hypothesis (H0) is that "there is nothing meaningful in
    the data". Alternative hypothesis (H1) on the contrary - that "there
    is something". Probability - that the null hypothesis (H0) is true
    - is estimated by the p-value: if the p-value is greater than the
    alpha significance level, then you must accept the null hypothesis.
    If p-value is small, i.e. p_value < alpha, then the alternative
    hypothesis is true.

    Note: a low p-value is a strong premise for rejecting the hypothesis
    a zero but high p-value is a poor premise for acceptance the null
    hypothesis. A value equal to the threshold ... does not conclude.

    Typically, the alpha significance level = 0.05 or 5%.
    """

    def __init__(self):
        """
        Init test.

        Note:
            Why this initializer has no parameters (except self)? Each
            test have completely different logic and must be hard-coded
            from a scratch. It is useless call parametrized initializer.

        Attributes:
            name (str): test short name.
            h0_thesis (str): short name for the null hypothesis.
            h1_thesis (str): short name for the alternative hypothesis.
        """
        self.name = _('test')
        self.h0_thesis = _('hipoteza zerowa')  # p_value > alpha
        self.h1_thesis = _('hipoteza alternatywna')  # p_value < alpha

    def __str__(self):
        """
        Return the name.

        Return:
            str: the name of this test.
        """
        return self.name

    def __call__(self, a, b=None):
        """
        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object
            b (Observable): an object of class Observable or None

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
        p_value = None
        stat_name = None
        stat_value = None
        return p_value, stat_name, stat_value

    @staticmethod
    def can_be_carried_out(a, b=None):  # pylint: disable=unused-argument
        """
        Check can test be preformed.

        Checks whether the test can be performed on observations a and b.
        A special case may be b = None. Abstract.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object
            b (Observable): an object of class Observable or None

        Returns:
            bool: True if the test can be applied to data a and b,
                False if the test cannot be used (e.g. the test requires
                NOMINAL variables, but data is CONTINUOUS type).
        """
        return False  # Should/must be overridden in subclasses.


class ChiSquareIndependenceTest(Test):  # pylint: disable=C0111
    """
    Chi-square test of independence (Pearson).

    We have cases that are described using two categorical variables
    using appropriate nominal scales. We want to find out if these
    variables are independent, i.e. whether the features described by
    the scales are significantly different.

    We formulate the null hypothesis and the alternative hypothesis:

        H0: There is no relationship between the categorical variables
        H1: Categorical variables are not independent

    We calculate the chi-square statistic for the corresponding crosstab
    and then we compare the p-value with the alpha significance level.
    Customary the alpha significance level is assumed to be 0.05
    (i.e. 5%), specifying it as "significant". A significance level of
    0.001 is sometimes referred to as "highly significant".

    If p-value is too small, the test reject the null hypothesis if
    p-value is  big - "we have no grounds to reject the null hypothesis"
    - de facto after we just take the null hypothesis.

    In the table form it looks like this:

                                  H0    H1
                -----------------------------------------------
                p_value < alpha:  no    yes   are dependent
                p_value > alpha:  yes   no    are NOT dependent

    For example, such a test could be used to check if a color of hair
    (referred to as blue, brown etc.) has to do with being right-handed
    or left-handed. If we were to get p-value equal to 0.00217 then
    because 0.00217 < 0.05, we reject the null hypothesis of
    "independent variables" and thus we adopt the alternative hypothesis
    "variables are dependent". If we were  they got a p-value of 0.13842
    that's because 0.13842 > 0.05, we find as insurance "there are no
    grounds to reject the null hypothesis" - that is, after we simply
    consider a 13.842% chance of making a first type error (consisting
    in making the null hypothesis false) is more than the assumed risk
    level of 5% (significance level alpha). It is possible (86.158%
    specifically) making the second type of error, which is recognizing
    the false null hypothesis as true.


        hypothesis    our conclusion    what is really?    probability
        --------------------------------------------------------------
        H0            independent       independent    p_value > alpha
        H0            independent       dependent          1 - p_value
        H1            dependent         variables          1 - p_value
        H1            dependent         dependent      p_value < alpha

    See also:
        https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
        https://onlinecourses.science.psu.edu/stat500/node/56/
    """

    def __init__(self):
        """
        Init test.
        """
        super().__init__()  # not necessary, but it is safer
        self.name = _('test niezależności chi-kwadrat (Pearsona)')
        self.h0_thesis = _('nie ma związku między zmiennymi kategorycznymi')
        self.h1_thesis = _('zmienne kategoryczne nie są niezależne')

    def __call__(self, a, b=None):
        """
        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object
            b (Observable): an object of class Observable or None

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

        # We count how many independent nominal(ordinal) values are so
        # in observable and what b.

        da = a.values_to_indices_dict()
        db = b.values_to_indices_dict()
        observed = np.zeros((len(da), len(db)))

        # In fact, key sets for observables a and b should be identical,
        # i.e.the features described by the observables should correspond
        # to the same entity.The common part (union of collections)
        # guarantees that for each key will be values in both dictionaries,
        # i.e. in dictionary a and dictionary b.

        keys = set(a.data.keys()) & set(b.data.keys())
        for k in keys:
            observed[da[a[k]], db[b[k]]] += 1

        try:
            # pylint: disable=unused-variable
            chi2, p_value, dof, expected = stats.chi2_contingency(observed)
        except Exception:  # pylint: disable=W0703
            p_value = 1.0
            chi2 = float('inf')

        return p_value, 'chi-sq', chi2

    @staticmethod
    def can_be_carried_out(a, b=None):
        """
        Check can test be preformed.

        Checks whether the test can be performed on observations a and b.
        A special case may be b = None. Abstract.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object
            b (Observable): an object of class Observable or None

        Returns:
            bool: True if the test can be applied to data a and b,
                False if the test cannot be used (e.g. the test requires
                NOMINAL variables, but data is CONTINUOUS type).
        """
        if a and b:
            good_a = a.is_nominal() or a.is_ordinal()
            good_b = b.is_nominal() or b.is_ordinal()
            if good_a and good_b:
                return True
        return False


class KruskalWallisTest(Test):  # pylint: disable=C0111
    """
    Kruskal-Wallis test.

    We have cases that can be classified using the nominal scale and
    numerical values (floating point numbers, integers). We want to find
    out if the distributions of a continuous variable are significantly
    different for each group formed by values having the same nominal
    value. We don't know if the data is normally distributed.
    We formulate null hypothesis and alternative hypothesis:

        H0: distribution functions are equal,
            no significant differences

        H1: distribution functions are not equal,
            there are significant differences

    If p-value is too small, reject the null hypothesis if p-value it is
    big, "we have no grounds to reject the null hypothesis" (de facto
    we just take the null hypothesis.) In the table it looks like this:

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
        """
        super().__init__()
        self.name = _('test Kruskala-Wallisa')
        self.h0_thesis = _('dystrybuanty są równe, brak istotnych różnic')
        self.h1_thesis = _('dystrybuanty nie są równe, są istotne różnice')

    def __call__(self, a, b=None):
        """
        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object
            b (Observable): an object of class Observable or None

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
        if a.IS_CONTINUOS:
            a, b = b, a

        # We collect all keys common for both observables.
        # And construct a mapping (dictionary) from a-values to b-values.
        #
        keys = set(a.data.keys()) & set(b.data.keys())
        observed = defaultdict(list)
        for k in keys:
            observed[a[k]].append(b[k])

        try:
            h, p_value = stats.mstats.kruskalwallis(*list(observed.values()))
        except Exception:  # pylint: disable=W0703
            h = float('inf')
            p_value = 1.0

        return p_value, 'H', h

    @staticmethod
    def can_be_carried_out(a, b=None):
        """
        Check can test be preformed.

        Checks whether the test can be performed on observations a and b.
        A special case may be b = None. Abstract.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object
            b (Observable): an object of class Observable or None

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
    Pearson r correlation test.

    We have cases that are described using two continuous variables.
    We want to find out if these variables are correlated or not.

    We formulate the null hypothesis and the alternative hypothesis:

        H0: there is no correlation
        H1: there is a correlation

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
        """
        super().__init__()
        self.name = 'test korelacji r Pearsona'
        self.h0_thesis = 'brak korelacji'
        self.h1_thesis = 'istnieje korelacja'

    @staticmethod
    def can_be_carried_out(a, b=None):
        """
        Check can test be preformed.

        Checks whether the test can be performed on observations a and b.
        A special case may be b = None. Abstract.

        Note:
            It is a static method - there is no need for a test object
            - we can check can_be_carried_out(a,b) before test creation.

        Args:
            a (Observable): observable class object
            b (Observable): an object of class Observable or None

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

    def __call__(self, a, b=None):
        """
        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object
            b (Observable): an object of class Observable or None

        Throws:
            TypeError: when observables aren't compatible with the test.

        Returns:
            tuple: (p_value, stat_name, stat_value); in subclasses:
                p_value (float): p_value value
                stat_name (str): the name of the statistic
                stat_value (float): the value of the statistic
        """
        x = []
        y = []
        keys = set(a.data.keys()) & set(b.data.keys())
        for k in keys:
            x.append(a[k])
            y.append(b[k])
        r, p_value = stats.pearsonr(x, y)
        return p_value, 'r', r


_ = statquest_locale.setup_locale()

TESTS_SUITE = (ChiSquareIndependenceTest(),
               KruskalWallisTest(),
               PearsonCorrelationTest())

if __name__ == "__main__":
    import doctest

    Test.print_descriptions(TESTS_SUITE)
    doctest.testmod(optionflags=doctest.ELLIPSIS)
