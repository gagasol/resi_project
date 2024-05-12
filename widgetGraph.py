# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QRadioButton, QCheckBox, QTableWidget, \
    QHeaderView, QAbstractScrollArea, QLabel, QTableWidgetItem
from PySide6 import QtWidgets

import numpy as np
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backend_bases import MouseButton

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEventLoop, QSizeF, QMarginsF, )
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform,
                           QPdfWriter, QPainter, QPageSize)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListView, QListWidget,
                               QListWidgetItem, QSizePolicy, QSpacerItem, QTextEdit,
                               QVBoxLayout, QWidget)

from dataModel import DataModel
from markerpresetwindow import MarkerPresetWindow


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.03, right=0.97, top=0.99, bottom=0.07)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class CustomRectangle(matplotlib.patches.Rectangle):
    # @todo add a saveDelete that accounts for the deleted element by adjusting the index and sets the new links
    # @todo while moving checkc if left or right marker gets to zero, if so stop
    def __init__(self, xy, width, height, index, name, canvas):
        super().__init__(xy, width, height)
        self.index = index
        self.name = name
        self.canvas = canvas

        self.lastXPos = xy[0]

        self._rightRect = None
        self._leftRect = None

    # region getter and setter
    def getRightRect(self):
        return self._rightRect

    def setRightRect(self, custRect):
        self._rightRect = custRect
        if (type(custRect) != CustomRectangle):
            pass#raise Exception("rightRect must be of type CustomRectangle")
        if (self._rightRect):
            pass#raise Exception("rightRect already set")
        self._rightRect = custRect

    def getLeftRect(self):
        return self._leftRect

    def setLeftRect(self, custRect):
        self._leftRect = custRect
        if (type(custRect) != CustomRectangle):
            pass#raise Exception("leftRect must be of type CustomRectangle")
        if (self._leftRect):
            pass#raise Exception("leftRect already set")
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
        self.updateTableMarker()
        self.resizeLinks(True)

    def resizeWidth(self, dw, direction, calledByScript=False):
        """
        resizes a CustomRectangle by dw and corrects leftRect or rightRect if they are not None
        :param dw: change in width
        :param direction resize to the right, left
        :param calledByScript: boolean to make sure that the program doesn't change all rects but only a max of 3
        :return: None
        """
        if (direction == "r"):
            self.set_width(self.get_width() + dw)
            self.updateTableMarker()
            self.resizeLinks(False, True)
            self.lastXPos = self.get_x()
        elif (direction == "l"):
            self.set_x(self.get_x() + dw)
            self.set_width(self.get_width() - dw)
            self.lastXPos = self.get_x()
            self.updateTableMarker()
            self.resizeLinks()


    def resizeLinks(self, flagMoves=False, flagSizeChanged=False):
            if (self._leftRect):
                self._leftRect.set_width(self.get_x() - self._leftRect.get_x())
                self._leftRect.updateTableMarker()
            if (self._rightRect):
                if (flagSizeChanged):
                    newRectXEnd = self.get_x() + self.get_width()
                    oldRectXEnd = self._rightRect.get_x() + self._rightRect.get_width()
                    self._rightRect.set_width(oldRectXEnd - newRectXEnd)
                    self._rightRect.set_x(self.get_x() + self.get_width())
                    self._rightRect.updateTableMarker()
                elif (flagMoves):
                    self._rightRect.set_width(self._rightRect.get_width() - self.get_x() + self.lastXPos)
                    self._rightRect.set_x(self.get_x() + self.get_width())
                    self._rightRect.updateTableMarker()



    def updateTableMarker(self):
        self.canvas.parent().parent().updateTableMarkerEntry(self.index, self.name, self.get_x(),
                                                    self.get_width() + self.get_x())


class AutoSizedTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(QHeaderView.Stretch)


    def resizeEvent(self, event):
        ratio = self.height() / self.rowCount() if self.rowCount() else 0
        for i in range(self.rowCount()):
            self.setRowHeight(i, ratio)


