# -*- coding: utf-8 -*-
"""
Program do analizy danych z bazy danych SQLite ProQuest.db.

Wstępne obliczenia różnych rzeczy - wyniki nie są pokazywane - ale zapamietane.

@file: proquest_data.py
@version: 0.3.2.2
@date: 10.07.2018
@author: dr Sławomir Marczyński, slawek@zut.edu.pl
"""


from collections import defaultdict
from proquest_globals import WEEKS_PER_MONTH, WEEKS_PER_YEAR
from proquest_database import query
from proquest_observable import Observable


OBSERVABLES = []


def q(sql):  # pylint: disable=C0103, C0111
    return dict(query(sql))


def o(key, sql, *args, **kwargs):  # pylint: disable=C0103
    "Dopisuje do obserwabli dane uzyskane zapytaniem SQL"
    obs = Observable(key, q(sql), *args, **kwargs)
    OBSERVABLES.append(obs)
    return obs


def d(key, dictionary, *args, **kwargs):  # pylint: disable=C0103
    "Dopisuje do obserwabli dane ze słownika dictionary"
    obs = Observable(key, dictionary, *args, **kwargs)
    OBSERVABLES.append(obs)
    return obs


# Lista pacjentów, tzn. lista identyfikatorów pacjentów.
# Lista pacjentów NIE JEST obserwablą, bo - zakładamy - id pacjenta jest
# przydzielane pacjentowi losowo i dlatego nie jest skorelowane z niczym.
#
PATIENTS = q('SELECT id, id FROM ankieta')


# Bieżący wiek pacjentów
#
CURRENT_AGE = o(
    'wiek pacjenta',
    '''
    SELECT id, wiek_liczba_lat
    FROM ankieta
    WHERE wiek_liczba_lat IS NOT NULL
    ''')


# Wiek pacjentów gdy owi pacjenci zachorowali na nowotwóry prostaty.
#
# Uwaga: poprzednio był odnotowywany albo wiek pacjenta w chwili
#        postawienia diagnozy (jeżeli zachorował na nowotwór prostaty),
#        albo wiek pacjenta gdy "miał on problemy z postatą (jeżeli
#        nie było informacji nt. diagnozy raka prostaty).
#
PROSTATE_CANCER_AGE = o(
    'wiek diagnozy',
    '''
    SELECT id, rak_prostaty_diagnoza_wiek
    FROM ankieta
    WHERE rak_prostaty_diagnoza_wiek IS NOT NULL
    ''')


# Podstawowe parametry: wzrost, masa ciała, wskaźnik BMI

HEIGHT = o(
    'wzrost, cm',
    '''
    SELECT id, wysokość_cm
    FROM ankieta
    WHERE wysokość_cm IS NOT NULL
    ''')


WEIGHT = o(
    'waga, kg',
    '''
    SELECT id, masa_kg
    FROM ankieta
    WHERE masa_kg IS NOT NULL
    ''')


BMI = o(
    'BMI, kg/m**2',
    '''
    SELECT id, masa_kg/wysokość_cm/wysokość_cm * 100 * 100
    FROM ankieta
    WHERE wysokość_cm IS NOT NULL AND masa_kg IS NOT NULL
    ''')


# Poziom stresu według skali Holmesa-Rahe'a
#
STRESS = o(
    'poziom stresu',
    '''
    SELECT ankieta.id,
    SUM (CASE
             WHEN ankieta.id = ankieta_stres.ankieta
                 THEN klucz_stres.level
                 ELSE 0
         END)
    FROM ankieta
    JOIN ankieta_stres
    JOIN klucz_stres ON klucz_stres.id = ankieta_stres.przyczyna
    GROUP BY ankieta.id
    ''')


# Obliczanie różnych aktywności.

#        intervals = dict(query('SELECT id, value FROM klucz_okres_życia'))

