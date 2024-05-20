# This Python file uses the following encoding: utf-8
import json
import logging
import sys

from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QRadioButton, QCheckBox, QTableWidget, \
    QHeaderView, QAbstractScrollArea, QLabel, QTableWidgetItem, QDialog
from PySide6 import QtWidgets

import numpy as np
import matplotlib
from matplotlib import pyplot, ticker
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
from pickMarkerWindow import PickMarker


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.03, right=0.97, top=0.99, bottom=0.07)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class CustomRectangle(matplotlib.patches.Rectangle):
    # @todo add a saveDelete that accounts for the deleted element by adjusting the index and sets the new links
    # @todo while moving checkc if left or right marker gets to zero, if so stop
    def __init__(self, xy, width, height, index, name, color, canvas):
        super().__init__(xy, width, height)
        self.index = index
        self.name = name
        self.canvas = canvas
        self.color = color

        self.lastXPos = xy[0]

        self._rightRect = None
        self._leftRect = None

        self._nextRectInSortedList = None
        self._lastRectInSortedList = None

        self.set_color(color)

    # region getter and setter
    def get_x1(self):
        return self.get_x() + self.get_width()

    def getNextRectInList(self):
        return self._nextRectInSortedList

    def setNextRectInList(self, custRect):
        logging.debug("~~~~~~~~~~~~ setNextRectInList ~~~~~~~~~~~~\n"
                      " Self: {0} \n Next: {1}".format(custRect, self._nextRectInSortedList))
        self._nextRectInSortedList = custRect

    def getLastRectInList(self):
        return self._lastRectInSortedList

    def setLastRectInList(self, custRect):
        logging.debug("~~~~~~~~~~~~ setLastRectInList ~~~~~~~~~~~~\n"
                      " Self: {0} \n Next: {1}".format(custRect, self._lastRectInSortedList))
        self._lastRectInSortedList = custRect

    def getRightRect(self):
        return self._rightRect

    def setRightRect(self, custRect):
        logging.debug("~~~~~~~~~~~~ setRightRect ~~~~~~~~~~~~\n"
                      " Self: {0} \n Right: {1}".format(custRect, self._rightRect))
        if (custRect == None):
            self._rightRect = None
            return
        if (self._rightRect != None):
            raise Exception("{0} has rightRect already set".format(self))
        self._rightRect = custRect

    def getLeftRect(self):
        return self._leftRect

    def setLeftRect(self, custRect):
        logging.debug("~~~~~~~~~~~~ setLeftRect ~~~~~~~~~~~~\n"
                      " Self: {0} \n Left: {1}".format(custRect, self._leftRect))
        if (custRect == None):
            self._leftRect = None
            return
        if (self._leftRect != None):
            raise Exception("{0} has leftRect already set".format(self))
        self._leftRect = custRect
    # endregion

    def getSaveState(self):
        state = {
            'index': self.index,
            'name': self.name,
            'color': self.color,
            'x': self.get_x(),
            'width': self.get_width()
        }
        return state

    def move(self, dx, calledByScript=False):
        """
        moves a CustomRectangle by dx and corrects leftRect or rightRect if they're not None
        :param dx: the amount to move the x position
        :param calledByScript: boolean to make sure that the program doesn't change all rects but only a max of 3
        :return: None
        """
        if (calledByScript):
            if (dx > 0):
                self.resizeRightRect(dx, False)
            else:
                self.resizeLeftRect(dx)


        self.lastXPos = self.get_x()
        self.set_x(self.get_x()+dx)
        self.updateTableMarker()

        if (not calledByScript):
            self.resizeLinks(dx, flagMoves=True)

    def resizeWidth(self, dw, direction, calledByScript=False):
        """
        resizes a CustomRectangle by dw and corrects leftRect or rightRect if they are not None
        :param dw: change in width
        :param direction resize to the right, left
        :param calledByScript: boolean to make sure that the program doesn't change all rects but only a max of 3
        :return: None
        """
        if(self._width - abs(dw) <= 0.1):
            return

        if (direction == "r"):
            self.set_width(self.get_width() + dw)
            self.updateTableMarker()
            self.resizeRightRect(dw, False)
            self.lastXPos = self.get_x()
        elif (direction == "l"):
            self.set_x(self.get_x() + dw)
            self.set_width(self.get_width() - dw)
            self.lastXPos = self.get_x()
            self.updateTableMarker()
            self.resizeLeftRect(dw)


    def resizeLinks(self, dx, flagMoves=False, flagSizeChanged=False):
            if (self._leftRect):
                if (self._leftRect.get_width()-abs(dx) <= 0.01 and dx < 0):
                    self._leftRect.move(dx, True)
                else:
                    self._leftRect.set_width(self.get_x() - self._leftRect.get_x())

                self._leftRect.updateTableMarker()

            if (self._rightRect):
                if (self._rightRect and self._rightRect.get_width()-abs(dx) <= 0.01 and dx > 0):
                    self._rightRect.move(dx, True)
                else:
                    if (flagSizeChanged):
                        newRectXEnd = self.get_x() + self.get_width()
                        oldRectXEnd = self._rightRect.get_x() + self._rightRect.get_width()
                        self._rightRect.set_width(oldRectXEnd - newRectXEnd)
                        self._rightRect.set_x(self.get_x() + self.get_width())
                    elif (flagMoves):
                        self._rightRect.set_width(self._rightRect.get_width() - self.get_x() + self.lastXPos)
                        self._rightRect.set_x(self.get_x() + self.get_width())

                self._rightRect.updateTableMarker()

    def resizeLeftRect(self, dx):
        if (self._leftRect):
            if (self._leftRect.get_width() - abs(dx) <= 0.01):
                self._leftRect.move(dx, True)
            else:
                self._leftRect.set_width(self.get_x() - self._leftRect.get_x())

            self._leftRect.updateTableMarker()


    def resizeRightRect(self, dx, flagMoves):
        if (self._rightRect):
            if (self._rightRect.get_width()-abs(dx) <= 0.01 and dx > 0):
                self._rightRect.move(dx, True)
            else:
                if (flagMoves):
                    self._rightRect.set_width(self._rightRect.get_width() - self.get_x() + self.lastXPos)
                    self._rightRect.set_x(self.get_x() + self.get_width())
                else:
                    newRectXEnd = self.get_x() + self.get_width()
                    oldRectXEnd = self._rightRect.get_x() + self._rightRect.get_width()
                    self._rightRect.set_width(oldRectXEnd - newRectXEnd)
                    self._rightRect.set_x(self.get_x() + self.get_width())

            self._rightRect.updateTableMarker()



    def updateTableMarker(self):
        self.canvas.parent().parent().updateTableMarkerEntry(self.index, self.name, self.get_x(),
                                                    self.get_x1())


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
    def __init__(self, MainWindow=None, pathToFile=None, loadedState=None, settingsSet=None, parent=None):
        super().__init__(parent)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

        file_handler.setFormatter(formatter)

        # add file handler to logger
        self.logger.addHandler(file_handler)

        # @todo add getter and setter for each of these variables
        # region settings variable
        self.verticalLayout_3 = None
        self.tableWidgetMarker = None
        self.heightWidgetTopPerc = 15
        self.heightWidgetGraphPerc = 75
        self.heightWidgetBottomPerc = 10
        self.heightRectMarkPerc = 3
        self.percMarkerFocusHeight = 5
        # endregion

        # marker variables
        self.markerList = []
        self.defaultMarkerDictName = ""

        self.deviceLength = None

        self.dxMarkerForTable = 0
        self.flagSetDxForMarker = False

        self.vLineRect = None
        self.flagVerticalLine = True

        self.showMarkingAreaRect = matplotlib.patches.Rectangle((0, - 10), 20, 200, facecolor="white",
                                                                alpha=0.5)
        self.showMarkingAreaRect.set_visible(False)

        self.focusedMarker = None
        self.lastXPos = 0
        self.xPosMarkerStart = 0
        self.clickCount = 0

        self.markerName = None
        self.markerColor = None

        self.canvasColor = None

        self.flagMarkerFocus = False
        self.flagMarkerRightFocus = False
        self.flagMarkerLeftFocus = False

        self.flagMarkerDragged = False
        self.flagMouseClicked = False

        self.flagShiftHeld = False
        self.flagShiftHeld = False
        self.flagMarking = False

        self.flagWindowClosedByUserSignal = False

        self.lockMarkerStart = False

        self.currentCursor = None

        self.maxLenColumns = []
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
        self.name = None

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
            if ("rgp" in pathToFile):
                self.dataModel = DataModel(pathToFile, self.mainWindow.listNameKeys)
            if (pathToFile == ""):
                self.dataModel = DataModel(pathToFile, self.mainWindow.listNameKeys, loadedState)


            self.defaultMarkerDictName = self.mainWindow.defaultPresetName
            pyplot.style.use('ggplot')
            self.setUpUi()
            self.setupTable()
            self.canvasColor = self.canvasGraph.axes.get_facecolor()
            self.canvasGraph.axes.add_patch(self.showMarkingAreaRect)
            self.toolbar = NavigationToolbar(self.canvasGraph, None)
            if (pathToFile==""):
                for markerState in self.dataModel.markerStateList:
                    self.addRectToCurrentCanv(None, markerState)
                    self.setDxForMarker(self.dataModel.dx_xlim)

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Alt and event.modifiers() == Qt.AltModifier:
            self.flagMarking = not self.flagMarking
            self.showMarkingOnScreen(self.flagMarking)
            self.showMarkingAreaRect.set_x(self.lastXPos)
            self.showMarkingAreaRect.set_width(0)
            self.clickCount = 0
            if (self.flagMarking):
                self.canvasGraph.setCursor(QCursor(Qt.CrossCursor))
                self.currentCursor = QCursor(Qt.CrossCursor)
            else:
                self.canvasGraph.setCursor(QCursor(Qt.ArrowCursor))
                self.currentCursor = None
            print("Marking" + str(self.flagMarking))
        if event.text().lower() == "r":
            self.canvasGraph.axes.set_xlim(0, self.deviceLength+0.1)
            self.canvasGraph.axes.set_ylim(-3, 100)
            self.canvasGraph.draw()
            print("R")
        if event.text().lower() == "a":
            self.flagSetDxForMarker = True
        if event.key() == Qt.Key_Shift:
            self.flagShiftHeld = True
            if (not 'pan/zoom' in self.toolbar.mode):
                self.flagShiftHeld = True
                self.toolbar.pan()
        super().keyPressEvent(event)


    def keyReleaseEvent(self, event):
        if event.text().lower() == "a":
            self.flagSetDxForMarker = False
        if event.key() == Qt.Key_Shift:
            if (self.flagShiftHeld):
                self.toolbar.pan()
                self.flagShiftHeld = False
        super().keyPressEvent(event)

    def setUpUi(self):

        self.name, deviceLength, dataDrill, dataFeed = self.dataModel.getGraphData()

        self.setFocusPolicy(Qt.ClickFocus)

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
        self.horizontalSpacer0 = QSpacerItem(70, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

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
        self.tableWidgetData.setMaximumSize(QSize(1000, 500))
        self.tableWidgetData.setAutoScroll(False)
        self.tableWidgetData.setProperty("isWrapping", True)
        self.tableWidgetData.setColumnCount(6)
        self.tableWidgetData.setRowCount(6)

        self.tableWidgetData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidgetData.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tableWidgetData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetData.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidgetData.setShowGrid(False)
        self.tableWidgetData.horizontalHeader().setVisible(False)
        self.tableWidgetData.verticalHeader().setVisible(False)
        self.tableWidgetData.verticalHeader().setMinimumSectionSize(0)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetData.sizePolicy().hasHeightForWidth())

        self.tableWidgetData.setSizePolicy(sizePolicy)



        self.tableWidgetData.setStyleSheet("QTableView::item:selected {background: none;}"
                                           "QTableWidget::item { margin: 0px; }")

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
        self.deviceLength = float(deviceLength)
        self.canvasGraph.axes.set_xlim(0, self.deviceLength+0.1)
        step = self.deviceLength / len(dataDrill)
        x = np.arange(0, self.deviceLength, step)
        self.canvasGraph.axes.plot(x, dataDrill, linewidth=0.7)
        self.canvasGraph.axes.plot(x, dataFeed, linewidth=0.7)
        self.canvasGraph.figure.subplots_adjust(left=0.036, bottom=0.2490168523424322, right=0.98, top=0.98)
        self.canvasGraph.axes.set_ylim(-3, 100)
        self.canvasGraph.axes.set_xticks(np.arange(0, 42, 2))
        self.canvasGraph.axes.set_yticks(np.arange(0, 110, 10))
        self.canvasGraph.axes.set_xlabel('Tiefe (cm)', fontsize=10)
        self.canvasGraph.axes.set_ylabel('Wiederstand (%)', fontsize=10)
        self.canvasGraph.axes.xaxis.label.set_position((0.98, 1))
        self.canvasGraph.axes.yaxis.label.set_position((1, 0.9))
        self.canvasGraph.axes.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        self.canvasGraph.draw()

        if (self.mainWindow):
            self.canvasGraph.mpl_connect('motion_notify_event', self.onMouseMove)
            self.canvasGraph.mpl_connect('button_press_event', self.onButtonPress)
            self.canvasGraph.mpl_connect('button_release_event', self.onButtonReleased)
            self.canvasGraph.mpl_connect('figure_enter_event', self.onAxesEnter)
            #self.test_canvas.mpl_connect('axes_leave_event', self.onAxesLeave)
            self.canvasGraph.mpl_connect('figure_leave_event', self.onAxesLeave)
            self.canvasGraph.mpl_connect('scroll_event', self.zoomOnMouseWheel)
            #self.canvasGraph.mpl_connect('key_press_event', self.testEvent)
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
        self.tableWidgetMarker.setMaximumSize(QSize(1000, 500))
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

        self.tableWidgetMarker.setStyleSheet("QTableView::item{font: 12pt;}"
                                             "QTableWidget::item { margin: 10px; }")

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

        self.setFocus()

    def setupTable(self):
        dataSet = self.dataModel.getTablaTopData()
        for i in range(len(dataSet[0])):
            m = i % 6
            n = (i // 6) + 1 * (i//6)
            l = i // 6 + 1 + 1 * (i//6)
            self.tableWidgetData.setItem(m, n, dataSet[0][i])
            self.tableWidgetData.setItem(m, l, dataSet[1][i])


        #self.tableWidgetData.setItem(0, 0, QTableWidgetItem("This shows in the first row/column"))



    # functionality for the matplotlib canvas
    def onMouseMove(self, event):
        # @todo create a global variable called backMarker and frontMarker which will be set with the next markers
        # in each direction of focusMarker after a marker got focused
        # then change snapOn() to check for 2 variables instead of the entire dict
        # kinda useless for this application but save them bytes where you can
        if (event.inaxes):
            if(self.currentCursor):
                self.canvasGraph.setCursor(self.currentCursor)
            if (self.flagMarking):
                self.showMarkingAreaRect.set_width(event.xdata - self.showMarkingAreaRect.get_x())
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
                    self.focusedMarker.move(event.xdata - self.lastXPos)
                    self.snapOn(event.canvas, self.focusedMarker)
                    self.updateTableMarkerEntry(self.focusedMarker.index, self.focusedMarker.name, self.focusedMarker.get_x(),
                                                self.focusedMarker.get_width() + self.focusedMarker.get_x())
                    self.lastXPos = event.xdata

                    if (self.flagMarking):
                        self.xPosMarkerStart = event.xdata

                # If flag for rectangle being focused on right side is set, resize rectangle from right
                elif (self.flagMarkerRightFocus):
                    self.flagMarkerDragged = True
                    self.focusedMarker.resizeWidth(event.xdata - self.lastXPos, "r")
                    self.snapOn(event.canvas, self.focusedMarker)
                    self.lastXPos = event.xdata

                    if (self.flagMarking):
                        self.xPosMarkerStart = event.xdata

                # If flag for rectangle being focused on left side is set, resize rectangle from left
                elif (self.flagMarkerLeftFocus):
                    self.flagMarkerDragged = True
                    self.focusedMarker.resizeWidth(event.xdata - self.lastXPos, "l")
                    self.snapOn(event.canvas, self.focusedMarker)
                    self.lastXPos = event.xdata

                    if (self.flagMarking):
                        self.xPosMarkerStart = event.xdata

            # Redraw canvas after processing actions
            event.canvas.draw()

    def onButtonPress(self, event):
        self.logger.info("~~~~~~~~~~~~ onButtonPress ~~~~~~~~~~~~")
        if (event.inaxes is None):
            return

        self.logger.info(" LastXPos: {0}\n eventPos: {1}".format(self.lastXPos, event.xdata))
        if (event.button == MouseButton.LEFT):
            self.flagMouseClicked = True

            self.lastXPos = event.xdata

            # check if any marker rectangle is close by
            if (self.markerList is not []):
                for marker in self.markerList:
                    if self.checkIfClickByRect(event, marker):
                        self.focusedMarker = marker
                        return
                    else:
                        self.focusedMarker = None

            self.logger.info(" focusedMarker {}".format(self.focusedMarker))

            if (not (self.flagMarkerFocus or self.flagMarkerLeftFocus or self.flagMarkerRightFocus)
                    and self.flagMarking and not self.flagShiftHeld):

                if (self.clickCount == 0):
                    self.logger.info("************ Marking_start ************")
                    self.focusedMarker = None
                    self.flagMarkerFocus = False
                    self.xPosMarkerStart = event.xdata
                    self.showMarkingAreaRect.set_x(event.xdata)
                    self.showMarkingAreaRect.set_visible(True)
                    self.logger.info(" xPosMarkerStart: {0} @clickCount: {1}".format(self.xPosMarkerStart, self.clickCount))

                elif (self.clickCount > 0):
                    if (self.xPosMarkerStart > event.xdata):
                        self.logger.error("Please mark forwards, this is still buggy")

                    name, col = self.mainWindow.openPickMarker(self.defaultMarkerDictName)

                    if (not (name or col)):
                        return

                    if (self.markerList == []):
                        if ("Borke/Rinde" in name):
                            self.setDxForMarker(event.xdata)

                    self.markerName = name
                    self.markerColor = col
                    self.addRectToCurrentCanv(event)

                    if (not self.lockMarkerStart):
                        self.logger.info(" xPosMarkerStart: {0} at clickCount: {1}"
                                    "event.xdata: {2}".format(self.xPosMarkerStart, self.clickCount, event.xdata))
                        self.xPosMarkerStart = event.xdata
                    else:
                        self.lockMarkerStart = False

                self.showMarkingAreaRect.set_x(event.xdata)
                self.clickCount += 1


        if (self.flagSetDxForMarker):
            print(" Adjusted x value: " + str(event.xdata))
            self.setDxForMarker(event.xdata)
            for marker in self.markerList:
                self.updateTableMarkerEntry(marker.index,
                                            marker.name,
                                            marker.get_x(),
                                            marker.get_x1())


        if (event.button == MouseButton.RIGHT):
            mode = self.toolbar.mode
            if ("pan/zoom" in mode):
                self.toolbar.pan()
                return

            if(not self.flagMarking):
                if (self.markerList is not []):
                    for marker in self.markerList:
                        if self.checkIfClickByRect(event, marker):
                            self.deleteMarker(marker)
                            return
                        else:
                            self.focusedMarker = None



        if (event.button == MouseButton.MIDDLE and not self.flagMarking):
            self.toolbar.pan()

    def onButtonReleased(self, event):

        if (self.flagMarkerDragged):
            if ("Rinde" in self.focusedMarker.name):
                self.setDxForMarker(self.focusedMarker.get_x1())
                for marker in self.markerList:
                    marker.updateTableMarker()
            self.flagMarkerDragged = False
            event.canvas.draw()

        self.flagMouseClicked = False#
        self.focusedMarker = None

    def zoomOnMouseWheel(self, event):

        ax = self.canvasGraph.axes
        xdata = event.xdata
        ydata = event.ydata
        baseScale = 1.5

        if event.button == 'down':
            scaleFactor = 1 / baseScale
        elif event.button == 'up':
            scaleFactor = baseScale
        else:
            scaleFactor = 1

        if (self.flagShiftHeld):
            ax.set_ylim([ydata - (ydata - ax.get_ylim()[0]) / scaleFactor,
                         ydata + (ax.get_ylim()[1] - ydata) / scaleFactor])
        else:
            ax.set_xlim([xdata - (xdata - ax.get_xlim()[0]) / scaleFactor,
                         xdata + (ax.get_xlim()[1] - xdata) / scaleFactor])

        self.canvasGraph.draw()

    def onAxesEnter(self, event):
        self.vLineRect.set_visible(True)
        self.setFocus()
        event.canvas.draw()

    def onAxesLeave(self, event):

        if (event is None
                or event.canvas is None
                or self.flagMouseClicked
                or self.clickCount > 0):
            return

        self.vLineRect.set_visible(False)
        event.canvas.draw()
        self.flagMarkerFocus = False
        self.flagMarkerLeftFocus = False
        self.flagMarkerRightFocus = False
        self.focusedMarker = None


    def setDxForMarker(self, dx):
        self.dxMarkerForTable = dx
        def customFormat(x, pos):
            newTick = round(x - self.dxMarkerForTable, 0)
            return newTick
        self.canvasGraph.axes.xaxis.set_major_formatter(matplotlib.pyplot.FuncFormatter(customFormat))
        self.canvasGraph.axes.set_xticks(np.arange(0+dx, 42, 2))
        self.canvasGraph.axes.set_xlim(0, self.deviceLength+0.1)
        self.canvasGraph.draw()


    def windowClosedByUser(self):
        self.flagWindowClosedByUserSignal = True
    def windowClosedProgrammatically(self):
        self.flagWindowClosedByUserSignal = False


    def showMarkingOnScreen(self, show):
        if (show):
            self.vLineRect.set_color("#a30cc2")
            self.showMarkingAreaRect.set_x(self.xPosMarkerStart)
            self.canvasGraph.axes.set_facecolor("#949494")
        else:
            self.vLineRect.set_color("black")
            self.showMarkingAreaRect.set_visible(False)
            self.canvasGraph.axes.set_facecolor(self.canvasColor)
            print(self.canvasColor)


    # region marker functionality
    def addRectToCurrentCanv(self, event=None, markerState=None, noOverlayCheck=False):
        logging.debug("~~~~~~~~~~~~ addRectToCurrentCanv ~~~~~~~~~~~~")
        axisHeight = 100
        tmpListRect = self.markerList

        if (markerState):
            self.logger.info("Loading marker {0} ..".format(markerState["name"]))
            self.logger.info("Marker values: index:{4}; xy:{0}; widt:{1}; name{2}; col:{3}".format(markerState["x"],
                                                                                                markerState["width"],
                                                                                                markerState["name"],
                                                                                                markerState["color"],
                                                                                                markerState["index"]))
            color = self.mainWindow.nameToColorDict[markerState["name"]]
            tmpRect = CustomRectangle((markerState["x"], -axisHeight * 0.4 / 100), markerState["width"],
                                      - axisHeight * self.heightRectMarkPerc / 100, markerState["index"],
                                      markerState["name"], markerState["color"], self.canvasGraph)
            tmpRect.set_edgecolor("black")
            tmpRect.set_linewidth(0.5)
            tmpListRect.append(tmpRect)
            self.addTableMarkerEntry(len(tmpListRect) - 1, markerState["name"], color, round(markerState["x"], 2),
                                     round(markerState["x"] + markerState["width"], 2))

        else:
            width = event.xdata - self.xPosMarkerStart
            anchorX = self.xPosMarkerStart if width > 0 else event.xdata
            width = abs(width)

            tmpRect = CustomRectangle((anchorX, -axisHeight * 0.4 / 100), width,
                                      -axisHeight * self.heightRectMarkPerc / 100, len(tmpListRect),
                                      self.markerName, self.markerColor, event.canvas)
            self.logger.info("Created new Marker ..")
            self.logger.info("Marker values: index:{4}; xy:{0}; widt:{1}; name{2}; col:{3}".format(anchorX,
                                                                                                width,
                                                                                                self.markerName,
                                                                                                self.markerColor,
                                                                                                len(tmpListRect)))
            tmpRect.set_edgecolor("black")
            tmpRect.set_linewidth(0.5)
            if (not noOverlayCheck and not self.adjustOverlay(event, tmpRect)):
                return
            logging.debug("Marker {0} created".format(tmpRect.name))
            tmpListRect.append(tmpRect)
            self.addTableMarkerEntry(len(tmpListRect) - 1, self.markerName, self.markerColor, round(anchorX, 2),
                                     round(event.xdata, 2))
            self.updateMarkerIndices()
            self.snapOn(event.canvas, tmpRect)



        # self.updateMarkerRectSave(event.canvas, tmpRect, argColorName=self.colorRect)

        self.canvasGraph.axes.add_patch(tmpRect)
        for marker in self.markerList:
            marker.updateTableMarker()
        self.canvasGraph.draw()

    # function to check if event coordinates are close to a Rectangle and/or close to either side of that Rectangle
    # if close to Rectangle and not close to either side make that rectangle movable
    # if close to either side expand or shrink from respective side
    # @todo highlight either side if hovered or change mouse
    def checkIfClickByRect(self, event, rect):
        logging.debug("~~~~~~~~~~~~ checkIfClickByRect ~~~~~~~~~~~~")

        axisHeight = event.canvas.axes.get_ylim()[1]

        rectCent = rect.get_center()
        rectWidth = rect.get_width()

        epsilonSides = rectWidth * 0.05

        rightEndX, leftEndX = rectCent[0] + rectWidth / 2, rectCent[0] - rectWidth / 2
        disRight = np.sqrt((rightEndX - event.xdata) ** 2)
        disLeft = np.sqrt((leftEndX - event.xdata) ** 2)

        rectX = rect.get_x()

        xRange = True if (rectX < event.xdata < rectX + rectWidth) else False
        yRange = True if (-20 < event.ydata <= axisHeight * self.percMarkerFocusHeight / 100) else False
        self.flagMarkerLeftFocus = True if ((disLeft < epsilonSides) and yRange) else False
        self.flagMarkerRightFocus = True if ((disRight < epsilonSides) and yRange) else False
        self.flagMarkerFocus = (
                xRange and yRange and not self.flagMarkerLeftFocus and not self.flagMarkerRightFocus)

        logging.debug("Leaving checkIfClickByRect with result: {}".format(
            self.flagMarkerLeftFocus or self.flagMarkerRightFocus or self.flagMarkerFocus))

        return self.flagMarkerLeftFocus or self.flagMarkerRightFocus or self.flagMarkerFocus

    def snapOn(self, canvas, focusRect):
        self.logger.info("~~~~~~~~~~~~ snapOn ~~~~~~~~~~~~")
        # @todo on snapon creates temporae gap between linked markers (adjust width of linked marker)
        if ((focusRect.getLeftRect() or focusRect.getNextRectInList() == None)
                and (focusRect.getRightRect() or focusRect.getLastRectInList() == None)):
            return

        snapDelta = self.canvasGraph.axes.get_xlim()[1] * 1 / 200
        nextAndLastRect = [focusRect.getLastRectInList(), focusRect.getNextRectInList()]

        for marker in nextAndLastRect:
            if (marker == None):
                continue
            fixedRectXStart = marker.get_x()
            fixedRectXEnd = marker.get_x() + marker.get_width()
            focusRectXStart = focusRect.get_x()
            focusRectXEnd = focusRectXStart + focusRect.get_width()

            if (focusRect.getRightRect() is None
                    and focusRectXEnd >= fixedRectXStart-snapDelta > focusRectXStart):
                focusRect.set_width(fixedRectXEnd - focusRectXStart)
                self.logger.info(" selfIndex: {0} rightMarker: {1}".format(focusRect.index, marker.index))
                focusRect.setRightRect(marker)
                marker.setLeftRect(focusRect)
                if (focusRect.getLeftRect()):
                    focusRect.getLeftRect().set_width(focusRect.getLeftRect().get_width() + snapDelta)
            elif (focusRect.getLeftRect() is None
                  and focusRectXStart <= fixedRectXEnd+snapDelta < focusRectXEnd):
                self.logger.info(" selfIndex: {0} leftMarker: {1}".format(focusRect.index, marker.index))
                focusRect.set_x(fixedRectXEnd)
                focusRect.setLeftRect(marker)
                marker.setRightRect(focusRect)
                if (focusRect.getRightRect()):
                    focusRect.getRightRect().set_x(focusRect.getRightRect().get_x() - snapDelta)
                    focusRect.getRightRect().set_width(focusRect.getRightRect().get_width() + snapDelta)

        for marker in self.markerList:
            marker.updateTableMarker()
        self.canvasGraph.draw()


    # 90% of this function is actually redundant because CustomRectangles resizeLinks() can take of most of it
    # not gonna change that though.
    # also @todo combine markers if leftMarker or richtMarker have the same name/color
    def adjustOverlay(self, event, tmpRect):
        self.logger.info("~~~~~~~~~~~~ adjustOverlay ~~~~~~~~~~~~")
        try:
            newRectXStart = tmpRect.get_x()
            newRectXEnd = tmpRect.get_x() + tmpRect.get_width()

            for marker in self.markerList:

                if (tmpRect.get_width() < 0 or marker.get_width() < 0):
                    logging.error("ERROR: the width of a rect is negative, something went horribly wrong!!!!")
                    return False

                oldRectXStart = marker.get_x()
                oldRectXEnd = marker.get_x() + marker.get_width()

                startInOld = oldRectXStart < newRectXStart < oldRectXEnd
                endInOld = oldRectXStart < newRectXEnd < oldRectXEnd

                if (startInOld ^ endInOld):
                    if (startInOld):
                        self.logger.info(" startInOld: newX: {0} newW: {1}  oldX: {2} oldW: {3}"
                                      "".format(newRectXStart, newRectXEnd, oldRectXStart, oldRectXEnd))
                        marker.set_width(newRectXStart-oldRectXStart)
                        marker._rightRect = None
                        marker.setRightRect(tmpRect)
                        tmpRect._leftRect = None
                        tmpRect.setLeftRect(marker)
                        if (self.clickCount > 1):
                            self.xPosMarkerStart = tmpRect.get_x1()
                            self.lockMarkerStart = True
                        logging.info(" tmpRect: {0}\n newRect: {1}".format(tmpRect, marker))
                        continue

                    if (endInOld):
                        self.logger.info(" endInOld: newX: {0} newW: {1}  oldX: {2} oldW: {3}"
                                      "".format(newRectXStart, newRectXEnd, oldRectXStart, oldRectXEnd))
                        marker.set_width(oldRectXEnd - newRectXEnd)
                        marker.set_x(newRectXEnd)
                        marker.setLeftRect(None)
                        marker.setLeftRect(tmpRect)
                        tmpRect._rightRect = None
                        tmpRect.setRightRect(marker)
                        logging.info(" tmpRect: {0}\n newRect: {1}".format(tmpRect, marker))
                        continue

                elif (startInOld and endInOld):
                    self.logger.info(" startAndEndInOld: newX: {0} newW: {1}  oldX: {2} oldW: {3}"
                                  "".format(newRectXStart, newRectXEnd, oldRectXStart, oldRectXEnd))
                    marker.set_width(newRectXStart - oldRectXStart)
                    splitMark2 = {'index': len(self.markerList)+1,
                                  'name': marker.name,
                                  'color': marker.color,
                                  'x': newRectXEnd,
                                  'width': oldRectXEnd-newRectXEnd}
                    logging.info(" tmpRect: {0}\n newRect: {1}".format(tmpRect, marker))
                    self.addRectToCurrentCanv(markerState=splitMark2, noOverlayCheck=True)
                    newRect = self.markerList[-1]
                    if (marker.getRightRect):
                        newRect.setRightRect(marker.getRightRect())
                        marker.setRightRect(None)

                    marker.setRightRect(tmpRect)
                    tmpRect.setLeftRect(marker)
                    tmpRect.setRightRect(newRect)
                    newRect.setLeftRect(tmpRect)
                    self.flagMarking = False
                    self.clickCount = 0
                    self.currentCursor = None
                    self.canvasGraph.setCursor(QCursor(Qt.ArrowCursor))

                    return True

                elif (newRectXStart < oldRectXStart and oldRectXEnd < newRectXEnd):
                    print("Marker almost crushed")
                    return False

        except IndexError:
            print("Index Error: Canvas list is empty.")

        return True

    def deleteMarker(self, marker):
        print("~~~~~~~~~~deleteMarker~~~~~~~~~~")
        print("Index: {0}".format(marker.index))
        self.flagMarkerRightFocus = False
        self.flagMarkerFocus = False
        self.flagMarkerLeftFocus = False
        self.focusedMarker = None
        if (marker.getLeftRect()):
            marker.getLeftRect().setNextRectInList(marker.getRightRect())
            marker.getLeftRect().setRightRect(None)
        if (marker.getRightRect()):
            marker.getRightRect().setLastRectInList(marker.getLeftRect())
            marker.getRightRect().setLeftRect(None)

        marker.remove()
        self.markerList.remove(marker)
        self.updateMarkerIndices()
        ind = 0
        for marker in self.markerList:
            marker.updateTableMarker()
            ind += 1
        self.addTableMarkerEntry(ind, "","","","")
        self.canvasGraph.draw()

    def updateMarkerIndices(self):
        logging.debug("~~~~~~~~~~~~ updateMarkerIndices ~~~~~~~~~~~~")
        markerList = self.markerList.copy()
        markerList.sort(key=lambda r: r.get_x())
        for i in range(len(markerList)):
            markerList[i].index = i
            if (i > 0):
                markerList[i].setLastRectInList(markerList[i-1])
            if(i < len(self.markerList)-1):
                markerList[i].setNextRectInList(markerList[i+1])

        for marker in markerList:
            logging.debug(" index: {0}; self: {1}\n"
                  " rect@lastIndex: {2};\n rect@nextIndex: {3};\n link@left: {4};\n link@right {5}\n"
                  "********************************************************************************"
                  "".format(marker.index, marker, marker.getLastRectInList(), marker.getNextRectInList(),
                            marker.getLeftRect(), marker.getRightRect()))

    # endregion

    def addTableMarkerEntry(self, index, name, color, x, dx):
        # @todo overload class to get a on_item_changed(self, item) signal and use it to change the markers
        if(index >= 6):
            if (index%6 == 0):
                n = self.tableWidgetMarker.columnCount()
                self.tableWidgetMarker.setColumnCount(n+1)

        if (name != ""):
            x = x - self.dxMarkerForTable
            dx = dx - self.dxMarkerForTable
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor(color))
            icon = QIcon(pixmap)
            # todo implement this
            """ @todo this
            self.maxLenColumns = []
            for i in range(self.tableWidgetMarker.columnCount()):
                maxLen = len(name)
                for j in range(self.tableWidgetMarker.rowCount()):
                    item = self.tableWidgetMarker.item(j, i)
                    if (item is not None):
                        maxLen = max(maxLen, len(item.text().split(":")[0].strip()))
            """
            item = QTableWidgetItem(name + "\t: {0} - {1}".format(x, dx))
            item.setIcon(icon)
        else:
            item = QTableWidgetItem("")

        self.tableWidgetMarker.setItem(index % 6, index // 6, item)

    def updateTableMarkerEntry(self, index, name, x, dx):
        try:
            x = x - self.dxMarkerForTable
            dx = dx - self.dxMarkerForTable
            color = self.mainWindow.nameToColorDict[name]
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor(color))
            icon = QIcon(pixmap)

            item = QTableWidgetItem(name + "\t: {0} - {1}".format(round(x, 2), round(dx, 2)))
            item.setIcon(icon)
            self.tableWidgetMarker.setItem(index % 6, index // 6, item)


        except KeyError:
            print("Not in dic")


    def changeWidgetsRelSpace(self, topPerc, graphPerc, botPerc, saveValues=False):
        if (topPerc + graphPerc + botPerc > 100):
            raise Exception("Sum must be less than 100")

        if (saveValues):
            self.heightWidgetTopPerc = topPerc
            self.heightWidgetGraphPerc = graphPerc
            self.heightWidgetBottomPerc = botPerc

        self.verticalLayout_2.setStretchFactor(self.widgetTop, topPerc)
        self.verticalLayout_2.setStretchFactor(self.widgetBottom, botPerc)
        self.verticalLayout_2.setStretchFactor(self.widgetGraph, graphPerc)

    def resetWidgetsRelSpace(self):
        self.verticalLayout_2.setStretchFactor(self.widgetTop, self.heightWidgetTopPerc)
        self.verticalLayout_2.setStretchFactor(self.widgetBottom, self.heightWidgetBottomPerc)
        self.verticalLayout_2.setStretchFactor(self.widgetGraph, self.heightWidgetGraphPerc)

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


    def getCurrentState(self):
        state = {}
        state.update({"data": self.dataModel.getSaveState()})
        markerStateList = []
        for marker in self.markerList:
            markerStateList.append(marker.getSaveState())

        state.update({"markerState": markerStateList})

        state.update({"dx_xlim": self.dxMarkerForTable})
        self.logger.info("state: {0}".format(state))
        return state


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