from PySide6.QtCore import QSize, Qt, QCoreApplication, QMarginsF
from PySide6.QtGui import QFont, QPixmap, QPainter, QPageSize, QTransform
from PySide6.QtPrintSupport import QPrinter

import settingsWindow
import widgetGraph


class PrintWindow:
    def __init__(self, graphWidget: widgetGraph.WidgetGraph, settings: settingsWindow.SettingsWindow,
                 suffix: str, filename: str):
        self.suffix = suffix
        self.graphWidget = graphWidget.copy()
        self.settings = settings
        self.currentGraphWidth = graphWidget.width()
        self.currentGraphHeight = graphWidget.height()

        self.fontDataUneven = graphWidget.tableWidgetData.item(0, 0).font()
        self.fontDataEven = graphWidget.tableWidgetData.item(0, 1).font()

        self.tableDataWidth = graphWidget.tableWidgetData.width()

        self.outputWidth = 1920
        self.outputHeight = 1080

        try:
            self.fontMarkerTable = graphWidget.tableWidgetMarker.item(0, 0).font()
            self.tableMarkerHeight = graphWidget.tableWidgetData.height()
        except AttributeError:
            self.fontMarkerTable = None
            graphWidget.tableWidgetMarker.hide()

        if '.rgp' in filename:
            self.filename = graphWidget.dataModel.fileDefaultSavePath + '/' + filename.replace('rgp', suffix)
        else:
            self.filename = graphWidget.dataModel.fileDefaultSavePath + '/' + filename + f'.{suffix}'

        if 'png' in suffix:
            self.prepareWidgetForPrint(1920, 1080)
            self.printPng()
            self.resetWidgetAfterPrint()
            print(f'png filename: {self.filename}')
        elif 'pdf' in suffix:
            self.prepareWidgetForPrint(1920, 1080)
            self.printPdf()
            self.resetWidgetAfterPrint()
            print(f'pdf filename: {self.filename}')


    def prepareWidgetForPrint(self, resizeWidth, resizeHeight):
        self.graphWidget.resize(resizeWidth, resizeHeight)

        heightTop = self.settings.getSettingsVariable("printHeightWidgetTopPerc")
        heightGraph = self.settings.getSettingsVariable("printHeightWidgetGraphPerc")
        heightBottom = self.settings.getSettingsVariable("printHeightWidgetBottomPerc")
        fontSize = int(self.settings.getSettingsVariable("printFontSize"))

        tableDataMaxItemHeight = (self.outputHeight * heightTop/100) / 6
        tableMarkerMaxItemHeight = (self.outputHeight * heightBottom / 100) / 6

        self.toggleUI('hide', True)

        self.graphWidget.changeWidgetsRelSpace(heightTop, heightGraph, heightBottom)
        self.graphWidget.canvasGraph.changeAxisFontsize(26)

        self.graphWidget.tableWidgetData.show()
        for i in range(self.graphWidget.tableWidgetData.rowCount()):
            for j in range(self.graphWidget.tableWidgetData.columnCount()):
                item = self.graphWidget.tableWidgetData.item(i, j)
                if item:
                    print(f'graphSize: {self.graphWidget.size()}')
                    self.graphWidget.tableWidgetData.adjustFontsizeToHeight(item, fontSize, 5, tableDataMaxItemHeight)

        totalWidth = 0
        for i in range(self.graphWidget.tableWidgetData.columnCount()):
            totalWidth += self.graphWidget.tableWidgetData.columnWidth(i)

        self.graphWidget.tableWidgetData.setFixedWidth(totalWidth)
        self.graphWidget.tableWidgetData.clearSelection()

        if not self.graphWidget.tableWidgetMarker.isHidden():
            iconSize = fontSize
            self.graphWidget.tableWidgetMarker.setIconSize(QSize(int(iconSize + iconSize*0.5), iconSize))
            for i in range(self.graphWidget.tableWidgetMarker.rowCount()):
                for j in range(self.graphWidget.tableWidgetMarker.columnCount()):
                    item = self.graphWidget.tableWidgetMarker.item(i, j)
                    if item:
                        self.graphWidget.tableWidgetData.adjustFontsizeToHeight(item, fontSize - 2, 5,
                                                                                tableMarkerMaxItemHeight)

            totalHeight = 0
            for i in range(self.graphWidget.tableWidgetMarker.rowCount()):
                totalHeight += self.graphWidget.tableWidgetMarker.rowHeight(i)
            self.graphWidget.tableWidgetMarker.resizeRowsToContents()
            #self.graphWidget.tableWidgetMarker.setFixedHeight(totalHeight)
            self.graphWidget.tableWidgetMarker.clearSelection()

        if self.graphWidget.textEditComment.toPlainText() == '':
            self.graphWidget.textEditComment.hide()
        else:
            comment = self.graphWidget.textEditComment
            font = comment.font()
            font.setPointSize(fontSize - fontSize*0.05)
            comment.setFont(font)
            comment.setFixedWidth(600)

        #self.graphWidget.resize(resizeWidth, resizeHeight)

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
            iconSize = self.settings.getSettingsVariable("fontSize")
            self.graphWidget.tableWidgetMarker.setIconSize(QSize(iconSize, iconSize))
            for i in range(self.graphWidget.tableWidgetMarker.rowCount()):
                for j in range(self.graphWidget.tableWidgetMarker.columnCount()):
                    item = self.graphWidget.tableWidgetMarker.item(i, j)
                    if item:
                        item.setFont(self.fontMarkerTable)
            #self.graphWidget.tableWidgetMarker.setFixedHeight(self.tableMarkerHeight)
        else:
            self.graphWidget.tableWidgetMarker.show()

        #self.graphWidget.resize(self.currentGraphWidth, self.currentGraphHeight)
        QCoreApplication.processEvents()

    def createPixmap(self, width, height):
        scaledPixmap = QPixmap(QSize(width, height))
        scaledPixmap.fill(Qt.transparent)

        return scaledPixmap

    def toggleUI(self, attr, noBackground):
        self.graphWidget.setAttribute(Qt.WA_NoSystemBackground, noBackground)
        widgets = [self.graphWidget.widgetMenu,
                   self.graphWidget.labelData,
                   self.graphWidget.canvasGraph.vLine]

        for widget in widgets:
            getattr(widget, attr)()
    def printPdf(self):
        dpi = 300
        widthRatio = (8.27 * dpi) / 1920
        printer = QPrinter()
        printer.setPageSize(QPageSize.A4)
        printer.PrinterMode.HighResolution
        printer.setResolution(dpi)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPageMargins(QMarginsF(0, 0, 0, 0))
        printRect = printer.pageLayout().paintRectPixels(printer.resolution())
        print(printRect)

        printer.setOutputFileName(self.filename)
        QCoreApplication.processEvents()
        self.graphWidget.resize(int(1920 * widthRatio), int(1080 * widthRatio))
        pixmap = self.graphWidget.grab()
        painter = QPainter(printer)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

    def printPng(self):
        QCoreApplication.processEvents()
        self.graphWidget.resize(1920, 1080)
        screenshot = self.graphWidget.grab()
        screenshot.save(self.filename, 'png')

    def addPixmaps(self, pixmaps: list[QPixmap]):
        amount = len(pixmaps)
        width = 1920
        height = 1080

        addedPixmap = QPixmap(QSize(width, height))
        addedPixmap.fill(Qt.transparent)

        widthScale = width / pixmaps[0].width()
        heightScale = (height/2) / pixmaps[0].height()

        printWidth = int(width * widthScale)
        printHeight = int(height * 0.5)

        painter = QPainter(addedPixmap)

        for i, pixmap in enumerate(pixmaps):
            tmpPixmap = pixmap.scaled(printWidth, printHeight)
            painter.drawPixmap(0, i * printHeight, tmpPixmap)

        painter.end()

        return addedPixmap

    @staticmethod
    def rotatePixmap(pixmap: QPixmap, angle: float):
        rotatedPixmap = QPixmap(QSize(pixmap.size().height(), pixmap.size().width()))
        rotatedPixmap.fill(Qt.transparent)

        painter = QPainter(rotatedPixmap)
        painter.setTransform(
            QTransform().translate(pixmap.width() / 2, pixmap.height() / 2).rotate(angle))
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return rotatedPixmap

