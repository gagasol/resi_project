# This Python file uses the following encoding: utf-8
import sys

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QDialog

from ui_files.ui_pickMarkerWindow import Ui_PickMarker
from markerpresetwindow import MarkerPresetWindow

class PickMarker(QDialog):
    signalCanceled = Signal()
    signalAccepted = Signal()
    def __init__(self, parentWindow, markerDict, parent=None):
        super().__init__(parent)
        self.ui = Ui_PickMarker()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.parentWindow = parentWindow

        self.flagCanceled = False

        self.ui.pushButtonOpenPresets.clicked.connect(self.pushButtonOpenPresetsClicked)
        self.ui.pushButtonClose.clicked.connect(self.cancel)

        self.addMarkerDict(markerDict)


    def closeEvent(self, event):
        if self.flagCanceled:
            print("CANCEL")
            self.signalCanceled.emit()
        else:
            print("ACCEPT")
            self.signalAccepted.emit()


    def pushButtonOpenPresetsClicked(self):
        markerPresetWin = MarkerPresetWindow()


    def cancel(self):
        print(self.flagCanceled)
        self.flagCanceled = True
        self.close()

    def mousePressEvent(self, event):

        widget = self.childAt(event.pos())

        if (type(widget) == QLabel):
            text = widget.text()
            col = widget.palette().color(widget.backgroundRole()).name()
            self.parentWindow.markerColor = col
            self.parentWindow.markerName = text
            self.close()


    def addMarkerDict(self, markerDict):
        for name, color in markerDict.items():
            if (name == "_NameForPreset"):
                continue
            index = self.ui.scrollAreaWidgetContents.layout().count() - 1
            newLabel = QLabel()
            newLabel.setStyleSheet("background-color:"+color)
            newLabel.setMinimumHeight(30)
            newLabel.setMaximumHeight(30)
            newLabel.setFixedWidth(90)
            newLabel.setText(name)
            #self.resize(100, self.height()+30)
            self.ui.scrollAreaWidgetContents.layout().insertWidget(index, newLabel)