SPORT_ACTIVITY_HOURS = [defaultdict(float) for i in range(5)]
SPORT_ACTIVITY_MET = [defaultdict(float) for i in range(5)]
HOME_ACTIVITY_HOURS = defaultdict(float)
HOME_ACTIVITY_MET = defaultdict(float)
HOME_TV_HOURS = defaultdict(float)
HOME_TV_MET = defaultdict(float)
WORK_ACTIVITY_HOURS = defaultdict(float)
WORK_ACTIVITY_MET = defaultdict(float)
TOTAL_ACTIVITY_HOURS = defaultdict(float)
TOTAL_ACTIVITY_MET = defaultdict(float)
TOTAL_ACTIVITY_HOURS_PER_DAY = defaultdict(float)
TOTAL_ACTIVITY_MET_PER_DAY = defaultdict(float)
TOTAL_ACTIVITY_KCAL_PER_DAY = defaultdict(float)
TEE_REE_RATIO = defaultdict(float)

# Możnaby to zorganizować inaczej, ale tym razem po prostu iterujemy obliczenia
# dla każdego pacjenta powtarzając ten sam algorytm. Być może jest tak trochę
# wolniej, ale w praktyce wystarczająco szybko.
#
for p in PATIENTS:

    # Zerowanie liczników prawie wszystkiego. Potem będą doliczane
    # aktualne wartości, ale jeżeli nie - to i tak będzie wpis 0, czyli
    # konkretna wartość dla każdego pacjenta.

    for i in range(5):
        SPORT_ACTIVITY_HOURS[i][p] = 0
        SPORT_ACTIVITY_MET[i][p] = 0
    HOME_ACTIVITY_HOURS[p] = 0
    HOME_ACTIVITY_MET[p] = 0
    HOME_TV_HOURS[p] = 0
    HOME_TV_MET[p] = 0
    WORK_ACTIVITY_HOURS[p] = 0
    WORK_ACTIVITY_MET[p] = 0
    TOTAL_ACTIVITY_HOURS[p] = 0
    TOTAL_ACTIVITY_MET[p] = 0
    TOTAL_ACTIVITY_HOURS_PER_DAY[p] = 0
    TOTAL_ACTIVITY_MET_PER_DAY[p] = 0
    TOTAL_ACTIVITY_KCAL_PER_DAY[p] = 0

    # Wiek pacjenta w chwili postawienia diagnozy
    # albo - gdyby był zdrowy - wiek pacjenta jako taki.
    #
    if p in PROSTATE_CANCER_AGE.data:
        age = PROSTATE_CANCER_AGE[p]
    else:
        age = CURRENT_AGE[p]

    # Jeżeli nadal nie znany jest wiek pacjenta, to jego ankieta
    # nie jest opracowywana dalej.
    #
    if not age:
        continue

    # Korekta, niezbyt dobrze uzasadniona, ale tak ma być.
    #
    age -= 1  # ???

    # spans to liczba lat przypadająca na dany okres indywidualnie
    # dla danego pacjenta p.
    #
    # Uwaga: ankietowani byli w podeszłym wieku, ale teoretycznie
    # nie jest niemożliwe by zapodany był wiek np. 15 lat. Takie
    # przypadki są po prostu odrzucane z dalszych obliczeń.
    #
    if age >= 50:
        spans = [0, 7, 14, 16, (age - 50) + 1]
    elif age >= 34:
        spans = [0, 7, 14, (age - 34) + 1, 0]
    elif age >= 21:
        spans = [0, 7, (age - 21) + 1, 0, 0]
    elif age >= 14:
        spans = [0, (age - 14) + 1, 0, 0, 0]
    else:
        spans = [0, 0, 0, 0]
        continue
    spans[0] = sum(spans)

    data = query('''
                 SELECT
                     MET,
                     okres,
                     liczba_lat,
                     liczba_miesięcy_w_roku,
                     liczba_godzin_w_tygodniu,
                     natężenie_wysiłku_sportowego
                 FROM ankieta_sport
                 INNER JOIN klucz_sport ON klucz_sport.id = dyscyplina
                 WHERE ankieta =
                 ''' + str(p))

    for met, interval, years, months, hours, intensity in data:

        # Jeżeli nie jest podana intensywność, to zakładamy że była ona
        # na średnim poziomie, czyli równa 2.
        #
        if intensity is None:
            intensity = 2

        # Sprawdzanie czy wszystkie konieczne do dalszych obliczeń dane
        # są tu i teraz dostępne. Oraz sprawdzanie czy okres życia jest
        # - tak jak powinien być - liczbą od 1 do 4 włącznie.
        #
        if (met and interval and years and months and hours
                and intensity and age and 1 <= interval <= 4):

            # Ograniczenie MET jeżeli uprawianie sportu
            # nie przebiegało z odpowiednio wysoką intensywnością.
            #
            if (intensity == 1) and (met > 3):
                met = 3
            if (intensity == 2) and (met > 6):
                met = 6

            # Po sprawdzeniu czy w ogóle pacjent żył w danym
            # zakresie lat: wliczanie aktywności tak do ogólnej
            # sumy (indeks 0), jak i do sum dla poszczególnych
            # okresów życia.
            #
            if spans[interval] > 0:
                activity = years * months * WEEKS_PER_MONTH * hours / WEEKS_PER_YEAR
                SPORT_ACTIVITY_HOURS[0][p] += activity / spans[0]
                SPORT_ACTIVITY_MET[0][p] += met * activity / spans[0]
                SPORT_ACTIVITY_HOURS[interval][p] += activity / spans[interval]
                SPORT_ACTIVITY_MET[interval][p] += met * activity / spans[interval]

    # Obliczanie aktywności "domowej" - różne czynności dnia codziennego.
    #
    # Czynności >= 13 nie są traktowane jako wysiłek, bo to np. oglądanie TV
    # @todo - można to chyba zrobić nieco ładniej...

    data = query('''
                 SELECT
                     MET,
                     liczba_lat,
                     liczba_miesięcy_w_roku,
                     liczba_dni_w_tygodniu,
                     czas_w_ciągu_dnia
                 FROM ankieta_czynności
                 INNER JOIN klucz_czynność
                     ON klucz_czynność.id = ankieta_czynności.czynność
                 WHERE czynność < 13 AND ankieta =
                 ''' + str(p))

    for met, years, months, days, hours in data:
        if met and years and months and days and hours:

            # Sprawdzanie czy ankieta była poprawnie wypełniona: jeżeli
            # liczba godzin jest 10 lub więcej, to nie jest to liczba
            # godzin dziennie - tylko cokolwiek innego, np. liczba
            # minut, albo liczba godzin tygodniowo - po prostu doba ma
            # 24 godziny i nie jest możliwe aby robić w tym czasie coś
            # przez 30 godzin bez przerwy.
            #
            if hours < 10:
                activity = years * months * WEEKS_PER_MONTH * days * hours / WEEKS_PER_YEAR / age
                HOME_ACTIVITY_HOURS[p] += activity
                HOME_ACTIVITY_MET[p] += met * activity

    # Aktywności "kanapowe" - oglądanie TV, spotkania z rodziną...
    #
    # Czynności >= 13 to np. oglądanie TV i są zliczane osobno.

    data = query('''
                 SELECT
                     MET,
                     liczba_lat,
                     liczba_miesięcy_w_roku,
                     liczba_dni_w_tygodniu,
                     czas_w_ciągu_dnia
                 FROM ankieta_czynności
                 INNER JOIN klucz_czynność
                     ON klucz_czynność.id = ankieta_czynności.czynność
                 WHERE czynność > 13 AND ankieta =
                 ''' + str(p))

    for met, years, months, days, hours in data:
        if met and years and months and days and hours:

            # Sprawdzanie czy ankieta była poprawnie wypełniona: jeżeli
            # liczba godzin jest 10 lub więcej, to nie jest to liczba
            # godzin dziennie - tylko cokolwiek innego, np. liczba
            # minut, albo liczba godzin tygodniowo - po prostu doba ma
            # 24 godziny i nie jest możliwe aby robić w tym czasie coś
            # przez 30 godzin bez przerwy.
            #
            if hours < 10:
                activity = years * months * WEEKS_PER_MONTH * days * hours / WEEKS_PER_YEAR / age
                HOME_TV_HOURS[p] += activity
                HOME_TV_MET[p] += met * activity

    # Obliczanie aktywności związanej z pracą.

    data = query('''
                 SELECT
                     MET,
                     liczba_lat,
                     liczba_miesięcy_w_roku,
                     liczba_dni_pracy_w_miesiącu,
                     czas_w_ciągu_dnia_godziny,
                     czas_w_ciągu_dnia_minuty,
                     czas_pracy_wykonywanej_siedząc,
                     czas_pracy_wykonywanej_stojąc,
                     czas_pracy_wykonywanej_chodząc,
                     natężenie_wysiłku_fizycznego
                 FROM ankieta_praca
                 INNER JOIN klucz_praca
                     ON klucz_praca.id = ankieta_praca.praca
                 WHERE ankieta =
                 ''' + str(p))

    for (met, years, months, days, hours, minutes,
         sitting, walking, standing, intensity) in data:

        # Uzupełnianie danych - niektóre niewypełnione pola mogą być
        # traktowane jako z wpisanymi wartościami zero.

        if not hours:
            hours = 0
        if not minutes:
            minutes = 0

        if met and years and months and days and (hours or minutes):

            # MET ograniczone przy małym wysiłku
            #
            if ((intensity == 1) or (intensity == 2)) and (met > 3):
                met = 3

            # MET ograniczone przy umiarkowanym wysiłku
            #
            if (intensity == 3) and (met > 6):
                met = 6

            activity = years * months * days * (hours + minutes/60) / 52 / age
            WORK_ACTIVITY_HOURS[p] += activity
            WORK_ACTIVITY_MET[p] += met * activity

    # Obliczanie łącznej aktywności ankietowanych. Bez TV.
    # Może się udać lub nie - jak się nie uda, to aktywność będzie 0

    try:
        total_hours = SPORT_ACTIVITY_HOURS[0][p] + HOME_ACTIVITY_HOURS[p] + WORK_ACTIVITY_HOURS[p]
        total_met = SPORT_ACTIVITY_MET[0][p] + HOME_ACTIVITY_MET[p] + WORK_ACTIVITY_MET[p]

        # Jeżeli pacjent wypełnił ankietę tak, że wychodzi więcej niż 24 godziny na dobę,
        # to taka ankieta jest odrzucana, tj. obliczenia są kontynuowane dla kolejnych pacjentów.
        # BTW, można byłoby wykorzystać informacje o czasie przeznaczanym na sen
        #
        if total_hours < 7 * 24:

            TOTAL_ACTIVITY_HOURS[p] = total_hours
            TOTAL_ACTIVITY_MET[p] = total_met

            # REE (Rest Energy Expenditure) danego pacjenta obliczone dla NIEAKTYWNOŚCI pacjenta,
            # a czas trwania tej ostatniej obliczamy jako 24 minus suma dziennej aktywności
            # wyrażoną w godzinach
            #
            # TEE danego pacjenta obliczone z sumy aktywności - wszystkich możliwych
            #
            # 1.1 jest magicznym współczynnikiem - sprawdzić skąd się bierze

            ree = (24 - 1 * total_hours / 7) * WEIGHT[p]  # Rest Energy Expenditure na dobę
            ref_ree = 24 * WEIGHT[p]  # Rest Energy Expenditure na dobę - przy 100% lenistwie i nic-nie-robieniu
            act = (SPORT_ACTIVITY_MET[0][p] + HOME_ACTIVITY_MET[p] + WORK_ACTIVITY_MET[p]) * WEIGHT[p] / 7
            tee = ree + 1.1 * act
            ratio = tee / ref_ree
            TOTAL_ACTIVITY_HOURS_PER_DAY[p] = total_hours / 7
            TOTAL_ACTIVITY_MET_PER_DAY[p] = total_met / 7
            TOTAL_ACTIVITY_KCAL_PER_DAY[p] = tee
            TEE_REE_RATIO[p] = ratio   # problem jeżeli ree == 0, ale wcześniej sprawdziliśmy że pacjent nie jest aktywny 24/24
    except Exception:  # pylint: disable=W0703
        pass