class WidgetGraph(QWidget):
    def __init__(self, MainWindow=None, pathToFile=None, parent=None):
        super().__init__(parent)

        # region settings variable
        self.heightWidgetTopPerc = 15
        self.heightWidgetGraphPerc = 75
        self.heightWidgetBottomPerc = 10
        self.heightRectMarkPerc = 3
        self.percMarkerFocusHeight = 20
        # endregion

        # marker variables
        self.dictCanvasToRectList = {}
        self.markerList = []

        self.vLineRect = None
        self.flagVerticalLine = True

        self.focusedMarker = None
        self.lastXPos = 0
        self.clickCount = 0

        self.markerName = None
        self.markerColor = None


        self.flagMarkerFocus = False
        self.flagMarkerRightFocus = False
        self.flagMarkerLeftFocus = False

        self.flagMarkerDragged = False
        self.flagMouseClicked = False

        self.flagWindowClosedByUserSignal = False
        # region tons of variables for the QTWidget
        self.labelData = None
        self.horizontalSpacer_3 = None
        self.checkBoxHideBot = None
        self.checkBoxHideTop = None
        self.horizontalLayout_3 = None
        self.widgetMenu = None
        self.horizontalSpacer_2 = None
        self.textEditComment = None
        self.listWidgetAnalysis = None
        self.horizontalLayout_2 = None
        self.widgetBottom = None
        self.widgetGraph = None
        self.canvasGraph = None
        self.horizontalSpacer = None
        self.tableWidgetData = None
        self.horizontalLayout = None
        self.widgetTop = None
        self.verticalLayout_2 = None
        self.measurementDrillDepth = None
        self.verticalLayout = None
        self.widgetDataTop = None
        self.horizontalSpacer0 = None
        # endregion
# data variables setup
        self._name = None

        self.dataDrill = []
        self.dataFeed = []

        self.listDataAll = []
        self.dictMeasurementData = {}

        self.strsToShowInGraph = []

# arg variables
        self.mainWindow = MainWindow
        self.pathToFile = pathToFile

