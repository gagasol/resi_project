# This Python file uses the following encoding: utf-8
import sys

import random
import string

from PySide6.QtCore import QEventLoop, Qt, Signal, QObject
from PySide6.QtGui import QPixmap, QColor, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_files.ui_form import Ui_SelectMarkerWindow
from editMarkerPreset import EditMarkerPresetWindow


class MarkerPresetWindow(QDialog):
    closedByUser = Signal()
    closedProgrammatically = Signal()

    def __init__(self, MainWindow, nameToColorDict=None, markerPresetList=None, parent=None):
        super().__init__(parent)
        if markerPresetList is None:
            markerPresets = []
        if nameToColorDict is None:
            markerDict = {}
        self.ui = Ui_SelectMarkerWindow()
        self.ui.setupUi(self)

        self.mainWindow = MainWindow
        self.dictAllMarkers = nameToColorDict
        self.listPresets = markerPresetList

        self.flagDelete = False
        self.flagCanceled = False

        self.comboBoxCount = 0
        self.comboBoxInd = 0

        self.markerColor = None
        self.markerName = None

        # bunch of stuff for trying stuff out


        if not self.listPresets:
            for dic in self.listPresets:
                self.listPresets.append(dic)
        if not self.dictAllMarkers:
            self.listPresetToFlatList()

        self.listComboBoxPresets = []

        self.loadPresets()
        self.ui.pushButtonAddPreset.clicked.connect(self.addPreset)
        self.ui.pushButtonChangePreset.clicked.connect(self.okButtonClicked)
        self.ui.pushButtonCancel.clicked.connect(self.cancelMarker)

    def closeEvent(self, event):
        if self.flagCanceled or self.sender() is None:
            print("NONE  BRO")
            self.closedByUser.emit()
        else:
            print("YOU DID IT BRO")
            self.closedProgrammatically.emit()


    def okButtonClicked(self):

        self.accept()

    def cancelMarker(self):
        self.flagCanceled = True
        self.reject()


    def onComboBoxItemChanged(self, index):

        textCurrentItem = self.sender().currentText()
        if (index == 0 or textCurrentItem == "_NameForPreset"):
            return
        if (textCurrentItem == "Add Marker"):
            selectMarkerWindow = EditMarkerPresetWindow(self, self.listPresets[self.sender().id_number],
                                                        self.sender().id_number)
            self.setWindowModality(Qt.NonModal)
            selectMarkerWindow.setWindowModality(Qt.ApplicationModal)
            selectMarkerWindow.setAttribute(Qt.WA_DeleteOnClose)
            selectMarkerWindow.show()

            waitForMarkerInputLoop = QEventLoop()
            selectMarkerWindow.destroyed.connect(waitForMarkerInputLoop.quit)
            waitForMarkerInputLoop.exec()

        for preset in self.listPresets:
            if (textCurrentItem in preset):
                self.mainWindow.markerColor = preset[textCurrentItem]
                self.mainWindow.markerName = textCurrentItem
                self.flagCanceled = False
                self.close()

    def onComboBoxActivated(self, index):
        print(self.sender().id_number)

    def addPreset(self):
        selectMarkerWindow = EditMarkerPresetWindow(self)
        self.setWindowModality(Qt.NonModal)
        selectMarkerWindow.setWindowModality(Qt.ApplicationModal)
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
            tmpComboBox.addItem(preset["_NameForPreset"])
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
    widget = EditMarkerPresetWindow()
    widget.show()
    sys.exit(app.exec())
'''
