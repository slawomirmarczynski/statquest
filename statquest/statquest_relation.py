#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program do analizy danych z bazy danych SQLite ProQuest.db.

Tworzenie, za pomocą testów, relacji pomiędzy obserwablami.

@file: proquest_relations.py
@version: 0.3.2.2
@date: 10.07.2018
@author: dr Sławomir Marczyński, slawek@zut.edu.pl
"""


from proquest_globals import ALPHA_LEVEL


class Relation:
    """
    Klasa Relation reprezentuje wynik testu statystycznego na dwóch różnych
    obserwablach. Przykładowo, mamy dwie obserwable (dwa zbiory danych)
    i test Anova - obiekt Relation będzie zawierał odniesienia do obserwabli,
    testu oraz p_value obliczone dla tego testu i tych danych.
    """

    def __init__(self, observable1, observable2, test):
        """
        Inicjalizator relacji test pomiędzy observable1 i observable2.

        Dane:
            observable1 -- obserwabla, zostanie przekazana do metody test
                           subklasy Test, ma być obiektem klasy Observable;
            observable2 -- obserwabla, zostanie przekazana do metody test
                           subklasy Test, ma być obiektem klasy Observable;
            test        -- test jaki ma być przeprowadzony na obsewablach.
        """

        # Atrybuty _observable1, _observable2 i _test są/mogą być potrzebne np.
        # aby dowiedzieć się jak nazywał się dany test, jak nazwywają się dane,
        # jakiego rodzaju wartości są przez nie reprezentowane itp.
        #
        self.observable1 = observable1
        self.observable2 = observable2
        self.test = test

        # Obliczana jest wartość p_value itp.
        #
        self.p_value, self.name, self.value = test(observable1, observable2)

    def __call__(self, a, b, symetric=True, alpha=ALPHA_LEVEL):
        if self.p_value <= alpha:
            if a == self.observable1 and b == self.observable2:
                return True
            if symetric and b == self.observable1 and a == self.observable2:
                return True
        return False

    def __str__(self):
        """
        Rzutowanie na łańcuch znaków istotnych informacji z obiektu Relation.
        """
        return '\t'.join(map(str, (self.observable1, self.observable2,
                                   self.p_value, self.name, self.value)))

    # Statyczne metody klasy, mające prawo sięgać do składowych chronionych.
    #
    # pylint: disable=W0212

    @staticmethod
    def write_csv(relations, sep='\t', file=None):
        """
        Zapisuje informacje o wszystkich relacjach w formacie CSV (separatorem
        jest '\t') do podanego pliku. Z założenia nazwy relacji nie powinny
        mieć w sobie znaku sep (domyślnie znaku tabulacji).

        Dane:
            relations -- kolekcja relacji, np. lista relacji;
            sep       -- separator, domyślnie znak tabulacji, oddzielający
                         poszczególne pola w pliku CSV;
            file      -- plik, otwarty przez open(), do którego zapisywane są
                         dane.
        """

        fmt = '{:40}\t{:40}\t{:20}\t{:20}\t{:20}\t{:40}'.replace('\t', sep)
        print(fmt.format(
            'dane1', 'dane2', 'test',
            'p_value', 'statystyka', 'wartość', 'teza'),
              file=file)

        for r in relations:
            print(fmt.format(
                r.observable1.name, r.observable2.name,
                r.test.name, r.p_value, r.name, r.value,
                r.test.h0_thesis if r.p_value >= ALPHA_LEVEL
                else r.test.h1_thesis),
                  file=file)

    @staticmethod
    def write_dot(relations, file=None):
        """
        Zapis danych w języku DOT - opisującym zależności jako graf.

            graph {
                    "obs1" -- "obs2"
                    ...
            }

        Dane:
            relations -- relacje do zapisania jako iterable;
            file      -- plik w którym mają być zapisane relacje.

        Uwaga: write_dot zapisuje wszystkie relacje podane jako parametr,
        nie oznacza to jednak że musi być używane do wypisywania nieselektywnie
        wszystkich relacji jakie są w programie. Logika "piętro wyżej" może
        dzielić/segregować relacje według założonych kryteriów i potem używać
        write_dot() do wypisywania tylko określonych relacji, np. takich które
        obejmują z góry wybrane obserwable.
        """
        print('graph {', file=file)
        for r in relations:
            if r.p_value <= ALPHA_LEVEL:
                print('"', r.observable1.name, '"', ' -- ',
                      '"', r.observable2.name, '"', sep='', file=file)
        print('}', file=file)

    @staticmethod
    def create_relations(observables, tests):
        """

        Args:
            observables:
            tests:

        Returns:

        """
        """
        Fabryka relacji. Tworzone są wszystkie możliwe relacje.
        Wszystkie relacje są traktowane jako symetryczne, tzn. gdy zbadana
        jest relacja pomiędzy obserwablami a i b to nie jest badana relacja
        pomiędzy b i a, bo z założenia nie dostarczy to dodatkowych informacji.
        Można to ograniczenie wyłączyć ustawiając symetric=False.

        Dane:
            observables -- kolekcja obiektów Observable,
                           powinny być w niej przynajmniej dwa takie obiekty;
            tests       -- kolekcja obiektów Tests.

        Zwraca:
            listę obiektów Relation, czyli kolekcję relacji jakie można
            utworzyć stosując testy do obserwabli.
        """

        # Poniższy algorytm niepotrzebne używa zbioru ab_tuples_set jeżeli
        # symetric=False, ale: po pierwsze zakładamy że zwykle będzie
        # symetric=True oraz że ewentualne narzuty na czas wykonania nie będą
        # na tyle znaczące, aby się tym przejmować.
        #
        # Sprawdzane są tylko krotki (a, b), ale do zbioru przeanalizowanych
        # już krotek ab_tuples_set dodawane są krotki (a, b) i (b, a). Chyba
        # że symetric=False.

        # We don't need check (a, b) tuple, because uniques (a, b) in trials
        # is granted by for-for loops. We need only check the reverse case,
        # i.e. (b, a) tuple ba_tuples_set.

        relations = []
        ba_tuples_set = set()
        for a in observables:
            for b in observables:
                if b is not a and (b, a) not in ba_tuples_set:
                    ba_tuples_set.add((a, b))
                    for test in tests:
                        if test.can_be_carried_out(a, b):
                            relations.append(Relation(a, b, test))
        return relations

    # pylint: disable=W0212
