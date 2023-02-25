#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate test data.

File:
    project: StatQuest
    name: generate_1.py
    version: 0.5.1.1
    date: 25.02.2023

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński
"""
#  Copyright (c) 2023 Sławomir Marczyński. All rights reserved.
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

import csv
from random import random, randint, choice
import string


N = 100
M = 50


def randomword(n):
    """
    Generate random string.

    Args:
        n: the length of the string to generate.

    Returns:
        str: the generated random string, only lowercase letters.
    """
    return ''.join(choice(string.ascii_lowercase) for i in range(n))


ordinal1 = [int(x) for x in range(N)]
continuous1 = [float(x + 0.5) for x in range(N)]
nominal1 = [randomword(5) for x in range(N)]

ordinal2 = [randint(-N, N) for x in range(N)]
continuous2 = [float(-random()) for x in range(N)]
nominal2 = [randomword(5)] * N


with open('../data/test_data_2.csv', 'w') as output_file:
    w = csv.writer(output_file)

    w.writerow([
        'ordinal1', 'continuous1', 'nominal1',
        'ordinal2', 'continuous2', 'nominal2',
    ])
    for i in range(N):
        w.writerow([
            ordinal1[i], continuous1[i], nominal1[i],
            ordinal2[i], continuous2[i], nominal2[i],
        ])
