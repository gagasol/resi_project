# This Python file uses the following encoding: utf-8
import logging
import sys

from PySide6 import QtCore
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QDialog

from ui_files.ui_pickMarkerWindow import Ui_PickMarker
from markerpresetwindow import MarkerPresetWindow


class CustomLabel(QLabel):
    def __init__(self, color, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.color = color
        self.setStyleSheet(("background-color : {0}; color : black;").format(self.color))

    def enterEvent(self, event):
        hex_color1 = "#000000"
        hex_color2 = self.color
        self.setStyleSheet(
            f"QWidget {{" +
            f"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {hex_color2}, stop:1 {hex_color1}); color : white;" +
            f"}}")
    def leaveEvent(self, event):
        self.setStyleSheet(("background-color : {0}; color : black;").format(self.color))

    def hexToRgb(self, hexColor):
        hexColor = hexColor.lstrip("#")  # Remove '#' if it exists
        return tuple(int(hexColor[i:i + 2], 16) for i in (0, 2, 4))

class PickMarker(QDialog):
    signalCanceled = Signal()
    signalAccepted = Signal()
    def __init__(self, mainWindow, markerDict, parent=None):
        super().__init__(parent)
        self.ui = Ui_PickMarker()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)

        self.mainWindow = mainWindow if mainWindow else None
        self.markerDict = markerDict

        self.markerName = ""
        self.markerColor = ""

        self.flagCanceled = False

        self.ui.pushButtonOpenPresets.clicked.connect(self.pushButtonOpenPresetsClicked)
        self.ui.pushButtonClose.clicked.connect(self.cancel)

        self.loadMarkerDict(markerDict)


    def closeEvent(self, event):
        if self.flagCanceled:
            print("CANCEL")
            self.signalCanceled.emit()
        else:
            print("ACCEPT")
            self.signalAccepted.emit()


    def pushButtonOpenPresetsClicked(self):
        markers = self.mainWindow.openChangeMarkerPreset(self.markerDict["_NameForPreset"])
        if (markers):
            logging.debug(markers)
            self.markerDict = markers
            self.loadMarkerDict(self.markerDict)


    def cancel(self):
        print(self.flagCanceled)
        self.flagCanceled = True
        self.reject()

    def mousePressEvent(self, event):

        widget = self.childAt(event.pos())

        if (type(widget) == CustomLabel):
            text = widget.text()
            col = widget.color
            self.markerColor = col
            self.markerName = text
            self.accept()


    def loadMarkerDict(self, markerDict):
        print("ok")
        layoutScrollArea = self.ui.scrollAreaWidgetContents.layout()
        for i in reversed(range(layoutScrollArea.count())):
            widget = layoutScrollArea.itemAt(i).widget()
            if (widget is not None and type(widget) == CustomLabel):
                layoutScrollArea.removeWidget(widget)
                widget.deleteLater()

        for name, color in markerDict.items():
            if (name == "_NameForPreset"):
                continue
            index = layoutScrollArea.count() - 1
            newLabel = CustomLabel(color)
            #newLabel.setStyleSheet("background-color:"+color)
            newLabel.setMinimumHeight(25)
            newLabel.setMaximumHeight(25)
            newLabel.setFixedWidth(100)
            newLabel.setText(name)
            newLabel.setWindowOpacity(1)
            #self.resize(100, self.height()+30)
            layoutScrollArea.insertWidget(index, newLabel)



