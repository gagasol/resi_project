from PySide6.QtCore import QSize, Qt, QCoreApplication
from PySide6.QtGui import QFont, QPixmap

import settingsWindow
import widgetGraph


class PrintWindow:
    def __init__(self, graphWidget: widgetGraph.WidgetGraph, settings: settingsWindow.SettingsWindow,
                 suffix: str, filename: str):
        self.suffix = suffix
        self.graphWidget = graphWidget
        self.settings = settings
        self.currentGraphWidth = graphWidget.width()
        self.currentGraphHeight = graphWidget.height()

        self.fontDataUneven = graphWidget.tableWidgetData.item(0, 0).font()
        self.fontDataEven = graphWidget.tableWidgetData.item(0, 1).font()

        self.tableDataWidth = graphWidget.tableWidgetData.width()
        self.tableMarkerHeight = graphWidget.tableWidgetData.height()

        try:
            self.fontMarkerTable = graphWidget.tableWidgetMarker.item(0, 0).font()
        except AttributeError:
            self.fontMarkerTable = None
            graphWidget.tableWidgetMarker.hide()

        if '.rgp' in filename:
            self.filename = './data/' + filename.replace('rpg', 'suffix')
        else:
            self.filename = './data/' + filename + f'.{suffix}'

        self.prepareWidgetForPrint(1920, 1080)
        self.printPng()
        self.resetWidgetAfterPrint()
        print(f'filename: {self.filename}')

    def prepareWidgetForPrint(self, resizeWidth, resizeHeight):
        heightTop = self.settings.getSettingsVariable("printHeightWidgetTopPerc")
        heightGraph = self.settings.getSettingsVariable("printHeightWidgetGraphPerc")
        heightBottom = self.settings.getSettingsVariable("printHeightWidgetBottomPerc")
        fontSize = self.settings.getSettingsVariable("printFontSize")

        self.toggleUI('hide', True)

        self.graphWidget.changeWidgetsRelSpace(heightTop, heightGraph, heightBottom)
        self.graphWidget.canvasGraph.changeAxisFontsize(26)

        for i in range(self.graphWidget.tableWidgetData.rowCount()):
            for j in range(self.graphWidget.tableWidgetData.columnCount()):
                item = self.graphWidget.tableWidgetData.item(i, j)
                if item:
                    font = item.font()
                    font.setWeight(QFont.Normal)
                    font.setPointSize(fontSize)
                    item.setFont(font)

        totalWidth = 0
        for i in range(self.graphWidget.tableWidgetData.columnCount()):
            totalWidth += self.graphWidget.tableWidgetData.columnWidth(i)

        self.graphWidget.tableWidgetData.setFixedWidth(totalWidth)

        if not self.graphWidget.tableWidgetMarker.isHidden():
            for i in range(self.graphWidget.tableWidgetMarker.rowCount()):
                for j in range(self.graphWidget.tableWidgetMarker.columnCount()):
                    item = self.graphWidget.tableWidgetMarker.item(i, j)
                    if item:
                        font = item.font()
                        font.setPointSize(fontSize - 2)
                        item.setFont(font)



        if self.graphWidget.textEditComment.toPlainText() == '':
            self.graphWidget.textEditComment.hide()

        self.graphWidget.resize(resizeWidth, resizeHeight)

    def resetWidgetAfterPrint(self):
        self.graphWidget.resetWidgetsRelSpace()

        labelFontSize = self.settings.getSettingsVariable("labelFontSize")
        self.toggleUI('show', False)
        self.graphWidget.canvasGraph.changeAxisFontsize(labelFontSize)

        for i in range(self.graphWidget.tableWidgetData.rowCount()):
            for j in range(self.graphWidget.tableWidgetData.columnCount()):
                item = self.graphWidget.tableWidgetData.item(i, j)
                if item:
                    if j%2 == 0:
                        item.setFont(self.fontDataUneven)
                    else:
                        item.setFont(self.fontDataEven)

        self.graphWidget.tableWidgetData.setFixedWidth(self.tableDataWidth)

        if not self.graphWidget.tableWidgetMarker.isHidden():
            for i in range(self.graphWidget.tableWidgetMarker.rowCount()):
                for j in range(self.graphWidget.tableWidgetMarker.columnCount()):
                    item = self.graphWidget.tableWidgetMarker.item(i, j)
                    if item:
                        item.setFont(self.fontMarkerTable)
            self.graphWidget.tableWidgetMarker.setFixedHeight(self.tableMarkerHeight)
        else:
            self.graphWidget.tableWidgetMarker.show()

        self.graphWidget.resize(self.currentGraphWidth, self.currentGraphHeight)
        QCoreApplication.processEvents()

    def createPixmap(self, width, height):
        scaledPixmap = QPixmap(QSize(width, height))
        scaledPixmap.fill(Qt.transparent)

        return scaledPixmap

    def toggleUI(self, attr, noBackground):
        self.graphWidget.setAttribute(Qt.WA_NoSystemBackground, noBackground)
        #self.graphWidget.setAttribute(Qt.TranslucentBackground, noBackground)
        widgets = [self.graphWidget.widgetMenu,
                   self.graphWidget.labelData,
                   self.graphWidget.canvasGraph.vLine]

        for widget in widgets:
            getattr(widget, attr)()
    def printPdf(self):
        pass

    def printPng(self):
        printImage = self.createPixmap(1920, 1080)
        QCoreApplication.processEvents()
        self.graphWidget.render(printImage)
        printImage.save(self.filename)
