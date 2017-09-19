#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xrayspectrumanalyzergui.gui.main_window
   :synopsis: Main window of the application.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Main window of the application.
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
import sys
import os.path

# Third party modules.
from qtpy.QtWidgets import QMainWindow, QAction, QApplication, QStyle, QFileDialog, QDockWidget, QLabel
from qtpy.QtCore import QSettings, Qt
from qtpy.QtGui import QIcon

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

# Local modules.

# Project modules.
from xrayspectrumanalyzergui.gui.spectrum_widget import SpectrumWidget
from xrayspectrumanalyzergui.gui.spectra import Spectra
import xrayspectrumanalyzergui.gui.svg_rc

# Globals and constants variables.


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.spectra = Spectra()

        self.init_ui()

        self.read_settings()

    def init_ui(self):
        # Define standard icon.
        standard_icon = self.style().standardIcon

        # Central widget.
        self.main_widget = SpectrumWidget(self.spectra)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # Project action
        new_project_action = QAction(QIcon(':/oi/svg/document.svg'), 'New project', self)
        new_project_action.setShortcut('Ctrl+N')
        new_project_action.setStatusTip('New project')
        new_project_action.triggered.connect(self.new_project)

        open_project_action = QAction(QIcon(':/oi/svg/envelope-open.svg'), 'Open project', self)
        open_project_action.setShortcut('Ctrl+O')
        open_project_action.setStatusTip('Open project')
        open_project_action.triggered.connect(self.open_project)

        close_project_action = QAction(QIcon(':/oi/svg/envelope-closed.svg'), 'Close project', self)
        close_project_action.setShortcut('Ctrl+C')
        close_project_action.setStatusTip('Close project')
        close_project_action.triggered.connect(self.close_project)

        save_project_action = QAction(QIcon(':/oi/svg/hard-drive.svg'), 'Save project', self)
        save_project_action.setShortcut('Ctrl+S')
        save_project_action.setStatusTip('Save project')
        save_project_action.triggered.connect(self.save_project)

        saveas_project_action = QAction(QIcon(':/oi/svg/hard-drive.svg'), 'Save project as ...', self)
        # saveas_project_action.setShortcut('Ctrl+S')
        saveas_project_action.setStatusTip('Save project as ...')
        saveas_project_action.triggered.connect(self.saveas_project)

        # Spectrum action
        import_spectrum_action = QAction(QIcon(':/oi/svg/account-login.svg'), 'Import spectrum', self)
        import_spectrum_action.setShortcut('Ctrl+I')
        import_spectrum_action.setStatusTip('Import spectrum')
        import_spectrum_action.triggered.connect(self.import_spectrum)

        export_spectrum_action = QAction(QIcon(':/oi/svg/account-logout.svg'), 'Export spectrum', self)
        # export_spectrum_action.setShortcut('Ctrl+I')
        export_spectrum_action.setStatusTip('Export spectrum')
        export_spectrum_action.triggered.connect(self.export_spectrum)

        # Exit action
        exit_action = QAction(QIcon(':/oi/svg/x.svg'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        # Status bar.
        self.statusBar()

        # Menu bar.
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_project_action)
        file_menu.addAction(open_project_action)
        file_menu.addAction(save_project_action)
        file_menu.addAction(saveas_project_action)
        file_menu.addAction(close_project_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu('&View')

        spectrum_menu = menubar.addMenu('&Spectrum')
        spectrum_menu.addAction(import_spectrum_action)

        analysis_menu = menubar.addMenu('&Analysis')

        # Toolbar
        file_toolbar = self.addToolBar('File')
        file_toolbar.addAction(new_project_action)
        file_toolbar.addAction(open_project_action)
        file_toolbar.addAction(save_project_action)
        file_toolbar.addAction(saveas_project_action)
        file_toolbar.addAction(close_project_action)
        file_toolbar.addAction(exit_action)
        view_menu.addAction(file_toolbar.toggleViewAction())

        spectrum_toolbar = self.addToolBar('Spectrum')
        spectrum_toolbar.addAction(import_spectrum_action)
        view_menu.addAction(spectrum_toolbar.toggleViewAction())

        analysis_toolbar = self.addToolBar('Analysis')
        view_menu.addAction(analysis_toolbar.toggleViewAction())

        view_menu.addSeparator()

        # Dock widget.
        self.graphic_settings_dock = QDockWidget("Graphic settings", self)
        self.graphic_settings_dock.setObjectName("graphic_settings_dock")
        self.graphic_settings_dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        label_test = QLabel("Test label")
        self.graphic_settings_dock.setWidget(label_test)
        view_menu.addAction(self.graphic_settings_dock.toggleViewAction())
        self.addDockWidget(Qt.AllDockWidgetAreas, self.graphic_settings_dock)
        print(self.graphic_settings_dock.objectName())

        # self.zero_loss_peak_dock = ZeroLossPeakWidget(self, self.spectra)
        # analysis_menu.addAction(self.zero_loss_peak_dock.toggleViewAction())
        # self.addDockWidget(Qt.AllDockWidgetAreas, self.zero_loss_peak_dock)

        # Final options.
        self.setWindowTitle('X-ray spectrum analyzer')
        self.show()

    def closeEvent(self, event):
        self.save_settings()
        super(MainWindow, self).closeEvent(event)

    def save_settings(self):
        settings = QSettings("openMicroanalysis", "xrayspectrumanalyzergui")
        # print(settings.fileName())

        settings.beginGroup("MainWindow")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())
        settings.endGroup()

        settings.beginGroup("graphic_settings_dock")
        settings.setValue("visible", self.graphic_settings_dock.isVisible())
        settings.endGroup()

        # settings.beginGroup("zero_loss_peak_dock")
        # settings.setValue("visible", self.zero_loss_peak_dock.isVisible())
        # settings.endGroup()

    def read_settings(self):
        settings = QSettings("openMicroanalysis", "xrayspectrumanalyzergui")
        # print(settings.fileName())
        # settings.clear()

        settings.beginGroup("MainWindow")
        geometry_value = settings.value("geometry")
        if geometry_value is None:
            self.setGeometry(300, 300, 600, 400)
        else:
            self.restoreGeometry(geometry_value)
        window_state_value = settings.value("window_state")
        if window_state_value is not None:
            self.restoreState(window_state_value)
        settings.endGroup()

        settings.beginGroup("graphic_settings_dock")
        visible_value = settings.value("visible")
        if visible_value is not None:
            if visible_value == "true":
                self.graphic_settings_dock.setVisible(True)
            elif visible_value == "false":
                self.graphic_settings_dock.setVisible(False)
        settings.endGroup()

        # settings.beginGroup("zero_loss_peak_dock")
        # visible_value = settings.value("visible")
        # if visible_value is not None:
        #     if visible_value == "true":
        #         self.zero_loss_peak_dock.setVisible(True)
        #     elif visible_value == "false":
        #         self.zero_loss_peak_dock.setVisible(False)
        # settings.endGroup()

    def import_spectrum(self):
        self.statusBar().showMessage("Import spectrum", 2000)

        path = os.path.dirname(__file__)
        formats = ["*.msa", "*.txt"]
        file_filters = "Spectrum file ({:s})".format(" ".join(formats))
        file_names = QFileDialog.getOpenFileName(self, "Import an x-ray spectrum", path, file_filters)

        # self.spectra.open_spectrum(file_names)
        #
        # elv_file = self.spectra.get_current_elv_file()
        # spectrum_data = elv_file.get_spectrum_data()
        # self.main_widget.update_figure(spectrum_data)

    def export_spectrum(self):
        self.statusBar().showMessage("Export spectrum", 2000)

    def new_project(self):
        self.statusBar().showMessage("New project", 2000)

    def open_project(self):
        self.statusBar().showMessage("Open project", 2000)

    def close_project(self):
        self.statusBar().showMessage("Close project", 2000)

    def save_project(self):
        self.statusBar().showMessage("Save project", 2000)

    def saveas_project(self):
        self.statusBar().showMessage("Save project as ...", 2000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
