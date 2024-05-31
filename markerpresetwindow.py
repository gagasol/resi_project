# This Python file uses the following encoding: utf-8
import sys

import random
import string

from PySide6.QtCore import QEventLoop, Qt, Signal, QObject
from PySide6.QtGui import QPixmap, QColor, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QDialog, \
    QCheckBox, QHBoxLayout, QRadioButton, QButtonGroup

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_files.ui_form import Ui_SelectMarkerWindow
from editMarkerPreset import EditMarkerPresetWindow, TextEntryDialog


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

        self.buttonGroup = QButtonGroup()

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
            self.closedByUser.emit()
        else:
            self.closedProgrammatically.emit()


    def okButtonClicked(self):
        self.checkSelection()
        print("[Debug Info] New defaultPresetName: " + self.mainWindow.defaultPresetName)
        self.accept()

    def cancelMarker(self):
        self.flagCanceled = True
        self.reject()


    def checkSelection(self):
        checkedButton = self.buttonGroup.checkedButton()
        if checkedButton is not None:
            self.mainWindow.defaultPresetName = checkedButton.objectName()


    def onComboBoxItemChanged(self, index):

        textCurrentItem = self.sender().currentText()
        if (index == 0 or textCurrentItem == "_NameForPreset"):
            return
        if (textCurrentItem == "Add Marker"):
            selectMarkerWindow = EditMarkerPresetWindow(self, self.listPresets[self.sender().id_number],
                                                        self.sender().id_number)
            selectMarkerWindow.exec()
            return

        print(self.sender().id_number, self.comboBoxCount)
        if ( self.sender().id_number == self.comboBoxCount ):
            pass

        preset = self.listPresets[self.sender().id_number]
        if (textCurrentItem in preset):
            col = preset[textCurrentItem]
            name = textCurrentItem
        else:
            col = ""
            name = ""
        self.mainWindow.overridePickMarkerDict(self.listPresets[self.sender().id_number], name, col)
        self.close()
        #return self.listPresets[self.sender().id_number]


    def onComboBoxActivated(self, index):
        print(self.sender().id_number)

    def addPreset(self):
        dialog = TextEntryDialog(self)

        if dialog.exec():
            text = dialog.text_entry.text()
            dictMarker = {"_NameForPreset", text}

            selectMarkerWindow = EditMarkerPresetWindow(self, argDictMarker=dictMarker)
            selectMarkerWindow.exec()


    def loadPresets(self):

        if (self.listComboBoxPresets):
            self.comboBoxCount = 0
            for i in range(len(self.listComboBoxPresets[1])):
                if (i == len(self.listComboBoxPresets[1]) - 1):
                    self.ui.scrollAreaWidgetContents.layout().removeWidget(self.listComboBoxPresets[1][i])
                    break

                self.ui.scrollAreaWidgetContents.layout().removeWidget(self.listComboBoxPresets[1][i].parent())

            self.listComboBoxPresets = []

        tmpComboBoxMarker = []
        tmpComboBoxes = []

        for preset in self.listPresets:
            widget = QWidget()
            verticalLayout = QHBoxLayout()
            checkBox = QRadioButton('Default')
            checkBox.setObjectName(preset["_NameForPreset"])
            if (preset["_NameForPreset"] == self.mainWindow.defaultPresetName):
                checkBox.setChecked(True)
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

            self.buttonGroup.addButton(checkBox)
            verticalLayout.addWidget(tmpComboBox)
            verticalLayout.addWidget(checkBox)
            widget.setLayout(verticalLayout)
            self.ui.scrollAreaWidgetContents.layout().insertWidget(len(tmpComboBoxMarker), widget)
            tmpComboBox.addItem("Add Marker")
            tmpComboBox.currentIndexChanged.connect(self.onComboBoxItemChanged)
            tmpComboBox.activated.connect(self.onComboBoxActivated)
            tmpComboBoxMarker.append(tmpComboBox)
            tmpComboBoxes.append(tmpComboBox)

        tmpComboBox = QComboBox()
        tmpComboBox.addItem(QObject.tr("All markers"))
        for index, (key, value) in enumerate(self.dictAllMarkers.items()):
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor(value))
            icon = QIcon(pixmap)
            tmpComboBox.addItem(key)
            tmpComboBox.setItemIcon(index+1, icon)

        tmpComboBoxes.append(tmpComboBox)

        self.ui.scrollAreaWidgetContents.layout().insertWidget(self.comboBoxCount, tmpComboBox)

        self.listComboBoxPresets = [tmpComboBoxMarker, tmpComboBoxes]

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
