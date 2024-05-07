# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QRadioButton, QCheckBox
from PySide6 import QtWidgets

import numpy as np
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backend_bases import MouseButton

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
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.03, right=0.97, top=0.99, bottom=0.07)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class WidgetGraph(QWidget):
    def __init__(self, MainWindow=None, graphData=None, parent=None):
        super().__init__(parent)

        pyplot.style.use('ggplot')

        self.mainWindow = MainWindow
        self.graphData = graphData

        self.verticalLayout_2 = QVBoxLayout()
        self.widgetTop = QWidget()
        self.widgetTop.setObjectName(u"widgetTop")
        self.widgetTop.setMaximumSize(QSize(16777215, 120))
        self.widgetTop.setStyleSheet(u"QListWidget{background:lightblue; spacing: 0;}")
        self.horizontalLayout = QHBoxLayout(self.widgetTop)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidgetData = QListWidget(self.widgetTop)
        self.listWidgetData.setObjectName(u"listWidgetData")
        self.listWidgetData.setAutoScroll(False)
        self.listWidgetData.setMovement(QListView.Snap)
        self.listWidgetData.setFlow(QListView.LeftToRight)
        self.listWidgetData.setProperty("isWrapping", True)
        self.listWidgetData.setResizeMode(QListView.Fixed)
        self.listWidgetData.setLayoutMode(QListView.SinglePass)
        self.listWidgetData.setSpacing(1)

        self.horizontalLayout.addWidget(self.listWidgetData)

        self.horizontalSpacer = QSpacerItem(472, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.widgetTop.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.widgetTop)

        self.canvasGraph = MplCanvas(self, width=6, height=4, dpi=100)

        self.canvasGraph.axes.plot(self.graphData[0], self.graphData[1])
        self.canvasGraph.draw()

        if (self.mainWindow):
            self.canvasGraph.mpl_connect('motion_notify_event', self.mainWindow.onMouseMove)
            self.canvasGraph.mpl_connect('button_press_event', self.mainWindow.onButtonPress)
            self.canvasGraph.mpl_connect('button_release_event', self.mainWindow.onButtonReleased)
            self.canvasGraph.mpl_connect('axes_enter_event', self.mainWindow.onAxesEnter)
            #self.test_canvas.mpl_connect('axes_leave_event', self.onAxesLeave)
            self.canvasGraph.mpl_connect('figure_leave_event', self.mainWindow.onAxesLeave)
            self.canvasGraph.mpl_connect('resize_event', self.mainWindow.onResize)

            self.mainWindow.dictCanvasToRectList.update({self.canvasGraph: []})

        self.widgetGraph = self.canvasGraph
        self.widgetGraph.setObjectName(u"widgetGraph")

        self.verticalLayout_2.addWidget(self.widgetGraph)

        self.widgetBottom = QWidget()
        self.widgetBottom.setObjectName(u"widgetBottom")
        self.widgetBottom.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout_2 = QHBoxLayout(self.widgetBottom)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listWidgetAnalysis = QListWidget(self.widgetBottom)
        self.listWidgetAnalysis.setObjectName(u"listWidgetAnalysis")

        self.horizontalLayout_2.addWidget(self.listWidgetAnalysis)

        self.horizontalSpacer_2 = QSpacerItem(369, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.textEditComment = QTextEdit(self.widgetBottom)
        self.textEditComment.setObjectName(u"textEditComment")
        self.textEditComment.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_2.addWidget(self.textEditComment)
        self.widgetBottom.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.widgetBottom)


        self.widgetRight = QWidget()
        self.widgetRight.setMaximumHeight(35)

        self.horizontalLayout_3 = QHBoxLayout()

        self.checkBoxHideTop = QCheckBox(self.widgetRight)
        self.checkBoxHideTop.setObjectName(u"radioButtonHideTop")
        self.checkBoxHideTop.setText("")
        self.checkBoxHideTop.checkStateChanged.connect(self.toggleHideTop)

        self.checkBoxHideBot = QCheckBox(self.widgetRight)
        self.checkBoxHideBot.setObjectName(u"radioButtonHideTop")
        self.checkBoxHideBot.setText("")
        self.checkBoxHideBot.checkStateChanged.connect(self.toggleHideBot)

        self.horizontalSpacer_3 = QSpacerItem(200, 35, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)
        self.horizontalLayout_3.addWidget(self.checkBoxHideTop)
        self.horizontalLayout_3.addWidget(self.checkBoxHideBot)

        self.widgetRight.setLayout(self.horizontalLayout_3)

        self.verticalLayout_2.addWidget(self.widgetRight)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.verticalLayout_2)


    def toggleHideTop(self):
        rndmBool = (self.checkBoxHideTop.checkState() == Qt.Checked)
        self.widgetTop.hide() if rndmBool else self.widgetTop.show()
        print("BLABALBLA")

    def toggleHideBot(self):
        rndmBool = (self.checkBoxHideBot.checkState() == Qt.Checked)
        self.widgetBottom.hide() if rndmBool else self.widgetBottom.show()

    def hideEverything(self):
        self.widgetTop.hide()
        self.widgetBottom.hide()
        self.widgetRight.hide()

    def showEverything(self):
        self.widgetTop.show()
        self.widgetBottom.show()
        self.widgetRight.show()
