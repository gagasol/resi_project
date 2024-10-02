# This Python file uses the following encoding: utf-8
import json
import logging
import sys

from PySide6.QtCore import Qt, QEventLoop, QPoint, QRect, QSize, QSizeF, QMarginsF, QObject
from PySide6.QtGui import QIcon, QPdfWriter, QPageSize, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QFileDialog, QMdiArea, QMdiSubWindow, \
    QMessageBox
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
from settingsWindow import SettingsWindow


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

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.ui.tabWidget.tabCloseRequested.connect(self.closeTab)

        file_handler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

        file_handler.setFormatter(formatter)

        # add file handler to logger
        self.logger.addHandler(file_handler)

        matplotlib_logger = logging.getLogger('matplotlib')
        matplotlib_logger.setLevel(logging.WARNING)

        # testing area @todo TBD!!!

        self.test_file_path = "C:/Users/Heisenberg/Documents/Programming/Python/resi_project/resi/resiProject/Ka_Adl2M001.rgp"

    # variable setup

        self.pickMarkerWin = None
        self.markerPresetWin = None
        self.settingsWindow = None
        # @todo IMPORTANT make the nameToColorDict into a real thing!
        self.listGraphWidgets = []
        self.nameToColorDict = {}
        self.listNameKeys = []
        self.markerPresetList = []

        self.defaultMarkerDictName = ""

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
        self.defaultMarkerDictName = self.settingsWindow.getSettingsVariable("defaultMarkerDictName")


        self.listNameKeys = ["idNumber", "date"]

        # flags
        self.flagWindowClosedByUserSignal = False
        # endregion

    # button events
        # clicked events
        self.ui.pushButtonOpen.clicked.connect(self.openButtonClicked)
        self.ui.pushButtonSave.clicked.connect(self.saveButtonClicked)
        self.ui.actionSaveAs.triggered.connect(self.showSaveFileDialog)
        self.ui.pushButtonTabView.clicked.connect(self.tabButtonClicked)
        self.ui.pushButtonWindowView.clicked.connect(self.windowButtonClicked)
        self.ui.pushButtonPdf.clicked.connect(self.pdfButtonClicked)
        self.ui.pushButtonToggleOverlay.clicked.connect(self.toggleOverlayButtonClicked)
        self.ui.pushButtonPng.clicked.connect(self.pngButtonClicked)
        self.ui.pushButtonSettings.clicked.connect(self.settingsButtonClicked)

    #TDL!!!!

        #self.openButtonClicked(self.test_file_path)


    # functionality for QPushButtons

    # functionality for the pushButtonOpen QPushButton
    # @todo add multiple file input
    # @todo get rid of the fileName argument befeore release
    def openButtonClicked(self, fileName=None):
        self.logger.info("~~~~~~~~~~~~ openButtonClicked ~~~~~~~~~~~~")
        fileName, _ = QFileDialog.getOpenFileName(None, "Select File", "", "*.rgp *.resi;;*.rgp;;*.resi")
        self.logger.info("filename :{0}".format(fileName))
        if (fileName == ""):
            return
        self.nameOfFile = fileName.split(".")[0].split("/")[-1]
        if (".resi" in fileName):
            with open(fileName, "r") as file:
                loadedState = json.load(file)

            print("loadedState len = 1")
            logging.info(" canvas :{0}".format(loadedState))
            widget = WidgetGraph(self, "", loadedState)
            self.listGraphWidgets.append(widget)
            self.ui.tabWidget.addTab(widget, self.nameOfFile)
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

        elif(".project" in fileName):
            with open(fileName, "r") as file:
                loadedState = json.load(file)

            for canvas in loadedState:
                print("loadedState len > 1")
                logging.info(" canvas :{0}".format(canvas))
                widget = WidgetGraph(self, "",  canvas)
                self.listGraphWidgets.append(widget)
                self.ui.tabWidget.addTab(widget, self.nameOfFile)

        else:
            widget = WidgetGraph(self, fileName)
            print(fileName)
            self.listGraphWidgets.append(widget)
            self.ui.tabWidget.addTab(widget, self.nameOfFile+".rgp")

            self.ui.tabWidget.setCurrentIndex(len(self.listGraphWidgets) - 1)
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

        #self.ui.tabWidget.addTab(widget, widget.name)

    # functionality for the pushButtonSave QPushButton
    def saveButtonClicked(self):
        tabWidget = self.ui.tabWidget
        currentIndex = tabWidget.currentIndex()

        if ".rgp" in tabWidget.tabText(currentIndex):
            tabWidget.setTabText(currentIndex, tabWidget.tabText(currentIndex).split(".rgp")[0])

        graphWidget = tabWidget.widget(currentIndex)

        self.saveGraphState(graphWidget)
        print("saveButtonClicked")


    def showSaveFileDialog(self):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        defaultName = graphWidget.name + ".resi"
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",
                                                  defaultName, "All Files (*);;Text Files (*.txt)", options=options)

        fileName = fileName if ".resi" in fileName else fileName + ".resi"

        if fileName:
            self.saveGraphState(graphWidget, fileName)


    def saveGraphState(self, graphWidget, path=""):
        if (graphWidget):
            if (path == ""):
                with open("./data/" + graphWidget.name + ".resi", "w") as file:
                    json.dump(graphWidget.getCurrentState(), file)
            else:
                with open(path, "w") as file:
                    json.dump(graphWidget.getCurrentState(), file)
        else:
            for widget in self.listGraphWidgets:
                with open("./data/" + widget.name + ".resi", "w") as file:
                    json.dump(widget.getCurrentState(), file)


    # functionality for the pushButtonTabView QPushButton
    def tabButtonClicked(self):
        if (self.ui.stackedWidgetWorkArea.currentIndex() != 0):
            for graphWidget in self.listGraphWidgets:
                graphWidget.setParent(None)
                self.ui.mdiArea.closeAllSubWindows()
                self.ui.tabWidget.addTab(graphWidget, graphWidget.name)

        self.ui.stackedWidgetWorkArea.setCurrentIndex(0)


    def closeTab(self, index):
        tabWidget = self.ui.tabWidget.widget(index)
        reply = QMessageBox.question(self, QObject.tr("Confirm close"), QObject.tr("Save before you close?"),
                                     QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if (reply == QMessageBox.Save):
            if tabWidget is not None:
                with open(tabWidget.name + ".resi", "w") as file:
                    json.dump(tabWidget.getCurrentState(), file)
                tabWidget.deleteLater()

            self.ui.tabWidget.removeTab(index)

        elif (reply == QMessageBox.No):
            if tabWidget is not None:
                tabWidget.deleteLater()
            self.ui.tabWidget.removeTab(index)


    # functionality for the pushButtonWindowView QPushButton
    def windowButtonClicked(self):
        QMessageBox.warning(self, "Under construction", "This function is still under construction")
        return

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
        self.ui.mdiArea.tileSubWindows()


    def pdfButtonClicked(self):
        self.printGraphWidgetAs("pdf")


    def pngButtonClicked(self):
        self.printGraphWidgetAs("png")


    def printGraphWidgetAs(self, suffix):
        """
        Save the current graph widget as a file with the specified suffix.

        :param suffix: The suffix of the file to be saved (e.g. "png", "pdf").
        :return: None
        """
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())

        originalFontDataUneven = graphWidget.tableWidgetData.item(0, 0).font()
        originalFontDataEven = graphWidget.tableWidgetData.item(0, 1).font()
        try:
            originalFontMarker = graphWidget.tableWidgetMarker.item(0, 0).font()
        except AttributeError:
            originalFontMarker = None
            graphWidget.tableWidgetMarker.hide()
            logging.info("No Markers set so far")

        self.printSetupStart(graphWidget)

        # @todo add globally
        filename = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        if (".rgp" in filename):
            filename = "./data/" + filename.replace(".rgp", ".") + suffix
        else:
            filename = "./data/" + filename + "." + suffix

        printWidth = 1900
        printHeight = 1080
        scaledPixmap = QPixmap(QSize(printWidth, printHeight))
        scaledPixmap.fill(Qt.transparent)

        # @todo as soon as I have a load function in widgetGraph I can change the way I take an image
        # instead of printWidget = graphWidget I copy the state not the instance (maybe add load state? overkill..)
        # printWidget.setAttribute(Qt.WA_DontShowOnScreen, True)
        # printWidget.setAttribute(Qt.WA_Mapped, True)

        graphWidget.resize(printWidth, printHeight)


        graphWidget.render(scaledPixmap)

        if (suffix == "png"):
            print("printing to png")
            scaledPixmap.save(filename)
            graphWidget.resetWidgetsRelSpace()

        elif (suffix == "pdf"):
            print("printing to pdf")
            pdfWriter = QPdfWriter(filename)
            pageSize = QPageSize(QSizeF(210, 125), QPageSize.Millimeter)
            pdfWriter.setPageSize(pageSize)
            pdfWriter.setResolution(230)
            pdfWriter.setPageMargins(QMarginsF(0, 0, 0, 0))

            pdfPainter = QPainter(pdfWriter)
            pdfPainter.drawPixmap(0, 0, scaledPixmap)
            pdfPainter.end()
            graphWidget.resetWidgetsRelSpace()

        self.printSetupEnd(graphWidget, originalFontDataUneven, originalFontDataEven, originalFontMarker)


    def printSetupStart(self, graphWidget):
        """
        :param graphWidget: The graph widget on which the setup changes will be applied.
        :return: None

        This method is used to make initial setup changes to the given graph widget before printing. It changes the size
        of the horizontal spacer, invalidates the horizontal layout, hides the widget menu, hides the widget bottom,
        hides the label data, and changes the relative space of the widgets.

        It also adjusts the font size of the items in the table widget data and table widget marker to 15 point size.

        Finally, it sets the parent of the tablewidgetmarker to None, inserts it into the horizontal layout at index 2,
        and shows the table widget marker.
        """

        heightTop = self.settingsWindow.getSettingsVariable("printHeightWidgetTopPerc")
        heightGraph = self.settingsWindow.getSettingsVariable("printHeightWidgetGraphPerc")
        heightBottom = self.settingsWindow.getSettingsVariable("printHeightWidgetBottomPerc")
        fontSize = self.settingsWindow.getSettingsVariable("printFontSize")

        graphWidget.horizontalSpacer0.changeSize(10, 20)
        graphWidget.horizontalSpacerPrint.changeSize(9, 20)
        #graphWidget.horizontalLayout.invalidate()
        graphWidget.widgetMenu.hide()
        graphWidget.widgetBottom.hide()
        graphWidget.labelData.hide()
        graphWidget.changeWidgetsRelSpace(heightTop, heightGraph, heightBottom)
        graphWidget.setAttribute(Qt.WA_NoSystemBackground, True)
        graphWidget.setAttribute(Qt.WA_TranslucentBackground, True)
        graphWidget.canvasGraph.vLine.hide()
        graphWidget.canvasGraph.changeAxisFontsize(26)
        for i in range(graphWidget.tableWidgetData.rowCount()):
            for j in range(graphWidget.tableWidgetData.columnCount()):
                item = graphWidget.tableWidgetData.item(i, j)
                if (item):
                    font = item.font()
                    font.setPointSize(fontSize)
                    item.setFont(font)


        if (not graphWidget.tableWidgetMarker.isHidden()):
            for i in range(graphWidget.tableWidgetMarker.rowCount()):
                for j in range(graphWidget.tableWidgetMarker.columnCount()):
                    item = graphWidget.tableWidgetMarker.item(i, j)
                    if (item):
                        font = item.font()
                        font.setPointSize(fontSize)
                        item.setFont(font)

            graphWidget.tableWidgetMarker.setParent(None)
            graphWidget.horizontalLayout.insertWidget(3, graphWidget.tableWidgetMarker)
            graphWidget.tableWidgetMarker.show()

        graphWidget.widgetTop.adjustSize()

    def printSetupEnd(self, graphWidget, originalFontDataUneven, originalFontDataEven, originalFontMarker):
        """
        :param graphWidget: The graph widget containing the table widgets.
        :param originalFontDataUneven: The original font to be set for the table data items on odd columns.
        :param originalFontDataEven: The original font to be set for the table data items on even columns.
        :param originalFontMarker: The original font to be set for the table marker items.
        :return: None

        This method sets the original fonts for the table data items and table marker items in the given graph widget.
        It also adjusts the size of the horizontal spacer and shows the necessary components in the graph widget.

        """
        fontSize = self.settingsWindow.getSettingsVariable("fontSize")

        graphWidget.canvasGraph.changeAxisFontsize(11)
        graphWidget.setAttribute(Qt.WA_NoSystemBackground, False)
        graphWidget.setAttribute(Qt.WA_TranslucentBackground, False)
        for i in range(graphWidget.tableWidgetData.rowCount()):
            for j in range(graphWidget.tableWidgetData.columnCount()):
                item = graphWidget.tableWidgetData.item(i, j)
                if  (item):
                    if(j%2 == 0):
                        item.setFont(originalFontDataUneven)
                    else:
                        item.setFont(originalFontDataEven)

        if (not graphWidget.tableWidgetMarker.isHidden()):
            for i in range(graphWidget.tableWidgetMarker.rowCount()):
                for j in range(graphWidget.tableWidgetMarker.columnCount()):
                    item = graphWidget.tableWidgetMarker.item(i, j)
                    if  (item):
                        item.setFont(originalFontMarker)

            graphWidget.tableWidgetMarker.setParent(None)
            graphWidget.horizontalLayout_2.insertWidget(0, graphWidget.tableWidgetMarker)

        graphWidget.tableWidgetMarker.show()
        graphWidget.horizontalSpacer0.changeSize(70, 20)
        graphWidget.widgetMenu.show()
        graphWidget.widgetBottom.show()
        graphWidget.labelData.show()
        graphWidget.canvasGraph.vLine.show()
        graphWidget.widgetTop.adjustSize()

    def settingsButtonClicked(self):
        markerPresetWin = MarkerPresetWindow(self, self.nameToColorDict, self.markerPresetList, calledByGraph=False)
        markerPresetWin.exec()

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
        if not self.markerPresetList:
            QMessageBox.warning(self, QObject.tr("Warning"), QObject.tr("No preset available"))
            return None, None
        defaultDict = None

        for presetDict in self.markerPresetList:
            if defaultPresetName in presetDict.values():
                defaultDict = presetDict
                break
        if defaultDict is None:
            for presetDict in self.markerPresetList:
                if self.defaultMarkerDictName in presetDict.values():
                    defaultDict = presetDict
            QMessageBox.warning(self, QObject.tr("Warning"),
                                QObject.tr(f"Preset {defaultPresetName} not found, changing to default"))

        self.pickMarkerWin = PickMarker(self, defaultDict)
        self.overridePickMarkerDict(defaultDict)
        if (self.pickMarkerWin.exec()):
            return self.pickMarkerWin.markerName, self.pickMarkerWin.markerColor
        else:
            return None, None


    def overridePickMarkerDict(self, markerDict=None, name="", col=""):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        if name != "":
            self.pickMarkerWin.markerName = name
            self.pickMarkerWin.markerColor = col
            self.pickMarkerWin.accept()
            self.pickMarkerWin.close()
        elif markerDict is not None:
            graphWidget.changeFileDefaultPresetName(markerDict["_NameForPreset"])
            self.pickMarkerWin.markerDict = markerDict
            self.pickMarkerWin.loadMarkerDict(markerDict)
            self.pickMarkerWin.accept()
            self.pickMarkerWin.close()
        else:
            graphWidget.changeFileDefaultPresetName(self.defaultMarkerDictName)

    def getGraphDefaultMarkerDictName(self):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        return graphWidget.defaultMarkerDictName

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
            with open("./settings/settings.json", "r") as file:
                loadedFile = json.load(file)
                self.settingsWindow = SettingsWindow(loadedFile[0])
                self.nameToColorDict = loadedFile[1]
                self.markerPresetList = loadedFile[2]
        except FileNotFoundError:
            settingsDict = {"defaultMarkerDictName": "",
                            "heightWidgetTopPerc": 15,
                            "heightWidgetGraphPerc": 75,
                            "heightWidgetBottomPerc": 10,
                            "colorBackground": "#dfe5e6",
                            "colorBackgroundMarking": "#8b888f",
                            "fontSize": 14,
                            "fontName": "Arial",
                            "colorFeedPlot": "#5c08c9",
                            "colorDrillPlot": "#eda31a",
                            "markerHeightPerc": 0.02,
                            "printHeightWidgetTopPerc": 18,
                            "printHeightWidgetGraphPerc": 82,
                            "printHeightWidgetBottomPerc": 0,
                            "printFontSize": 30,
                            "printFontName": "Arial"}

            self.settingsWindow = SettingsWindow(settingsDict)
            print("First startup detected")

    def closeEvent(self, event):
        if self.defaultMarkerDictName is not None:
            saveData = [self.settingsWindow.defaultSettingsDict, self.nameToColorDict, self.markerPresetList]
        else:
            saveData = [self.settingsWindow.defaultSettingsDict, self.nameToColorDict, self.markerPresetList]
        with open("./settings/settings.json", "w") as f:
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