# Skoro mamy policzone to co mamy policzone, to czas na dodanie tego do listy
# wszystkich znanych obserwabli. Pomijamy total_activity_hours_per_day oraz
# TOTAL_ACTIVITY_MET_PER_DAY, bo nie wnoszą one nic, czego już nie wiemy.

d('aktywność sportowa, godziny tygodniowo', SPORT_ACTIVITY_HOURS[0])
d('aktywność sportowa A, godziny tygodniowo', SPORT_ACTIVITY_HOURS[1])
d('aktywność sportowa B, godziny tygodniowo', SPORT_ACTIVITY_HOURS[2])
d('aktywność sportowa C, godziny tygodniowo', SPORT_ACTIVITY_HOURS[3])
d('aktywność sportowa D, godziny tygodniowo', SPORT_ACTIVITY_HOURS[4])
d('aktywność sportowa, MET tygodniowo', SPORT_ACTIVITY_MET[0])
d('aktywność sportowa A, MET tygodniowo', SPORT_ACTIVITY_MET[1])
d('aktywność sportowa B, MET tygodniowo', SPORT_ACTIVITY_MET[2])
d('aktywność sportowa C, MET tygodniowo', SPORT_ACTIVITY_MET[3])
d('aktywność sportowa D, MET tygodniowo', SPORT_ACTIVITY_MET[4])
d('aktywność domowa, godziny tygodniowo', HOME_ACTIVITY_HOURS)
d('aktywność domowa, MET tygodniowo', HOME_ACTIVITY_MET)
d('aktywność TV, godziny tygodniowo', HOME_TV_HOURS)
d('aktywność TV, MET tygodniowo', HOME_TV_MET)
d('aktywność w pracy, godziny tygodniowo', WORK_ACTIVITY_HOURS)
d('aktywność w pracy, MET tygodniowo', WORK_ACTIVITY_MET)
d('aktywność całkowita, godziny tygodniowo', TOTAL_ACTIVITY_HOURS)
d('aktywność całkowita, MET tygodniowo', TOTAL_ACTIVITY_MET)
d('aktywność całkowita, kcal dziennie', TOTAL_ACTIVITY_KCAL_PER_DAY)
d('TEE/REE', TEE_REE_RATIO)

