#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The support for l10n/i18n.

File:
    project: StatQuest
    name: statquest_locale.py
    version: 0.4.0.1
    date: 19.06.2022

Authors:
    Sławomir Marczyński

Copyright (c) 2022 Sławomir Marczyński.
"""

#  Copyright (c) 2022 Sławomir Marczyński. All rights reserved.
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met: 1. Redistributions of source code must retain the above
#  copyright notice, this list of conditions and the following
#  disclaimer. 2. Redistributions in binary form must reproduce the
#  above copyright notice, this list of conditions and the following
#  disclaimer in the documentation and/or other materials provided with
#  the distribution. 3. Neither the name of the copyright holder nor
#  the names of its contributors may be used to endorse or promote
#  products derived from this software without specific prior written
#  permission. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
#  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
#  BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
#  THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#  STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#  OF THE POSSIBILITY OF SUCH DAMAGE.

import gettext
import locale
import os

_setlocale_called = False


def setup_locale_translation_gettext(messages_domain='messages'):
    """
    Setup locale according to the system configuration.

    Notes:
        May change the environment. It is necessary for gettext,
        because gettext get current language from  LANGUAGE,
        LC_MESSAGES, LC_ALL or LAN environmental variables.

    Args:
        messages_domain (str): the name of the messages' domain,
            i.e. a name of the mo-file.

    Returns:
        gettext function to translate strings.
    """

    # Reset all locale settings to the user's default settings.
    #
    global _setlocale_called
    if not _setlocale_called:
        locale.setlocale(locale.LC_ALL, '')
        _setlocale_called = True

    # Set language for default locale. It is a kind of magic on MS Windows
    # because locale.getdefaultlocale() CAN obtain this information without
    # environmental variables (see below).
    #
    lang, encoding = locale.getdefaultlocale()

    # 'LANG' environmental variable is changed only when it is really needed.
    #
    if all(x not in os.environ for x in
           ('LANGUAGE', 'LC_MESSAGES', 'LC_ALL', 'LANG')):
        os.environ['LANG'] = lang

    # Construct and return translation object.
    #
    directory = os.path.dirname(__file__)
    localedir = os.path.join(directory, 'locale')
    translation = gettext.translation(messages_domain, localedir=localedir,
                                      languages=[lang], fallback=True)
    return translation.gettext


def setup_locale_csv_format(locale_code='default'):
    """
    Get settings for reading CSV files.

    Args:
        locale: locale code like 'pl_PL'; 'default' for system-default.

    Returns:
        kwargs dictionary with appropriate settings for pandas.read_csv()
    """
    if locale_code == 'default':
        locale_code, encoding = locale.getdefaultlocale()
    kwargs = {}
    if locale_code is None:
        kwargs = {}
    elif locale_code == 'pl_PL':
        kwargs = {'encoding': 'cp1250', 'sep': ';', 'decimal': ','}
    elif locale_code == 'en_US':
        kwargs = {}
    return kwargs
