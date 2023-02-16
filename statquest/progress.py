#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tkinter GUI for StatQuest.

File:
    project: StatQuest
    name: statquest_gui.py
    version: 0.4.1.0
    date: 07.02.2023

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

import tkinter.ttk as ttk

class Progress:
    """Facade for tkinter.ttk.Progressbar."""

    def __init__(self, parent_frame):
        """
        Przekazuje obiekt progress do obiektu klasy Progress.

        Args:
            progress (tkinter.tkk.Progress): obiekt toolkitu tkinter który ma
            się kryć za fasadą klasy Progress.
        """
        self.progress = ttk.Progressbar(parent_frame)

    def set(self, x):
        """
        Ustawia wartość pokazywaną przez progress bar.

        Args:
            x: wartość jaka powinna być ustawiona
        """
        self.progress['value'] = x

    def step(self, delta=1):
        """
        Zwiększa postęp pokazywany przez progress o zadany krok.

        Args:
            delta: wartość o jaką powinien powiększyć się progress.
        """
        self.progress['value'] += delta
        self.progress.update()

    def range(self, maximal_value):
        """
        Ustawia zakres dla progress-u.

        Args:
            maximal_value: ustala maksymalną wartość jaką ma pokazywać
                progress.
        """
        self.progress['maximum'] = maximal_value