# Dopisywanie wartości z II tury.

o('miejsce zamieszkania',
  '''
  SELECT ankieta.id, klucz_miejsce_zamieszkania.value
  FROM ankieta
  INNER JOIN klucz_miejsce_zamieszkania
      ON klucz_miejsce_zamieszkania.id = miejsce_zamieszkania
  WHERE miejsce_zamieszkania IS NOT NULL
  ''')

o('wykształcenie',
  '''
  SELECT ankieta.id, klucz_wykształcenie.value
  FROM ankieta
  INNER JOIN klucz_wykształcenie ON  klucz_wykształcenie.id = wykształcenie
  WHERE wykształcenie IS NOT NULL
  ''')

o('stan cywilny',
  '''
  SELECT ankieta.id, klucz_stan_cywilny.value
  FROM ankieta
  INNER JOIN klucz_stan_cywilny ON  klucz_stan_cywilny.id = stan_cywilny
  WHERE stan_cywilny IS NOT NULL
  ''')

o('liczba dzieci', 'SELECT id, COALESCE(liczba_dzieci, 0) FROM ankieta')

o('sytuacja materialna dawniej',
  '''
  SELECT ankieta.id, klucz_sytuacja_materialna.value
  FROM ankieta
  INNER JOIN klucz_sytuacja_materialna
      ON klucz_sytuacja_materialna.id = sytuacja_materialna_dawniej
  WHERE sytuacja_materialna_dawniej IS NOT NULL
  ''')

