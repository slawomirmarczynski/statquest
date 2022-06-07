# -*- coding: utf-8 -*-
"""
Program do analizy danych z bazy danych SQLite ProQuest.db.

Obiekty Obsevable i fabryka obiektów Observable.

@file: proquest_obsevables.py
@version: 0.3.2.2
@date: 10.07.2018
@author: dr Sławomir Marczyński, slawek@zut.edu.pl
"""


from proquest_statistics import descriptive_statistics, frequency_table


class Observable:
    """
    Observable jest klasą przechowującą rozmaitego rodzaju dane odnoszące się
    do identyfikowalnych (w domyśle identyfikowalni to pacjenci, ale być może
    daje sie to uogólnić na cokolwiek).

    Obserwable moga być typu nominalnego, porządkowego albo ciągłego. Przyszłe
    wersje programu mogą wprowadzić jeszcze typ interwałowy. Obserwabla jest
    typu ciągłego jeżeli jej wartości są liczbami zmiennoprzecinkowymi.
    Obserwabla jest typu porządkowego, jeżeli jej wartości są liczbami int.
    Obserwable nominalne są łańcuchami znaków. Obserwable interwałowe parami
    liczb zmiennoprzecinkowych.
    """

    def __init__(self, name, data, parent=None):
        """
        Inicjalizuje obiekt klasy Observable.

        Dane:
            name   -- nazwa obserwabli jako łańcuch znaków, powinna być (jeżeli
                      to możliwe) unikalna, nie powinna być None;
            data   -- słownik lub lista par, albo coś co można przekształcić na
                      słownik;
            parent -- obserwabla "macierzysta" - pozwoli to, podczas testów,
                      na sprawdzenie czy dwie obserwable nie są ze soba
                      powiązane, np. wzrost wyrażony w centymerach mógłby mieć
                      jako obserwablę macierzystą wzrost wyrażony w metrach.
        """
        assert name is not None

        self.name = name
        self.data = dict(data)
        self.parent = parent

    def __getitem__(self, key):
        """
        Zwraca wartość dla podanego klucza key, tym samym obiekt obs klasy
        Observable będzie zachowywał się w "przeźroczysty" sposób - dając od
        razu dostęp do danych, np. obs[119] da dane skojarzone z kluczem 119.

        Dane:
            key -- klucz do słownika data.

        Zwraca:
            odpowiedni element zapisany w data.

        Przykład:

            >>> obs = Observable('example', {1: 'A', 2: 'B'})
            >>> obs[2]
            'B'
        """
        return self.data[key]

    def __len__(self):
        """
        Podaje rozmiar danych trzymanych w obserwabli.

        Przykłady:

            >>> obs = Observable('example', {1: 'A', 2: 'B'})
            >>> len(obs)
            2

            >>> e = Observable('empty observable', dict())
            >>> if not e: print('empty')
            empty
        """
        return len(self.data)

    def __str__(self):
        """
        Podaje nazwę obserwabli.

        Przykład:

            >>> obs = Observable('example', {1: 'A', 2: 'B'})
            >>> print(obs)
            example
        """
        return self.name

    @staticmethod
    def print_freq(observables, sep='\t', file=None):

        N_LIMIT = 30

        for obs in observables:
            nominal = obs.is_nominal()
            ordinal = obs.is_ordinal() and len(obs.freq()) <= N_LIMIT
            if nominal or ordinal:
                print(obs, file=file)
                freq = obs.freq()
                for k in sorted(freq.keys()):
                    print('', k, freq[k], sep=sep, file=file)
                print('', 'razem:', sum(freq.values()), sep=sep, file=file)
                print(file=file)

    @staticmethod
    def print_stat(observables, sep='\t', file=None):

        for obs in observables:
            if obs.is_continous() or obs.is_ordinal():
                keys = obs.stat().keys()
                break

        print('dane', *keys, sep=sep, file=file)
        for obs in observables:
            if obs.is_continous() or obs.is_ordinal():
                print(obs, *obs.stat().values(), sep=sep, file=file)

    def freq(self):
        """
        Zwraca słownik z uporządkowaną tablicą częstości. Za obliczenia jest
        odpowiedzialny moduł proquest_statistics.

        Uwaga: dane powinny być albo nominalne, albo porządkowe - obliczenia
               dla danych ciągłych (zmienoprzecinkowych) są problematyczne.

        Przykład:

            >>> obs = Observable('example', {1: 'A', 2: 'B', 3: 'A'})
            >>> print(obs.freq())
            {'A': 2, 'B': 1}
        """
        assert self.is_ordinal() or self.is_nominal()
        return frequency_table(self.data)

    def is_continous(self, verify=False):
        """
        Sprawdza, czy obserwabla jest continous, czyli czy przedstawia zmienną
        ciągłą. Zakłada się, że obserwabla jest contionous jeżeli jej wartości
        są zapisane jako liczby rzeczywiste.

        Dane:
            verify -- jeżeli jest True, to sprawdzane są wszystkie dane
                      zapisane w obserwabli; jeżeli False to sprawdzany
                      jest tylko pierwsza pozycja w słowniku self.data,
                      co jest znacznie szybsze.

        Zwraca:
            True jeżeli obserwabla jest typu continous, False jeżeli nie.

        Przykłady:

            >>> obs1 = Observable('example', {1: 10.5, 2: 10.2, 3: '11.5'})
            >>> obs1.is_continous()
            True

            >>> obs2 = Observable('example', {1: 'nie', 2: 'tak'})
            >>> obs2.is_continous()
            False

            >>> obs3 = Observable('example', {1: 3.1, 2: 'not float'})
            >>> obs3.is_continous(verify=True)
            False
        """
        return self._check_kind(float, verify)

    def is_nominal(self, verify=False):
        """
        Sprawdza, czy obserwabla jest nominal, czyli czy przedstawia zmienną
        nominalną. Zakłada się, że obserwabla jest nominalną jeżeli jej
        wartości są zapisane jako napisy, tj łańcuchy znaków.

        Dane:
            verify -- jeżeli jest True, to sprawdzane są wszystkie dane
                      zapisane w obserwabli; jeżeli False to sprawdzany
                      jest tylko pierwsza pozycja w słowniku self.data.

        Zwraca:
            True jeżeli obserwabla jest typu nominal, False jeżeli nie.

        Przykłady:

            >>> obs1 = Observable('example', {1: 'A', 2: 'B', 3: 'ABC'})
            >>> obs1.is_nominal()
            True

            >>> obs2 = Observable('example', {1: 3.1, 2: 3.2})
            >>> obs2.is_nominal()
            False

            >>> obs3 = Observable('example', {1: 31, 2: 32})
            >>> obs3.is_nominal()
            False

            >>> obs4 = Observable('example', {1: 'A', 2: 'B', 3: 3.142})
            >>> obs4.is_nominal(verify=True)
            False
        """
        return self._check_kind(str, verify)

    def is_ordinal(self, verify=False):
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
            >>> obs1.is_ordinal()
            True

            >>> obs2 = Observable('example', {1: 3.1, 2: 3.2})
            >>> obs2.is_ordinal()
            False

            >>> obs3 = Observable('example', {1: '1', 2: '2'})
            >>> obs3.is_ordinal()
            False

            >>> obs4 = Observable('example', {1: 1, 2: 2, 3: 'ABC'})
            >>> obs4.is_ordinal(verify=True)
            False
        """
        return self._check_kind(int, verify)

    def is_related(self, observable):
        """
        Sprawdzanie, czy dwie obserwable mają wspólnego przodka, tj. czy są
        spokrewnione.

        Dane:
            observable -- obiekt klasy Observable dla którego jest sprawdzane
                          pokrewieństwo z obiektem self.

        Zwraca:
            true lub false -- jeżeli true to jest wspólny przodek, jeżeli false
                              wspólnego przodka nie ma.

        Przykłady:

            >>> obs1 = Observable('X', {1: 1, 2: 2, 3: 3})
            >>> obs2 = Observable('X', {1: 1, 2: 4, 3: 9}, parent=obs1)
            >>> obs3 = Observable('X', {1: 1, 2: 8, 3: 27}, parent=obs2)
            >>> obs4 = Observable('X', {1: 'A', 2: 'B', 3: 'C'})

            >>> obs1.is_related(obs1)
            True

            >>> obs1.is_related(obs2)
            True

            >>> obs1.is_related(obs3)
            True

            >>> obs1.is_related(obs4)
            False
        """

        def root(element):
            """
            Szukanie korzenia, tj. elementu który był przodkiem (albo przodkiem
            przodkiem itd.), ale który sam nie ma już przodka.
            """
            if element:
                while element.parent:
                    element = element.parent
            return element

        root1 = root(self)
        root2 = root(observable)

        # Jeżeli root1 i root2 są oba None, to root1 == root2, bo None == None.
        # Dlatego sprawdzane jest czy root1 nie jest None. Nie trzeba sprawdzać
        # czy root2 jest None, bo jeżeli root1 nie jest, to nie nigdy nie jest
        # None == None. BTW, priorytet operatorów jest inny w Pytonie niż w C.
        # Sprawdzane jest także, czy przypadkiem nie mamy dwa razy tego samego
        # obiektu Observable - wtedy także wynikiem jest True.
        #
        return root1 is not None and (self == observable or root1 == root2)

    def values_to_indices_dict(self):
        """
        Tworzy słownik odwzorowujący klucz słownika data na liczbę od 0 do n-1,
        gdzie n jest ilością elementów w słowniku data. Odpowiadnie wartości
        kluczy (utworzone ze słownika data) daje metoda values_to_values_list.

        Przykład:

            >>> x = Observable('X', {'C': 'Celina', 'B': 'Basia', 'A': 'Ala'})
            >>> x.values_to_indices_dict()
            {'Ala': 0, 'Basia': 1, 'Celina': 2}
        """
        values_as_keys = self.values_to_values_list()
        return {values_as_keys[i]: i for i in range(len(values_as_keys))}

    def values_to_values_list(self):
        """
        Pozyskuje posortowaną listę wartości opartą na wartościach
        zgromadzonych we słowniku data.

        Zwraca:
            uporządkowaną listę.

        Przykład:

            >>> x = Observable('X', {'C': 'Celina', 'B': 'Basia', 'A': 'Ala'})
            >>> x.values_to_values_list()
            ['Ala', 'Basia', 'Celina']
        """
        return sorted(list(self.freq().keys()))

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
        return list(map(str, self.values_to_values_list()))

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
        return list(map(int, self.values_to_values_list()))

    def stat(self):
        """
        Obliczanie statystyk opisowych. Statystyki są obliczane na nowo przy
        każdym wywołaniu, więc jeżeli zostały zmienione dane, to statystyki
        będą miały i tak poprawne wartości.

        Zwraca:
            słownik, kluczami są nazwy statystyk, wartościami sa wartości
            statystyk.
                if observable.is_ordinal() or observable.is_continous():
        data = list(data.values())

        Przykład:
            >>> obs = Observable('example', {1: 10.5, 2: 10.2, 3: 10.9})
            >>> obs.stat()
            {'średnia': 10.533333333333333, 'mediana': 10.5, ...
        """
        return descriptive_statistics(tuple(self.data.values()))

    def _check_kind(self, T, verify=False):
        """
        Metoda chroniona klasy Observable: implementacja sprawdzania typu
        zmiennych jakie mają wartości słownika self.data.

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
            >>> obs1._check_kind(float)
            True

            >>> obs2 = Observable('example', {1: 10, 2: 11, 3: 12})
            >>> obs2._check_kind(float)
            False

            >>> obs3 = Observable('example', {1: 'A', 2: 'AB', 3: 'ABC'})
            >>> obs3._check_kind(float)
            False
        """
        assert isinstance(self.data, dict)

        if not self.data:
            return False

        if verify:
            for v in self.data.values():
                if not isinstance(v, T):
                    return False
            return True
        return isinstance(self.data[next(iter(self.data))], T)


if __name__ == "__main__":

    # Jeżeli moduł będzie bezpośrednio uruchomiony, to przeprowadzone zostaną
    # testy doctest wbudowane w docstring'i.

    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
