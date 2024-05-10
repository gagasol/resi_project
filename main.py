# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtCore import Qt, QEventLoop, QPoint, QRect
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QFileDialog, QMdiArea, QMdiSubWindow
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


class CustomRectangle(matplotlib.patches.Rectangle):
    def __init__(self, xy, width, height, index, name):
        super().__init__(xy, width, height)
        self.index = index
        self.name = name
        self.lastXPos = xy[0]

        self._rightRect = None
        self._leftRect = None

    # region getter and setter
    def getRightRect(self):
        return self._rightRect

    def setRightRect(self, custRect):
        print("Right set " + custRect.name)
        if (type(custRect) != CustomRectangle):
            raise Exception("rightRect must be of type CustomRectangle")

        self._rightRect = custRect

    def getLeftRect(self):
        return self._leftRect

    def setLeftRect(self, custRect):
        print("Left set " + custRect.name)
        if (type(custRect) != CustomRectangle):
            raise Exception("leftRect must be of type CustomRectangle")
        self._leftRect = custRect
    # endregion

    def move(self, dx, calledByScript=False):
        """
        moves a CustomRectangle by dx and corrects leftRect or rightRect if they're not None
        :param dx: the amount to move the x position
        :param calledByScript: boolean to make sure that the program doesn't change all rects but only a max of 3
        :return: None
        """
        self.lastXPos = self.get_x()
        self.set_x(self.get_x()+dx)
        self.resizeLinks(True)

    def resizeWidth(self, dw, direction, calledByScript=False):
        '''
        resizes a CustomRectangle by dw and corrects leftRect or rightRect if they are not None
        :param dw: change in width
        :param direction resize to the right, left
        :param calledByScript: boolean to make sure that the program doesn't change all rects but only a max of 3
        :return: None
        '''
        if (direction == "r"):
            self.set_width(self.get_width() + dw)
            self.resizeLinks(False, True)
            self.lastXPos = self.get_x()
        elif (direction == "l"):
            self.set_x(self.get_x() + dw)
            self.set_width(self.get_width() - dw)
            self.lastXPos = self.get_x()
            self.resizeLinks()


    def resizeLinks(self, flagMoves=False, flagSizeChanged=False):
            if (self._leftRect):
                self._leftRect.set_width(self.get_x() - self._leftRect.get_x())
            if (self._rightRect):
                if (flagSizeChanged):
                    newRectXEnd = self.get_x() + self.get_width()
                    oldRectXEnd = self._rightRect.get_x() + self._rightRect.get_width()
                    self._rightRect.set_width(oldRectXEnd - newRectXEnd)
                    self._rightRect.set_x(self.get_x() + self.get_width())
                elif (flagMoves):
                    self._rightRect.set_width(self._rightRect.get_width() - self.get_x() + self.lastXPos)
                    self._rightRect.set_x(self.get_x() + self.get_width())






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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # testing area TBD!!!

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

        # region data, counter, flags
        # @xDataForMarker variable that holds the first clicked position to draw a marker from that to the second click
        # @dict dictMarker dictionary containing a "String::Name: String::HexColor" pair to save all Marker
        # @list listMarkerPreset list containing all named presets where <key>:"name" corresponds to the name
        # @colorRect variable set by selectMarkerWindow that determines the color of a rectangle
        # @nameRectMark variable set by selectMarkerWindow is the name of a marker rectangle
        # @heightRectMarkPerc sets the height of the marker as percent of the y-axis
        # @percMarkerFocusHeight sets the height of the focus for the marker as a percent of the y-axis

        self.xDataForMarker = None

        self.dictMarker = {}
        self.listMarkerPreset = []
        self.colorRect = "#000000"
        self.nameRectMark = ""
        self.heightRectMarkPerc = 3
        self.percMarkerFocusHeight = 30

        self.dictCanvasToRectList = {}
        self.listGraphWidgets = []

        # counter
        # @variable clickCount counts to a max of 1, on 0 it sets the xDataForMarker var
        self.clickCount = 0

        # flags
        self.flagRectFocus = False
        self.flagRectLeftFocus = False
        self.flagRectRightFocus = False
        self.flagMouseClicked = False
        self.flagVerticalLine = True
        self.flagMarkerDragged = False
        self.flagMarkerChanges = False
        # endregion

    # button events
        # clicked events
        self.ui.pushButtonOpen.clicked.connect(self.openButtonClicked)
        self.ui.pushButtonSave.clicked.connect(self.saveButtonClicked)
        self.ui.pushButtonTabView.clicked.connect(self.tabButtonClicked)
        self.ui.pushButtonWindowView.clicked.connect(self.windowButtonClicked)

    # functionality for the matplotlib canvas

    def onMouseMove(self, event):
        if (event.inaxes):
            # Draw vertical line
            if (self.flagVerticalLine):
                self.vLineRect.set_x(event.xdata)

            # If left mouse button is clicked
            if (event.button == MouseButton.LEFT):
                # If flag for rectangle being focused is set, move the rectangle
                if (self.flagRectFocus):
                    self.flagMarkerDragged = True
                    self.clickCount = 0
                    self.focusRect.move(event.xdata - self.test_x_start)
                    self.snapOn(event.canvas, self.focusRect)
                    self.test_x_start = event.xdata

                # If flag for rectangle being focused on right side is set, resize rectangle from right
                elif (self.flagRectRightFocus):
                    self.clickCount = 0
                    self.focusRect.resizeWidth(event.xdata - self.test_x_start, "r")
                    self.snapOn(event.canvas, self.focusRect)
                    self.test_x_start = event.xdata

                # If flag for rectangle being focused on left side is set, resize rectangle from left
                elif (self.flagRectLeftFocus):
                    self.clickCount = 0
                    self.focusRect.resizeWidth(event.xdata - self.test_x_start, "l")
                    self.snapOn(event.canvas, self.focusRect)
                    self.test_x_start = event.xdata

            # Redraw canvas after processing actions
            event.canvas.draw()

    def onButtonPress(self, event):

        if (event.inaxes is None):
            return

        if (event.button == MouseButton.LEFT):
            self.flagMouseClicked = True

            self.test_x_start = event.xdata

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

        if (self.flagMarkerDragged):
            self.flagMarkerDragged = False
            event.canvas.draw()

        self.flagMouseClicked = False
        self.flagRectFocus = False
        self.focusRect = None
        self.flagRectLeftFocus = False
        self.flagRectRightFocus = False

    def onAxesEnter(self, event):
        self.vLineRect.set_visible(True)
        event.canvas.axes.add_patch(self.vLineRect)
        event.canvas.draw()


    def onAxesLeave(self, event):

        if (event is None
                or event.canvas is None
                or self.flagMouseClicked
                or self.clickCount == 1):
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
        self.listGraphWidgets.append(widget)
        #self.ui.tabWidget.addTab(widget, widget.name)

    # functionality for the pushButtonSave QPushButton
    # @todo save stuff, duh
    def saveButtonClicked(self):
        print(self.dictMarker)
        print(self.listMarkerPreset)
        print("saveButtonClicked")

    # functionality for the pushButtonTabView QPushButton
    def tabButtonClicked(self):
        if(self.ui.stackedWidgetWorkArea.currentIndex() != 0):
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
        self.flagRectLeftFocus = True if ((disLeft < epsilonSides) and yRange) else False
        self.flagRectRightFocus = True if ((disRight < epsilonSides) and yRange) else False
        self.flagRectFocus = (
                xRange and yRange and not self.flagRectLeftFocus and not self.flagRectRightFocus)

        return self.flagRectLeftFocus or self.flagRectRightFocus or self.flagRectFocus


    # @todo fix the potential problem when a marker gets draged over another completly
    # this leads tho those markers eating themselves
    def snapOn(self, canvas, focusRect):
        if (focusRect.getLeftRect() and focusRect.getRightRect()):
            return

        for tupleCanv in self.dictCanvasToRectList[canvas]:
            if (tupleCanv[0] == focusRect.getRightRect() or tupleCanv[0] == focusRect.getLeftRect()):
                return
            fixedRectXStart = tupleCanv[0].get_x()
            fixedRectRectXEnd = tupleCanv[0].get_x() + tupleCanv[0].get_width()
            focusRectXStart = focusRect.get_x()
            focusRectXEnd = focusRectXStart + focusRect.get_width()

            if (focusRect.getRightRect() is None and fixedRectXStart <= focusRectXEnd and focusRectXStart < fixedRectXStart):
                focusRect.setRightRect(tupleCanv[0])
                tupleCanv[0].setLeftRect(focusRect)
            elif (focusRect.getLeftRect() is None and focusRect.get_x() <= fixedRectRectXEnd and fixedRectRectXEnd < focusRectXEnd):
                focusRect.setLeftRect(tupleCanv[0])
                tupleCanv[0].setRightRect(focusRect)




    def addRectToCurrentCanv(self, event):

        width = event.xdata - self.xDataForMarker
        anchorX = self.xDataForMarker if width > 0 else event.xdata
        width = abs(width)
        axisHeight = event.canvas.axes.get_ylim()[1]
        tmpListRect = self.dictCanvasToRectList[event.canvas]



        tmpRect = CustomRectangle((anchorX, -axisHeight*0.8/100), width,
                                  - axisHeight * self.heightRectMarkPerc / 100, len(tmpListRect), self.nameRectMark)

        # @todo put this in a correctOverlap() function
        if (not self.adjustOverlay(event, tmpRect)):
            return

        tmpRect.set_color(self.colorRect)
        tmpListRect.append((tmpRect, self.nameRectMark))

        # self.updateMarkerRectSave(event.canvas, tmpRect, argColorName=self.colorRect)

        event.canvas.axes.add_patch(tmpRect)
        event.canvas.draw()

        event.canvas.parent().addTableMarkerEntry(len(tmpListRect)-1, self.nameRectMark,
                                                  self.colorRect, round(anchorX, 2), round(event.xdata, 2))



    # 90% of this function is actually redundant because CustomRectangles resizeLinks() can take of most of it
    # not gonna change that though.
    def adjustOverlay(self, event, tmpRect):
        try:
            newRectXStart = tmpRect.get_x()
            newRectXEnd = tmpRect.get_x()+tmpRect.get_width()

            for tupleCanv in self.dictCanvasToRectList[event.canvas]:

                if (tmpRect.get_width() < 0 or tupleCanv[0].get_width() < 0):
                    print("ERROR: the width of a rect is negative, something went horrible wrong!!!!")
                    return False

                oldRectXStart = tupleCanv[0].get_x()
                oldRectXEnd = tupleCanv[0].get_x()+tupleCanv[0].get_width()

                startInOld = oldRectXStart < newRectXStart <= oldRectXEnd
                endInOld = oldRectXStart < newRectXEnd <= oldRectXEnd
                if (startInOld ^ endInOld):

                    if (startInOld):
                        tupleCanv[0].set_width(newRectXStart-oldRectXStart)
                        tupleCanv[0].setRightRect(tmpRect)
                        tmpRect.setLeftRect(tupleCanv[0])
                    if (endInOld):
                        #tupleCanv[0].set_width(tupleCanv[0].get_width() - newRectXEnd - tupleCanv[0].get_x())
                        tupleCanv[0].set_width(oldRectXEnd-newRectXEnd)
                        tupleCanv[0].set_x(newRectXEnd)
                        tupleCanv[0].setLeftRect(tmpRect)
                        tmpRect.setRightRect(tupleCanv[0])

                elif (startInOld and endInOld):
                    return False

                elif (newRectXStart < oldRectXStart and oldRectXEnd < newRectXEnd):
                    tupleCanv[0].remove()
                    self.dictCanvasToRectList[event.canvas].remove(tupleCanv)
                    return True

        except IndexError:
            print("Index Error: Canvas list is empty.")

        return True


    def addMarkerToTable(self, currentCanvas):
        ind = len(self.dictCanvasToRectList[currentCanvas])



# TDL functions I use for things


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
