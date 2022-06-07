# -*- coding: utf-8 -*-
"""
Program do analizy danych z bazy danych SQLite ProQuest.db.

Moduł komunikujący się z bazą SQL - wszystkie zapytania do bazy przechodzą
przez ten moduł - nic (?) nie jest robione "za plecami" tego modułu.

@file: proquest_database.py
@version: 0.3.2.2
@date: 10.07.2018
@author: dr Sławomir Marczyński, slawek@zut.edu.pl
"""


import sqlite3
from proquest_globals import DATA_BASE_NAME


def query(sql):
    """
    Fasada do obsługi bazy danych, dostarcza ekstremalnie prostego mechanizmu
    odpytywania bazy SQL-owej. Zadaje pytanie SQL bazie danych. Ponieważ jest
    to wystarczająco wydajne, to każde zapytanie tworzy na nowo połączenie
    z bazą danych. Dzięki temu dostęp nie jest blokowany.

    Sposób działania może nie być odpowiedni gdy danych będzie zbyt dużo
    i nie będą się one już mieścić w pamięci RAM. Ale przy kilkuset rekordach
    sprawdza się dostatecznie dobrze.

    Dane:
        sql -- zapytanie w SQL jako łańcuch znaków,
               na przykład 'SELECT COUNT(*) FORM ankieta'

    Stałe globalne:
        DATA_BASE_NAME -- nazwa bazy danych.

    Zwraca:
        krotkę krotek z kolejnymi wierszami tablicy.
    """
    with sqlite3.connect(DATA_BASE_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
