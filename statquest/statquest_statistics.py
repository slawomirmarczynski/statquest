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
from statquest_relations import Relation

_ = statquest_locale.setup_locale()


class Test:
    """
    Abstract Statistical Test.

    Here, in derived classes, should be a description of the test
    procedure, with reference to sources etc.
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
            prove_relationship (bool): True if true h0_thesis prove
                observables relationship; False if true h0_thesis mean
                that observables are independent.
        """
        self.name = _('test')
        self.h0_thesis = _('H0: null hypothesis')         # p_value > alpha
        self.h1_thesis = _('H1: alternative hypothesis')  # p_value < alpha
        self.prove_relationship = True

    def __str__(self):
        """
        Return the name.

        Return:
            str: the name of this test.
        """
        return self.name

    def __call__(self, a, b):
        """
        Relation factory.

        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object
            b (Observable): an object of class Observable or None

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

    def can_be_carried_out(self, a, b):  # pylint: disable=unused-argument
        """
        Can test be carried out?

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
    Pearson's Chi-Square Test of Independence.

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

        Attributes:
            name (str): test short name.
            h0_thesis (str): short name for the null hypothesis.
            h1_thesis (str): short name for the alternative hypothesis.
            prove_relationship (bool): True if true h0_thesis prove
                observables relationship; False if true h0_thesis deny
                that observables are independent.
        """
        super().__init__()  # not necessary, but it is safer

        # @todo: przenieść do plików z translacją
        #
        # self.name = _('test niezależności chi-kwadrat (Pearsona)')
        # self.h0_thesis = _('nie ma związku między zmiennymi kategorycznymi')
        # self.h1_thesis = _('zmienne kategoryczne nie są niezależne')

        self.name = _("Pearson's Chi-Square Test of Independence")
        self.h0_thesis = _('H0: variables are independent')
        self.h1_thesis = _('H1: variables are not independent')
        self.prove_relationship = False

    def __call__(self, a, b, alpha):
        """
        Relation factory.

        Perform a statistical test on observations a and b.

        Args:
            a (Observable): Observable class object
            b (Observable): an object of class Observable or None
            alpha (float): the significance level, 0.0 <= alpha <= 1.0

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
            chisq, p_value, dof, expected = stats.chi2_contingency(observed)
        except:  # pylint: disable=broad-except
            p_value = 1.0
            chisq = float('inf')

        q_value = 1.0 - p_value
        return Relation(a, b, self, chisq, p_value, q_value)

    def can_be_carried_out(self, a, b):
        """
        Can test be preformed?

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

        Attributes:
            name (str): test short name.
            h0_thesis (str): short name for the null hypothesis.
            h1_thesis (str): short name for the alternative hypothesis.
            prove_relationship (bool): True if true h0_thesis prove
                observables relationship; False if true h0_thesis mean
                that observables are independent.
        """
        super().__init__()
        self.name = _('Kruskal-Wallis Test')
        self.h0_thesis = _('H0: distributions are equal')
        self.h1_thesis = _('H1: distributions are not equal')
        self.prove_relationship = True

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

        q_value = p_value
        return Relation(a, b, self, h, p_value, q_value)

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

        Attributes:
            name (str): test short name.
            h0_thesis (str): short name for the null hypothesis.
            h1_thesis (str): short name for the alternative hypothesis.
            prove_relationship (bool): True if true h0_thesis prove
                observables relationship; False if true h0_thesis mean
                that observables are independent.
        """
        super().__init__()
        self.name = 'Pearson Correlation Test'
        self.h0_thesis = 'H0: data are not correlated'
        self.h1_thesis = 'H1: data are correlated'
        self.prove_relationship = False

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
        q_value = 1.0 - p_value
        return Relation(a, b, self, r, p_value, q_value)


ALL_STATISTICAL_TESTS = (ChiSquareIndependenceTest(),
                         KruskalWallisTest(),
                         PearsonCorrelationTest())

if __name__ == "__main__":
    import doctest

    Test.print_descriptions(ALL_STATISTICAL_TESTS)
    doctest.testmod(optionflags=doctest.ELLIPSIS)
