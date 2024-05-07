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
    def __init__(self, MainWindow, flagChange=False, listPresets=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_SelectMarkerWindow()
        self.ui.setupUi(self)

        self.mainWindow = MainWindow
        self.dictAllMarkers = {}


        self. flagChange = flagChange
        self.listPresets = listPresets if listPresets else []

        # bunch of stuff for trying stuff out
        self.listPresets = [
            {
                "Red": "#FF0000",
                "Green": "#008000",
                "Blue": "#0000FF",
                "Yellow": "#FFFF00",
                "Black": "#000000",
                "White": "#FFFFFF"
            },
            {
                "Aloof": "#7B68EE",
                "Cherish": "#FFB6C1",
                "Divine": "#FFA07A",
                "Elapse": "#8B0000",
                "Green": "#00FF00"
            },
            {"Coral": "#FF7F50",
             "Cyan": "#00FFFF",
             "Chocolate": "#D2691E",
             "Crimson": "#DC143C"}
        ]

        self.listComboBoxPresets = []

        self.loadPresets()
        self.ui.pushButtonAddPreset.clicked.connect(self.manipulatePresets)

    def closeEvent(self, event):
        if self.sender() is None:
            self.closedByUser.emit()
        else:
            self.closedProgrammatically.emit()


    def onComboBoxItemChanged(self, index):
        if (index == 0):
            return
        if (self.sender().currentText() == "Add Marker"):
            self.listPresetToFlatList()
            self.selectMarkerWindow = SelectMarkerWindow(self, self.listPresets[0])
            self.selectMarkerWindow.setAttribute(Qt.WA_DeleteOnClose)
            self.selectMarkerWindow.show()

            waitForMarkerInputLoop = QEventLoop()
            self.selectMarkerWindow.destroyed.connect(waitForMarkerInputLoop.quit)
            waitForMarkerInputLoop.exec()
            print("Create new life!!!")


        for preset in self.listPresets:
            if self.sender().currentText() in preset:
                self.mainWindow.colorRect = preset[self.sender().currentText()]
                self.mainWindow.nameRectMark = self.sender().currentText()
                self.close()


        print(self.sender().currentText())

    def manipulatePresets(self):

        if (self.flagChange):
            print("I will change")
        else:
            tmpComboBox = self.makeComboBox()
            self.loadPresets()


    def loadPresets(self):

        if (self.listComboBoxPresets):
            for comboBox in self.listComboBoxPresets:
                self.ui.scrollAreaWidgetContents.layout().removeWidget(comboBox)

        tmpComboBoxMarker = []

        for preset in self.listPresets:
            tmpComboBox = QComboBox(self)
            tmpComboBox.addItem("Pick a Marker")
            i = 1
            for marker in preset:
                pixmap = QPixmap(30, 30)
                pixmap.fill(QColor(preset.get(marker)))
                icon = QIcon(pixmap)
                tmpComboBox.addItem(marker)
                tmpComboBox.setItemIcon(i, icon)
                i += 1

            self.ui.scrollAreaWidgetContents.layout().insertWidget(len(tmpComboBoxMarker), tmpComboBox)
            tmpComboBox.addItem("Add Marker")
            tmpComboBox.currentIndexChanged.connect(self.onComboBoxItemChanged)
            tmpComboBoxMarker.append(tmpComboBox)


        self.listComboBoxPresets.append(tmpComboBoxMarker)


    def listPresetToFlatList(self):
        for preset in self.listPresets:
            self.dictAllMarkers.update(preset)



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
