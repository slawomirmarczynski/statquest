#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program do analizy danych z bazy danych SQLite ProQuest.db.

Analizy statystyczne. Statystyki opisowe i testy statystyczne.

@file: proquest_tests.py
@version: 0.3.2.2
@date: 10.07.2018
@author: dr Sławomir Marczyński, slawek@zut.edu.pl
"""


from collections import defaultdict
import numpy as np
from scipy import stats


# @todo Na razie nie jest do niczego używane.
#
def cast_continous_to_occurrences(data, tresholds, prefix='', postfix=''):
    """
    Rzutowanie ze zmiennej continous na zmieną nominal - dla zapodanych progów
    tresholds tworzony jest słownik, którego klucze opisowo zapodają zakresy,
    a wartości odpowiadają liczbom przypadków.

    Dane:
        data      -- słownik zawierający dane, interesujące są tylko wartości;
        tresholds -- progi jako ciąg wartości,
                     np. [-float(inf), -1, 0, 1, float(inf)]
        perfix    -- prefiks dodawany przed zakresem;
        postfix   -- postfix dodawany po zakresie.

    Zwraca:
        słownik, którego kluczami są np. 'waga od 1 do 5 kg' itd.

    Przykład:

        >>> data = {1: -1.0, 2: 5, 3: 7, 10: 999, 4: -0.5}
        >>> trsh = [-float('inf'), 0, float('inf')]
        >>> prefix = 'I = '
        >>> postfix = ' [mA]'
        >>> cast_continous_to_occurrences(data, trsh, prefix, postfix)
        {'I = od -inf do 0 [mA]': 2, 'I = od 0 do inf [mA]': 3}
    """
    data = list(data.values())
    buckets = dict()
    for i in range(len(tresholds) - 1):
        low = tresholds[i]
        high = tresholds[i + 1]
        count = 0
        for value in data:
            if value is not None and low <= value < high:
                count += 1
        key = prefix + 'od ' + str(low) + ' do ' + str(high) + postfix
        buckets[key] = count
    return buckets


def frequency_table(data):
    """
    Dla zmiennych nie będących zmiennymi ciągłymi zlicza częstości
    występowania poszczególnych wartości. Ze skali nominalnej w ten sposób
    można dostać skalę porządkową/ciągłą.

    >>> frequency_table({1:'A', 2:'A', 3:'B', 4:'A', 5:'B', 6:'C'})
    {'A': 3, 'B': 2, 'C': 1}
    """
    freq = defaultdict(int)
    for item in data.values():
        freq[item] += 1
    freq = dict(sorted(tuple(freq.items())))
    return freq


def descriptive_statistics(data):
    """
    Jeżeli to możliwe to oblicza statystyki opisowe.
    """

    # BTW, observable.values to zawsze powinien być słownik (lub None).
    #
    # Dane mogą być nominal, ordinal, continous, interval.

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


class Test:  # pylint: disable=C0111
    description = """
    Abstrakcyjna klasa bazowa dla testów statystycznych.

    Tu powinien być opis testu, z odesłaniem do ew. materiałów źródłowych.
    Opisy z wszystkich testów trafiają do pliku tekstowego jako dokumentacja
    obliczen - dlatego ten docstring jest zaetykietowany jako description.

    Hipoteza zerowa (H0) to stwierdzenie że nie ma niczego znaczącego w danych.
    Hipoteza alternatywna (H1) odwrotnie - że coś jest. Prawdopodobieństwo że
    prawdziwa jest hipoteza zerowa (H0) jest oszacowane przez wartość p-value:
    jeżeli p-value jest większe niż poziom istotności alfa, to znaczy że trzeba
    przyjąć hipotezę zerową. Jeżeli p-value jest małe, tzn. p_value < alpha,
    to prawdziwa jest hipoteza alternatywna.

    Uwaga: niska wartość p-value jest silną przesłanką za odrzuceniem hipotezy
    zerowej, ale wysoka wartość p-value jest słabą przesłanką za przyjęciem
    hipotezy zerowej. Wartość równa progowi istotności... nie rozstrzyga.

    Zwykle poziom istotności alpha = 0.05, czyli 5%.
    """

    def __init__(self):
        """
        Inicjalizacja testu.
        """
        self.name = 'test'
        self.h0_thesis = 'hipoteza zerowa'  # p_value > alpha
        self.h1_thesis = 'hipoteza alternatywna'  # p_value < alpha

    def __str__(self):
        """
        Zwraca nazwę testu.
        """
        return self.name

    @staticmethod
    def can_be_carried_out(a, b=None):  # pylint: disable=unused-argument
        """
        Sprawdza, czy test może być przeprowadzony na obserwablach a i b.
        Szczególnym przypadkiem może być b=None. Abstrakcyjna.

        Dane:
            a -- obiekt klasy Observable
            b -- obiekt klasy Observable lub None

        Zwraca:
            True jeżeli można zastosować test do danych a i b, False jeżeli
            nie można zastosować testu (np. test wymaga zmiennych typu NOMINAL,
            a dane są typu CONTINOUS). Jeżeli b == None (lub jest pominięte),
            to test jest (ma być) przeprowadzany na jednej tylko obserwabli.
        """
        return False

    @staticmethod
    def print_descriptions(tests, file=None):
        print('='*80, file=file)
        for test in tests:
            print(test, file=file)
            print('-'*80, file=file)
            print(test.description, file=file)
            print('='*80, file=file)

    def __call__(self, a, b=None):
        """
        Przeprowadza test statystyczny na obserwablach a i b.

        Uwaga: zakłada się, że test taki da się wykonać - co sprawdzono
               wcześniej przez can_be_carried_out() - dlatego dane wejściowe
               nie są powtórnie weryfikowane. Abstrakcyjna.

        Dane:
            a -- obiekt klasy Observable
            b -- obiekt klasy Observable lub None

        Zwraca:
            p_value    -- wartość p_value
            stat_name  -- nazwę statystyki
            stat_value -- wartość statystyki
        """
        p_value = None
        stat_name = None
        stat_value = None
        return p_value, stat_name, stat_value


class ChiSquareIndependenceTest(Test):  # pylint: disable=C0111
    description = """
    Test niezależności chi-kwadrat (Pearsona).

    Mamy przypadki, które są opisane przy użyciu dwóch zmiennych kategorycznych
    za pomocą odpowiednich skal nominalnych. Chcemy dowiedzieć się, czy zmienne
    te są niezależne, tj. czy cechy opisane przez skale są istotnie różne.

    Formułujemy hipotezę zerową i hipotezę alternatywną:

        H0: nie ma związku między zmiennymi kategorycznymi
        H1: zmienne kategoryczne nie są niezależne

    Obliczamy statystykę chi-kwadrat dla odpowiedniej tablicy krzyżowej
    i następnie porównujemy p-value z poziomem istotności alpha. Zwyczajowo
    poziom istotności alpha przyjmuje się równy 0.05 (czyli 5%), określając
    go jako "znaczący". Poziom istotności równy 0.001 bywa określany jako
    "wielce znaczący".

    Jeżeli p-value jest zbyt małe to odrzucamy hipotezę zerową, jeżeli p-value
    jest duże to "nie mamy podstaw do odrzucenia hipotezy zerowej" (de facto po
    prostu przyjmujemy hipotezę zerową). W tabelce wygląda to tak:

                                H0      H1      wniosek
            ----------------------------------------------------------
            p_value < alpha:    nie     tak     zmienne zależne
            p_value > alpha:    tak     nie     zmienne NIE SĄ zależne

    Przykładowo, tego rodzaju test mógłby posłużyć do sprawdzenia, czy kolor
    włosów (określanych jako niebieskie, brązowe itp.) ma związek z bycia prawo
    lub lewo-ręcznym. Gdybyśmy otrzymali p-value równe 0.00217 to, ponieważ
    0.00217 < 0.05, odrzucamy hipotezę zerową "zmienne niezależne", a tym samym
    przyjmujemy hipotezę alternatywną "zmienne sa zależne". Gdybyśmy natomiast
    otrzymali p-value równe 0.13842 to, ponieważ 0.13842 > 0.05, stwierdzamy
    asekuracyjnie "nie ma podstaw do odrzucenia hipotezy zerowej" - czyli po
    prostu uznajemy że 13.842% szans na popełnienie błędu pierwszego rodzaju
    (polegającego na uznaniu za fałszywą prawdziwej hipotezy zerowej) to więcej
    niż założony poziom ryzyka 5% (poziom istotności alpha). Istnieje możliwość
    (konkretnie 86.158%) popełnienia błędu drugiego rodzaju, polegającego na
    uznaniu za prawdziwą fałszywej hipotezy zerowej.


        hipoteza    co stwierdzamy?     co jest naprawdę?   prawdopodobieństwo
        ----------------------------------------------------------------------
        H0          niezależne          niezależne          p_value > alpha
        H0          niezależne          zmienne zależne     1 - p_value
        H1          zmienne zależne     niezależne          1 - p_value
        H1          zmienne zależne     zmienne zależne     p_value < alpha


    Patrz także:
        https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
        https://onlinecourses.science.psu.edu/stat500/node/56/
    """

    def __init__(self):
        """
        Inicjalizacja testu.
        """
        super().__init__()
        self.name = 'test niezależności chi-kwadrat (Pearsona)'
        self.h0_thesis = 'nie ma związku między zmiennymi kategorycznymi'
        self.h1_thesis = 'zmienne kategoryczne nie są niezależne'

    @staticmethod
    def can_be_carried_out(a, b=None):
        """
        Sprawdza, czy test może być przeprowadzony na obserwablach a i b.
        Szczególnym przypadkiem może być b=None.

        Dane:
            a -- obiekt klasy Observable
            b -- obiekt klasy Observable lub None

        Zwraca:
            True jeżeli można zastosować test do danych a i b, False jeżeli
            nie można zastosować testu (np. test wymaga zmiennych typu NOMINAL,
            a dane są typu CONTINOUS).
        """
        if a and b:
            good_a = a.is_nominal() or a.is_ordinal()
            good_b = b.is_nominal() or b.is_ordinal()
            if good_a and good_b:
                return True
        return False

    def __call__(self, a, b=None):
        """
        Przeprowadza test statystyczny na obserwablach a i b.

        Uwaga: zakłada się, że test taki da się wykonać - co sprawdzono
               wcześniej przez can_be_carried_out() - dlatego dane wejściowe
               nie są powtórnie weryfikowane.

        Dane:
            a -- obiekt klasy Observable
            b -- obiekt klasy Observable lub None

        Zwraca:
            p_value    -- wartość p_value
            stat_name  -- nazwę statystyki
            stat_value -- wartość statystyki
        """

        # Zliczamy ile jest niezależnych wartości nominalnych (porządkowych)
        # tak w obserwabli a jaki b.

        da = a.values_to_indices_dict()
        db = b.values_to_indices_dict()
        observed = np.zeros((len(da), len(db)))

        # W istocie rzeczy zbiory kluczy dla obserwabli a i b powinny być
        # identyczne, tzn. cechy opisane przez obserwable powinny odnosić się
        # do tych samych bytów. Część wspólna (unia zbiorów) gwarantuje że dla
        # każdego klucza tak wybranego będzie on określał wartości w obu
        # słownikach, tj. w słowniku a i w słowniku b.
        #
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


class KruskalWallisTest(Test):  # pylint: disable=C0111
    description = """
    Test Kruskala-Wallisa.

    Mamy przypadki, które można sklasyfikować za pomocą skali nominalnej oraz
    wartościami liczbowymi (liczbami zmiennoprzecinkowymi, ewentualnie liczbami
    całkowitymi). Chcemy dowiedzieć się, czy rozkłady zmiennej ciągłej są
    istotnie różne dla każdej grupy utworzonej przez wartości mające tę samą
    wartość nominalną. Nie wiemy czy dane mają rozkład normalny. Formułujemy
    hipotezę zerową i hipotezę alternatywną:

        H0: dystrybuanty są równe, brak istotnych różnic
        H1: dystrybuanty nie są równe, są istotne różnice

    Jeżeli p-value jest zbyt małe to odrzucamy hipotezę zerową, jeżeli p-value
    jest duże to "nie mamy podstaw do odrzucenia hipotezy zerowej" (de facto
    po prostu przyjmujemy hipotezę zerową). W tabelce wygląda to tak:

                                H0      H1      wniosek
            ----------------------------------------------------------
            p_value < alpha:    nie     tak     rozkłady NIE SĄ takie same
            p_value > alpha:    tak     nie     rozkłady są takie same


    Przykładowo, tego rodzaju test mógłby posłużyć do sprawdzenia, czy wzrost
    pacjenta (w centymerach) ma związek z bycia prawo lub lewo-ręcznym.

    Patrz także
    https://en.wikipedia.org/wiki/Kruskal-Wallis_one-way_analysis_of_variance
    http://www.biostathandbook.com/kruskalwallis.html
    """

    def __init__(self):
        """
        Inicjalizacja testu.
        """
        super().__init__()
        self.name = 'test Kruskala-Wallisa'
        self.h0_thesis = 'dystrybuanty są równe, brak istotnych różnic'
        self.h1_thesis = 'dystrybuanty nie są równe, są istotne różnice'

    @staticmethod
    def can_be_carried_out(a, b=None):
        """
        Sprawdza, czy test może być przeprowadzony na obserwablach a i b.
        Szczególnym przypadkiem może być b=None.

        Dane:
            a -- obiekt klasy Observable
            b -- obiekt klasy Observable lub None

        Zwraca:
            True jeżeli można zastosować test do danych a i b, False jeżeli
            nie można zastosować testu (np. test wymaga zmiennych typu NOMINAL,
            a dane są typu CONTINOUS).
        """
        if a and b:
            if (a.is_nominal() or a.is_ordinal()) and b.is_continous():
                return True
            if (b.is_nominal() or b.is_ordinal()) and a.is_continous():
                return True
        return False

    def __call__(self, a, b=None):
        """
        Przeprowadza test statystyczny na obserwablach a i b.

        Uwaga: zakłada się, że test taki da się wykonać - co sprawdzono
               wcześniej przez can_be_carried_out() - dlatego dane wejściowe
               nie są powtórnie weryfikowane.

        Dane:
            a -- obiekt klasy Observable
            b -- obiekt klasy Observable lub None

        Zwraca:
            p_value    -- wartość p_value
            stat_name  -- nazwę statystyki
            stat_value -- wartość statystyki
        """

        # Jeżeli obserwabla b jest CONTINOUS, czyli obserwabla b jest (powinna
        # być) NOMINAL lub ORDINAL, to zamieniane są a z b. W ten sposób zawsze
        # (od tego miejsca) a jest wyrażone w skali nominalnej (porządkowej),
        # b jest zawsze wyrażone przez wartości ciągłe (liczby rzeczywiste,
        # ciekawe czy także mogą być to liczby zespolone?).
        #
        if a.is_continous():
            a, b = b, a

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


class PearsonCorrelationTest(Test):  # pylint: disable=C0111
    description = """
    Test korelacji r Pearsona.

    Mamy przypadki, które są opisane przy użyciu dwóch zmiennych ciągłych.
    Chcemy dowiedzieć się, czy zmienne te są czy nie są skorelowane .

    Formułujemy hipotezę zerową i hipotezę alternatywną:

        H0: brak korelacji
        H1: istnieje korelacja

    Jeżeli p-value jest zbyt małe to odrzucamy hipotezę zerową, jeżeli p-value
    jest duże to "nie mamy podstaw do odrzucenia hipotezy zerowej" (de facto
    po  prostu przyjmujemy hipotezę zerową). W tabelce wygląda to tak:

                                H0      H1      wniosek
            ----------------------------------------------------------
            p_value < alpha:    nie     tak     istnieje korelacja
            p_value > alpha:    tak     nie     brak korelacji

    Przykładowo, tego rodzaju test mógłby posłużyć do sprawdzenia, czy masa
    ciała pacjenta jest zależna od jego wzrostu.

    W przypadku testu korelacji r problematyczne są: wymóg normalności badanych
    rozkładów; możliwość że zależność jest bardziej skomplikowana niż zależność
    liniowa. Można dość łatwo stworzyć takie zestawy danych, dla których test
    korelacji daje w oczywisty sposób błędne rezultaty.
    """

    def __init__(self):
        """
        Inicjalizacja testu.
        """
        super().__init__()
        self.name = 'test korelacji r Pearsona'
        self.h0_thesis = 'brak korelacji'
        self.h1_thesis = 'istnieje korelacja'

    @staticmethod
    def can_be_carried_out(a, b=None):
        """
        Sprawdza, czy test może być przeprowadzony na obserwablach a i b.
        Szczególnym przypadkiem może być b=None.

        Dane:
            a -- obiekt klasy Observable
            b -- obiekt klasy Observable lub None

        Zwraca:
            True jeżeli można zastosować test do danych a i b, False jeżeli
            nie można zastosować testu (np. test wymaga zmiennych typu NOMINAL,
            a dane są typu CONTINOUS).
        """
        if (a is not None) and (b is not None):
            good_a = a.is_ordinal() or a.is_continous()
            good_b = b.is_ordinal() or b.is_continous()
            if good_a and good_b:
                return True
        return False

    def __call__(self, a, b=None):
        """
        Przeprowadza test statystyczny na obserwablach a i b.

        Uwaga: zakłada się, że test taki da się wykonać - co sprawdzono
               wcześniej przez can_be_carried_out() - dlatego dane wejściowe
               nie są powtórnie weryfikowane.

        Dane:
            a -- obiekt klasy Observable
            b -- obiekt klasy Observable lub None

        Zwraca:
            p_value    -- wartość p_value
            stat_name  -- nazwę statystyki
            stat_value -- wartość statystyki
        """

        x = []
        y = []
        keys = set(a.data.keys()) & set(b.data.keys())
        for k in keys:
            x.append(a[k])
            y.append(b[k])
        r, p_value = stats.pearsonr(x, y)

        return p_value, 'r', r


# Zestaw testów jest tworzony niezależnie od tego jak wywołany będzie ten moduł
#
TESTS_SUITE = (ChiSquareIndependenceTest(),
               KruskalWallisTest(),
               PearsonCorrelationTest())


if __name__ == "__main__":

    # Jeżeli moduł będzie bezpośrednio uruchomiony, to przeprowadzone zostaną
    # testy doctest wbudowane w docstring'i.

    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
