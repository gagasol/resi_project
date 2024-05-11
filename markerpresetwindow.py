# This Python file uses the following encoding: utf-8
import sys

import random
import string

from PySide6.QtCore import QEventLoop, Qt, Signal, QObject
from PySide6.QtGui import QPixmap, QColor, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_files.ui_form import Ui_SelectMarkerWindow
from editMarkerPreset import SelectMarkerWindow


class MarkerPresetWindow(QWidget):
    closedByUser = Signal()
    closedProgrammatically = Signal()

    def __init__(self, MainWindow, markerDict=None, markerPresets=None, parent=None):
        super().__init__(parent)
        if markerPresets is None:
            markerPresets = []
        if markerDict is None:
            markerDict = {}
        self.ui = Ui_SelectMarkerWindow()
        self.ui.setupUi(self)

        self.mainWindow = MainWindow
        self.dictAllMarkers = markerDict
        self.listPresets = markerPresets

        self.flagDelete = False

        self.comboBoxCount = 0
        self.comboBoxInd = 0

        self.markerColor = None
        self.markerName = None

        # bunch of stuff for trying stuff out
        self.listPreset = [
            {
                "_NameForPreset": "Preset_1",
                "Red": "#FF0000",
                "Green": "#008000",
                "Blue": "#0000FF",
                "Yellow": "#FFFF00",
                "Black": "#000000",
                "White": "#FFFFFF"
            },
            {
                "_NameForPreset": "Preset_2",
                "Aloof": "#7B68EE",
                "Cherish": "#FFB6C1",
                "Divine": "#FFA07A",
                "Elapse": "#8B0000",
                "Green": "#00FF00"
            },
            {
                "_NameForPreset": "Preset_3",
                "Coral": "#FF7F50",
                "Cyan": "#00FFFF",
                "Chocolate": "#D2691E",
                "Crimson": "#DC143C"}
        ]

        if not self.listPresets:
            for dic in self.listPreset:
                self.listPresets.append(dic)
        if not self.dictAllMarkers:
            self.listPresetToFlatList()

        self.listComboBoxPresets = []

        self.loadPresets()
        self.ui.pushButtonAddPreset.clicked.connect(self.addPreset)

    def closeEvent(self, event):
        if self.sender() is None:
            self.closedByUser.emit()
        else:
            self.closedProgrammatically.emit()
            return

    def onComboBoxItemChanged(self, index):

        textCurrentItem = self.sender().currentText()
        if (index == 0 or textCurrentItem == "_NameForPreset"):
            return
        if (textCurrentItem == "Add Marker"):
            selectMarkerWindow = SelectMarkerWindow(self, self.listPresets[self.sender().id_number],
                                                    self.sender().id_number)
            selectMarkerWindow.setAttribute(Qt.WA_DeleteOnClose)
            selectMarkerWindow.show()

            waitForMarkerInputLoop = QEventLoop()
            selectMarkerWindow.destroyed.connect(waitForMarkerInputLoop.quit)
            waitForMarkerInputLoop.exec()

        for preset in self.listPresets:
            if (textCurrentItem in preset):
                self.mainWindow.markerColor = preset[textCurrentItem]
                self.mainWindow.markerName = textCurrentItem
                self.close()

    def onComboBoxActivated(self, index):
        print(self.sender().id_number)

    def addPreset(self):
        selectMarkerWindow = SelectMarkerWindow(self)
        selectMarkerWindow.setAttribute(Qt.WA_DeleteOnClose)
        selectMarkerWindow.show()

        waitForMarkerInputLoop = QEventLoop()
        selectMarkerWindow.destroyed.connect(waitForMarkerInputLoop.quit)
        waitForMarkerInputLoop.exec()

    def loadPresets(self):

        if (self.listComboBoxPresets):
            self.comboBoxCount = 0
            for comboBox in self.listComboBoxPresets:
                self.ui.scrollAreaWidgetContents.layout().removeWidget(comboBox)

        tmpComboBoxMarker = []

        for preset in self.listPresets:
            tmpComboBox = QComboBox(self)
            tmpComboBox.id_number = self.comboBoxCount
            self.comboBoxCount += 1
            tmpComboBox.addItem("Pick a Marker")
            i = 1
            for marker in preset:
                if (marker == "_NameForPreset"):
                    continue
                pixmap = QPixmap(30, 30)
                pixmap.fill(QColor(preset.get(marker)))
                icon = QIcon(pixmap)
                tmpComboBox.addItem(marker)
                tmpComboBox.setItemIcon(i, icon)
                i += 1

            self.ui.scrollAreaWidgetContents.layout().insertWidget(len(tmpComboBoxMarker), tmpComboBox)
            tmpComboBox.addItem("Add Marker")
            tmpComboBox.currentIndexChanged.connect(self.onComboBoxItemChanged)
            tmpComboBox.activated.connect(self.onComboBoxActivated)
            tmpComboBoxMarker.append(tmpComboBox)

        self.listComboBoxPresets = tmpComboBoxMarker

    def listPresetToFlatList(self):
        for preset in self.listPresets:
            self.dictAllMarkers.update(preset)

        self.dictAllMarkers.pop("_NameForPreset")

    def makeComboBox(self):
        tmpComboBox = QComboBox(self)
        tmpComboBox.addItems(["A", "B", "C", "D", "E", "F"])

        return tmpComboBox


# useless functions


'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SelectMarkerWindow()
    widget.show()
    sys.exit(app.exec())
'''
