# @todo check if this code is really needed
#
# @staticmethod
# def print_freq(observables, sep='\t', file=None):
#
#     N_LIMIT = 30
#
#     for obs in observables:
#         nominal = obs.is_nominal()
#         ordinal = obs.is_ordinal() and len(obs.freq()) <= N_LIMIT
#         if nominal or ordinal:
#             print(obs, file=file)
#             freq = obs.freq()
#             for k in sorted(freq.keys()):
#                 print('', k, freq[k], sep=sep, file=file)
#             print('', 'razem:', sum(freq.values()), sep=sep, file=file)
#             print(file=file)



# @todo Na razie nie jest do niczego używane.
#
import itertools


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





observables_relations = {}
sorted(itertools.chain.from_iterable(observables_relations.values()),
       key=lambda)

                 def test_print_descriptive_statistics_1(self):
"""Write to file"""
file = Mock()
Observable.print_descriptive_statistics((
    self.observable_ordinal,
    self.observable_continuous,
    self.observable_nominal), file=file)
self.assertTrue(len(file.method_calls) > 0)


def test_print_descriptive_statistics_2(self):
    """Write to file"""
    obs = Observable('obs', {1: 1.00, 2: 0.99, 3: 1.01, 4: 1.03, 5: 1.05})
    file = Mock()
    Observable.print_descriptive_statistics((obs,), file=file)
    self.assertTrue(len(file.method_calls) > 0)


def test_print_descriptive_statistics_3(self):
    """Write to file"""
    obs = Observable('empty observable', {})
    file = Mock()
    Observable.print_descriptive_statistics((obs,), file=file)
    self.assertTrue(len(file.method_calls) == 0)


    # usunięte z class Relation, bo niepotrzebne
    #
    # def __str__(self, sep='\t'):
    #     """
    #     Cast to string.
    #
    #     Args:
    #         sep (str): a separator, default '\t'.
    #
    #     Returns:
    #         str: readable string describing the relation.
    #     """
    #     return sep.join(map(
    #         str,
    #         (self.observable1, self.observable2, self.test.name,
    #          self.p_value, self.stat_name, self.stat_value)))

#=------
relations = sorted(relations, key=lambda relation: relation.p_value)

# relations_list = sorted(
#     itertools.chain.from_iterable(relations.values()),
#     key=lambda relation: relation.p_value )




def print_to_file(description, file_name, writer, iterable, **kwargs):
    print(description, _('są zapisywane do pliku'), file_name)
    with open(file_name, 'wt', encoding='utf-8') as file:
        writer(iterable, file=file, **kwargs)


CSV_SEPARATOR = ';'

# Stałe: średnia ilość tygodni na miesiąc, liczba tygodni rocznie.
#
WEEKS_PER_MONTH = 4.33
WEEKS_PER_YEAR = 52



# def setup_locale_main():
#     locale.setlocale(locale.LC_ALL, '')
#     lang, _encoding = locale.getdefaultlocale()
#     translation = gettext.translation(('statquest',),
#                                       localedir='locale',
#                                       languages=[lang],
#                                       fallback=True)
#     translation.install('statquest')
#     return translation.gettext
