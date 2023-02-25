#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A facade for tkinter.ttk.Progressbar.

File:
    project: StatQuest
    name: progress.py
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

import tkinter.ttk as ttk


class Progress:
    """Facade for tkinter.ttk.Progressbar."""

    def __init__(self, parent_frame):
        """
        Creates an facade object (proxy) for the tkinter.ttk progress bar.

        Args:
            parent_frame (tkinter.tkk.Frame): the host for the progress bar.
        """
        self.progress = ttk.Progressbar(parent_frame)

    def set(self, x):
        """
        Set the current value displayed by progress bar.

        Args:
            x (float): value to set.
        """
        self.progress.stop()
        self.progress['mode'] = 'determinate'
        self.progress['value'] = x

    def step(self, delta=1):
        """
        Increases the progress shown by the progress bar.

        Args:
            delta (float): increment by which the displayed value is to be
                increased.
        """
        self.progress['value'] += delta
        self.progress.update()

    def range(self, maximal_value):
        """
        Set up the end of the scale.

        Args:
            maximal_value (float): the end of the scale.
        """
        self.progress.stop()
        self.progress['mode'] = 'determinate'
        self.progress['maximum'] = maximal_value

    def auto(self):
        """
        Turn on automatic indeterminate progress animation.
        """
        self.progress['mode'] = 'indeterminate'
        self.progress['maximum'] = 100
        self.progress.start()

    def stop(self):
        """
        Stop animations, but don't change the mode to determinate.
        """
        self.progress.stop()

    def update(self):
        """
        Force update of the progress bar.
        """
        self.progress.update()