o('sytuacja materialna obecnie',
  '''
  SELECT ankieta.id, klucz_sytuacja_materialna.value
  FROM ankieta
  INNER JOIN klucz_sytuacja_materialna
      ON klucz_sytuacja_materialna.id = sytuacja_materialna_teraz
  WHERE sytuacja_materialna_teraz IS NOT NULL
  ''')

o('regularne badania prostaty',
  '''
  SELECT id,
  CASE WHEN prostata_regularne_badania_tak THEN 'tak' ELSE 'nie' END
  FROM ankieta
  ''')

o('aktywność seksualna',
  '''
  SELECT id,
  CASE WHEN aktywność_seksualna_tak THEN 'tak' ELSE 'nie' END
  FROM ankieta
  ''')

OBS_STRESS = o('stres - liczba stresorów',
               '''
               SELECT ankieta.id,
               SUM (CASE WHEN ankieta.id = ankieta_stres.ankieta
                         THEN 1 ELSE 0 END)
               FROM ankieta
               JOIN ankieta_stres
               GROUP BY ankieta.id
               ''')

o('stres - tak/nie',
  '''
  SELECT ankieta.id,
  CASE
      WHEN SUM (CASE WHEN ankieta.id = ankieta_stres.ankieta THEN 1 ELSE 0 END) > 0
          THEN 'tak' ELSE 'nie'
      END
        FROM ankieta
        JOIN ankieta_stres
        GROUP BY ankieta.id
  ''', parent=OBS_STRESS)

