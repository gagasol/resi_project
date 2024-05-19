# This Python file uses the following encoding: utf-8
import json
import logging
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
from editMarkerPreset import EditMarkerPresetWindow
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
        logging.basicConfig(level=logging.DEBUG)

        matplotlib_logger = logging.getLogger('matplotlib')
        matplotlib_logger.setLevel(logging.WARNING)

        # testing area @todo TBD!!!

        self.test_file_path = "C:/Users/Heisenberg/Documents/Programming/Python/resi_project/resi/resiProject/Ka_Adl2M001.rgp"

    # variable setup

        # classes
        # @markerWindow variable to store a selectMarkerWindow.py
        # @vLineRect constant that marks the vertical position of the mouse cursor across the MplCanvas
        # @currentTargetRect variable that holds a rectangle if it has been clicked on

        self.pickMarkerWin = None
        self.markerPresetWin = None
        # @todo IMPORTANT make the nameToColorDict into a real thing!
        self.listGraphWidgets = []
        self.nameToColorDict = {}
        self.listNameKeys = []
        self.markerPresetList = []

        self.defaultPresetName = ""

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
        self.loadPreset()


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
        if (fileName == ""):
            return
        self.nameOfFile = fileName.split(".")[0].split("/")[-1]
        if (".resi" in fileName):
            with open(fileName, "r") as file:
                loadedState = json.load(file)

            for canvas in loadedState:
                widget = WidgetGraph(self, "",  canvas)
                self.listGraphWidgets.append(widget)
                self.ui.tabWidget.addTab(widget, self.nameOfFile)
        else:
            widget = WidgetGraph(self, fileName)
            print(fileName)
            self.listGraphWidgets.append(widget)
            self.ui.tabWidget.addTab(widget, self.nameOfFile)

        #self.ui.tabWidget.addTab(widget, widget.name)

    # functionality for the pushButtonSave QPushButton
    # @todo save stuff, duh
    def saveButtonClicked(self):
        projectSave = []
        for widget in self.listGraphWidgets:
            projectSave.append(widget.getCurrentState())
            with open(self.nameOfFile + ".resi", "w") as file:
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
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        graphWidget.horizontalSpacer0.changeSize(10, 20)
        graphWidget.horizontalLayout.invalidate()
        graphWidget.widgetMenu.hide()
        graphWidget.widgetBottom.hide()
        graphWidget.labelData.hide()
        graphWidget.changeWidgetsRelSpace(15, 85, 0)

        originalFontDataUneven = graphWidget.tableWidgetData.item(0, 0).font()
        originalFontDataEven = graphWidget.tableWidgetData.item(0, 1).font()
        try:
            originalFontMarker = graphWidget.tableWidgetMarker.item(0, 0).font()
        except AttributeError:
            logging.info("No Markers set so far")

        for i in range(graphWidget.tableWidgetData.rowCount()):
            for j in range(graphWidget.tableWidgetData.columnCount()):
                item = graphWidget.tableWidgetData.item(i, j)
                if (item):
                    font = item.font()
                    font.setPointSize(15)
                    item.setFont(font)

        for i in range(graphWidget.tableWidgetMarker.rowCount()):
            for j in range(graphWidget.tableWidgetMarker.columnCount()):
                item = graphWidget.tableWidgetMarker.item(i, j)
                if  (item):
                    font = item.font()
                    font.setPointSize(15)
                    item.setFont(font)

        graphWidget.tableWidgetMarker.setParent(None)
        graphWidget.horizontalLayout.insertWidget(2, graphWidget.tableWidgetMarker)
        graphWidget.tableWidgetMarker.show()
        # @todo add globally
        filename = self.nameOfFile + "." + suffix
        printWidth = 1920
        printHeight = 1080
        scaledPixmap = QPixmap(QSize(printWidth, printHeight))
        print(scaledPixmap.size())

        # @todo as soon as I have a load function in widgetGraph I can change the way I take an image
        # instead of printWidget = graphWidget I copy the state not the instance (maybe add load state? overkill..)
        # printWidget.setAttribute(Qt.WA_DontShowOnScreen, True)
        # printWidget.setAttribute(Qt.WA_Mapped, True)

        graphWidget.resize(printWidth, printHeight)


        graphWidget.render(scaledPixmap)

        if (suffix == "png"):
            print("printing to png")
            filename = filename
            scaledPixmap.save(filename)
            graphWidget.resetWidgetsRelSpace()

        elif (suffix == "pdf"):
            print("printing to pdf")
            filename = filename.strip()
            pdfWriter = QPdfWriter(filename)
            pageSize = QPageSize(QSizeF(210, 297), QPageSize.Millimeter)
            pdfWriter.setPageSize(pageSize)
            pdfWriter.setResolution(230)
            pdfWriter.setPageMargins(QMarginsF(0, 0, 0, 0))

            pdfPainter = QPainter(pdfWriter)
            pdfPainter.drawPixmap(0, 0, scaledPixmap)
            pdfPainter.end()
            graphWidget.resetWidgetsRelSpace()

        for i in range(graphWidget.tableWidgetData.rowCount()):
            for j in range(graphWidget.tableWidgetData.columnCount()):
                item = graphWidget.tableWidgetData.item(i, j)
                if  (item):
                    if(j%2 == 0):
                        item.setFont(originalFontDataUneven)
                    else:
                        item.setFont(originalFontDataEven)

        for i in range(graphWidget.tableWidgetMarker.rowCount()):
            for j in range(graphWidget.tableWidgetMarker.columnCount()):
                item = graphWidget.tableWidgetMarker.item(i, j)
                if  (item):
                    item.setFont(originalFontMarker)

        graphWidget.horizontalSpacer0.changeSize(70, 20)
        graphWidget.widgetMenu.show()
        graphWidget.widgetBottom.show()
        graphWidget.labelData.show()
        graphWidget.tableWidgetMarker.setParent(None)
        graphWidget.horizontalLayout_2.insertWidget(0, graphWidget.tableWidgetMarker)
        graphWidget.tableWidgetMarker.show()



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


    def openPickMarker(self, defaultPresetName):
        defaultDict = None
        for presetDict in self.markerPresetList:
            if (defaultPresetName in presetDict.values()):
                defaultDict = presetDict
                break
        if (defaultDict is None):
            raise Exception("No preset named '" + defaultPresetName + "'")

        self.pickMarkerWin = PickMarker(self, defaultDict)
        if (self.pickMarkerWin.exec()):
            return self.pickMarkerWin.markerName, self.pickMarkerWin.markerColor
        else:
            return None, None


    def overridePickMarkerDict(self, markerDict, name="", col=""):
        if (name != ""):
            self.pickMarkerWin.loadMarkerDict(markerDict)
            self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex()).defaultMarkerDictName = markerDict["_NameForPreset"]
            self.pickMarkerWin.markerName = name
            self.pickMarkerWin.markerColor = col
            self.pickMarkerWin.accept()
            self.pickMarkerWin.close()
        else:
            self.pickMarkerWin.loadMarkerDict(markerDict)


    def openChangeMarkerPreset(self, defaultPresetName=None):
        markerPresetWin = MarkerPresetWindow(self, self.nameToColorDict, self.markerPresetList)
        if (markerPresetWin.exec()):
            for markerDict in self.markerPresetList:
                if (defaultPresetName in markerDict.values()):
                    return markerDict
        else:
            return None


    def loadPreset(self):
        try:
            with open("markerSave.json", "r") as file:
                loadedFile = json.load(file)
                self.nameToColorDict = loadedFile[0]
                self.markerPresetList = loadedFile[1]
                self.defaultPresetName = loadedFile[2]
        except FileNotFoundError:
            print("First startup detected")

    def closeEvent(self, event):
        if (self.defaultPresetName is not None):
            saveData = [self.nameToColorDict, self.markerPresetList, self.defaultPresetName]
        else:
            saveData = [self.nameToColorDict, self.markerPresetList]
        with open("markerSave.json", "w") as f:
            json.dump(saveData, f)

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
# todo table data change row with tab not column
# todo set certain ifnormation as constant in table data
# todo icons add a down arrow for overriding the options
# todo show marking area while marking
# todo give option to show markers behind graph
# todo add project option

# @IMPORTANT TODO fix markerPreset