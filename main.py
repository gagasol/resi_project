# This Python file uses the following encoding: utf-8
import json
import sys

from PySide6.QtCore import Qt, QEventLoop, QPoint, QRect, QSize, QSizeF, QMarginsF
from PySide6.QtGui import QIcon, QPdfWriter, QPageSize, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QFileDialog, QMdiArea, QMdiSubWindow
from PySide6 import QtWidgets

import numpy as np
import matplotlib
from matplotlib.patches import Rectangle
from matplotlib.backend_bases import MouseButton

import markerpresetwindow
from widgetGraph import WidgetGraph
from ui_files.ui_mainwindow import Ui_MainWindow
from markerpresetwindow import MarkerPresetWindow
from editMarkerPreset import SelectMarkerWindow
from pickMarkerWindow import PickMarker


class CustomQMdiArea(QMdiArea):
    def tileSubWindowsH(self):
        if len(self.subWindowList()) == 0:
            return

        position = QPoint(0, 0)
        windowWidth = self.width() // 3
        for window in self.subWindowList():
            rect = QRect(0, 0, self.height(), windowWidth)
            window.setGeometry(rect)
            window.move(position)
            position.setX(position.x() + windowWidth)

    def tileSubWindowsV(self):
        if len(self.subWindowList()) == 0:
            return

        position = QPoint(0, 0)
        windowHeight = self.height() // 3
        for window in self.subWindowList():
            rect = QRect(0, 0, self.width(), windowHeight)
            window.setGeometry(rect)
            window.move(position)
            position.setY(position.y() + windowHeight)

    def resizeEvent(self, event):
        self.tileSubWindowsV()
        print(f"New size: {self.size()}")
        super().resizeEvent(event)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Initializes the MainWindow class.

        :return: None
        """
        super(MainWindow, self).__init__()
        self.markerWindow = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # testing area @todo TBD!!!

        self.test_file_path = "C:/Users/Heisenberg/Documents/Programming/Python/resi_project/resi/resiProject/Ka_Adl2M001.rgp"

    # variable setup

        # classes
        # @markerWindow variable to store a selectMarkerWindow.py
        # @vLineRect constant that marks the vertical position of the mouse cursor across the MplCanvas
        # @currentTargetRect variable that holds a rectangle if it has been clicked on

        self.listGraphWidgets = []
        self.nameToColorDict = {}
        self.listNameKeys = []
        self.markerPrestDict = {}

        # @todo delete later
        self.nameToColorDict = {
            "Red": "#FF0000",
            "Blue": "#0000FF",
            "Yellow": "#FFFF00",
            "Black": "#000000",
            "White": "#FFFFFF",
            "Aloof": "#7B68EE",
            "Cherish": "#FFB6C1",
            "Divine": "#FFA07A",
            "Elapse": "#8B0000",
            "Green": "#00FF00",
            "Coral": "#FF7F50",
            "Cyan": "#00FFFF",
            "Chocolate": "#D2691E",
            "Crimson": "#DC143C"
        }


        self.listNameKeys = ["idNumber", "date"]

        # flags
        self.flagWindowClosedByUserSignal = False
        # endregion

    # button events
        # clicked events
        self.ui.pushButtonOpen.clicked.connect(self.openButtonClicked)
        self.ui.pushButtonSave.clicked.connect(self.saveButtonClicked)
        self.ui.pushButtonTabView.clicked.connect(self.tabButtonClicked)
        self.ui.pushButtonWindowView.clicked.connect(self.windowButtonClicked)
        self.ui.pushButtonPdf.clicked.connect(self.pdfButtonClicked)
        self.ui.pushButtonToggleOverlay.clicked.connect(self.toggleOverlayButtonClicked)
        self.ui.pushButtonPng.clicked.connect(self.pngButtonClicked)

    #TDL!!!!

        #self.openButtonClicked(self.test_file_path)


    # functionality for QPushButtons

    # functionality for the pushButtonOpen QPushButton
    # @todo add multiple file input
    # @todo get rid of the fileName argument befeore release
    def openButtonClicked(self, fileName=None):

        fileName, _ = QFileDialog.getOpenFileName(None, "Select File", "", "*.rgp;;*.resi")

        if (".resi" in fileName):
            with open(fileName, "r") as file:
                loadedState = json.load(file)

            for canvas in loadedState:
                widget = WidgetGraph(self, "",  canvas)
                self.listGraphWidgets.append(widget)
                self.ui.tabWidget.addTab(widget, widget.name)
        else:
            widget = WidgetGraph(self, fileName)
            print(fileName)
            self.listGraphWidgets.append(widget)
            self.ui.tabWidget.addTab(widget, widget.name)

        #self.ui.tabWidget.addTab(widget, widget.name)

    # functionality for the pushButtonSave QPushButton
    # @todo save stuff, duh
    def saveButtonClicked(self):
        projectSave = []
        for widget in self.listGraphWidgets:
            titel = widget.name.replace(".", "")
            projectSave.append(widget.getCurrentState())
            with open(titel + ".resi", "w") as file:
                json.dump(projectSave, file)

        with open(".project", "w") as file:
            json.dump(projectSave, file)

        print("saveButtonClicked")

    # functionality for the pushButtonTabView QPushButton
    def tabButtonClicked(self):
        if (self.ui.stackedWidgetWorkArea.currentIndex() != 0):
            for graphWidget in self.listGraphWidgets:
                graphWidget.setParent(None)
                self.ui.mdiArea.closeAllSubWindows()
                self.ui.tabWidget.addTab(graphWidget, graphWidget.name)

        self.ui.stackedWidgetWorkArea.setCurrentIndex(0)

    # functionality for the pushButtonWindowView QPushButton
    def windowButtonClicked(self):
        if (self.ui.stackedWidgetWorkArea.currentIndex() != 1):
            for graphWidget in self.listGraphWidgets:
                self.ui.tabWidget.clear()
                subwindow = QMdiSubWindow()
                widget = graphWidget
                widget.setParent(None)
                subwindow.setWidget(widget)
                subwindow.show()
                widget.show()
                self.ui.mdiArea.addSubWindow(widget)

        self.ui.stackedWidgetWorkArea.setCurrentIndex(1)
        self.ui.mdiArea.tileSubWindowsV()


    def pdfButtonClicked(self):
        self.saveGraphWidgetAs("pdf")


    def pngButtonClicked(self):
        self.saveGraphWidgetAs("png")


    def saveGraphWidgetAs(self, suffix):
        for graphWidget in self.listGraphWidgets:
            # @todo add globally
            filename = "test_output"
            printWidth = 1906
            printHeight = 1000
            scaledPixmap = QPixmap(QSize(printWidth, printHeight))
            print(scaledPixmap.size())

            printWidget = WidgetGraph()
            # @todo as soon as I have a load function in widgetGraph I can change the way I take an image
            # instead of printWidget = graphWidget I copy the state not the instance (maybe add load state? overkill..)
            # printWidget.setAttribute(Qt.WA_DontShowOnScreen, True)
            # printWidget.setAttribute(Qt.WA_Mapped, True)
            printWidget = graphWidget

            printWidget.resize(printWidth, printHeight)
            printWidget.render(scaledPixmap)

            if (suffix == "png"):
                print("printing to png")
                filename = filename + ".png"
                scaledPixmap.save(filename)
                return

            elif (suffix == "pdf"):
                print("printing to pdf")
                filename = filename.strip() + ".pdf"
                pdfWriter = QPdfWriter(filename)
                pageSize = QPageSize(QSizeF(210, 297), QPageSize.Millimeter)
                pdfWriter.setPageSize(pageSize)
                pdfWriter.setResolution(230)
                pdfWriter.setPageMargins(QMarginsF(0, 0, 0, 0))

                pdfPainter = QPainter(pdfWriter)
                pdfPainter.drawPixmap(0, 0, scaledPixmap)
                pdfPainter.drawPixmap(0, 960, scaledPixmap)
                pdfPainter.end()


    def toggleOverlayButtonClicked(self):
        # If overlay_widget visible, hide it, else show it
        if self.ui.widgetOverlay.isVisible():
            self.ui.widgetOverlay.hide()
            self.ui.horizontalSpacerManual1.changeSize(0, 17)
            icon_in = QIcon()
            icon_in.addFile(u":/icons/icons/text-outdent.svg", QSize(), QIcon.Normal, QIcon.On)
            self.ui.pushButtonToggleOverlay.setIcon(icon_in)
            self.ui.pushButtonToggleOverlay.setIconSize(QSize(25, 25))
        else:
            self.ui.widgetOverlay.show()
            spacerWidth = self.ui.widgetOverlay.width() - self.ui.pushButtonToggleOverlay.width()
            self.ui.horizontalSpacerManual1.changeSize(spacerWidth, 17)
            icon_in = QIcon()
            icon_in.addFile(u":/icons/icons/text-indent.svg", QSize(), QIcon.Normal, QIcon.On)
            self.ui.pushButtonToggleOverlay.setIcon(icon_in)
            self.ui.pushButtonToggleOverlay.setIconSize(QSize(25, 25))


    def openPickMarker(self, defaultPreset=None):
        defaultDict = self.markerPrestDict["default"] if defaultPreset is None else defaultPreset
        pickMarkerWin = PickMarker(self, defaultDict)

    # algorithms


    # TDL functions I use for things


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

# todo Linux zeigt keiine Schrift außer im Hover -> setColorText black
# todo name von preset statt Pick Marker
# todo save each file on its own
# todo keep marking after one click
# todo toggle marking active on key input
# todo change pick system to a List of labels in the current default preset
# todo mouse panning remove y axis
# todo table data change row with tab not column
# todo set certain ifnormation as constant in table data
# todo icons add a down arrow for overriding the options
# todo on right click set delta for marker
# todo marker window activate cancel
# todo show marking area while marking
# todo give option to show markers behind graph
# todo adjust snapOn to snap on sooner (or later, or not at all)
# todo add project option