OBS_SLEEP = o('sen',
              '''
              SELECT DISTINCT ankieta.id, klucz_sen.value
              FROM ankieta
              INNER JOIN klucz_sen ON  sen = klucz_sen.id
              WHERE sen IS NOT NULL
              ''')

o('sen - mniej/więcej niż 7 godzin',
  '''
  SELECT id,
  CASE WHEN sen <= 2 THEN 'mniej niż 7 godzin' ELSE 'więcej niż 7 godzin' END
  FROM ankieta
  WHERE sen IS NOT NULL
  ''', parent=OBS_SLEEP)

o('kontrola diety',
  '''
  SELECT id, CASE WHEN kontrola_diety_tak THEN 'tak' ELSE 'nie' END
  FROM ankieta
  ''')

OBS_SUP = o(
    'suplementy diety',
    '''
    SELECT id,
    CASE
        WHEN suplement_multiwitamina THEN 'multiwitamina'
        WHEN suplement_selen THEN 'selen'
        WHEN suplement_wapno THEN 'wapno'
        WHEN suplement_witamina_C THEN 'witamina C'
        WHEN suplement_witamina_E THEN 'witamina E'
        WHEN suplement_żelazo THEN 'żelazo'
        ELSE 'nie'
        END
  FROM ankieta
  ''')

o('suplementy diety - tak/nie',
  '''
  SELECT id,
  CASE
      WHEN suplement_multiwitamina THEN 'tak'
      WHEN suplement_selen THEN 'tak'
      WHEN suplement_wapno THEN 'tak'
      WHEN suplement_witamina_C THEN 'tak'
      WHEN suplement_witamina_E THEN 'tak'
      WHEN suplement_żelazo THEN 'tak'
      ELSE 'nie'
  END
  FROM ankieta
  ''', parent=OBS_SUP)

OBS_SMOKE = o('palenie (także bierne)',
              '''
              SELECT id,
                  CASE WHEN papierosy=1 AND papierosy_partnerka=1
                       THEN 'nie' ELSE 'tak' END
              FROM ankieta
              WHERE papierosy IS NOT NULL OR papierosy_partnerka IS NOT NULL
              ''')

o('palenie czynne',
  '''
  SELECT ankieta.id, klucz_papierosy.value
  FROM ankieta
  INNER JOIN klucz_papierosy ON klucz_papierosy.id = papierosy
  WHERE papierosy <= 3 AND papierosy IS NOT NULL
  ''', parent=OBS_SMOKE)

