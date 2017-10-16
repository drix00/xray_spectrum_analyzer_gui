#!/usr/bin/env python
""" """

###############################################################################
# Copyright 2016 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.

# Third party modules.

import xrayspectrumanalyzergui.gui.tk.MainWindow
# Local modules.
import xrayspectrumanalyzergui.gui.tk.Options
import xrayspectrumanalyzergui.gui.tk.SpectrumAnalyzerData as SpectrumAnalyzerData
import xrayspectrumanalyzergui.gui.tk.SpectrumAnalyzerEngine as SpectrumAnalyzerEngine

# Globals and constants variables.

class SpectrumAnalyzerGUI(object):
    def __init__(self, args=None, configurationFile=None):
        self._options = xrayspectrumanalyzergui.gui.Tk.Options.Options(args, configurationFile)

        self._data = SpectrumAnalyzerData.SpectrumAnalyzerData()

        self._engine = SpectrumAnalyzerEngine.SpectrumAnalyzerEngine()

    def run(self):
        if self._options.getUI() == xrayspectrumanalyzergui.gui.Tk.Options.UI_TK:
            self._runTk()

    def _runTk(self):
        xrayspectrumanalyzergui.gui.Tk.MainWindow.run(self._options, self._data, self._engine)

# TODO: Read command line options.
# TODO: Read configuration files options.
# TODO: Read and save GUI options.

def run():
    saGUI = SpectrumAnalyzerGUI()

    saGUI.run()
