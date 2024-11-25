from typing import List

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QColor, QAction, QPen, QPainter
from PySide6.QtWidgets import QMessageBox, QMenu, QGraphicsItem
from pyqtgraph import ArrowItem

from markerRectItem import MarkerRectItem


class CustomCircle(pg.EllipseROI):
    def __init__(self, pos, size, angle=0):
        super().__init__(pos, size, angle=angle, movable=True, scaleSnap=True, translateSnap=True)
        self.removeHandle(0)
        self.addRotateHandle([1, 0], [0.5, 0.5])

        arrow_length = min(size) / 2
        self.arrow = pg.ArrowItem(pos=(0.5, 0.5), angle=angle, headLen=arrow_length, tailLen=arrow_length, parent=self)

    def hoverEvent(self, event):
        if event.isExit():
            print("Hover exited")
        elif event.isEnter():
            print("Hover entered")

    def getArrayRegion(self, *args, **kwargs):
        return None

    def scale(self, *args, **kwargs):
        pass

    def rotate(self, *args, **kwargs):
        super().rotate(*args, **kwargs)
        self.arrow.setRotation(self.angle())


class CustomInfiniteLine(pg.InfiniteLine):
    def __init__(self, canvas, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._canvas = canvas
        self.color = self.pen.color()
        self.hoverColor = 'red'
    def updateColor(self, color):
        pen = self.pen
        pen.setColor(color)
        self.setPen(pen)

    def setPenColor(self, color):
        self.color = color
    def setHoverColor(self, color):
        self.hoverColor = color

    def updateWidth(self, width):
        pen = self.pen
        pen.setWidth(width)
        self.setPen(pen)

    def paint(self, painter, *args):
        painter.setRenderHint(QPainter.Antialiasing)
        if self.mouseHovering:
            self.updateColor(self.hoverColor)
        else:
            self.updateColor(self.color)
        super().paint(painter, *args)

    def hoverEvent(self, event):
        if event.isExit():
            self.mouseHovering = False
            self._canvas.removeFocus()
        else:
            self._canvas.focusFigure(self)
            self.mouseHovering = True
        self.update()

    def deleteSelf(self):
        self._canvas.removeFocus()
        self._canvas.deleteFigure(self)


class CustomPlotWidget(pg.PlotWidget):
    def __init__(self, xLimit, parentWindow, defaultMarkerDictName, markerPresetsList, colorBackgroundHex,
                 colorWhileMarkingHex, defaultFont, markerHeightPerc, *args, **kwargs):
        super(CustomPlotWidget, self).__init__(*args, **kwargs)

        self.colorBackgroundHex = QColor(colorBackgroundHex)
        self.colorWhileMarkingHex = QColor(colorWhileMarkingHex)
        self.setBackground(colorBackgroundHex)
        self.setLimits(xMin=0, xMax=xLimit, yMin=-110*markerHeightPerc, yMax=102)
        self.setRange(xRange=(0, xLimit), yRange=(-3, 105))

        self.getAxis("bottom").setLabel(QObject().tr("Tiefe"), units="cm")
        self.getAxis("left").setLabel(QObject().tr("Widerstand"), units="%")
        #self.changeAxisFontsize(11)

        self.getViewBox().sigRangeChanged.connect(self.rangeChanged)
        self.getViewBox().setMenuEnabled(False)

        pen_line = pg.mkPen('black')
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pen_line)
        self.addItem(self.vLine)

        self.markingRegion = pg.LinearRegionItem([0, 0])
        self.markingRegion.hide()
        self.addItem(self.markingRegion)

        # TEST

        # variables
        self.parentWindow = parentWindow
        self.settings = parentWindow.mainWindow.settingsWindow
        self.pickMarkerWin = None
        self.fileDefaultMarkerDictName = self.parentWindow.defaultMarkerDictName
        self.markerPresetNames = markerPresetsList
        self.xLimit = xLimit

        self.lastClicks: List[float] = []
        self.markerList: List[MarkerRectItem] = []
        self.figureList = []
        self.figureInFocus = None

        self.markerHeightPerc = parentWindow.markerHeightPerc

        self.gridLines = {'x': [], 'y': [], 'dx': 0}

        self.markingEnabled = False
        self.draggingMarker = False

        self.createGridLines()

    def changeAxisFontsize(self, fontSize):
        color = self.settings.getSettingsVariable('colorLabel')

        self.getAxis("bottom").setLabel(QObject().tr("Tiefe"), units="cm", color=color,
                                        **{'font-size': str(fontSize) + "pt"})
        self.getAxis("left").setLabel(QObject().tr("Widerstand"), units="%", color=color,
                                      **{'font-size': str(fontSize) + "pt"})

    def initAxisLabels(self):
        fontSize = self.settings.getSettingsVariable('labelFontSize')
        color = self.settings.getSettingsVariable('colorLabel')

        self.getAxis("bottom").setLabel(QObject().tr("Tiefe"), units="cm", color=color,
                                        **{'font-size': str(fontSize) + "pt"})
        self.getAxis("left").setLabel(QObject().tr("Widerstand"), units="%", color=color,
                                      **{'font-size': str(fontSize) + "pt"})
    def changeAxisLabelColor(self, color):
        pass

    def contextMenuEvent(self, event):
        contextMenu = QMenu()

        pos = event.pos()
        axisPos = self.mapToScene(pos)
        mousePoint = self.getPlotItem().vb.mapSceneToView(axisPos)
        marker = self.getMarkerAtPos(mousePoint)

        item1 = QAction(QObject.tr("Reset zoom"), self)
        item1.triggered.connect(self.resetZoom)
        contextMenu.addAction(item1)

        contextMenuMarkingStr = 'Stop marking' if self.markingEnabled else 'Start marking'

        item2 = QAction(QObject.tr(contextMenuMarkingStr), self)
        item2.triggered.connect(self.switchMarkingContextMenu)
        contextMenu.addAction(item2)

        item3 = QAction(QObject.tr('Show grid'))
        item3.triggered.connect(self.toggleGrid)
        contextMenu.addAction(item3)

        addFigurMenu = QMenu(QObject.tr('Add figure'))

        subActionAddArrow = QAction(QObject.tr('Add arrow'))
        subActionAddArrow.triggered.connect(lambda: self.addFigureToPlot('arrow', mousePoint))
        # addFigurMenu.addAction(subActionAddArrow)

        subActionAddLine = QAction(QObject.tr('Add line'))
        subActionAddLine.triggered.connect(lambda: self.addFigureToPlot('vLine', mousePoint))
        addFigurMenu.addAction(subActionAddLine)

        contextMenu.addMenu(addFigurMenu)



        if marker:
            itemDelMarker = QAction(QObject.tr("Delete marker"), self)
            itemDelMarker.triggered.connect(marker.deleteSelf)
            contextMenu.addAction(itemDelMarker)
        elif self.figureInFocus:
            itemDelFigure = QAction(QObject.tr("Delete line"), self)
            itemDelFigure.triggered.connect(self.figureInFocus.deleteSelf)
            contextMenu.addAction(itemDelFigure)


        contextMenu.exec_(event.globalPos())

    def setZoom(self, x0, x1, y0, y1):
        self.setRange(xRange=(x0, x1), yRange=(y0, y1))

    def resetZoom(self):
        self.setRange(xRange=(0, self.xLimit), yRange=(-3, 105))

    def switchMarkingContextMenu(self):
        x = self.lastClicks[0]
        self.switchMarking()
        if self.markingEnabled:
            self.lastClicks.append(x)
            self.markingRegion.setRegion([x, x])
            self.markingRegion.show()

    def createGridLines(self):
        bottomAxis = self.getAxis("bottom")
        axisData = bottomAxis.getAxisData()
        self.gridLines['dx'] = axisData[0]

        xGridInterval = self.settings.getSettingsVariable('defaultGridIntervalX')
        yGridInterval = self.settings.getSettingsVariable('defaultGridIntervalY')
        hexColor = self.settings.getSettingsVariable('gridColor').lstrip('#')
        opacity = self.settings.getSettingsVariable('gridOpacity')
        rgbColor = tuple(int(hexColor[i:i + 2], 16) for i in (0, 2, 4)) + (opacity,)

        ticks = np.arange(0, self.xLimit, xGridInterval)
        xMajorTicks = [x + axisData[0] for x in ticks]

        y = np.arange(0, 100, yGridInterval)

        for val in xMajorTicks:
            pen = pg.mkPen(color=rgbColor, width=0.5)
            gridLine = self.plot([val, val], [0, 100], pen=pen)
            gridLine.setZValue(10)
            gridLine.hide()
            self.gridLines['x'].append(gridLine)

        for val in y:
            pen = pg.mkPen(color=rgbColor, width=0.5)
            gridLine = self.plot([0, self.xLimit], [val, val], pen=pen)
            gridLine.setZValue(10)
            gridLine.hide()
            self.gridLines['y'].append(gridLine)

    def toggleGrid(self):
        for line in self.gridLines['x']:
            line.setVisible(not line.isVisible())
        for line in self.gridLines['y']:
            line.setVisible(not line.isVisible())

    def updateXGrid(self):
        bottomAxis = self.getAxis("bottom")
        axisData = bottomAxis.getAxisData()
        offset = axisData[0] - self.gridLines['dx']
        self.gridLines['dx'] = axisData[0]
        for line in self.gridLines['x']:
            x, y = line.getData()
            x = x + offset
            print(f'x: {x[0]}')
            line.setData(x=x, y=y)

    def repaintGrid(self):
        self.deleteGrid()
        self.createGridLines()

    def deleteGrid(self):
        for line in self.gridLines['x']:
            self.removeItem(line)
        for line in self.gridLines['y']:
            self.removeItem(line)

        self.gridLines['x'] = []
        self.gridLines['y'] = []


    def addFigureToPlot(self, figureName: str, pos):
        if figureName == 'arrow':
            circle = CustomCircle(pos, (2, 5))
            self.figureList.append(circle)
            self.addItem(circle)
            '''
            print(f'xPos: {pos.x()}, yPos: {pos.y()}')
            arrow = CustomArrow(pos=(pos.x(), pos.y()))
            self.figureList.append(arrow)
            self.addItem(arrow)
            arrow.show()
            '''
        elif figureName == 'vLine':
            vLine = CustomInfiniteLine(self, pen='#000000', angle=90, movable=True)
            vLine.setPos(pos.x())
            self.figureList.append(vLine)
            self.addItem(vLine)

    def enterEvent(self, event):
        self.setFocus()
        super().enterEvent(event)

    def mousePressEvent(self, event):
        pos = event.position()

        if self.sceneBoundingRect().contains(pos):

            if self.markingEnabled and event.button() == Qt.LeftButton:
                mousePoint = self.getPlotItem().vb.mapSceneToView(pos)
                self.lastClicks.append(mousePoint.x())
                self.markingRegion.setRegion([mousePoint.x(), mousePoint.x()])
                self.markingRegion.show()

                if len(self.lastClicks) == 2:
                    x = min(self.lastClicks)
                    width = abs(self.lastClicks[0] - self.lastClicks[1])

                    print(self.fileDefaultMarkerDictName)
                    name, col = self.parentWindow.openPickMarkerFromGraph(self.fileDefaultMarkerDictName)

                    if not (name or col):
                        self.markingRegion.hide()
                        self.switchMarking()
                        return

                    if not self.markerList:
                        if "Borke" in name or "Rinde" in name:
                            self.parentWindow.changeXAxisZero(self.lastClicks[1])
                            self.parentWindow.dxMarkerForTable = self.lastClicks[1]
                            x = 0

                    tmpMarkerState = {"index": len(self.markerList),
                                      "name": name,
                                      "color": col,
                                      "x": x,
                                      "width": width}

                    self.addMarker(tmpMarkerState)
                    self.lastClicks.remove(self.lastClicks[0])

            elif not self.lastClicks and event.button() == Qt.RightButton:
                mousePoint = self.getPlotItem().vb.mapSceneToView(pos)
                self.lastClicks.append(mousePoint.x())

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.position()
        if self.sceneBoundingRect().contains(pos):
            mousePoint = self.getPlotItem().vb.mapSceneToView(pos)
            if not self.draggingMarker:
                self.vLine.setPos(mousePoint.x())
                self.update()

            if len(self.lastClicks) == 1:
                self.markingRegion.setRegion([self.lastClicks[0], mousePoint.x()])

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Alt:
            self.switchMarking()
        elif event.key() == Qt.Key.Key_R:
            self.resetZoom()

    def switchMarking(self):
        self.lastClicks = []
        self.markingRegion.hide()
        self.markingEnabled = not self.markingEnabled
        color = self.colorWhileMarkingHex if self.markingEnabled else self.colorBackgroundHex
        self.setBackground(color)

    def changeVLineX(self, x):
        self.vLine.setPos(x)
        self.update()

    def rangeChanged(self):
        xAxisView = self.getViewBox().viewRange()[0]
        yAxisView = self.getViewBox().viewRange()[1]
        yAxisViewRange = yAxisView[1] - yAxisView[0]

        height = yAxisViewRange * self.markerHeightPerc
        y = yAxisView[0]


        for marker in self.markerList:
            marker.canvasViewChanged(y, height, xAxisView, yAxisView)
        print("rangeChanged")

    def changeAxisLabel(self, axis, font):
        if axis == "bottom":
            self.getAxis("bottom").setLabelFont(font)
        elif axis == "left":
            self.getAxis("left").setLabelFont(font)

    def addMarker(self, markerState):
        yAxisView = self.getViewBox().viewRange()[1]
        yAxisViewRange = yAxisView[1] - yAxisView[0]

        height = yAxisViewRange * self.markerHeightPerc
        y = yAxisView[0]

        tmpMarker = MarkerRectItem(markerState["index"], markerState["name"], markerState["color"], self,
                                   markerState["x"], y, markerState["width"], height
                                   )

        self.markerList.append(tmpMarker)

        self.updateMarkerIndices()

        self.checkAndHandleCollision(tmpMarker)

        print(tmpMarker, type(tmpMarker))
        self.addItem(tmpMarker)
        self.updateTable(tmpMarker.getIndex(), tmpMarker.getName(), tmpMarker.getColor(), tmpMarker.getX0(),
                         tmpMarker.getX1())

    def getMarkerAtPos(self, pos):
        if pos.y() > 0:
            return None
        for marker in self.markerList:
            if marker.getX0() <= pos.x() <= marker.getX1():
                print(f"markerX0 {marker.getX0()} pos {pos.x()} markerX1 {marker.getX1()}")
                return marker

        return None

    def focusFigure(self, figure):
        self.figureInFocus = figure

    def removeFocus(self):
        self.figureInFocus = None

    def changeMarker(self, index, **kwargs):
        marker = self.markerList[index]
        marker.changeVariables(**kwargs)

    def updateMarkerIndices(self):
        if self.markerList:
            markerList = self.markerList
            markerList.sort(key=lambda m: m.getX0())
            for i in range(len(markerList)):
                markerList[i].setIndex(i)
                self.updateTable(markerList[i].getIndex(),  markerList[i].getName(),  markerList[i].getColor(),
                                 markerList[i].getX0(),  markerList[i].getX1())
                if i > 0:
                    markerList[i].setPreviousMarker(markerList[i - 1])
                if i < len(self.markerList) - 1:
                    markerList[i].setNextMarker(markerList[i + 1])

            self.parentWindow.addTableMarkerEntry(markerList[-1].getIndex() + 1, "", "", -1, -1)

    def deleteMarker(self, marker: MarkerRectItem):
        self.removeItem(marker)
        self.markerList.remove(marker)
        self.parentWindow.addTableMarkerEntry(marker.getIndex(), "", "", 0, 0)
        self.updateMarkerIndices()
        self.draggingMarker = False
        if self.markingEnabled:
            self.switchMarking()
        self.markingRegion.hide()
        self.setFocus()

    def deleteFigure(self, figure):
        self.figureList.remove(figure)
        self.removeItem(figure)
        figure.deleteLater()

    def checkAndHandleCollision(self, marker: MarkerRectItem):
        markerNeighbors = [marker.getPreviousMarker(), marker.getNextMarker()]
        for m in markerNeighbors:
            if m is None:
                continue

            if m.getX0() < marker.getX0() < marker.getX1() < m.getX1():
                markerState = {"index": -1,
                               "name": m.getName(),
                               "color": m.getColor(),
                               "x": marker.getX1(),
                               "width": m.getX1() - marker.getX1()}
                m.setX1(marker.getX0())
                self.addMarker(markerState)
                break

            if m.getX0() <= marker.getX1() < m.getX1():
                marker.linkMarker("right")
                print("right overlap")
                continue
            if m.getX1() >= marker.getX0() >= m.getX0():
                marker.linkMarker("left")
                print("left overlap")
                continue

            if m.getX0() > marker.getX0() and m.getX1() < marker.getX1():
                msgBox = QMessageBox()
                msgBox.setText(QObject().tr("Markers overlap, do you want to delete {0}".format(m.getName())))
                msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
                if msgBox.exec() == QMessageBox.Yes:
                    print("Deleting...")
                    m.deleteSelf()

    def updateTable(self, index: int, name: str, color: str, x: float, dx: float):
        if "borke" in name or "rinde" in name.lower() and index == 0:
            self.parentWindow.changeXAxisZero(dx)
            #self.getAxis('bottom').updateTicks()
            self.parentWindow.dxMarkerForTable = dx
            self.updateXGrid()
            x = 0

        self.parentWindow.updateTableMarkerEntry(index, name, color, x, dx)

    def getCanvasState(self):
        markerStateList = []
        for marker in self.markerList:
            markerStateList.append(marker.getState())

        return markerStateList