o('palenie bierne',
  '''
  SELECT ankieta.id, klucz_papierosy_partnerka.value
  FROM ankieta
  INNER JOIN klucz_papierosy_partnerka
      ON klucz_papierosy_partnerka.id = papierosy_partnerka
  WHERE papierosy_partnerka <= 3 AND papierosy_partnerka IS NOT NULL
  ''', parent=OBS_SMOKE)

OBS_ALCO = o('picie alkoholu',
             '''
             SELECT ankieta.id, klucz_alkohol.value
             FROM ankieta
             INNER JOIN klucz_alkohol ON klucz_alkohol.id = ankieta.alkohol
             WHERE alkohol IS NOT NULL
             ''')

o('alkohol - co najmniej raz w tygodniu',
  '''
  SELECT id, CASE WHEN alkohol >= 4 THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE alkohol IS NOT NULL
  ''', parent=OBS_ALCO)

OBS_MILK = o('picie mleka',
             '''
             SELECT ankieta.id, klucz_mleko.value
             FROM ankieta
             INNER JOIN klucz_mleko ON klucz_mleko.id = ankieta.mleko
             WHERE mleko IS NOT NULL
             ''')

o('mleko - co najmniej 3 razy w tygodniu',
  '''
  SELECT id, CASE WHEN mleko >= 3 THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE mleko IS NOT NULL
  ''', parent=OBS_MILK)

OBS_JUICE = o('picie soku',
              '''
              SELECT ankieta.id, klucz_sok.value
              FROM ankieta
              INNER JOIN klucz_sok ON klucz_sok.id = ankieta.sok
              WHERE sok IS NOT NULL
              ''')

o('sok - co najmniej 3 razy w tygodniu',
  '''
  SELECT id, CASE WHEN sok >= 3 THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sok IS NOT NULL
  ''', parent=OBS_JUICE)

o('samoocena aktywności fizycznej',
  '''
  SELECT ankieta.id, klucz_aktywność_fizyczna.value
  FROM ankieta
  INNER JOIN klucz_aktywność_fizyczna
      ON aktywność_fizyczna = klucz_aktywność_fizyczna.id
  WHERE aktywność_fizyczna IS NOT NULL
  ''')

o('sport, motywacja - poprawa sylwetki oraz kondycji fizycznej',
  '''
  SELECT id,
      CASE WHEN sport_dla_sylwetki_i_kondycji THEN 'tak' ELSE 'nie' END
      FROM ankieta
      WHERE sport_dla_sylwetki_i_kondycji IS NOT NULL
  ''')

o('sport, motywacja - zwiększenie energii i wzmacnianie siły mięśni',
  '''
  SELECT id,
  CASE WHEN sport_dla_energii_i_siły THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_dla_energii_i_siły IS NOT NULL
  ''')

o('sport, motywacja - stracenie zbędnych kilogramów',
  '''
  SELECT id,
  CASE WHEN sport_dla_masy_ciała THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_dla_masy_ciała IS NOT NULL
  ''')

o('sport, motywacja - poprawa stanu zdrowia',
  '''
  SELECT id,
  CASE WHEN sport_dla_stanu_zdrowia THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_dla_stanu_zdrowia IS NOT NULL
  ''')

o('sport, motywacja - przyjemność i poprawa samopoczucia',
  '''
  SELECT id,
  CASE WHEN sport_dla_przyjemności THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_dla_przyjemności IS NOT NULL
  ''')

o('sport, motywacja - okazja do spotkań ze znajomymi',
  '''
  SELECT id,
  CASE WHEN sport_dla_spotkań THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_dla_spotkań IS NOT NULL
  ''')

o('sport, motywacja - inne powody',
  '''
  SELECT id,
  CASE WHEN sport_dla_inne THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_dla_inne IS NOT NULL
  ''')

o('sport, demotywacja - brak czasu',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_czas THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_czas IS NOT NULL
  ''')

o('sport, demotywacja - nadmiar obowiązków domowych',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_obowiązki_domowe THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_obowiązki_domowe IS NOT NULL
  ''')

