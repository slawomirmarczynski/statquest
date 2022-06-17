#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The support for l10n/i18n.

File:
    project: StatQuest
    name: statquest_locale.py
    version: 0.4.0.0
    date: 08.06.2022

Authors:
    Sławomir Marczyński, slawek@zut.edu.pl
"""

import gettext
import locale


def setup_locale():
    locale.setlocale(locale.LC_ALL, '')
    lang, _encoding = locale.getdefaultlocale()
    translation = gettext.translation('statquest',
                                      languages=[lang],
                                      fallback=True)
    return translation.gettext


# def setup_locale_main():
#     locale.setlocale(locale.LC_ALL, '')
#     lang, _encoding = locale.getdefaultlocale()
#     translation = gettext.translation(('statquest',),
#                                       localedir='locale',
#                                       languages=[lang],
#                                       fallback=True)
#     translation.install('statquest')
#     return translation.gettext
