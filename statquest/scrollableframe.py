#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A scrollable frame container for tkinter.

File:
    project: StatQuest
    name: scrollableframe.py
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

import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """
    Enables vertical scrolling of widgets inserted into the scrollable frame.
    """

    def __init__(self, *args, **kwargs):
        """
        Tworzenie subklasy tkinter.ttk.Frame umożliwiającej przewijanie
        pionowe.

        Args:
            *args: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
            **kwargs: takie same jak dla klasy bazowej, tj. tkinter.tk.Frame.
        """
        super().__init__(*args, **kwargs)

        # A Canvas object, unlike a Frame object, can be scrolling. However,
        # it is more convenient to nest objects inside Frame than inside
        # Canvas. That's why Frame (objects) are created inside Canvas
        # inside Frame. This is how it looks from the outside Frame objects,
        # and Canvas (and ScrollBar) objects are hidden in the object
        # ScrollableFrame. Tworzenie pustego canvas, czyli czegoś co można
        # przewijać. Na razie canvas jest puste, bez żadnej zawartości.
        #
        # bd=0 means we don't want a margin around the canvas.
        # highlightthickness=0 means we don't want to show focus.
        #
        canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        canvas.pack(side='left', fill='both', expand=True)

        # Created is a ScrollBar object as a scroll controller.
        #
        sb = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        sb.pack(side='right', fill='y')

        # Create a container (ttk.Frame class object) that user will be able
        # to scroll.
        #
        # The <Configure> event watcher is needed in case had to redefine
        # the scroll range. for he is set at the canvas level and needs to
        # be refreshed in this situation.
        #
        self._scrollable_frame = ttk.Frame(canvas)
        self._scrollable_frame.bind(
            '<Configure>',
            lambda event: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        # Adding content - another widget - to the canvas is done method
        # create_window. The name may be associated with some factory or
        # functions/methods that create windows (CreateWindow is e.g. Windows
        # Microsoft's API), but in tkinter it makes a little different sense.
        #
        # After inserting, we get the ID of the inserted element, which will
        # be very useful to us soon.
        #
        scrollable_frame_canvas_id = canvas.create_window(
            (0, 0), window=self._scrollable_frame, anchor='nw')

        # Now the hard part - we add an observer to watch over the width of
        # the canvas matched the width of the area what is available. If we
        # don't, the canvas will (usually) were the wrong size. And although
        # there could still be elements inserted into it visible, then the
        # geometry manager would not be able to act accordingly with our
        # expectations.
        #
        def update_scrollable_frame_width(event):
            if self._scrollable_frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(
                    scrollable_frame_canvas_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', update_scrollable_frame_width)

        # We could do it a bit earlier, but we do it last: connect the
        # canvas scroll with what is set by the beam scrolling (i.e. via
        # scroll bar).
        #
        canvas.configure(yscrollcommand=sb.set)

        # We're also adding mouse wheel scrolling.
        #
        canvas.bind_all(
            "<MouseWheel>",
            lambda event:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        )

    @property
    def scrollable_frame(self):
        """
        Scrollable window as read-only property.

        Returns:
            tkinter.ttk.Frame class object where widgets can be embedded.
        """
        return self._scrollable_frame
