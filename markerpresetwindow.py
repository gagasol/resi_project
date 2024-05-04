# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_files.ui_form import Ui_SelectMarkerWindow


class MarkerPresetWindow(QWidget):
    def __init__(self, MainWindow, flagChange=False, listPresets=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_SelectMarkerWindow()
        self.ui.setupUi(self)

        self.mainWindow = MainWindow

        self. flagChange = flagChange
        self.listPresets = listPresets if listPresets else []

        self.listPresets = [
            {"Aa": "A1", "Ab": "A2", "Ac" : "A3", "Ad": "A4"},
            {"Ba": "B1", "Bb": "B2", "Bc" : "B3", "Bd" : "B4"},
            {"Ca": "C1", "Cb": "C2", "Cc" : "C3", "Cd" : "C4"},
            {"Da": "D1", "Db": "D2", "Eb" : "E3", "Ed" : "E4"},
            {"Ea": "E1", "Eb" : "E2", "Ec" : "E3", "Ed" : "E4"}
        ]

        self.listComboBoxPresets = []

        self.ui.pushButtonAddPreset.clicked.connect(self.manipulatePresets)

    # @todo add an on focus change fct that changes a label that represents the color or something. FUCK ME xD
    def manipulatePresets(self):

        if (self.flagChange):
            print("I will change")
        else:
            tmpComboBox = self.makeComboBox()
            self.loadPresets()
            print(self.ui.scrollAreaWidgetContents.layout())

    def loadPresets(self):

        tmpComboBoxMarker = []

        for preset in self.listPresets:
            tmpComboBox = QComboBox(self)
            for marker in preset:
                tmpComboBox.addItem(marker)

            tmpComboBoxMarker.append(tmpComboBox)
            self.ui.scrollAreaWidgetContents.layout().insertWidget(1, tmpComboBox)


        self.listComboBoxPresets.append(tmpComboBoxMarker)


    def makeComboBox(self):
        tmpComboBox = QComboBox(self)
        tmpComboBox.addItems(["A", "B", "C", "D", "E", "F"])

        return tmpComboBox



'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SelectMarkerWindow()
    widget.show()
    sys.exit(app.exec())
'''
