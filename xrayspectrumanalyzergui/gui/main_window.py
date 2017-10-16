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
import logging
from logging.handlers import RotatingFileHandler

# Third party modules.
from qtpy.QtWidgets import QMainWindow, QAction, QApplication, QStyle, QFileDialog, QDockWidget, QLabel, \
    QDesktopWidget, QMessageBox, QHBoxLayout, QGroupBox, QSizePolicy, QVBoxLayout, QListWidget, QToolTip, QTextEdit
from qtpy.QtCore import QSettings, Qt, QPoint, QSize
from qtpy.QtGui import QIcon, QDesktopServices, QKeySequence, QFont

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Local modules.

# Project modules.
from xrayspectrumanalyzergui.gui.spectrum_widget import SpectrumWidget
import xrayspectrumanalyzergui.gui.svg_rc

# Globals and constants variables.
APPLICATION_NAME = "xrayspectrumanalyzer"
ORGANIZATION_NAME = "McGill University"
LOG_FILENAME = APPLICATION_NAME + '.log'

MODULE_LOGGER = logging.getLogger(APPLICATION_NAME)


class MainWindow(QMainWindow):
    def __init__(self):
        self.logger = logging.getLogger(APPLICATION_NAME + '.MainWindow')
        self.logger.info("MainWindow.__init__")

        super(MainWindow, self).__init__()

        self.init_ui()

        self.read_settings()

    def init_ui(self):
        # Define standard icon.
        standard_icon = self.style().standardIcon

        # Central widget.
        self.main_widget = SpectrumWidget()
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

    def create_gui(self):
        self.logger.info("MainWindow.create_gui")

        self._create_main_window()
        self._create_actions()
        self._create_menus()
        self._create_toolbars()
        self._create_tooltip()
        self._create_spectra_display()
        self._create_data_display()
        self._create_operations_display()
        self._create_layout()
        self._create_statusbar()

        self._read_settings()

        self.show()

    def _create_main_window(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Spectrum Analyzer')
        # self.setWindowIcon(QIcon('../../../images/cog.svg'))
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        self._center_main_window()

    def _center_main_window(self):
        self.logger.info("MainWindow._center_main_window")

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _create_menus(self):
        self.logger.info("MainWindow._create_menus")

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def _create_layout(self):
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        mainLayout.addWidget(self.plotGroupBox)
        mainLayout.addWidget(self.operationsGroupBox)

        self.mainGroupBox = QGroupBox("Main layout")
        self.mainGroupBox.setLayout(mainLayout)
        self.setCentralWidget(self.mainGroupBox)

    def _create_spectra_display(self):
        self.plotGroupBox = QGroupBox("Plot layout")

        self.figure1 = Figure(facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setParent(self.plotGroupBox)
        self.canvas1.setFocusPolicy(Qt.StrongFocus)
        self.canvas1.setFocus()
        self.canvas1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas1.updateGeometry()

        self.mpl_toolbar1 = NavigationToolbar(self.canvas1, self.plotGroupBox)
        self.canvas1.mpl_connect('key_press_event', self.on_key_press)

        self.figure2 = Figure(facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setParent(self.plotGroupBox)
        self.mpl_toolbar2 = NavigationToolbar(self.canvas1, self.plotGroupBox)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas1)
        layout.addWidget(self.mpl_toolbar1)
        layout.addWidget(self.canvas2)
        layout.addWidget(self.mpl_toolbar2)
        self.plotGroupBox.setLayout(layout)

    def _create_data_display(self):
        self.dataGroupBox = QGroupBox("Data layout")
        data_layout = QVBoxLayout()

        group_box = QGroupBox("Spectra")
        self.spectra_list_view = QListWidget(self)
        self.spectra_list_view.setMinimumWidth(200)

        layout = QVBoxLayout()
        layout.addWidget(self.spectra_list_view)
        group_box.setLayout(layout)
        data_layout.addWidget(group_box)

        group_box = QGroupBox("ROI")
        roi_list_view = QListWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(roi_list_view)
        group_box.setLayout(layout)
        data_layout.addWidget(group_box)

        group_box = QGroupBox("Elements")
        element_list_view = QListWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(element_list_view)
        group_box.setLayout(layout)
        data_layout.addWidget(group_box)

        self.dataGroupBox.setLayout(data_layout)

    def _create_operations_display(self):
        self.operationsGroupBox = QGroupBox("Operations layout")
        results_layout = QVBoxLayout()

        group_box = QGroupBox("Operation")
        results_layout.addWidget(group_box)
        group_box = QGroupBox("Results")
        results_layout.addWidget(group_box)

        self.operationsGroupBox.setLayout(results_layout)

    def _create_tooltip(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

    def _create_actions(self):
        self.logger.info("MainWindow._create_actions")

        self.newAct = QAction(self.style().standardIcon(QStyle.SP_FileIcon), "&New",
                self, shortcut=QKeySequence.New,
                statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction(self.style().standardIcon(QStyle.SP_DirOpenIcon),
                "&Open...", self, shortcut=QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton),
                "&Save", self, shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), "Save &As...", self,
                shortcut=QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        self.exitAct = QAction(self.style().standardIcon(QStyle.SP_DialogCloseButton),
                                     "E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)

        self.textEdit = QTextEdit()

        self.aboutAct = QAction(self.style().standardIcon(QStyle.SP_MessageBoxInformation), "&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction(self.style().standardIcon(QStyle.SP_TitleBarMenuButton), "About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication().aboutQt)

    def _create_toolbars(self):
        self.logger.info("MainWindow._create_toolbars")

        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

    def _create_statusbar(self):
        self.logger.info("MainWindow._create_statusbar")

        self.statusBar().showMessage("Ready")

    def _read_settings(self):
        self.logger.info("MainWindow._read_settings")

        settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        pos = settings.value("pos", QPoint(200, 200))
        size = settings.value("size", QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def _write_settings(self):
        self.logger.info("MainWindow._write_settings")

        settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def maybeSave(self):
        self.logger.info("MainWindow.maybeSave")

        if self.textEdit.document().isModified():
            ret = QMessageBox.warning(self, "Application",
                    "The document has been modified.\nDo you want to save "
                    "your changes?",
                    QMessageBox.Save | QMessageBox.Discard |
                    QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.save()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def closeEvent(self, event):
        self.logger.info("MainWindow.closeEvent")

        if self.maybeSave():
            self._write_settings()
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        self.logger.info("MainWindow.newFile")

        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFile('')

    def open(self):
        self.logger.info("MainWindow.open")

        if self.maybeSave():
            filepath, _filtr = QFileDialog.getOpenFileName(self)
            if filepath:
                self.spectrumAnalyzer.readSpectrum(filepath)
                filename = os.path.basename(filepath)
                self.spectra_list_view.addItem(filename)
                self.spectrumAnalyzer.plotSpectrum(self.figure1)
                self.canvas1.draw()

    def save(self):
        self.logger.info("MainWindow.save")

        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    def saveAs(self):
        self.logger.info("MainWindow.saveAs")

        fileName, _filtr = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    def about(self):
        self.logger.info("MainWindow.about")

        QMessageBox.about(self, "About xrayspectrumanalyzer",
                "The <b>xrayspectrumanalyzer</b> extract peak intensity from EDS spectrum.")

    def documentWasModified(self):
        self.logger.info("MainWindow.documentWasModified")

        self.setWindowModified(self.textEdit.document().isModified())

    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas1, self.mpl_toolbar1)

# TODO: Add Menubar
# TODO: Add statusbar
# TODO: Save project (autosave)
# TODO: Add toolbars
# TODO: Add spectrum list
# TODO: Add spectrum display
# TODO: Add ROI list
# TODO: Add ROI display
# TODO: Elements list
# TODO: Element+line display
# TODO: Add main window
# TODO: Add layout management
# TODO: Add log file
# TODO: Fit dialog recipe
# TODO: Add drag and drop


def create_application():
    application = QApplication(sys.argv)
    application.setApplicationName(APPLICATION_NAME)
    application.setOrganizationName(ORGANIZATION_NAME)

    return application


def start_logging():
    data_location = QDesktopServices.storageLocation(QDesktopServices.DataLocation)
    if not os.path.isdir(data_location):
        os.makedirs(data_location)

    log_filepath = os.path.join(data_location, LOG_FILENAME)
    fh = RotatingFileHandler(log_filepath, maxBytes=1024*30, backupCount=10)
    MODULE_LOGGER.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
    fh.setFormatter(formatter)
    MODULE_LOGGER.addHandler(fh)
    MODULE_LOGGER.info("startLogging")

    MODULE_LOGGER.debug("Data location: %s", data_location)
    MODULE_LOGGER.debug("Applications location: %s", QDesktopServices.storageLocation(QDesktopServices.ApplicationsLocation))
    MODULE_LOGGER.debug("Home location: %s", QDesktopServices.storageLocation(QDesktopServices.HomeLocation))
    MODULE_LOGGER.debug("Temp location: %s", QDesktopServices.storageLocation(QDesktopServices.TempLocation))
    MODULE_LOGGER.debug("Cache location: %s", QDesktopServices.storageLocation(QDesktopServices.CacheLocation))


if __name__ == '__main__':
    start_logging()

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
