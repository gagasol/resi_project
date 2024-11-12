# This Python file uses the following encoding: utf-8
import logging
import re

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import (QSize, Qt, QObject, )
from PySide6.QtGui import (QColor, QIcon,
                           QPixmap, QKeyEvent, QFont, QFontMetrics)
from PySide6.QtWidgets import QCheckBox, QTableWidget, \
    QHeaderView, QAbstractScrollArea, QLabel, QTableWidgetItem, QStyledItemDelegate, QLineEdit, QAbstractItemView, \
    QDialog, QPushButton
from PySide6.QtWidgets import (QHBoxLayout, QSizePolicy, QSpacerItem, QTextEdit,
                               QVBoxLayout, QWidget)

from customPlotWidget import CustomPlotWidget
from dataModel import DataModel


class RangeDialog(QDialog):
    def __init__(self, x0=0, x1=0, parent=None):
        super(RangeDialog, self).__init__(parent)

        self.setWindowTitle("Range Dialog")
        # First widget with label and line edit
        self.labelFrom = QLabel(QObject.tr("From") + ": ", self)
        self.editFrom = QLineEdit(self)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.labelFrom)
        layout1.addWidget(self.editFrom)

        # Second widget with label and line edit
        self.labelTo = QLabel(QObject.tr("To") + ": ", self)
        self.editTo = QLineEdit(self)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.labelTo)
        layout2.addWidget(self.editTo)

        if x0 != x1:
            self.editFrom.setText(str(x0))
            self.editTo.setText(str(x1))

        # Ok and close buttons
        self.okButton = QPushButton("OK", self)
        self.closeButton = QPushButton("Close", self)

        # Connect the buttons to their respective slots
        self.okButton.clicked.connect(self.on_ok_clicked)
        self.closeButton.clicked.connect(self.on_close_clicked)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.closeButton)

        # Main Vertical Layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(buttonLayout)

        # Slot for ok button click

    def on_ok_clicked(self):
        if float(self.editFrom.text()) < float(self.editTo.text()):
            self.accept()

        # Slot for close button click

    def on_close_clicked(self):
        # Close the dialog
        self.reject()


