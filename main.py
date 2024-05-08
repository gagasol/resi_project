# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtCore import Qt, QEventLoop
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PySide6 import QtWidgets

import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backend_bases import MouseButton

import markerpresetwindow
from widgetGraph import WidgetGraph
from ui_files.ui_mainwindow import Ui_MainWindow
from markerpresetwindow import MarkerPresetWindow
from editMarkerPreset import SelectMarkerWindow


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.03, right=0.97, top=0.99, bottom=0.07)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Initializes the MainWindow class.

        :return: None
        """
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # testing area TBD!!!

        self.test_rect = Rectangle((0, 0), 0.2, - 0.03)
        self.test_x_start = 0

        self.flagWindowClosedByUserSignal = False

    # variable setup

        # classes
        # @markerWindow variable to store a selectMarkerWindow.py
        # @vLineRect constant that marks the vertical position of the mouse cursor across the MplCanvas
        # @currentTargetRect variable that holds a rectangle if it has been clicked on
        self.markerWindow = None

        self.vLineRect = Rectangle((-5, 0), 0.05, 120)
        self.focusRect = None

        # data
        # @xDataForMarker variable that holds the first clicked position to draw a marker from that to the second click
        # @dict dictMarker dictionary containing a "String::Name: String::HexColor" pair to save all Marker
        # @list listMarkerPreset list containing all named presets where <key>:"name" corresponds to the name
        # @colorRect variable set by selectMarkerWindow that determines the color of a rectangle
        # @nameRectMark variable set by selectMarkerWindow is the name of a marker rectangle
        # @heightRectMarkPerc sets the height of the marker as percent of the y-axis
        # @percMarkerFocusHeight sets the height of the focus for the marker as a percent of the y-axis

        self.dictMarkerRectSetupData = {}
        self.xDataForMarker = None

        self.dictMarker = {}
        self.listMarkerPreset = []
        self.colorRect = "#000000"
        self.nameRectMark = ""
        self.heightRectMarkPerc = 3
        self.percMarkerFocusHeight = 30

        self.dictCanvasToRectList = {}

        # counter
        # @variable clickCount counts to a max of 1, on 0 it sets the xDataForMarker var
        self.clickCount = 0

        # flags
        self.flagRectFocus = False
        self.flagRectLeftFocus = False
        self.flagRectRightFocus = False
        self.flagMouseClicked = False
        self.flagVerticalLine = True


    # button events
        # clicked events
        self.ui.pushButtonOpen.clicked.connect(self.openButtonClicked)
        self.ui.pushButtonSave.clicked.connect(self.saveButtonClicked)
        self.ui.pushButtonTabView.clicked.connect(self.tabButtonClicked)
        self.ui.pushButtonWindowView.clicked.connect(self.windowButtonClicked)

    # functionality for the matplotlib canvas

    def onMouseMove(self, event):

        # draw vertical line
        if event.inaxes and self.flagVerticalLine:
            self.vLineRect.set_x(event.xdata)

        # test on how to move a rectangle
        if (event.inaxes and event.button == MouseButton.LEFT and self.flagRectFocus):
            currentX = self.focusRect.get_x()

            self.focusRect.set_x(
                currentX + (event.xdata - self.test_x_start))
            self.test_x_start = event.xdata

        # test on how to change the length of a rectangle
        if (event.inaxes and event.button == MouseButton.LEFT and self.flagRectRightFocus):
            currentWidth = self.focusRect.get_width()

            self.focusRect.set_width(
                currentWidth + (event.xdata - self.test_x_start))
            self.test_x_start = event.xdata

        if (event.inaxes and event.button == MouseButton.LEFT and self.flagRectLeftFocus):
            currentX = self.focusRect.get_x()
            currentWidth = self.focusRect.get_width()

            self.focusRect.set_x(
                currentX + (event.xdata - self.test_x_start))
            self.focusRect.set_width(
                currentWidth - (event.xdata - self.test_x_start))
            self.test_x_start = event.xdata

        if (event.inaxes):
            event.canvas.draw()

    def onButtonPress(self, event):

        if (event.inaxes is None):
            return

        print(event.canvas.parent)

        self.flagMouseClicked = True

        self.test_x_start = event.xdata
        print(event.xdata, event.ydata)

        # check if any marker rectangle is close by
        # @todo add the loop to the function and just call the function
        if (self.dictCanvasToRectList[event.canvas] is not []):
            for rect, color in self.dictCanvasToRectList[event.canvas]:
                if self.checkIfClickByRect(event, rect):
                    self.focusRect = rect
                    return

        # logic for creating markers with addRectToCurrentCanv
        if (not (self.flagRectFocus or self.flagRectLeftFocus or self.flagRectRightFocus)):

            if (self.clickCount == 0):
                self.xDataForMarker = event.xdata

            elif (self.clickCount == 1):
                self.markerWindow = markerpresetwindow.MarkerPresetWindow(self)
                self.markerWindow.setAttribute(Qt.WA_DeleteOnClose)
                self.markerWindow.show()
                self.markerWindow.destroyed.emit()

                waitForMarkerInputLoop = QEventLoop()
                self.markerWindow.closedByUser.connect(self.windowClosedByUser)
                self.markerWindow.closedProgrammatically.connect(self.windowClosedProgrammatically)
                self.markerWindow.destroyed.connect(waitForMarkerInputLoop.quit)
                waitForMarkerInputLoop.exec()

                if (not self.flagWindowClosedByUserSignal):
                    self.addRectToCurrentCanv(event)
                self.flagMouseClicked = False

            self.clickCount = self.clickCount + 1 if (self.clickCount < 1) else 0


    def onButtonReleased(self, event):

        self.flagMouseClicked = False
        self.flagRectFocus = False
        self.flagRectLeftFocus = False
        self.flagRectRightFocus = False

    def onAxesEnter(self, event):
        self.vLineRect.set_visible(True)
        event.canvas.axes.add_patch(self.vLineRect)


    def onAxesLeave(self, event):


        print(event.canvas)
        if (event is None
                or event.canvas is None
                or self.clickCount == 1
                or self.flagMouseClicked):
            return

        self.vLineRect.remove()
        event.canvas.draw()
        self.flagRectFocus = False
        self.flagRectLeftFocus = False
        self.flagRectRightFocus = False
        self.focusRect = None

    def onResize(self, event):
        pass

    # functionality for QPushButtons

    # functionality for the pushButtonOpen QPushButton
    # @todo on click open x files and read the data into specific array indicies
    def openButtonClicked(self):

        fileName, _ = QFileDialog.getOpenFileName(None, "Select File", "", "*.rgp")
        widget = WidgetGraph(self, fileName)
        self.ui.tabWidget.addTab(widget, widget.name)

    # functionality for the pushButtonSave QPushButton
    # @todo save stuff, duh
    def saveButtonClicked(self):
        print(self.dictMarker)
        print(self.listMarkerPreset)
        print("saveButtonClicked")

    # functionality for the pushButtonTabView QPushButton
    def tabButtonClicked(self):
        self.ui.stackedWidgetWorkArea.setCurrentIndex(0)

    # functionality for the pushButtonWindowView QPushButton
    def windowButtonClicked(self):
        self.ui.stackedWidgetWorkArea.setCurrentIndex(1)


    # event listener handling
    def windowClosedByUser(self):
        self.flagWindowClosedByUserSignal = True
    def windowClosedProgrammatically(self):
        self.flagWindowClosedByUserSignal = False

    # algorithms

    # function to check if event coordinates are close to a Rectangle and/or close to either side of that Rectangle
    # if close to Rectangle and not close to either side make that rectangle movable
    # if close to either side expand or shrink from respective side
    # @todo highlight either side if hovered or change mouse
    def checkIfClickByRect(self, event, rect):

        axisHeight = event.canvas.axes.get_ylim()[1]

        rectCent = rect.get_center()
        rectWidth = rect.get_width()

        epsilonSides = rectWidth * 0.10

        rightEndX, leftEndX = rectCent[0] + rectWidth / 2, rectCent[0] - rectWidth / 2
        disRight = np.sqrt((rightEndX - event.xdata) ** 2)
        disLeft = np.sqrt((leftEndX - event.xdata) ** 2)

        rectX = rect.get_x()

        xRange = True if (rectX < event.xdata < rectX + rectWidth) else False
        yRange = True if (-20 < event.ydata <= axisHeight*self.percMarkerFocusHeight/100) else False
        print(xRange, yRange)
        self.flagRectLeftFocus = True if ((disLeft < epsilonSides) and yRange) else False
        self.flagRectRightFocus = True if ((disRight < epsilonSides) and yRange) else False
        self.flagRectFocus = (
                xRange and yRange and not self.flagRectLeftFocus and not self.flagRectRightFocus)

        return self.flagRectLeftFocus or self.flagRectRightFocus or self.flagRectFocus


    def addRectToCurrentCanv(self, event):


        anchorX = self.xDataForMarker
        width = event.xdata - self.xDataForMarker
        axisHeight = event.canvas.axes.get_ylim()[1]
        # if length of listReactByCanvInd is smaller than currentCanvasInd create a new list for that canvas
        # else select the already existing list
        tmpListRect = self.dictCanvasToRectList[event.canvas]

        tmpRect = Rectangle((anchorX, -axisHeight*0.8/100), width, - axisHeight * self.heightRectMarkPerc / 100)
        tmpRect.set_color(self.colorRect)
        tmpListRect.append((tmpRect, self.nameRectMark))

        # self.updateMarkerRectSave(event.canvas, tmpRect, argColorName=self.colorRect)
        self.dictMarkerRectSetupData.update({tmpRect: [[tmpRect.xy, tmpRect.get_width()], [self.nameRectMark]]})

        event.canvas.axes.add_patch(tmpRect)
        event.canvas.draw()

        event.canvas.parent().addTableMarkerEntry(len(tmpListRect)-1, self.nameRectMark,
                                                  self.colorRect, round(anchorX, 2), round(event.xdata, 2))


    def addMarkerToTable(self, currentCanvas):
        ind = len(self.dictCanvasToRectList[currentCanvas])



# TDL functions I use for things


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
