#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xrayspectrumanalyzer.gui.spectra
   :synopsis: Container of EELS spectrum.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Container of EELS spectrum.
"""

###############################################################################
# GUI for the x-ray spectrum analyzer project
# Copyright (C) 2017  Hendrix Demers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

# Standard library modules.
import os.path

# Third party modules.
import six

# Local modules.
from pysemeels.hitachi.eels_su.elv_file import ElvFile

# Project modules.

# Globals and constants variables.

class Spectra(object):
    def __init__(self):
        self.spectra = {}
        self.current_elv_file = None

    def open_spectrum(self, file_names):
        if six.PY3:
            if isinstance(file_names, str):
                file_names = [file_names]
        elif six.PY2:
            if isinstance(file_names, basestring):
                file_name = [file_names]

        for file_name in file_names:
            if os.path.splitext(file_name)[1] == ".elv":
                with open(file_name, 'r') as elv_text_file:
                    elv_file = ElvFile()
                    elv_file.read(elv_text_file)

                    self.set_current_elv_file(elv_file)

    def set_current_elv_file(self, elv_file):
        self.current_elv_file = elv_file

    def get_current_elv_file(self):
        return self.current_elv_file

