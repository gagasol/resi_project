# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, \
    QInputDialog, QLabel, QMessageBox, QScrollArea
from PySide6.QtGui import QColor, QPixmap, QIcon, QDrag, QCursor
from PySide6.QtCore import Qt, QSize, QMimeData
from PySide6 import QtWidgets

import pickMarkerWindow
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_files.ui_markerPresetForm import Ui_markerPresetWindow



# @todo implement the text fields as the input after the button is clicked, check if fields are not None and if color is a hex nr



class TextEntryDialog(QDialog):
    def __init__(self, parent=None):
        super(TextEntryDialog, self).__init__(parent)

        self.setWindowTitle("New Preset Name")
        self.layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.label.setText("Name :")
        self.layout.addWidget(self.label)
        self.text_entry = QLineEdit(self)
        self.layout.addWidget(self.text_entry)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)


class EditMarkerPresetWindow(QDialog):
    def __init__(self, MarkerPresetWindow, argDictMarker=None, presetInd=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_markerPresetWindow()
        self.ui.setupUi(self)

        self.markerPresetWindow = MarkerPresetWindow
        self.markerPresetList = self.markerPresetWindow.markerPresetList

# variable setup
        self.listLabel = []
        self.dictMarker = argDictMarker if argDictMarker else {}

        self.dictMarkerList = []

        if (self.dictMarker != {}):
            print(self.dictMarker)
            self.dictMarkerList.append(("_NameForPreset", self.dictMarker["_NameForPreset"]))
            self.ui.lineEditPresetName.setText(self.dictMarker["_NameForPreset"])
        else:
            dialog = TextEntryDialog(self)
            if dialog.exec():
                text = dialog.text_entry.text()
                self.dictMarkerList.append(("_NameForPreset", text))
                self.ui.lineEditPresetName.setText(text)

        self.presetInd = presetInd

        self.flagDelete = False

        self.ui.pushButtonColorPick.clicked.connect(self.colorButtonClicked)
        self.ui.pushButtonChgMrk.clicked.connect(self.addButtonClicked)
        #self.ui.pushButtonDelMrk.clicked.connect(self.delButtonClicked)

        self.ui.buttonBox.accepted.connect(self.acceptButtonClicked)
        self.ui.buttonBox.rejected.connect(self.rejectedButtonClicked)

        self.ui.lineEditColor.textChanged.connect(self.colorTextChanged)

        self.loadAllMarkers()
        self.loadPresetMarkers()


# event functions
    '''
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        pos = event.pos()
        widget = event.source()
        for n in range(self.ui.scrollAreaWidgetContents.layout().count()):
            w = self.ui.scrollAreaWidgetContents.layout().itemAt(n).widget()
            print(w)
            wPos = w.mapTo(self.ui.widget_3, w.pos())
            if w and pos.y()-20 < wPos.y():
                self.ui.scrollAreaWidgetContents.layout().insertWidget(n-1, widget)
                break

        event.accept()
    '''


# buttons clicked functions
    def colorButtonClicked(self):

        color = QtWidgets.QColorDialog.getColor().name()
        self.ui.lineEditColor.setText(color)


    def addButtonClicked(self):

        text = self.ui.lineEditName.text()
        color = self.ui.lineEditColor.text()

        if (text == ""):
           QMessageBox.warning(self, "Warning", "Please enter a name and press "+" afterwards!")
           return
        if (color == ""):
            QMessageBox.warning(self, "Warning", "Please enter a color")
            return

        self.ui.lineEditName.setText("")
        self.ui.lineEditColor.setText("")
        self.ui.lineEditColor.setStyleSheet("color: #000000; background-color: #ffffff;")
        self.addOrChangeMarker(argText=text, argColor=color)


    def delButtonClicked(self):
        self.flagDelete = not self.flagDelete
        if(self.flagDelete):
            self.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def acceptButtonClicked(self):
        returnList = self.ui.scrollAreaWidgetContents.getAllMarkers()
        returnList.insert(0, ("_NameForPreset", self.ui.lineEditPresetName))
        self.markerPresetWindow.setWindowModality(Qt.ApplicationModal)
        dictMarker = dict(returnList)
        dictMarker["_NameForPreset"] = self.ui.lineEditPresetName.text()
        print(dictMarker)
        if self.presetInd is not None:
            self.markerPresetWindow.markerPresetList[self.presetInd] = dictMarker
        else:
            self.markerPresetWindow.markerPresetList.append(dictMarker)
        self.markerPresetWindow.loadPresets()
        self.dictMarkerList.remove(self.dictMarkerList[0])
        self.close()


    def rejectedButtonClicked(self):
        self.close()


    def onIndexChange(self, index):
        if index == 0:
            return

        senderText = self.sender().currentText()
        self.ui.lineEditName.setText(senderText)

        icon = self.sender().itemIcon(index)
        pixmap = icon.pixmap(30, 30)
        color = pixmap.toImage().pixelColor(0, 0)
        self.ui.lineEditColor.setText(color.name())


    def colorTextChanged(self):
        if (len(self.ui.lineEditColor.text()) == 7):
            self.ui.lineEditColor.setStyleSheet("color: {color}; background-color: {color};".format(color = str(self.ui.lineEditColor.text())))
            #self.addButtonClicked()


# algorithm section

# algorithmic
    def addOrChangeMarker(self, argText, argColor, widget=None):
        """
        creates a new marker entry and adds it as a label or changes it if widget != None
        Parameters
        argText (str): the text of the marker
        argColor (str): the color of the marker
        widget (QLabel): the widget to change
        """
        if (argText == "_NameForPreset"):
            return

        text = argText
        color = argColor

        self.ui.scrollAreaWidgetContents.addMarkerLabel(argText, argColor)

        self.dictMarkerList.append((text, color))
        scrollAreaSize = min((self.ui.scrollArea.size() + QSize(0, 35)).height(), 500)
        self.ui.scrollArea.setMinimumHeight(scrollAreaSize)
        self.ui.scrollArea.setMaximumHeight(scrollAreaSize)

    def loadPresetMarkers(self):
        if self.dictMarker:
            for key, value in self.dictMarker.items():
                self.addOrChangeMarker(key, value)

    def loadAllMarkers(self):

        allMarkersList = []

        self.ui.comboBoxAddExistingMarker.currentIndexChanged.connect(self.onIndexChange)
        self.ui.comboBoxAddExistingMarker.addItem("Add existing marker")
        for preset in self.markerPresetList:
            for key, value in preset.items():
                if "_NameForPreset" in key:
                    continue
                if key+value in allMarkersList:
                    continue

                allMarkersList.append(key+value)
                pixmap = QPixmap(30, 30)
                pixmap.fill(QColor(value))
                print(pixmap.toImage().pixelColor(0, 0))
                icon = QIcon(pixmap)
                fakeIndex = self.ui.comboBoxAddExistingMarker.count()
                self.ui.comboBoxAddExistingMarker.addItem(key)
                self.ui.comboBoxAddExistingMarker.setItemIcon(fakeIndex, icon)

# IMPORTANT : Add a function that updates the main marker list when self.addOrChangeMarker(self) is called
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MarkerPresetWindow()
    widget.show()
    sys.exit(app.exec())
'''
