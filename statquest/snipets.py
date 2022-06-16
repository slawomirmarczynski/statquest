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


