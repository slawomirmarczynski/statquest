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

