# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget
from PySide6 import QtWidgets

import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backend_bases import MouseButton

# this ist stuff only used for the stpuidGraphFunction, should probably source that one out
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEventLoop)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListView, QListWidget,
                               QListWidgetItem, QSizePolicy, QSpacerItem, QTextEdit,
                               QVBoxLayout, QWidget)

import markerpresetwindow
from ui_files.ui_mainwindow import Ui_MainWindow
from markerpresetwindow import MarkerPresetWindow
from selectmarkerwindow import SelectMarkerWindow


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.03, right=0.97, top=0.99, bottom=0.07)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # testing area TBD!!!

        self.test_rect = Rectangle((0, 0), 0.2, - 0.03)
        self.test_x_start = 0

        self.test_map_title_to_ind = {}
        self.test_array_mplCanvas = []
        self.test_rectFocusInd = None

    # variable setup

        # classes
        # @markerWindow variable to store a selectMarkerWindow.py
        # @vLineRect constant that marks the vertical position of the mouse cursor across the MplCanvas
        # @currentTargetRect variable that holds a rectangle if it has been clicked on
        self.markerWindow = None

        self.vLineRect = Rectangle((0, 0), 0.0005, 1)
        self.currentTargetRect = None

        # data
        # @xDataForMarker variable that holds the first clicked position to draw a marker from that to the second click
        # @dict dictMarker dictionary containing a "String::Name: String::HexColor" pair to save all Marker
        # @list listMarkerRect list that doesnt do anything I believe @todo check this variable
        # @colorRect variable given from selectMarkerWindow that determines the color of a rectangle
        # @int currentCanvasInd variable that saves the Index of the focus Canvas
        # @list listRectByCanvInd a list of lists of rectangles each i_ind points to the canvas, j_ind to the rect
            # listRectCanvInd[canvasIndex][rectangleIndex] -> Rectangle
        self.xDataForMarker = None

        self.dictMarker = {}
        self.listMarkerRect = []
        self.colorRect = "#000000"

        self.currentCanvasInd = None
        self.listRectByCanvInd = []

        # counter
        # @variable clickCount counts to a max of 1, on 0 it sets the xDataForMarker var
        self.clickCount = 0

        # flags
        self.flagRectFocus = False
        self.flagRectLeftFocus = False
        self.flagRectRightFocus = False
        self.flagMouseClicked = False
        self.flagVerticalLine = True


        # @todo delete the entire self.sc because the canvas will be generated programmatically
        self.sc = MplCanvas(self, width=6, height=4, dpi=100)
        #self.sc.axes.add_patch(self.rect)
        #self.sc.axes.add_patch(self.test_rect)
        self.sc.axes.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5], [0, 0.1, 0.2, 0.3, 0.4, 0.5])
        self.sc.draw()

        self.sc.mpl_connect('motion_notify_event', self.onMouseMove)
        self.sc.mpl_connect('button_press_event', self.onButtonPress)
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
            #print(event.xdata, event.ydata)
            self.vLineRect.set_x(event.xdata)

        # test on how to move a rectangle
        if (event.inaxes and event.button == MouseButton.LEFT and self.flagRectFocus):
            currentX = self.currentTargetRect.get_x()

            self.currentTargetRect.set_x(
                currentX + (event.xdata - self.test_x_start))
            self.test_x_start = event.xdata

        # test on how to change the length of a rectangle
        if (event.inaxes and event.button == MouseButton.LEFT and self.flagRectRightFocus):
            currentWidth = self.currentTargetRect.get_width()

            self.currentTargetRect.set_width(
                currentWidth + (event.xdata - self.test_x_start))
            self.test_x_start = event.xdata

        if (event.inaxes and event.button == MouseButton.LEFT and self.flagRectLeftFocus):
            currentX = self.currentTargetRect.get_x()
            currentWidth = self.currentTargetRect.get_width()

            self.currentTargetRect.set_x(
                currentX + (event.xdata - self.test_x_start))
            self.currentTargetRect.set_width(
                currentWidth - (event.xdata - self.test_x_start))
            self.test_x_start = event.xdata

        if (self.currentCanvasInd is not None):
            self.test_array_mplCanvas[self.currentCanvasInd].draw_idle()

    def onButtonPress(self, event):

        if (event.inaxes is None):
            return

        self.flagMouseClicked = True

        self.test_x_start = event.xdata
        print(event.xdata, event.ydata)

        if (len(self.listRectByCanvInd) > self.currentCanvasInd):

            i = 0
            for rect in self.listRectByCanvInd[self.currentCanvasInd]:

                if (self.checkIfClickByRect(event, rect)):
                    self.currentTargetRect = self.listRectByCanvInd[self.currentCanvasInd][i]
                    self.test_rectFocusInd = i
                    return
                else:
                    i += 1

        # logic for creating markers with addRectToCurrentCanv
        if (not self.flagRectFocus
                and not self.flagRectLeftFocus
                and not self.flagRectRightFocus):

            if (self.clickCount == 0):
                self.xDataForMarker = event.xdata

            else:
                self.markerWindow = markerpresetwindow.MarkerPresetWindow(self)
                self.markerWindow.setAttribute(Qt.WA_DeleteOnClose)
                self.markerWindow.show()

                waitForMarkerInputLoop = QEventLoop()
                self.markerWindow.destroyed.connect(waitForMarkerInputLoop.quit)
                waitForMarkerInputLoop.exec()
                self.addRectToCurrentCanv(self.xDataForMarker, event.xdata - self.xDataForMarker)

            self.clickCount = self.clickCount + 1 if (self.clickCount < 1) else 0

    def onButtonRelease(self, event):

        self.flagMouseClicked = False
        self.flagRectFocus = False
        self.flagRectLeftFocus = False
        self.flagRectRightFocus = False

    def onAxesEnter(self, event):

        if (self.flagMouseClicked): return
        self.currentCanvasInd = self.test_map_title_to_ind.get(event.inaxes.get_title())

        self.test_array_mplCanvas[self.currentCanvasInd].axes.add_patch(self.vLineRect)
        #event.inaxes.add_patch(self.rect)
        print(event.inaxes.get_title(), self.test_map_title_to_ind.get(event.inaxes.get_title()))

    def onAxesLeave(self, event):
        if (self.currentCanvasInd is None or self.flagMouseClicked):
            return
        #self.test_array_mplCanvas[self.test_currentCanvasInd].axes.clear()
        print("Exit axe")
        self.vLineRect.remove()
        self.test_array_mplCanvas[self.currentCanvasInd].draw()
        self.currentCanvasInd = None
        self.flagRectFocus = False
        self.flagRectLeftFocus = False
        self.flagRectRightFocus = False
        self.test_rectFocusInd = None

    def onResize(self, event):
        print("RESIZED")
        #self.test_array_mplCanvas[self.test_currentCanvasInd].draw()

    # functionality for QPushButtons

    # functionality for the pushButtonOpen QPushButton
    # @todo on click open x files and read the data into specific array indicies
    def openButtonClicked(self):

        layout = self.makeStupidGraph()
        #layout.addWidget(self.sc)
        #layout.addWidget(QPushButton())

        widget = QWidget()
        widget.setLayout(layout)
        self.ui.tabWidget.addTab(widget, "Graph?")

    # functionality for the pushButtonSave QPushButton
    # @todo save stuff, duh
    def saveButtonClicked(self):

        print("saveButtonClicked")
        print(self.listRectByCanvInd)

    # functionality for the pushButtonTabView QPushButton
    def tabButtonClicked(self):
        self.ui.stackedWidgetWorkArea.setCurrentIndex(0)

    # functionality for the pushButtonWindowView QPushButton
    def windowButtonClicked(self):
        self.ui.stackedWidgetWorkArea.setCurrentIndex(1)

    # algorithms

    # function to check if event coordinates are close to a Rectangle and/or close to either side of that Rectangle
    # if close to Rectangle and not close to either side make that rectangle movable
    # if close to either side expand or shrink from respective side
    # @todo highlight either side if hovered or change mouse
    def checkIfClickByRect(self, event, rect):

        rectCent = rect.get_center()
        rectWidth = rect.get_width()

        epsilonSides = rectWidth * 0.10

        rightEndX, leftEndX = rectCent[0] + rectWidth / 2, rectCent[0] - rectWidth / 2
        disRight = np.sqrt((rightEndX - event.xdata) ** 2)
        disLeft = np.sqrt((leftEndX - event.xdata) ** 2)

        rectX = rect.get_x()

        xRange = True if (rectX < event.xdata < rectX + rectWidth) else False
        yRange = True if (0.1 > event.ydata >= rect.get_height()) else False

        self.flagRectLeftFocus = True if ((disLeft < epsilonSides) and yRange) else False
        self.flagRectRightFocus = True if ((disRight < epsilonSides) and yRange) else False
        self.flagRectFocus = (
                xRange and yRange and not self.flagRectLeftFocus and not self.flagRectRightFocus)

        return self.flagRectLeftFocus or self.flagRectRightFocus or self.flagRectFocus

    # testing for the stupid graph widget
    def makeStupidGraph(self):

        verticalLayout_2 = QVBoxLayout()
        widgetTop = QWidget()
        widgetTop.setObjectName(u"widgetTop")
        widgetTop.setMaximumSize(QSize(16777215, 120))
        widgetTop.setStyleSheet(u"QListWidget{background:lightblue; spacing: 0;}")
        horizontalLayout = QHBoxLayout(widgetTop)
        horizontalLayout.setObjectName(u"horizontalLayout")
        listWidgetData = QListWidget(widgetTop)
        listWidgetData.setObjectName(u"listWidgetData")
        listWidgetData.setAutoScroll(False)
        listWidgetData.setMovement(QListView.Snap)
        listWidgetData.setFlow(QListView.LeftToRight)
        listWidgetData.setProperty("isWrapping", True)
        listWidgetData.setResizeMode(QListView.Fixed)
        listWidgetData.setLayoutMode(QListView.SinglePass)
        listWidgetData.setSpacing(1)

        horizontalLayout.addWidget(listWidgetData)

        horizontalSpacer = QSpacerItem(472, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        horizontalLayout.addItem(horizontalSpacer)

        verticalLayout_2.addWidget(widgetTop)

        test_canvas = MplCanvas(self, width=6, height=4, dpi=100)
        test_title = "titleVar" + str(len(self.test_array_mplCanvas))
        test_canvas.axes.set_title(test_title)
        test_canvas.axes.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5], [0, 0.1, 0.2, 0.3, 0.4, 0.5])
        test_canvas.draw()

        test_canvas.mpl_connect('motion_notify_event', self.onMouseMove)
        test_canvas.mpl_connect('button_press_event', self.onButtonPress)
        test_canvas.mpl_connect('axes_enter_event', self.onAxesEnter)
        test_canvas.mpl_connect('axes_leave_event', self.onAxesLeave)
        test_canvas.mpl_connect('figure_leave_event', self.onAxesLeave)
        test_canvas.mpl_connect('resize_event', self.onResize)

        test_canvas.figure.set_gid(len(self.test_array_mplCanvas))

        self.test_map_title_to_ind.update({test_title: len(self.test_array_mplCanvas)})
        self.test_array_mplCanvas.append(test_canvas)

        widgetGraph = test_canvas
        widgetGraph.setObjectName(u"widgetGraph")

        verticalLayout_2.addWidget(widgetGraph)

        widgetBottom = QWidget()
        widgetBottom.setObjectName(u"widgetBottom")
        widgetBottom.setMaximumSize(QSize(16777215, 120))
        horizontalLayout_2 = QHBoxLayout(widgetBottom)
        horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        listWidgetAnalysis = QListWidget(widgetBottom)
        listWidgetAnalysis.setObjectName(u"listWidgetAnalysis")

        horizontalLayout_2.addWidget(listWidgetAnalysis)

        horizontalSpacer_2 = QSpacerItem(369, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        horizontalLayout_2.addItem(horizontalSpacer_2)

        textEditComment = QTextEdit(widgetBottom)
        textEditComment.setObjectName(u"textEditComment")
        textEditComment.setMaximumSize(QSize(200, 16777215))

        horizontalLayout_2.addWidget(textEditComment)

        verticalLayout_2.addWidget(widgetBottom)

        return verticalLayout_2

    def addRectToCurrentCanv(self, anchorX, width):

        # return if no Canvas selected
        if (self.currentCanvasInd is None):
            return

        # if length of listReactByCanvInd is smaller than currentCanvasInd create a new list for that canvas
        # else select the already existing list
        if (len(self.listRectByCanvInd) <= self.currentCanvasInd):
            tmpListRect = []
            self.listRectByCanvInd.append(tmpListRect)

        else:
            tmpListRect = self.listRectByCanvInd[self.currentCanvasInd]

        tmpRect = Rectangle((anchorX, 0), width, -0.02)
        tmpRect.set_color(self.colorRect)
        tmpListRect.append(tmpRect)

        self.listRectByCanvInd[self.currentCanvasInd] = tmpListRect

        self.test_array_mplCanvas[self.currentCanvasInd].axes.add_patch(tmpRect)
        self.test_array_mplCanvas[self.currentCanvasInd].draw()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