# initialize Data and Ui
        if (self.mainWindow):
            self.data = DataModel(pathToFile, self.mainWindow.listNameKeys)
            pyplot.style.use('ggplot')
            self.setUpUi()
            self.setupTable()

            self.vLineRect = self.canvasGraph.axes.axvline(color='black', lw=0.8, linestyle='-')


    def resizeEvent(self, event):
        # this is neccecary because matplotlib doesn't resize linear or whatever, need to look into that and find
        # a better way to resize the window, right now using a fitted function is the best way to go I guess
        # sorry for people that have a resolution wider than full HD LOL
        leftMargin = self.reciprocal_func(self.mainWindow.width(), "l")
        bottomMargin = self.reciprocal_func(self.mainWindow.height(), "b")

        #self.canvasGraph.figure.subplots_adjust(left=mainWidth*slope+yIntercept)
        self.canvasGraph.figure.subplots_adjust(left=leftMargin, bottom=bottomMargin)
        self.canvasGraph.draw()


    def setUpUi(self):

        self._name, deviceLength, dataDrill, dataFeed = self.data.getGraphData()

        self.verticalLayout_2 = QVBoxLayout()
        self.widgetTop = QWidget()
        self.widgetTop.setObjectName(u"widgetTop")
        self.widgetTop.setMinimumSize(QSize(0, 0))
        self.widgetTop.setMaximumSize(QSize(16777215, 999999))
        self.widgetTop.setStyleSheet(u"QListWidget{background:lightblue; spacing: 0;}")
        self.horizontalLayout = QHBoxLayout(self.widgetTop)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer0 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer0)

        self.widgetDataTop = QWidget(self.widgetTop)
        self.widgetDataTop.setObjectName(u"widget")

        self.verticalLayout = QVBoxLayout(self.widgetDataTop)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.labelData = QLabel(self.widgetDataTop)
        self.labelData.setObjectName(u"labelData")
        self.labelData.setText("Mess- / Objektdaten")
        self.labelData.setMaximumSize(QSize(10000000, 20))

        self.tableWidgetData = AutoSizedTable(self.widgetDataTop)
        self.tableWidgetData.setObjectName(u"tableWidgetData")
        self.tableWidgetData.setMinimumSize(QSize(0, 0))
        self.tableWidgetData.setMaximumSize(QSize(1000, 150))
        self.tableWidgetData.setAutoScroll(False)
        self.tableWidgetData.setProperty("isWrapping", True)
        self.tableWidgetData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidgetData.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tableWidgetData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetData.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidgetData.setShowGrid(False)
        self.tableWidgetData.horizontalHeader().setVisible(False)
        self.tableWidgetData.verticalHeader().setVisible(False)
        self.tableWidgetData.setColumnCount(3)
        self.tableWidgetData.setRowCount(6)
        self.tableWidgetData.verticalHeader().setMinimumSectionSize(0)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetData.sizePolicy().hasHeightForWidth())

        self.tableWidgetData.setSizePolicy(sizePolicy)

        self.tableWidgetData.setStyleSheet("QTableView::item:selected {background: none;}")

        for i in range(6):
            self.tableWidgetData.setRowHeight(i, 50)

        self.verticalLayout.addWidget(self.labelData)
        self.verticalLayout.addWidget(self.tableWidgetData)

        self.widgetDataTop.setLayout(self.verticalLayout)

        self.horizontalLayout.addWidget(self.widgetDataTop)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.widgetTop.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.widgetTop)

        self.canvasGraph = MplCanvas(self, width=19, height=10, dpi=100)
        self.canvasGraph.axes.set_ylim(-5, 100)
        self.canvasGraph.axes.set_xlabel('Depth')
        self.canvasGraph.axes.set_ylabel('Data')
        # @todo remove later
        deviceLength = float(deviceLength)
        self.canvasGraph.axes.set_xlim(0, deviceLength+0.1)
        step = deviceLength / len(dataDrill)
        x = np.arange(0, deviceLength, step)
        self.canvasGraph.axes.plot(x, dataDrill, linewidth=0.7)
        self.canvasGraph.axes.plot(x, dataFeed, linewidth=0.7)
        self.canvasGraph.figure.subplots_adjust(left=0.036, bottom=0.2490168523424322, right=0.98, top=0.98)
        # left on start left=0.049 ; bottom=0.155 1277 1920
        # Coordinates left : 1920/0.035 1277/0.049 265/0.28
        # Coordinates bot : 1017/0.035 502/0.25
        self.canvasGraph.draw()

        if (self.mainWindow):
            self.canvasGraph.mpl_connect('motion_notify_event', self.onMouseMove)
            self.canvasGraph.mpl_connect('button_press_event', self.onButtonPress)
            self.canvasGraph.mpl_connect('button_release_event', self.onButtonReleased)
            self.canvasGraph.mpl_connect('figure_enter_event', self.onAxesEnter)
            #self.test_canvas.mpl_connect('axes_leave_event', self.onAxesLeave)
            self.canvasGraph.mpl_connect('figure_leave_event', self.onAxesLeave)
            self.canvasGraph.mpl_connect('scroll_event', self.zoomOnMouseWheel)
            #self.canvasGraph.mpl_connect('resize_event', self.onResize)

            #self.dictCanvasToRectList.update({self.canvasGraph: []})

        self.widgetGraph = QWidget()
        self.widgetGraph.setObjectName(u"widgetGraph")

        self.verticalLayout_3 = QVBoxLayout(self.widgetGraph)
        self.verticalLayout_3.addWidget(self.canvasGraph)
        self.verticalLayout_3.setSpacing(5)

        self.widgetGraph.setLayout(self.verticalLayout_3)
        #self.widgetGraph.setStyleSheet("border: 1px solid black;")

        self.widgetGraph.setMinimumHeight(200)

        self.verticalLayout_2.addWidget(self.widgetGraph)

        self.widgetBottom = QWidget()
        self.widgetBottom.setObjectName(u"widgetBottom")
        self.widgetBottom.setContentsMargins(0, 0, 0, 0)
        self.widgetBottom.setMinimumSize(QSize(0, 0))
        self.widgetBottom.setMaximumSize(QSize(16777215, 999999))
        self.horizontalLayout_2 = QHBoxLayout(self.widgetBottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.tableWidgetMarker = AutoSizedTable(self.widgetBottom)
        self.tableWidgetMarker.setObjectName(u"tableWidgetMarker")
        self.tableWidgetMarker.setMinimumSize(QSize(0, 0))
        self.tableWidgetMarker.setMaximumSize(QSize(1000, 150))
        self.tableWidgetMarker.setAutoScroll(False)
        self.tableWidgetMarker.setProperty("isWrapping", True)
        self.tableWidgetMarker.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidgetMarker.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.tableWidgetMarker.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetMarker.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidgetMarker.setShowGrid(False)
        self.tableWidgetMarker.horizontalHeader().setVisible(False)
        self.tableWidgetMarker.verticalHeader().setVisible(False)
        self.tableWidgetMarker.setColumnCount(1)
        self.tableWidgetMarker.setRowCount(6)
        self.tableWidgetMarker.verticalHeader().setMinimumSectionSize(0)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidgetData.sizePolicy().hasHeightForWidth())
        self.tableWidgetMarker.setStyleSheet("""QTableView::item:selected {background: none;}""")
        self.tableWidgetMarker.setSizePolicy(sizePolicy2)

        self.tableWidgetMarker.setStyleSheet("QTableView::item{font: 12pt \"Bahnschrift\" Condensed;}")

        self.horizontalLayout_2.addWidget(self.tableWidgetMarker)

        self.horizontalSpacer_2 = QSpacerItem(369, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.textEditComment = QTextEdit(self.widgetBottom)
        self.textEditComment.setObjectName(u"textEditComment")
        self.textEditComment.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_2.addWidget(self.textEditComment)
        self.widgetBottom.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.widgetBottom)


        self.widgetMenu = QWidget()
        self.widgetMenu.setMaximumHeight(35)

        self.horizontalLayout_3 = QHBoxLayout()

        self.checkBoxHideTop = QCheckBox(self.widgetMenu)
        self.checkBoxHideTop.setObjectName(u"radioButtonHideTop")
        self.checkBoxHideTop.setText("")
        self.checkBoxHideTop.checkStateChanged.connect(self.toggleHideTop)

        self.checkBoxHideBot = QCheckBox(self.widgetMenu)
        self.checkBoxHideBot.setObjectName(u"radioButtonHideTop")
        self.checkBoxHideBot.setText("")
        self.checkBoxHideBot.checkStateChanged.connect(self.toggleHideBot)

        self.horizontalSpacer_3 = QSpacerItem(200, 35, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)
        self.horizontalLayout_3.addWidget(self.checkBoxHideTop)
        self.horizontalLayout_3.addWidget(self.checkBoxHideBot)

        self.widgetMenu.setLayout(self.horizontalLayout_3)

        self.verticalLayout_2.addWidget(self.widgetMenu)

        self.setContentsMargins(0, 0, 0, 0)

        sizePolicyMT = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicyMT.setHorizontalStretch(0)
        sizePolicyMT.setVerticalStretch(0)#self.heightWidgetTopPerc)
        sizePolicyMT.setHeightForWidth(self.widgetTop.sizePolicy().hasHeightForWidth())
        self.widgetTop.setSizePolicy(sizePolicyMT)

        sizePolicyMG = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicyMG.setHorizontalStretch(0)
        sizePolicyMG.setVerticalStretch(0)#self.heightWidgetGraphPerc)
        sizePolicyMG.setHeightForWidth(self.widgetTop.sizePolicy().hasHeightForWidth())
        self.widgetTop.setSizePolicy(sizePolicyMG)

        sizePolicyMB = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicyMB.setHorizontalStretch(0)
        sizePolicyMB.setVerticalStretch(0)#self.heightWidgetBottomPerc)
        sizePolicyMB.setHeightForWidth(self.widgetBottom.sizePolicy().hasHeightForWidth())
        self.widgetBottom.setSizePolicy(sizePolicyMB)

        self.verticalLayout_2.setStretchFactor(self.widgetTop, self.heightWidgetTopPerc)
        self.verticalLayout_2.setStretchFactor(self.widgetBottom, self.heightWidgetBottomPerc)
        self.verticalLayout_2.setStretchFactor(self.widgetGraph, self.heightWidgetGraphPerc)
        self.setLayout(self.verticalLayout_2)


    def setupTable(self):
        i, j = 0, 0
        for entry in self.data.getTablaTopData():
            self.tableWidgetData.setItem(i % 6, j // 6, entry)
            i, j = i + 1, j + 1


    # functionality for the matplotlib canvas
    def onMouseMove(self, event):
        # @todo create a global variable called backMarker and frontMarker which will be set with the next markers
        # in each direction of focusMarker after a marker got focused
        # then change snapOn() to check for 2 variables instead of the entire dict
        # kinda useless for this application but save them bytes where you can
        if (event.inaxes):
            # Draw vertical line
            if (self.flagVerticalLine):
                self.vLineRect.set_xdata(event.xdata)
                self.vLineRect.set_visible(True)
                event.canvas.draw()

            # If left mouse button is clicked
            if (event.button == MouseButton.LEFT):
                # If flag for rectangle being focused is set, move the rectangle
                if (self.flagMarkerFocus):
                    self.flagMarkerDragged = True
                    self.clickCount = 0
                    self.focusedMarker.move(event.xdata - self.lastXPos)
                    self.snapOn(event.canvas, self.focusedMarker)
                    self.updateTableMarkerEntry(self.focusedMarker.index, self.focusedMarker.name, self.focusedMarker.get_x(),
                                                self.focusedMarker.get_width() + self.focusedMarker.get_x())
                    self.lastXPos = event.xdata

                # If flag for rectangle being focused on right side is set, resize rectangle from right
                elif (self.flagMarkerRightFocus):
                    self.clickCount = 0
                    self.focusedMarker.resizeWidth(event.xdata - self.lastXPos, "r")
                    self.snapOn(event.canvas, self.focusedMarker)
                    self.lastXPos = event.xdata

                # If flag for rectangle being focused on left side is set, resize rectangle from left
                elif (self.flagMarkerLeftFocus):
                    self.clickCount = 0
                    self.focusedMarker.resizeWidth(event.xdata - self.lastXPos, "l")
                    self.snapOn(event.canvas, self.focusedMarker)
                    self.lastXPos = event.xdata

            if (event.button == 2):
                ax = self.canvasGraph.axes
                xMin, xMax = ax.get_xlim()
                diff = xMax - xMin
                delta = 1 / 20 * diff
                if (event.xdata > self.lastXPos):
                    ax.set_xlim(xMin + delta, xMax + delta)
                else:
                    ax.set_xlim(xMin - delta, xMax - delta)
                self.canvasGraph.draw()

            self.lastXPos = event.xdata
            # Redraw canvas after processing actions
            event.canvas.draw()

    def onButtonPress(self, event):

        if (event.inaxes is None):
            return

        if (event.button == MouseButton.LEFT):
            self.flagMouseClicked = True

            self.lastXPos = event.xdata

            # check if any marker rectangle is close by
            # @todo add the loop to the function and just call the function
            if (self.markerList is not []):
                for marker in self.markerList:
                    if self.checkIfClickByRect(event, marker):
                        self.focusedMarker = marker
                        return

        # logic for creating markers with addRectToCurrentCanv
            if (not (self.flagMarkerFocus or self.flagMarkerLeftFocus or self.flagMarkerRightFocus)):

                if (self.clickCount == 0):
                    self.xPosMarkerStart = event.xdata

                elif (self.clickCount == 1):
                    markerWindow = MarkerPresetWindow(self, {})
                    markerWindow.setAttribute(Qt.WA_DeleteOnClose)
                    markerWindow.show()
                    markerWindow.destroyed.emit()

                    waitForMarkerInputLoop = QEventLoop()
                    markerWindow.closedByUser.connect(self.windowClosedByUser)
                    markerWindow.closedProgrammatically.connect(self.windowClosedProgrammatically)
                    markerWindow.destroyed.connect(waitForMarkerInputLoop.quit)
                    waitForMarkerInputLoop.exec()

                    if (not self.flagWindowClosedByUserSignal):
                        self.addRectToCurrentCanv(event)

                    self.flagMouseClicked = False

                self.clickCount = self.clickCount + 1 if (self.clickCount < 1) else 0


        if (event.button == MouseButton.RIGHT):
            self.canvasGraph.axes.set_xlim(event.xdata)

    def onButtonReleased(self, event):

        if (self.flagMarkerDragged):
            self.flagMarkerDragged = False
            event.canvas.draw()

        self.flagMouseClicked = False
        self.flagMarkerFocus = False
        self.focusedMarker = None
        self.flagMarkerLeftFocus = False
        self.flagMarkerRightFocus = False

    def zoomOnMouseWheel(self, event):

        ax = self.canvasGraph.axes
        xdata = event.xdata
        ydata = event.ydata
        baseScale = 2.

        if event.button == 'down':
            scaleFactor = 1 / baseScale
        elif event.button == 'up':
            scaleFactor = baseScale
        else:
            scaleFactor = 1

        ax.set_xlim([xdata - (xdata - ax.get_xlim()[0]) / scaleFactor,
                     xdata + (ax.get_xlim()[1] - xdata) / scaleFactor])

        self.canvasGraph.draw()

    def onAxesEnter(self, event):
        self.vLineRect.set_visible(True)
        self.vLineRect.set_visible(True)
        event.canvas.draw()

    def onAxesLeave(self, event):

        if (event is None
                or event.canvas is None
                or self.flagMouseClicked
                or self.clickCount == 1):
            return

        self.vLineRect.set_visible(False)
        event.canvas.draw()
        self.flagMarkerFocus = False
        self.flagMarkerLeftFocus = False
        self.flagMarkerRightFocus = False
        self.focusedMarker = None


    def windowClosedByUser(self):
        self.flagWindowClosedByUserSignal = True
    def windowClosedProgrammatically(self):
        self.flagWindowClosedByUserSignal = False

    # region marker functionality

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
        self.flagMarkerLeftFocus = True if ((disLeft < epsilonSides) and yRange) else False
        self.flagMarkerRightFocus = True if ((disRight < epsilonSides) and yRange) else False
        self.flagMarkerFocus = (
                xRange and yRange and not self.flagMarkerLeftFocus and not self.flagMarkerRightFocus)

        return self.flagMarkerLeftFocus or self.flagMarkerRightFocus or self.flagMarkerFocus


    def snapOn(self, canvas, focusRect):
        if (focusRect.getLeftRect() and focusRect.getRightRect()):
            return

        for marker in self.markerList:
            if (marker == focusRect.getRightRect() or marker == focusRect.getLeftRect()):
                return
            fixedRectXStart = marker.get_x()
            fixedRectRectXEnd = marker.get_x() + marker.get_width()
            focusRectXStart = focusRect.get_x()
            focusRectXEnd = focusRectXStart + focusRect.get_width()

            if (focusRect.getRightRect() is None and focusRectXEnd >= fixedRectXStart > focusRectXStart):
                focusRect.setRightRect(marker)
                marker.setLeftRect(focusRect)
            elif (focusRect.getLeftRect() is None and focusRect.get_x() <= fixedRectRectXEnd < focusRectXEnd):
                focusRect.setLeftRect(marker)
                marker.setRightRect(focusRect)


    # @todo handle the marker setup in the widget graph because its the only place its used
    def addRectToCurrentCanv(self, event):

        width = event.xdata - self.xPosMarkerStart
        anchorX = self.xPosMarkerStart if width > 0 else event.xdata
        width = abs(width)
        axisHeight = event.canvas.axes.get_ylim()[1]
        tmpListRect = self.markerList



        tmpRect = CustomRectangle((anchorX, -axisHeight*0.8/100), width,
                                  - axisHeight * self.heightRectMarkPerc / 100, len(tmpListRect),
                                  self.markerName, event.canvas)

        if (not self.adjustOverlay(event, tmpRect)):
            return

        tmpRect.set_color(self.markerColor)
        tmpListRect.append(tmpRect)

        # self.updateMarkerRectSave(event.canvas, tmpRect, argColorName=self.colorRect)

        event.canvas.axes.add_patch(tmpRect)
        event.canvas.draw()

        self.addTableMarkerEntry(len(tmpListRect) - 1, self.markerName, self.markerColor, round(anchorX, 2),
                                 round(event.xdata, 2))


    # 90% of this function is actually redundant because CustomRectangles resizeLinks() can take of most of it
    # not gonna change that though.
    # also @todo add this to widgetGraph as well
    def adjustOverlay(self, event, tmpRect):
        try:
            newRectXStart = tmpRect.get_x()
            newRectXEnd = tmpRect.get_x()+tmpRect.get_width()

            for marker in self.markerList:

                if (tmpRect.get_width() < 0 or marker.get_width() < 0):
                    print("ERROR: the width of a rect is negative, something went horrible wrong!!!!")
                    return False

                oldRectXStart = marker.get_x()
                oldRectXEnd = marker.get_x()+marker.get_width()

                startInOld = oldRectXStart < newRectXStart <= oldRectXEnd
                endInOld = oldRectXStart < newRectXEnd <= oldRectXEnd
                if (startInOld ^ endInOld):

                    if (startInOld):
                        marker.set_width(newRectXStart-oldRectXStart)
                        marker._rightRect = None
                        marker.setRightRect(tmpRect)
                        tmpRect._leftRect = None
                        tmpRect.setLeftRect(marker)
                    if (endInOld):
                        # marker.set_width(marker.get_width() - newRectXEnd - marker.get_x())
                        marker.set_width(oldRectXEnd - newRectXEnd)
                        marker.set_x(newRectXEnd)
                        marker.setLeftRect(None)
                        marker.setLeftRect(tmpRect)
                        tmpRect._rightRect = None
                        tmpRect.setRightRect(marker)

                elif (startInOld and endInOld):
                    return False

                elif (newRectXStart < oldRectXStart and oldRectXEnd < newRectXEnd):
                    if (marker.getRightRect()):
                        marker.getRightRect().setLeftRect(None)
                    if (marker.getLeftRect()):
                        marker.getLeftRect().setRightRect(None)

                    marker.remove()
                    self.markerList.remove(marker)
                    return True

        except IndexError:
            print("Index Error: Canvas list is empty.")

        return True

    # endregion

    def addTableMarkerEntry(self, index, name, color, x, dx):
        # @todo overload class to get a on_item_changed(self, item) signal and use it to change the markers
        pixmap = QPixmap(30, 30)
        pixmap.fill(QColor(color))
        icon = QIcon(pixmap)

        if(index >= 6):
            if (index%6 == 0):
                n = self.tableWidgetMarker.columnCount()
                self.tableWidgetMarker.setColumnCount(n+1)

        item = QTableWidgetItem(name + "\t: {0} - {1}".format(x, dx))
        item.setIcon(icon)
        self.tableWidgetMarker.setItem(index % 6, index // 6, item)


    def updateTableMarkerEntry(self, index, name, x, dx):
        try:
            color = self.mainWindow.dictMarker[name]
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor(color))
            icon = QIcon(pixmap)

            item = QTableWidgetItem(name + "\t: {0} - {1}".format(round(x, 2), round(dx, 2)))
            item.setIcon(icon)
            self.tableWidgetMarker.setItem(index % 6, index // 6, item)


        except KeyError:
            print("Not in dic")


    def changeAxisLim(self, side, xLim=None, yLim=None):
        x_Lim = xLim if xLim is not None else self.canvasGraph.axes.get_xlim()
        y_Lim = xLim if yLim is not None else self.canvasGraph.axes.get_ylim()
        self.canvasGraph.axes.set_xlim(x_Lim)
        self.canvasGraph.axes.set_ylim(y_Lim)
        self.canvasGraph.draw()


    def toggleHideTop(self):
        rndmBool = (self.checkBoxHideTop.checkState() == Qt.Checked)
        self.widgetTop.hide() if rndmBool else self.widgetTop.show()

    def toggleHideBot(self):
        rndmBool = (self.checkBoxHideBot.checkState() == Qt.Checked)
        self.widgetBottom.hide() if rndmBool else self.widgetBottom.show()

    def hideEverything(self):
        self.widgetTop.hide()
        self.widgetBottom.hide()

    def showEverything(self):
        self.widgetTop.show()
        self.widgetBottom.show()
        self.widgetRight.show()


    # had to make this function in order to resize the matplotlib because I guess it takes the axes values not the pixel
    def reciprocal_func(self, x, side):
        if side == "l":
            a, b, c = 306479, 4138.91, -0.00757828
        elif side == "b":
            a, b, c = 355871, 2004.66, -0.10082
        else:
            return 0

        return a / (b*x) + c

# @todo put the create marker function in here for loading and saving reasons