class CustomAxis(pg.AxisItem):
    def __init__(self, start, end, xMajorTickInterval, xMinorTickInterval, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = start
        self.end = end
        self.xMajorTickInterval = xMajorTickInterval
        self.xMinorTickInterval = xMinorTickInterval
        self.offset = 0

    def setOffset(self, offset):
        print(f"Setting offset to {offset}")
        self.offset = offset
        print(f"Offset is now {self.offset}")
        self.update()
        print("Finished updating")

    def updateTicks(self):
        ticks = np.arange(self.start, self.end, self.xMajorTickInterval)
        majorTicks = [(v + self.offset, str(v)) for v in ticks]
        minorTicks = []
        for i in range(self.start, self.end):
            minorIntervals = np.linspace(i + self.offset, i+self.xMajorTickInterval + self.offset,
                                         self.xMinorTickInterval+1)[1:-1]
            for val in minorIntervals:
                minorTicks.append((val, ''))

        self.setTicks([majorTicks, minorTicks])

    def tickStrings(self, values, scale, spacing):
        return [str(round((val - self.offset), 2)) for val in values]

    def getAxisData(self):
        returnData = [self.offset, self.xMajorTickInterval, self.xMinorTickInterval]
        return returnData

class AutoSizedTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(QHeaderView.Stretch)
        #self.setItemDelegate(MyDelegate(self))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # Disable moving down on Enter
        if event.key() in {Qt.Key_Return, Qt.Key_Enter}:
            self.focusNextPrevChild(True)
        else:
            super().keyPressEvent(event)

    def focusNextPrevChild(self, next):
        if (next):
            currentRow = self.currentRow()
            currentColumn = self.currentColumn()
            while True:
                currentColumn = (currentColumn + (currentRow + 1) // 6) % self.columnCount()
                currentRow = (currentRow + 1) % self.rowCount()

                nextItem = self.item(currentRow, currentColumn)

                if (nextItem and nextItem.flags() & Qt.ItemIsEditable):
                    self.setCurrentCell(nextItem.row(), nextItem.column())
                    break

        else:
            if self.currentRow() - 1 >= 0:
                self.setCurrentCell(self.currentRow() - 1, self.currentColumn())
            else:
                if self.currentColumn() - 1 >= 0:
                    self.setCurrentCell(self.rowCount() - 1, self.currentColumn() - 1)

        return True

    @staticmethod
    def adjustFontsizeToHeight(widgetItem, maxFontsize, minFontsize, maxHeight=None):
        itemHeight = maxHeight if maxHeight else widgetItem.sizeHint().height()
        font = widgetItem.font()
        font.setPointSize(minFontsize)

        for fontsize in range(maxFontsize, minFontsize - 1, -1):
            fontMetric = QFontMetrics(QFont('', fontsize))
            print(f'fontMetric.height: {fontMetric.height()}; itemHeight: {itemHeight}')
            if fontMetric.height() <= itemHeight:
                font.setWeight(QFont.Normal)
                font.setPointSize(fontsize)
                break

        widgetItem.setFont(font)


class MyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)

        if isinstance(editor, QLineEdit):
            # Get notified when editing is finished
            editor.editingFinished.connect(self._handleEditingFinished)

        return editor

    def _handleEditingFinished(self):
        editor = self.sender()

        if not editor:
            return

        editor.editingFinished.disconnect(self._handleEditingFinished)

        # After editing, move the focus to the next cell
        tableWidget = editor.parent().parent()
        current = tableWidget.currentItem()
        row = current.row()
        column = current.column()
        if row < tableWidget.rowCount() - 1:
            nextItem = tableWidget.item(row, column)
            if nextItem:
                tableWidget.setCurrentItem(nextItem)
        elif column < tableWidget.columnCount() - 1:
            nextItem = tableWidget.item(0, column)
            if nextItem:
                tableWidget.setCurrentItem(nextItem)

        editor.editingFinished.connect(self._handleEditingFinished)

    def resizeEvent(self, event):
        ratio = self.height() / self.rowCount() if self.rowCount() else 0
        for i in range(self.rowCount()):
            self.setRowHeight(i, ratio)


class WidgetGraph(QWidget):
    def __init__(self, MainWindow=None, pathToFile=None, loadedState=None, settingsSet=None, parent=None):
        super().__init__(parent)


        self.x = 0
        self.checkBoxShowInGraphInfo = None
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
        self.settingsWindow = MainWindow.settingsWindow
        self.heightWidgetTopPerc = self.settingsWindow.getSettingsVariable("heightWidgetTopPerc")
        self.heightWidgetGraphPerc = self.settingsWindow.getSettingsVariable("heightWidgetGraphPerc")
        self.heightWidgetBottomPerc = self.settingsWindow.getSettingsVariable("heightWidgetBottomPerc")
        self.markerHeightPerc = self.settingsWindow.getSettingsVariable("markerHeightPerc")
        self.strsToShowInGraph = self.settingsWindow.getSettingsVariable("strsToShowInGraph")
        # endregion

        self.pickMarkerWin = None

        # marker variables
        self.markerList = []
        self.defaultMarkerDictName = ""

        self.depthMsmt = None
        self.deviceLength = 40

        self.dxMarkerForTable = 0
        self.flagSetDxForMarker = False

        self.flagWindowClosedByUserSignal = False

        self.maxLenColumns = []
        # region tons of variables for the QTWidget
        self.labelData = None
        self.horizontalSpacer_3 = None
        self.checkBoxHideBot = None
        self.horizontalSpacer01 = None
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
        self.horizontalSpacerPrint = None
        # endregion
        # data variables setup
        self.name = None

        self.dataDrill = []
        self.dataFeed = []

        self.listDataAll = []
        self.dictMeasurementData = {}

        self.textInGraph = None
        # todo delete later
        # arg variables
        self.mainWindow = MainWindow
        self.pathToFile = pathToFile

        # initialize Data and Ui
        if self.mainWindow:
            if "rgp" in pathToFile:
                self.dataModel = DataModel(pathToFile, self.mainWindow.listNameKeys)
                self.defaultMarkerDictName = self.mainWindow.defaultMarkerDictName
            if pathToFile == "":
                self.dataModel = DataModel(pathToFile, self.mainWindow.listNameKeys, loadedState)
                self.defaultMarkerDictName = self.dataModel.fileDefaultPresetName

            self.labelFontSize = self.mainWindow.settingsWindow.getSettingsVariable("labelFontSize")
            self.setUpUi()
            self.initializeData()

            self.markerHeightPerc = self.mainWindow.settingsWindow.getSettingsVariable("markerHeightPerc")

    def setUpUi(self):

        self.name, depthMsmt, dataDrill, dataFeed = self.dataModel.getGraphData()

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
        self.horizontalSpacer0 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

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
        self.tableWidgetData.setMaximumSize(QSize(2000, 500))
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
        self.tableWidgetData.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidgetData.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetData.sizePolicy().hasHeightForWidth())

        self.tableWidgetData.setSizePolicy(sizePolicy)

        self.tableWidgetData.setStyleSheet("QTableView::item:selected {background: none;}"
                                           "QTableWidget::item { margin: 0px;"
                                           "background-color: white; }")

        for i in range(6):
            self.tableWidgetData.setRowHeight(i, 50)

        self.verticalLayout.addWidget(self.labelData)
        self.verticalLayout.addWidget(self.tableWidgetData)

        self.widgetDataTop.setLayout(self.verticalLayout)

        self.horizontalLayout.addWidget(self.widgetDataTop)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalSpacerPrint = QSpacerItem(0, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacerPrint)

        self.widgetTop.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.widgetTop)

        # @todo remove later
        self.depthMsmt = float(depthMsmt)
        step = self.depthMsmt / len(dataDrill)
        #stepFeed = self.deviceLength / len(dataFeed)
        self.x = np.arange(0, self.depthMsmt, step)[:len(dataDrill)]

        self.widgetGraph = QWidget()
        self.widgetGraph.setObjectName(u"widgetGraph")

        start = 0
        end = 40
        majorTicksInterval = self.settingsWindow.getSettingsVariable("majorTicksInterval")
        minorTicksInterval = self.settingsWindow.getSettingsVariable("minorTicksInterval")

        bottom_axis = CustomAxis(start, end, majorTicksInterval, minorTicksInterval, orientation="bottom")
        xLimit = self.deviceLength + 0.5
        colorBackground = self.settingsWindow.getSettingsVariable("colorBackground")
        colorBackgroundMarking = self.settingsWindow.getSettingsVariable("colorBackgroundMarking")
        colorFeedPlot = self.settingsWindow.getSettingsVariable("colorFeedPlot")
        colorDrillPlot = self.settingsWindow.getSettingsVariable("colorDrillPlot")
        markerHeightPerc = self.settingsWindow.getSettingsVariable("markerHeightPerc")
        fontName = self.settingsWindow.getSettingsVariable("fontName")
        fontSize = self.labelFontSize
        font = QFont(fontName, fontSize)
        self.canvasGraph = CustomPlotWidget(xLimit, self, self.defaultMarkerDictName, self.mainWindow.markerPresetList,
                                            colorBackground, colorBackgroundMarking, font, markerHeightPerc,
                                            axisItems={"bottom": bottom_axis})
        self.canvasGraph.showGrid(x=False, y=False)

        penDrill = pg.mkPen(color=colorDrillPlot, width=0.7)
        penFeed = pg.mkPen(color=colorFeedPlot, width=0.7)

        self.canvasGraph.plot(self.x, dataDrill, pen=penFeed)
        self.canvasGraph.plot(self.x, dataFeed, pen=penDrill)

        self.canvasGraph.changeAxisFontsize(self.labelFontSize)

        self.canvasGraph.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3 = QVBoxLayout(self.widgetGraph)
        self.verticalLayout_3.addWidget(self.canvasGraph)
        self.verticalLayout_3.setSpacing(5)

        self.widgetGraph.setLayout(self.verticalLayout_3)
        #self.widgetGraph.setStyleSheet("border: 1px solid black;")

        self.widgetGraph.setMinimumHeight(200)

        self.verticalLayout_2.addWidget(self.widgetGraph)

        self.textInGraph = pg.TextItem(text="", color="#000000")
        self.textInGraph.setPos(0, 100)
        self.textInGraph.hide()
        self.canvasGraph.addItem(self.textInGraph)
        self.setTextToShowInGraph()

        self.widgetBottom = QWidget()
        self.widgetBottom.setObjectName(u"widgetBottom")
        self.widgetBottom.setContentsMargins(0, 0, 0, 0)
        self.widgetBottom.setMinimumSize(QSize(0, 0))
        self.widgetBottom.setMaximumSize(QSize(16777215, 999999))
        self.horizontalLayout_2 = QHBoxLayout(self.widgetBottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.horizontalSpacer01 = QSpacerItem(8, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer01)

        self.tableWidgetMarker = AutoSizedTable(self.widgetBottom)
        self.tableWidgetMarker.setObjectName(u"tableWidgetMarker")
        self.tableWidgetMarker.setMinimumSize(QSize(0, 0))
        self.tableWidgetMarker.setMaximumSize(QSize(2500, 500))
        self.tableWidgetMarker.setAutoScroll(False)
        self.tableWidgetMarker.setProperty("isWrapping", True)
        self.tableWidgetMarker.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidgetMarker.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidgetMarker.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidgetMarker.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.tableWidgetMarker.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetMarker.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidgetMarker.setShowGrid(False)
        self.tableWidgetMarker.horizontalHeader().setVisible(False)
        self.tableWidgetMarker.verticalHeader().setVisible(False)
        self.tableWidgetMarker.setColumnCount(2)
        self.tableWidgetMarker.setRowCount(6)
        self.tableWidgetMarker.verticalHeader().setMinimumSectionSize(0)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidgetData.sizePolicy().hasHeightForWidth())
        self.tableWidgetMarker.setStyleSheet("""QTableView::item:selected {background: none;}""")
        self.tableWidgetMarker.setSizePolicy(sizePolicy2)

        self.tableWidgetMarker.setStyleSheet("QTableView::item{font: 12pt;}"
                                             "QTableView::item:selected {background: none;}"
                                             "QTableWidget::item { margin: 0px; "
                                             "background-color: white; }")

        self.tableWidgetMarker.cellDoubleClicked.connect(self.onTableMarkerCellClicked)
        self.tableWidgetMarker.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.horizontalLayout_2.addWidget(self.tableWidgetMarker)

        self.horizontalSpacer_2 = QSpacerItem(369, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.textEditComment = QTextEdit(self.widgetBottom)
        self.textEditComment.setObjectName(u"textEditComment")
        self.textEditComment.setMaximumSize(QSize(200, 16777215))
        self.textEditComment.setText(self.dataModel.getComment())
        self.textEditComment.setStyleSheet("QTextEdit { background-color: white; color: black; }")

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

        self.checkBoxShowInGraphInfo = QCheckBox(self.widgetMenu)
        self.checkBoxShowInGraphInfo.setObjectName(u"checkBoxShowInGraphInfo")
        self.checkBoxShowInGraphInfo.setText("")
        self.checkBoxShowInGraphInfo.checkStateChanged.connect(self.showInfoInGraph)

        self.horizontalSpacer_3 = QSpacerItem(200, 35, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)
        self.horizontalLayout_3.addWidget(self.checkBoxHideTop)
        self.horizontalLayout_3.addWidget(self.checkBoxHideBot)
        self.horizontalLayout_3.addWidget(self.checkBoxShowInGraphInfo)

        self.widgetMenu.setLayout(self.horizontalLayout_3)

        self.verticalLayout_2.addWidget(self.widgetMenu)

        self.setContentsMargins(0, 0, 0, 0)

        sizePolicyMT = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicyMT.setHorizontalStretch(0)
        sizePolicyMT.setVerticalStretch(0)  #self.heightWidgetTopPerc)
        sizePolicyMT.setHeightForWidth(self.widgetTop.sizePolicy().hasHeightForWidth())
        self.widgetTop.setSizePolicy(sizePolicyMT)

        sizePolicyMG = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicyMG.setHorizontalStretch(0)
        sizePolicyMG.setVerticalStretch(0)  #self.heightWidgetGraphPerc)
        sizePolicyMG.setHeightForWidth(self.widgetTop.sizePolicy().hasHeightForWidth())
        self.widgetTop.setSizePolicy(sizePolicyMG)

        sizePolicyMB = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicyMB.setHorizontalStretch(0)
        sizePolicyMB.setVerticalStretch(0)  #self.heightWidgetBottomPerc)
        sizePolicyMB.setHeightForWidth(self.widgetBottom.sizePolicy().hasHeightForWidth())
        self.widgetBottom.setSizePolicy(sizePolicyMB)

        self.verticalLayout_2.setStretchFactor(self.widgetTop, self.heightWidgetTopPerc)
        self.verticalLayout_2.setStretchFactor(self.widgetBottom, self.heightWidgetBottomPerc)
        self.verticalLayout_2.setStretchFactor(self.widgetGraph, self.heightWidgetGraphPerc)
        self.setLayout(self.verticalLayout_2)

    def updateUi(self):
        self.heightWidgetTopPerc = self.settingsWindow.getSettingsVariable("heightWidgetTopPerc")
        self.heightWidgetGraphPerc = self.settingsWindow.getSettingsVariable("heightWidgetGraphPerc")
        self.heightWidgetBottomPerc = self.settingsWindow.getSettingsVariable("heightWidgetBottomPerc")
        self.markerHeightPerc = self.settingsWindow.getSettingsVariable("markerHeightPerc")
        self.canvasGraph.colorBackgroundHex = QColor(self.settingsWindow.getSettingsVariable("colorBackground"))
        self.canvasGraph.colorWhileMarkingHex = QColor(self.settingsWindow.getSettingsVariable("colorBackgroundMarking"))
        self.canvasGraph.changeAxisFontsize(self.settingsWindow.getSettingsVariable("labelFontSize"))
        self.strsToShowInGraph = self.settingsWindow.getSettingsVariable("strsToShowInGraph")
        self.resetWidgetsRelSpace()
        self.setTextToShowInGraph()

    def initializeData(self):
        dataSet = self.dataModel.getTablaTopData()
        for i in range(len(dataSet[0])):
            m = i % 6
            n = (i // 6) + 1 * (i // 6)
            l = i // 6 + 1 + 1 * (i // 6)
            self.tableWidgetData.setItem(m, n, dataSet[0][i])
            self.tableWidgetData.setItem(m, l, dataSet[1][i])

        self.tableWidgetData.cellChanged.connect(self.onCellChangeTableTop)

        for markerState in self.dataModel.markerStateList:
            self.canvasGraph.addMarker(markerState)

    def onCellChangeTableTop(self, row, column):
        # todo fix size of last column, check if entry is longer and if make size relative to content again
        item = self.tableWidgetData.item(row, column)
        entry = item.text()
        print(f'entry on cellchanged {entry}')
        if entry:
            if column % 2 != 0:
                while re.match(r'^\s*:', entry):
                    entry = ''.join(entry.split(':')[1:]).lstrip()

                tableEntry = ': ' + entry.lstrip()

                item.setText(tableEntry)
                self.tableWidgetData.setItem(row, column, item)
                self.dataModel.changeCustomDataEntry(row, column, entry)

    def changeTableTopEntry(self, row, column, entry):
        item = self.tableWidgetData.item(row, column)
        print(f'MY TEXT IS: {item.text()}')
        item.setText(entry)
        self.tableWidgetData.setItem(row, column, item)
        self.dataModel.changeCustomDataEntry(row, column, entry)
        print(f'THIS IS {self.name}')

    def windowClosedByUser(self):
        self.flagWindowClosedByUserSignal = True

    def windowClosedProgrammatically(self):
        self.flagWindowClosedByUserSignal = False

    def addTableMarkerEntry(self, index, name, color, x, dx):
        # @todo overload class to get a on_item_changed(self, item) signal and use it to change the markers
        row = index % 6
        column = index // 6 + 1 * index // 6

        x = round(x, 2)
        dx = round(dx, 2)

        if index >= 6:
            if index % 6 == 0:
                n = self.tableWidgetMarker.columnCount()
                self.tableWidgetMarker.setColumnCount(n + 2)

        if name != "":
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
            itemName = QTableWidgetItem(name)
            itemName.setIcon(icon)
            itemNumbers = QTableWidgetItem(": {0} cm bis {1} cm".format(x, dx))
            itemName.setForeground(QColor("#000000"))
            itemNumbers.setForeground(QColor("#000000"))
        else:
            itemName = None
            itemNumbers = None
            '''
            rowStart = row % 6 + (1 - row // 6) # get the next row index
            columnStart = column + row // 6
            for i in range(columnStart, self.tableWidgetMarker.columnCount()):
                for j in range(rowStart, self.tableWidgetMarker.rowCount()):
                    item = self.tableWidgetMarker.item(j, i)
                    if item is not None:
                        item.setText("")
            '''
        print("~~~~~~~~ addTableMarkerEntry ~~~~~~~~~~")
        print(" Index: {0}\n row: {1}\n column: {2}\n name: {3}".format(index, row, column, itemName))
        self.tableWidgetMarker.setItem(row, column, itemName)
        self.tableWidgetMarker.setItem(row, column + 1, itemNumbers)

    def onTableMarkerCellClicked(self, row, column):
        if column % 2 == 0:
            name, col = self.mainWindow.openPickMarker(self.defaultMarkerDictName)
            if name:
                self.updateTableMarkerEntryNameCol(row + column, name, col, )
                self.canvasGraph.changeMarker(row + column, _name=name, _color=col)
        else:
            item = self.tableWidgetMarker.item(row, column)
            x0 = float(item.text().split(" ")[1])
            x1 = float(item.text().split(" ")[4])
            test = RangeDialog(x0, x1)
            if test.exec():
                x0 = float(test.editFrom.text()) + self.dxMarkerForTable
                x1 = float(test.editTo.text()) + self.dxMarkerForTable
                self.updateTableMarkerEntryRangeCol(row, column, x0, x1)
                self.canvasGraph.changeMarker(row + column - 1, _x0=x0, _x1=x1)

    def updateTableMarkerEntry(self, index, name, color, xPar, dxPar):
        row = index % 6
        column = index // 6 + 1 * index // 6
        x = xPar - self.dxMarkerForTable
        dx = dxPar - self.dxMarkerForTable
        pixmap = QPixmap(30, 30)
        pixmap.fill(QColor(color))
        icon = QIcon(pixmap)

        itemName = QTableWidgetItem(name)
        itemName.setIcon(icon)
        itemName.setForeground(QColor("#000000"))

        item = QTableWidgetItem(": {0} cm bis {1} cm".format(round(x, 2), round(dx, 2)))
        item.setForeground(QColor("#000000"))

        self.tableWidgetMarker.setItem(row, column, itemName)
        self.tableWidgetMarker.setItem(row, column + 1, item)

    def updateTableMarkerEntryNameCol(self, index, name, color):
        row = index % 6
        column = index // 6 + 1 * index // 6

        pixmap = QPixmap(30, 30)
        pixmap.fill(QColor(color))
        icon = QIcon(pixmap)

        itemName = QTableWidgetItem(name)
        itemName.setIcon(icon)
        itemName.setForeground(QColor("#000000"))

        self.tableWidgetMarker.setItem(row, column, itemName)

    def updateTableMarkerEntryRangeCol(self, row, column, x0Par, x1Par):
        x0 = x0Par - self.dxMarkerForTable
        x1 = x1Par - self.dxMarkerForTable
        item = QTableWidgetItem(": {0} cm bis {1} cm".format(round(x0, 2), round(x1, 2)))
        self.tableWidgetMarker.setItem(row, column, item)

    def changeXAxisZero(self, xOffset):
        bottom_axis = self.canvasGraph.getPlotItem().getAxis("bottom")
        bottom_axis.setOffset(xOffset)
        bottom_axis.updateTicks()
        self.canvasGraph.getPlotItem().setAxisItems({"bottom": bottom_axis})
        self.canvasGraph.getPlotItem().update()

    def setTextToShowInGraph(self):
        textStr = ""
        maxLen = 0
        for key in self.strsToShowInGraph:
            textStr += f"{self.dataModel.getNameByKey(key)}: {self.dataModel.getDataByKey(key)}\n"
            maxLen = max(maxLen, len(f"{self.dataModel.getNameByKey(key)}: {self.dataModel.getDataByKey(key)}"))
        self.textInGraph.setText(textStr[:-1])

    def changeFileDefaultPresetName(self, defaultPresetName):
        self.canvasGraph.fileDefaultMarkerDictName = defaultPresetName
        self.defaultMarkerDictName = defaultPresetName
        self.dataModel.fileDefaultPresetName = defaultPresetName

    def changeWidgetsRelSpace(self, topPerc, graphPerc, botPerc, saveValues=False):
        if topPerc + graphPerc + botPerc > 100:
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

    def showInfoInGraph(self):
        if self.checkBoxShowInGraphInfo.isChecked():
            self.textInGraph.show()
        else:
            self.textInGraph.hide()

    def hideEverything(self):
        self.widgetTop.hide()
        self.widgetBottom.hide()

    def showEverything(self):
        self.widgetTop.show()
        self.widgetBottom.show()
        self.widgetRight.show()

    def getCurrentState(self):
        self.saveComment()
        state = {}
        state.update({"data": self.dataModel.getSaveState()})
        markerStateList = self.canvasGraph.getCanvasState()

        print(markerStateList)
        state.update({"markerState": markerStateList})

        state.update({"dx_xlim": self.dxMarkerForTable})
        self.logger.info("state: {0}".format(state))
        return state

    def saveComment(self):
        self.dataModel.setComment(self.textEditComment.toPlainText())

    def openPickMarkerFromGraph(self, defaultPresetName):
        return self.mainWindow.openPickMarker(defaultPresetName)

    def copy(self):
        return WidgetGraph(self.mainWindow, "", self.getCurrentState())

# @todo put the create marker function in here for loading and saving reasons
