#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: gui.test_svg_rc

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`xrayspectrumanalyzergui.gui.svg_rc`.
"""

###############################################################################
# Copyright 2017 Hendrix Demers
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
import unittest

# Third party modules.
from qtpy.QtCore import QFile

# Local modules.

# Project modules.
from xrayspectrumanalyzergui.gui.svg_rc import qCleanupResources, qInitResources

# Globals and constants variables.


class TestSvgRc(unittest.TestCase):
    """
    TestCase class for the module `xrayspectrumanalyzergui.gui.svg_rc`.
    """

    def setUp(self):
        """
        Setup method.

        qInitResources is run during module import, but might be closed by another test so setup call it.
        """

        unittest.TestCase.setUp(self)

        qInitResources()

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        # self.fail("Test if the testcase is working.")

    def test_qInitResources(self):
        """
        Test qInitResources.

        qInitResources is run during module import, but might be closed by another test so setup call it.
        """

        icon_file = QFile(':/oi/svg/document.svg')
        self.assertTrue(icon_file.exists())

        # self.fail("Test if the testcase is working.")

    def test_qCleanupResources(self):
        """
        Test qCleanupResources.
        """

        file_before = QFile(':/oi/svg/document.svg')
        self.assertTrue(file_before.exists())

        qCleanupResources()

        file_after = QFile(':/oi/svg/document.svg')
        self.assertFalse(file_after.exists())

        # self.fail("Test if the testcase is working.")


if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.runmodule()
