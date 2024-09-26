from typing import List, Dict

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGraphicsRectItem, QGraphicsItem, QMenu, \
    QMessageBox
from PyQt6.QtGui import QColor, QPen, QBrush, QGuiApplication, QMouseEvent, QAction
from PyQt6.QtCore import Qt, QRectF, QPointF, QObject
import pyqtgraph as pg
import numpy as np

from markerRectItem import MarkerRectItem

class CustomPlotWidget(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super(CustomPlotWidget, self).__init__(*args, **kwargs)

        self.setBackground(QColor("#DEE2E2"))
        self.showGrid(x=True, y=True)
        self.setLimits(xMin=-0.5, xMax=42, yMin=-2.2, yMax=102)
        self.setRange(xRange=(-1, 42), yRange=(-3,105))

        self.getAxis("bottom").setLabel(QObject.tr("Tiefe"), units="cm")
        self.getAxis("left").setLabel(QObject.tr("Widerstand"), units="%")

        self.getViewBox().sigRangeChanged.connect(self.rangeChanged)

        pen_line = pg.mkPen('black')
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pen_line)
        self.addItem(self.vLine)

        self.markingRegion = pg.LinearRegionItem([0, 0])

        # TEST



        #variables
        self.lastClicks: List[float] = []
        self.markerList: List[MarkerRectItem] = []

        self.markerHeightPerc = 0.02

        self.markingEnabled = False
        self.draggingMarker = False



    def mousePressEvent(self, event):
        pos = event.position()
        if self.sceneBoundingRect().contains(pos):
            if self.markingEnabled:
                mousePoint = self.getPlotItem().vb.mapSceneToView(pos)
                self.lastClicks.append(mousePoint.x())
                self.markingRegion.setRegion([mousePoint.x(), mousePoint.x()])
                self.addItem(self.markingRegion)

                if len(self.lastClicks) == 2:
                    x = min(self.lastClicks)
                    width = abs(self.lastClicks[0] - self.lastClicks[1])

                    tmpMarkerState = {"index": len(self.markerList),
                                      "name": "Test",
                                      "color": "#F92CE1",
                                      "x": x,
                                      "width": width}

                    self.addMarker(tmpMarkerState)
                    self.lastClicks.remove(self.lastClicks[0])

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
            self.lastClicks = []
            self.removeItem(self.markingRegion)
            self.markingEnabled = not self.markingEnabled


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

        self.addItem(tmpMarker)

    def updateMarkerIndices(self):
        markerList = self.markerList
        markerList.sort(key=lambda m: m.getXPos())
        for i in range(len(markerList)):
            markerList[i].setIndex(i)
            if i > 0:
                markerList[i].setPreviousMarker(markerList[i - 1])
            if i < len(self.markerList) - 1:
                markerList[i].setNextMarker(markerList[i + 1])

    def deleteMarker(self, marker: MarkerRectItem):
        self.removeItem(marker)
        self.markerList.remove(marker)
        self.updateMarkerIndices()

    def checkAndHandleCollision(self, marker: MarkerRectItem):
        markerNeighbors = [marker.getPreviousMarker(), marker.getNextMarker()]
        for m in markerNeighbors:
            if m is None:
                continue

            if m.getXPos() < marker.getXPos() < marker.getX1() < m.getX1():
                markerState = {"index": -1,
                               "name": m.getName(),
                               "color": m.getColor(),
                               "x": marker.getX1(),
                               "width": m.getX1() - marker.getX1()}
                m.setX1(marker.getXPos())
                self.addMarker(markerState)
                break

            if m.getXPos() <= marker.getX1() < m.getX1():
                marker.linkMarker("right")
                print("right overlap")
                continue
            if m.getX1() >= marker.getXPos() >= m.getXPos():
                marker.linkMarker("left")
                print("left overlap")
                continue

            if m.getXPos() > marker.getXPos() and m.getX1() < marker.getX1():
                msgBox = QMessageBox()
                msgBox.setText(QObject.tr("Markers overlap, do you want to delete {0}".format(m.getName())))
                msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
                if msgBox.exec() == QMessageBox.StandardButton.Yes:
                    print("Deleting...")
                    m.deleteSelf()