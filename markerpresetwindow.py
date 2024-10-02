# This Python file uses the following encoding: utf-8
import sys

import random
import string

from PySide6.QtCore import QEventLoop, Qt, Signal, QObject
from PySide6.QtGui import QPixmap, QColor, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QDialog, \
    QCheckBox, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton

from ui_files.ui_form import Ui_SelectMarkerWindow
from editMarkerPreset import EditMarkerPresetWindow, TextEntryDialog


class MarkerPresetWindow(QDialog):
    closedByUser = Signal()
    closedProgrammatically = Signal()

    def __init__(self, MainWindow, nameToColorDict=None, markerPresetList=None, parent=None, calledByGraph=True):
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

        self.calledByGraph = calledByGraph

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
        self.accept()

    def cancelMarker(self):
        self.flagCanceled = True
        self.reject()


    def checkSelection(self):
        checkedButton = self.buttonGroup.checkedButton()
        if checkedButton is not None:
            if not self.calledByGraph:
                self.mainWindow.defaultMarkerDictName = checkedButton.objectName()
                self.mainWindow.settingsWindow.setSettingsVariable("defaultMarkerDictName", checkedButton.objectName())

            for preset in self.listPresets:
                if self.calledByGraph and preset["_NameForPreset"] == checkedButton.objectName():
                    self.mainWindow.overridePickMarkerDict(preset)
                    break


    def onComboBoxItemChanged(self, index):

        textCurrentItem = self.sender().currentText()
        if index == 0 or textCurrentItem == "_NameForPreset":
            return
        if index == self.sender().count()-1:
            selectMarkerWindow = EditMarkerPresetWindow(self, self.listPresets[self.sender().id_number],
                                                        self.sender().id_number)
            selectMarkerWindow.exec()
            self.buttonGroup.buttons()[self.sender().id_number].setChecked(True)
            self.sender().setCurrentIndex(0)
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
            dictMarker = {"_NameForPreset": text}
            selectMarkerWindow = EditMarkerPresetWindow(self, argDictMarker=dictMarker)
            selectMarkerWindow.exec()

    def deletePreset(self):
        presetName = self.sender().objectName()
        print(presetName)
        for preset in self.listPresets:
            if preset["_NameForPreset"] == presetName:
                self.listPresets.remove(preset)
                self.loadPresets()
                break

    def loadPresets(self):

        if self.listComboBoxPresets:
            self.comboBoxCount = 0

            for button in self.buttonGroup.buttons():
                self.buttonGroup.removeButton(button)

            for i in range(len(self.listComboBoxPresets[1])):
                self.ui.scrollAreaWidgetContents.layout().removeWidget(self.listComboBoxPresets[1][i].parent())
                self.listComboBoxPresets[1][i].parent().deleteLater()

            self.listComboBoxPresets = []

        tmpComboBoxMarker = []
        tmpComboBoxes = []

        for preset in self.listPresets:
            widget = QWidget()
            verticalLayout = QHBoxLayout()
            checkBox = QRadioButton(QObject.tr('File Default'))
            checkBox.setObjectName(preset["_NameForPreset"])
            deleteButton = QPushButton(QObject.tr('Delete'))
            deleteButton.setObjectName(preset["_NameForPreset"])
            deleteButton.clicked.connect(self.deletePreset)
            if self.calledByGraph and preset["_NameForPreset"] == self.mainWindow.getGraphDefaultMarkerDictName():
                checkBox.setChecked(True)
            elif not self.calledByGraph and preset["_NameForPreset"] == self.mainWindow.defaultMarkerDictName:
                checkBox.setChecked(True)

            if len(self.listPresets) == 1:
                checkBox.setChecked(True)
                self.mainWindow.defaultMarkerDictName = preset["_NameForPreset"]

            tmpComboBox = QComboBox(self)
            tmpComboBox.id_number = self.comboBoxCount
            self.comboBoxCount += 1
            tmpComboBox.addItem(preset["_NameForPreset"])

            for i, marker in enumerate(preset):
                if (marker == "_NameForPreset"):
                    continue
                pixmap = QPixmap(30, 30)
                pixmap.fill(QColor(preset.get(marker)))
                icon = QIcon(pixmap)
                tmpComboBox.addItem(marker)
                tmpComboBox.setItemIcon(i, icon)

            self.buttonGroup.addButton(checkBox)
            verticalLayout.addWidget(tmpComboBox)
            verticalLayout.addWidget(deleteButton)
            verticalLayout.addWidget(checkBox)


            widget.setLayout(verticalLayout)
            self.ui.scrollAreaWidgetContents.layout().insertWidget(len(tmpComboBoxMarker), widget)
            tmpComboBox.addItem(QObject.tr("Change Preset"))
            tmpComboBox.currentIndexChanged.connect(self.onComboBoxItemChanged)
            tmpComboBox.activated.connect(self.onComboBoxActivated)
            tmpComboBoxMarker.append(tmpComboBox)
            tmpComboBoxes.append(tmpComboBox)

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
