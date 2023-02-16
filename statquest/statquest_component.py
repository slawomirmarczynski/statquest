#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The definition of Component class.

File:
    project: StatQuest
    name: statquest_component.py
    version: 0.5.0.0
    date: 16.02.2023

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

from tkinter import ttk


class Component:
    """
    The base class for creating program components.
    """

    def __init__(self, parent_component, parent_frame=None, border=True):
        """
        A program component is an object that can have a window/widget
        embedded in the parent window/widget. However, it is not an element
        in itself GUI interface. And there is no need for such an object to
        have a  window/widget GUI, because it might as well not have.

        Args:
            parent_component: any object, not necessarily a component itself
                (you can embed components inside objects of any class);
                theoretically, it can even be None, but it's hard to say
                what it would be used for.
            parent_frame: any tkinter widget or None.
            border (bool): if True (default) and if there is a frame then
                the frame has a drawn border.
        """
        self._parent_component = parent_component
        self._parent_frame = parent_frame
        self._observers = []
        self._frame = None
        if parent_frame:
            self._frame = ttk.Frame(parent_frame)
            if border:
                self._frame.configure(relief='solid', borderwidth=5)
            self._frame.pack(side='top', fill='x', expand=True)
            self._frame.pack_configure(padx=10, pady=10)

    def update(self, observed):
        """The default call handling as an observer/listener."""
        pass

    def add_listener(self, observer):
        """
        Observer pattern - adding an observer to the list of recipients of
        subscribed information.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_listener(self, observer):
        """
        Observer pattern - removing an observer from the list of recipients
        of subscribed information.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def callback(self, *args):
        """
        Observer pattern - broadcast to recipients of subscribed information.
        """
        if self._observers:
            for observer in self._observers:
                observer.update(self)