o('sport, demotywacja - zmęczenie po pracy',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_zmęczenie_pracą THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_zmęczenie_pracą IS NOT NULL
  ''')

o('sport, demotywacja - brak chęci do ćwiczen',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_brak_chęci THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_brak_chęci IS NOT NULL
  ''')

o('sport, demotywacja - zły stan zdrowia',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_brak_zdrowia THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_brak_zdrowia IS NOT NULL
  ''')

o('sport, demotywacja - ciekawsze zainteresowania niż sport',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_inne_zainteresowania THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_inne_zainteresowania IS NOT NULL
  ''')

o('sport, demotywacja - zbyt wysoki koszt',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_duży_koszt THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_duży_koszt IS NOT NULL
  ''')

o('sport, demotywacja - brak umiejętności wykonywania ćwiczeń',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_brak_ćwiczeń THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_brak_ćwiczeń IS NOT NULL
  ''')

o('sport, demotywacja - brak w pobliżu klubu sportowego',
  '''
  SELECT id,
  CASE WHEN sport_nie_bo_brak_klubu THEN 'tak' ELSE 'nie' END
  FROM ankieta
  WHERE sport_nie_bo_brak_klubu IS NOT NULL
  ''')

OBS_CANCER = o('rak prostaty u ojca i/lub brata',
               '''
               SELECT ankieta.id,
               CASE WHEN rak_prostaty_brat_tak OR rak_prostaty_ojciec_tak
                    THEN 'tak' ELSE 'nie' END
               FROM ankieta
               ''')

o('rak prostaty u ojca',
  '''
  SELECT ankieta.id,
  CASE WHEN rak_prostaty_ojciec_tak THEN 'tak' ELSE 'nie' END
  FROM ankieta
  ''', parent=OBS_CANCER)

o('rak prostaty u ojca i/lub brata',
  '''
  SELECT ankieta.id,
  CASE WHEN rak_prostaty_brat_tak THEN 'tak' ELSE 'nie' END
  FROM ankieta
  ''', parent=OBS_CANCER)

o('inne choroby nowotworowe w rodzinie',
  '''
  SELECT ankieta.id,
  CASE WHEN inna_choroba_nowotworowa_w_rodzinie
       OR   inna_choroba_nowotworowa_ojciec
       OR   inna_choroba_nowotworowa_brat
       OR   inna_choroba_nowotworowa_dzieci
       OR   inna_choroba_nowotworowa_matka
       OR   inna_choroba_nowotworowa_siostra
       THEN 'tak' ELSE 'nie'
  END
  FROM ankieta
  ''')

o('choroby nowotworowe w rodzinie',
  '''
  SELECT ankieta.id,
  CASE WHEN inna_choroba_nowotworowa_w_rodzinie
      OR   inna_choroba_nowotworowa_ojciec
      OR   inna_choroba_nowotworowa_brat
      OR   inna_choroba_nowotworowa_dzieci
      OR   inna_choroba_nowotworowa_matka
      OR   inna_choroba_nowotworowa_siostra
      OR   rak_prostaty_brat_tak OR rak_prostaty_ojciec_tak
      THEN 'tak' ELSE 'nie'
  END
  FROM ankieta
  ''')

FOODS = q('SELECT id, value FROM klucz_żywienie_pokarm')
for k in FOODS:
    o('pokarm - ' + FOODS[k],
      '''
      SELECT ankieta_żywienie.ankieta, klucz_żywienie_częstość.value
      FROM ankieta_żywienie
      INNER JOIN klucz_żywienie_częstość
          ON klucz_żywienie_częstość.id = ankieta_żywienie.częstość
      WHERE ankieta_żywienie.częstość < 7 AND ankieta_żywienie.pokarm =
      ''' + str(k))

o('lata pracy zawodowej',
  'SELECT ankieta, SUM(liczba_lat) FROM ankieta_praca GROUP BY ankieta')

o('depresja',
  '''
  SELECT ankieta,
  CASE WHEN przyczyna = 9 THEN "depresja" ELSE "brak depresji" END
  FROM ankieta_stres
  ''')
