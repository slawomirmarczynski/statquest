#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main module of StatQuest.

File:
    project: StatQuest
    name: statquest.py
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

import matplotlib  # todo: move to gui?

from scrollableframe import ScrollableFrame
from statquest_intro import Intro
from statquest_parameters import Parameters
from statquest_suite import Suite
from statquest_filesnames import FilesNames
from statquest_input import Input
from statquest_launcher import Launcher
from statquest_outtro import Outtro
from statquest_output import Output


class Program:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('StatQuest version 0.5.0.0')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        root_width = int(screen_width * 0.75)
        root_height = int(screen_height * 0.75)
        self.root.geometry(f'{root_width}x{root_height}')

        self.frame = ScrollableFrame(self.root)
        self.frame.pack(fill='both', expand=True)

        def create_component(ComponentClass, border=True):
            parent = self
            component = ComponentClass(parent, self.frame.scrollable_frame,
                                       border)
            return component

        self.intro = create_component(Intro, border=False)
        self.parameters = create_component(Parameters)
        self.suite = create_component(Suite)
        self.files_names = create_component(FilesNames)
        self.input = create_component(Input)
        self.output = Output(self)
        self.launcher = create_component(Launcher, border=False)
        self.outtro = create_component(Outtro, border=False)
        self.parameters.add_listener(self.input)
        self.files_names.add_listener(self.input)

    def run(self):
        self.root.mainloop()

def main():
    matplotlib.use('TkAgg')  # todo: move to gui?
    program = Program()
    program.run()


if __name__ == '__main__':
    main()
