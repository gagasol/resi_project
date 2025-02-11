from typing import Optional, Union

from PySide6.QtCore import QSize, Qt, QCoreApplication, QMarginsF, QSizeF
from PySide6.QtGui import QFont, QPixmap, QPainter, QPageSize, QTransform, QFontMetrics
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import QDialog

import settingsWindow
from widgetGraph import WidgetGraph

from ui_files.ui_printWindow import Ui_printWindow


class PrintWindow(QDialog):
    def __init__(self, listGraphWidget: list[WidgetGraph], settings: settingsWindow.SettingsWindow,
                 parent=None):
        super().__init__(parent)
        self.ui = Ui_printWindow()
        self.ui.setupUi(self)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        graphWidgetNames = [graph.name for graph in listGraphWidget]

        self.ui.createNameList(graphWidgetNames)

        self.listGraphWidgets = listGraphWidget
        self.settings = settings
        self.suffix = 'png'
        self.removeFromHeightPerc = 0

    def getPrintWidgetGraph(self, graphWidgetAtt: WidgetGraph, suffix: str, width: int, height: int) -> WidgetGraph:

        graphWidget = graphWidgetAtt.copy()

        currentGraphWidth = graphWidget.width()
        currentGraphHeight = graphWidget.height()

        fontDataUneven = graphWidget.tableWidgetData.item(0, 0).font()
        fontDataEven = graphWidget.tableWidgetData.item(0, 1).font()

        tableDataWidth = graphWidget.tableWidgetData.width()

        outputWidth = width
        outputHeight = height

        try:
            fontMarkerTable = graphWidget.tableWidgetMarker.item(0, 0).font()
            tableMarkerHeight = graphWidget.tableWidgetData.height()
        except AttributeError:
            fontMarkerTable = None
            graphWidget.tableWidgetMarker.hide()

        if 'png' in suffix:
            graphWidget.resize(outputWidth, outputHeight)
            self.prepareWidgetForPrint(graphWidget, outputWidth, outputHeight)
        elif 'pdf' in suffix:
            dpi = 300
            widthRatio = (8.27 * dpi) / outputWidth
            heightRatio = (8.27 * dpi) / outputHeight

            ratio = min(widthRatio, heightRatio)

            outputWidth = int((210 * dpi) / 25.4)
            outputHeight = int(outputWidth * (1080 / 1920))

            print(f'Width: {outputWidth}, Height: {outputHeight}')

            self.prepareWidgetForPrint(graphWidget, outputWidth, outputHeight)

        return graphWidget

    @staticmethod
    def getFilePathFromGraph(graph: WidgetGraph, filename: str, suffix: str) -> str:
        pathToFile = graph.dataModel.fileDefaultSavePath
        if '.rgp' in filename:
            filePath = pathToFile + '/' + filename.replace('rgp', suffix)
        else:
            filePath = pathToFile + '/' + filename + f'.{suffix}'

        return filePath

    def prepareWidgetForPrint(self, graphWidget: WidgetGraph, resizeWidth: int, resizeHeight: int):
        graphWidget.resize(resizeWidth, resizeHeight)

        heightTop = self.settings.getSettingsVariable("printHeightWidgetTopPerc")
        heightGraph = self.settings.getSettingsVariable("printHeightWidgetGraphPerc")
        heightBottom = self.settings.getSettingsVariable("printHeightWidgetBottomPerc")
        fontSize = int(self.settings.getSettingsVariable("printFontSize"))
        printLabelFontSize = int(self.settings.getSettingsVariable("printLabelFontSize"))

        maxRows = self.settings.getSettingsVariable('defaultMarkerTableRows')
        maxRows = maxRows if 0 < maxRows <= len(graphWidget.canvasGraph.markerList) else (
            len(graphWidget.canvasGraph.markerList))

        graphWidget.maxRows = maxRows
        graphWidget.updateTableMarker()

        # todo put this into a function fitHeightToFontSize(height, fontSize, rows) -> newHeight
        if maxRows == 0:
            graphWidget.widgetBottom.hide()
            maxRows = 1

        heightTop, deltaTop, tableDataMaxItemHeight = (
            self.fitHeightToFontSize(resizeHeight, heightTop, fontSize, 6))
        heightBottom, deltaBottom, tableMarkerMaxItemHeight = (
            self.fitHeightToFontSize(resizeHeight, heightBottom, fontSize, maxRows))

        heightGraph += int(deltaTop) + int(deltaBottom)

        print(f'prepareWidgetForPrint: Top: {heightTop}, Bot: {heightBottom}, Graph: {heightGraph}')

        self.toggleUI(graphWidget, 'hide', True)

        widgets = {
            self.ui.checkBoxShowTop: graphWidget.widgetTop,
            self.ui.checkBoxShowBottom: graphWidget.widgetBottom,
            self.ui.checkBoxShowData: graphWidget.textInGraph
        }

        for checkbox, widget in widgets.items():
            if checkbox.isChecked():
                widget.show()
            else:
                widget.hide()

        graphWidget.changeWidgetsRelSpace(heightTop, heightGraph, heightBottom)
        graphWidget.canvasGraph.changeAxisFontsize(printLabelFontSize)

        graphWidget.tableWidgetData.show()
        for i in range(graphWidget.tableWidgetData.rowCount()):
            for j in range(graphWidget.tableWidgetData.columnCount()):
                item = graphWidget.tableWidgetData.item(i, j)
                if item:
                    graphWidget.tableWidgetData.adjustFontsizeToHeight(item, fontSize, 5, tableDataMaxItemHeight)

        totalWidth = 0
        for i in range(graphWidget.tableWidgetData.columnCount()):
            totalWidth += graphWidget.tableWidgetData.columnWidth(i)

        graphWidget.tableWidgetData.setFixedWidth(totalWidth)
        graphWidget.tableWidgetData.clearSelection()

        if not graphWidget.tableWidgetMarker.isHidden():
            iconSize = fontSize
            graphWidget.tableWidgetMarker.setIconSize(QSize(int(iconSize + iconSize * 0.5), iconSize))
            for i in range(graphWidget.tableWidgetMarker.rowCount()):
                for j in range(graphWidget.tableWidgetMarker.columnCount()):
                    item = graphWidget.tableWidgetMarker.item(i, j)
                    if item:
                        graphWidget.tableWidgetData.adjustFontsizeToHeight(item, fontSize - 2, 5,
                                                                           tableMarkerMaxItemHeight)

            totalHeight = 0
            for i in range(graphWidget.tableWidgetMarker.rowCount()):
                totalHeight += graphWidget.tableWidgetMarker.rowHeight(i)
                print(f'printWindow.prepareWidgetForPrint: row {i} height {graphWidget.tableWidgetData.rowHeight(i)}')

            print(f'rows multiplied: {graphWidget.tableWidgetMarker.rowCount() * graphWidget.tableWidgetMarker.rowHeight(0)}')
            print(f'row count: {graphWidget.tableWidgetMarker.rowCount()}')
            print(f'printWindow.prepareWidgetForPrint: Total height: {totalHeight}')

            graphWidget.tableWidgetMarker.resizeRowsToContents()
            #self.graphWidget.tableWidgetMarker.setFixedHeight(totalHeight)
            graphWidget.tableWidgetMarker.clearSelection()

        if graphWidget.textEditComment.toPlainText() == '':
            graphWidget.textEditComment.hide()
        else:
            comment = graphWidget.textEditComment
            font = comment.font()
            font.setPointSize(fontSize - fontSize * 0.05)
            comment.setFont(font)
            comment.setFixedWidth(600)

        print('PrintWindow.prepareWidgetForPrint done')

        #self.graphWidget.resize(resizeWidth, resizeHeight)

    def fitHeightToFontSize(self, heightTotal: int, heightPercentage: float, fontSize: int, rows: int) \
            -> [float, float, float]:
        newHeightPercentage = heightPercentage
        deltaPercentage = 0

        if rows == 0:
            return newHeightPercentage, 0, 0

        tableMaxItemHeight = (heightTotal * heightPercentage / 100) / rows

        fontMetric = QFontMetrics(QFont('', fontSize))

        if heightTotal * heightPercentage / 100 > fontMetric.height() * rows:
            newHeightPercentage = ((fontMetric.height() * rows) / heightTotal) * 100
            deltaPercentage = abs(heightPercentage - newHeightPercentage)


        return newHeightPercentage, deltaPercentage, tableMaxItemHeight

    '''def resetWidgetAfterPrint(self):
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
        QCoreApplication.processEvents()'''

    def toggleUI(self, graphWidget, attr, noBackground):
        graphWidget.setAttribute(Qt.WA_NoSystemBackground, noBackground)
        widgets = [graphWidget.widgetMenu,
                   graphWidget.labelData,
                   graphWidget.canvasGraph.vLine]

        for widget in widgets:
            getattr(widget, attr)()

    def printPixmap(self, pixmap, filePath, suffix):
        if suffix == 'png':
            pixmap.save(filePath, 'png')
        elif suffix == 'pdf':
            self.printPdf(pixmap, filePath)

    def printPdf(self, pixmap: QPixmap, filePath: str):
        orientation = self.ui.comboBoxPageOrient.currentText()
        dpi = 300

        width = 210.0 if orientation == 'horizontal' else 297.0

        pageSize = QPageSize(QSizeF(width, (pixmap.height() / dpi) * 25.4),
                             QPageSize.Millimeter)

        printer = QPrinter()
        printer.setPageSize(pageSize)
        printer.PrinterMode.HighResolution
        printer.setResolution(dpi)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPageMargins(QMarginsF(0, 0, 0, 0))
        printRect = printer.pageLayout().paintRectPixels(printer.resolution())

        printer.setOutputFileName(filePath)
        painter = QPainter(printer)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

    def convertGraphsToPixmap(self, graphs: list[WidgetGraph], suffix: str, rows: int,
                              columns: int) -> Union[QPixmap, None]:

        amount = len(graphs)
        if amount <= 0:
            return None

        if 'png' in suffix:
            printWidth = int(self.ui.lineEditDimWidth.text())
            printHeight = int(self.ui.lineEditDimHeight.text())
            width = printWidth * columns
            height = printHeight * rows
        else:
            dpi = 300
            orientation = self.ui.comboBoxPageOrient.currentText()
            print(orientation)
            if orientation == 'vertical':
                graphsPerPageHeight = rows if rows < 2 else 2
                width = int((297 * dpi) / 25.4)
                height = (width * (1920 / 1080)) * graphsPerPageHeight
                maxHeight = int((210 * dpi) / 25.4)
            else:
                graphsPerPageHeight = rows if rows < 4 else 4
                width = int((210 * dpi) / 25.4)
                height = (width * (1080 / 1920)) * graphsPerPageHeight
                maxHeight = int((297 * dpi) / 25.4)

            if height > maxHeight:
                height = maxHeight

            printWidth = int(width / columns)
            printHeight = int(height / graphsPerPageHeight)

        addedPixmap = QPixmap(QSize(width, height))
        addedPixmap.fill(Qt.transparent)

        painter = QPainter(addedPixmap)

        for i in range(rows):
            for j in range(columns):
                try:
                    graph = graphs[j + (i * columns)].copy()
                    self.prepareWidgetForPrint(graph, printWidth, printHeight)
                    tmpPixmap = graph.grab()
                    tmpPixmap = tmpPixmap.scaled(printWidth, printHeight)
                    painter.drawPixmap(j * printWidth, i * printHeight, tmpPixmap)
                except IndexError:
                    print('PrintWindow.convertGraphsToPixmap(): IndexError')
                    break

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

    def quickExportAs(self, graphWidget: WidgetGraph, suffix: str, filename: str):
        width = 1920
        height = 1080
        pixmapToPrint = self.getPrintWidgetGraph(graphWidget, suffix, width, height).grab()
        filePath = self.getFilePathFromGraph(graphWidget, filename, suffix)
        self.printPixmap(pixmapToPrint, filePath, suffix)

    def exportSelectedGraphs(self):
        graphsToPrint = []
        checkboxes = self.ui.checkedBoxes

        checkboxes = sorted(checkboxes, key=lambda x: x.objectName())

        printCount = len(checkboxes)

        suffix = self.ui.comboBoxSuffix.currentText()

        rows = self.ui.spinBoxRowTotal.value()
        columns = self.ui.spinBoxColumnTotal.value()

        graphsPerPage = rows * columns

        pages = printCount // graphsPerPage
        print(f'pages: {pages}')
        counterExtension = -1 if pages > 1 else 1

        filename = self.ui.lineEditPrintName.text()

        for i, box in enumerate(checkboxes):
            name = box.text()
            for graphWidget in self.listGraphWidgets:
                if name in graphWidget.name:
                    print(f'### printWindow.exportSelectedGraphs() ###\n Boxtext {name} Boxname {box.objectName()}')
                    graphsToPrint.append(graphWidget)
                    filePath = self.getFilePathFromGraph(graphWidget, name, suffix)
                    if (i + 1) % graphsPerPage == 0:
                        if graphsPerPage > 1:
                            filePath = filePath.rsplit('/', 1)[0]
                            count = '_' + str(counterExtension) if counterExtension >= 1 else ''
                            filePath += '/' + filename + count + '.' + suffix
                            counterExtension += 1
                            print(f'ACCEPTED FILEPATH {filePath}')
                        pixmapToPrint = self.convertGraphsToPixmap(graphsToPrint, suffix, rows, columns)
                        self.printPixmap(pixmapToPrint, filePath, suffix)
                        print(f'printWindow.exportSelectedGraphs : Filepath {filePath}')
                        graphsToPrint.clear()

        pixmapToPrint = self.convertGraphsToPixmap(graphsToPrint, suffix, rows, columns)
        if pixmapToPrint:
            self.printPixmap(pixmapToPrint, filePath, suffix)

    def accept(self):
        self.exportSelectedGraphs()
        '''graphsToPrint = []
        checkboxes = self.ui.checkedBoxes

        checkboxes = sorted(checkboxes, key=lambda x: x.objectName())

        printCount = len(checkboxes)

        suffix = self.ui.comboBoxSuffix.currentText()

        rows = self.ui.spinBoxRowTotal.value()
        columns = self.ui.spinBoxColumnTotal.value()

        graphsPerPage = rows * columns

        pages = printCount // graphsPerPage
        print(f'pages: {pages}')
        counterExtension = -1 if pages > 1 else 1

        filename = self.ui.lineEditPrintName.text()

        for i, box in enumerate(checkboxes):
            name = box.text()
            for graphWidget in self.listGraphWidgets:
                if name == graphWidget.name:
                    pixmap, filePath = self.createPixmap(graphWidget, suffix, name)
                    print(f'### printWindow.accept() ###\n Boxtext {name} Boxname {box.objectName()}')
                    graphsToPrint.append(pixmap)
                    if (i + 1) % graphsPerPage == 0:
                        if graphsPerPage > 1:
                            filePath = filePath.rsplit('/', 1)[0]
                            count = '_' + str(counterExtension) if counterExtension >= 1 else ''
                            filePath += '/' + filename + count + '.' + suffix
                            counterExtension += 1
                            print(f'ACCEPTED FILEPATH {filePath}')
                        pixmapToPrint = self.addPixmaps(graphsToPrint, rows, columns)
                        self.printPixmap(pixmapToPrint, filePath, suffix)
                        graphsToPrint.clear()

        pixmapToPrint = self.addPixmaps(graphsToPrint, rows, columns)
        if pixmapToPrint:
            self.printPixmap(pixmapToPrint, filePath, suffix)'''

        super().accept()

    def reject(self):
        print('Challenge rejected')
        super().reject()
