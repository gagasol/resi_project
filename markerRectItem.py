import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QBrush, QAction
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QMenu


class MarkerRectItem(QGraphicsRectItem):
    def __init__(self, index: int, name: str, color: str, canvas: pg.PlotWidget, *args, **kwargs):
        super(MarkerRectItem, self).__init__(*args, **kwargs)

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setOpacity(1)
        self.setZValue(10)

        self._index = index
        self._x0 = args[0]
        self._y = args[1]
        self._width = args[2]
        self._height = args[3]
        self._x1 = self._x0 + self._width
        self._name = name
        self._color = color
        self._canvas = canvas
        self._xAxisViewRange = self._canvas.getViewBox().viewRange()[0][1] - self._canvas.getViewBox().viewRange()[0][0]
        self._yAxisViewRange = self._canvas.getViewBox().viewRange()[1][1] - self._canvas.getViewBox().viewRange()[1][0]

        self._nextMarker = None
        self._previousMarker = None

        self._linkedLeft = False
        self._linkedRight = False

        self.markerDragArea = None
        self.lastMousePosX = None

        self.toDeleteLater = False

        self.addColor(self._color)

    def getIndex(self) -> int:
        return self._index

    def setIndex(self, index: int):
        self._index = index

    def getX0(self) -> float:
        return self._x0

    def setX0(self, x: float):
        self._x0 = x
        self._x1 = self._x0 + self._width
        self.updateRect()

    def getWidth(self) -> float:
        return self._width

    def setWidth(self, width: float):
        self._width = width
        self._x1 = self._x0 + self._width
        self.updateRect()

    def getX1(self) -> float:
        return self._x1

    def setX1(self, x1: float):
        self._x1 = x1
        self._width = x1 - self._x0
        self.updateRect()

    def getName(self) -> str:
        return self._name

    def setName(self, name: str):
        self._name = name

    def getColor(self) -> str:
        return self._color

    def setColor(self, color: str):
        self._color = color
        self.addColor(color)

    def getNextMarker(self) -> "MarkerRectItem":
        return self._nextMarker

    def setNextMarker(self, marker: "MarkerRectItem"):
        self._nextMarker = marker

    def getPreviousMarker(self) -> "MarkerRectItem":
        return self._previousMarker

    def setPreviousMarker(self, marker: "MarkerRectItem"):
        self._previousMarker = marker

    def getLinkedLeft(self) -> bool:
        return self._linkedLeft

    def setLinkedLeft(self, linkedLeft: bool):
        self._linkedLeft = linkedLeft

    def getLinkedRight(self) -> bool:
        return self._linkedRight

    def setLinkedRight(self, linkedRight: bool):
        self._linkedRight = linkedRight

    def contextMenuEvent(self, pos):
        menu = QMenu()
        action1 = QAction("Delete Marker")
        menu.addAction(action1)

        print(pos)
        action = menu.exec_(pos)

        if action == action1:
            print("Deleting Marker")
            self.deleteSelf()


    def hoverEnterEvent(self, event):
        self.addColor("#000000")
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.addColor(self._color)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if self.isUnderMouse():
            self._canvas.draggingMarker = True
            self._canvas.canvasPaintingChanged()
            self.lastMousePosX = event.pos().x()
            if event.pos().x() < self._x0 + self._width * 0.1:
                self.markerDragArea = "left"
                print("Clicked on the left!")
            elif event.pos().x() > self._x1 - self._width * 0.1:
                self.markerDragArea = "right"
                print("Clicked on the right!")
            else:
                self.markerDragArea = None

    def mouseReleaseEvent(self, event):
        self._canvas.draggingMarker = False
        self.lastMousePosX = None

    def mouseMoveEvent(self, event):
        if self.lastMousePosX is not None:
            dx = event.pos().x() - self.lastMousePosX
            if self.markerDragArea is None:
                self.changeMarkerCoords(dx, "middle")

            elif self._x1 - self._x0 > self._xAxisViewRange * 0.02:
                self.changeMarkerCoords(dx, self.markerDragArea)

    def updateRect(self):
        self.setRect(self._x0, self._y, self._width, self._height)

    def changeMarkerCoords(self, dx: float, direction: str, calledByUser=True):
        if direction == "middle":
            self._x0 = self._x0 + dx
            self._x1 = self._x0 + self._width
            self.updateRect()
            self._canvas.updateTable(self._index, self._name, self._color, self._x0, self._x1)

            if dx > 0:
                self._canvas.changeVLineX(self._x1)
            elif dx < 0:
                self._canvas.changeVLineX(self._x0)

            self.lastMousePosX += dx

            if self._linkedLeft:
                self._previousMarker.changeMarkerCoords(dx, "right", False)
            elif self._previousMarker is not None:
                if self._x0 <= self._previousMarker.getX1():
                    self.linkMarker("left")

            if self._linkedRight:
                self._nextMarker.changeMarkerCoords(dx, "left", False)
            elif self._nextMarker is not None:
                if self._x1 >= self._nextMarker.getX0():
                    self.linkMarker("right")

        elif direction == "left":
            self._x0 = self._x0 + dx
            self._width = self._width - dx
            self._x1 = self._x0 + self._width
            self.updateRect()
            self._canvas.updateTable(self._index, self._name, self._color, self._x0, self._x1)

            if calledByUser:
                self._canvas.changeVLineX(self._x0)
                self.lastMousePosX += dx
                if self._linkedLeft:
                    self._previousMarker.changeMarkerCoords(dx, "right", False)
                elif self._previousMarker is not None:
                    if self._x0 <= self._previousMarker.getX1():
                        self.linkMarker("left")

        elif direction == "right":
            self._width = self._width + dx
            self._x1 = self._x0 + self._width
            self.updateRect()
            self._canvas.updateTable(self._index, self._name, self._color, self._x0, self._x1)

            if calledByUser:
                self._canvas.changeVLineX(self._x1)
                self.lastMousePosX += dx
                if self._linkedRight:
                    self._nextMarker.changeMarkerCoords(dx, "left", False)
                elif self._nextMarker is not None:
                    if self._x1 >= self._nextMarker.getX0():
                        self.linkMarker("right")

    def linkMarker(self, direction: str):
        if direction == "left":
            self._linkedLeft = True
            self._previousMarker.setLinkedRight(True)
            self._previousMarker.setX1(self._x0)
            print("link left:")
            print("x value caller: {0}, x1 value called: {1}".format(self._x0, self._previousMarker.getX1()))

        elif direction == "right":
            self._linkedRight = True
            self._nextMarker.setLinkedLeft(True)
            self._nextMarker.setX0(self._x1)
            print("linked right:")
            print("x1 value caller: {0}, x value called: {1}".format(self._x1, self._nextMarker.getX0()))

    def adjustLinkedMarker(self):
        pass

    def addColor(self, color):
        self.setBrush(QBrush(QColor(color)))
        self.setPen(QPen(Qt.PenStyle.NoPen))

    def canvasViewChanged(self, y, height, xAxisView, yAxisView):
        self._y = y
        self._height = height
        self._xAxisViewRange = xAxisView[1] - xAxisView[0]
        self.setRect(self._x0, self._y, self._width, self._height)

    def deleteSelf(self):
        if self._previousMarker is not None:
            self._previousMarker.setNextMarker(self._nextMarker)
            self._previousMarker.setLinkedRight(False)
        if self._nextMarker is not None:
            self._nextMarker.setPreviousMarker(self._previousMarker)
            self._nextMarker.setLinkedLeft(False)

        self._previousMarker = None
        self._nextMarker = None
        self._canvas.deleteMarker(self)

    def getState(self):
        returnDict = {"index": self._index, "name": self._name, "color": self._color, "x": self._x0,
                      "width": self._width}
        print(returnDict)
        return returnDict

    def changeVariables(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setterMethod = getattr(self, "set" + key[1:].capitalize())
                if callable(setterMethod):
                    setterMethod(value)
                else:
                    print(f"Setter method for {key} does not exist, setting manually!")
                    setattr(self, key, value)
            else:
                print(f"{key} does not exist in MarkerRectItem class.")
