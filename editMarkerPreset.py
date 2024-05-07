# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, \
    QInputDialog, QLabel, QMessageBox
from PySide6.QtGui import QColor, QPixmap, QIcon, QDrag, QCursor
from PySide6.QtCore import Qt, QSize, QMimeData
from PySide6 import QtWidgets
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_files.ui_markerPresetForm import Ui_markerPresetWindow

'''
Cool way to overload a function
 ###
 need to add the following :
     tmpLabel = ClickableLabel(self.onLabelClicked)

     def onLabelClicked(self, event):
         button = event.button()
         modifiers = event.modifiers()

         if modifiers == Qt.NoModifier and button == Qt.LeftButton:
             print("event")

 ###
class ClickableLabel(QtWidgets.QLabel):
    def __init__(self, whenClicked, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
        self._whenClicked = whenClicked

    def mousePressEvent(self, event):
        print(self.text(), self.palette().color(self.backgroundRole()).name())
        self._whenClicked(event)
'''
# @todo implement the text fields as the input after the button is clicked, check if fields are not None and if color is a hex nr


class TextEntryDialog(QDialog):
    def __init__(self, parent=None):
        super(TextEntryDialog, self).__init__(parent)

        self.setWindowTitle("New Preset Name")
        self.layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.label.setText("Name :")
        self.text_entry = QLineEdit(self)
        self.layout.addWidget(self.text_entry)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)


class SelectMarkerWindow(QWidget):
    def __init__(self, MarkerPresetWindow, argDictMarker=None, presetInd=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_markerPresetWindow()
        self.ui.setupUi(self)

        self.markerPresetWindow = MarkerPresetWindow
        self.allMarkerDict = self.markerPresetWindow.dictAllMarkers

# variable setup
        self.listLabel = []
        self.dictMarker = argDictMarker if argDictMarker else {}

        self.dictMarkerList = []
        print(self.dictMarker.items())
        print(self.dictMarkerList)

        if (self.dictMarker != None):
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
        self.ui.pushButtonDelMrk.clicked.connect(self.delButtonClicked)

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

    def mousePressEvent(self, event):

        widget = self.childAt(event.pos())

        if (type(widget) == QLabel):
            text = widget.text()
            col = widget.palette().color(widget.backgroundRole()).name()
            self.addOrChangeMarker(text, col, widget)

# buttons clicked functions
    def colorButtonClicked(self):

        color = QtWidgets.QColorDialog.getColor().name()
        self.ui.lineEditColor.setText(color)


    def addButtonClicked(self):

        text = self.ui.lineEditName.text()
        color = self.ui.lineEditColor.text()

        if (text == ""):
           QMessageBox.warning(self, "Warning", "Please enter a name")
        if (color == ""):
            QMessageBox.warning(self, "Warning", "Please enter a color")
        if (text in self.dictMarker or any(text in tup for tup in self.dictMarkerList)):
            QMessageBox.warning(self, "Warning", "The chosen Name is already in this preset")
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
        if (self.presetInd is not None):
            self.markerPresetWindow.listPresets[self.presetInd] = dict(self.dictMarkerList)
        else:
            self.markerPresetWindow.listPresets.append(dict(self.dictMarkerList))
        self.markerPresetWindow.loadPresets()
        self.close()


    def rejectedButtonClicked(self):
        self.close()


    def onIndexChange(self, index):
        if (index == 0):
            return

        self.ui.lineEditName.setText(self.sender().currentText())
        self.ui.lineEditColor.setText(self.allMarkerDict[self.ui.comboBox.currentText()])
        print(self.sender().currentText())


    def colorTextChanged(self):
        if (len(self.ui.lineEditColor.text()) == 7):
            self.ui.lineEditColor.setStyleSheet("color: {color}; background-color: {color};".format(color = str(self.ui.lineEditColor.text())))


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

        if (widget != None):
            if(not self.flagDelete):
                dialog = QInputDialog()
                dialog.exec()

                text = dialog.textValue()
                color = QtWidgets.QColorDialog.getColor().name()

                color = argColor if color == "#ffffff" or color == "#000000" else color
                text = argText if text == "" else text
            print(self.dictMarkerList)
            for i in range(len(self.dictMarkerList)):
                if (argText == self.dictMarkerList[i][0]):
                    if (self.flagDelete):
                        print(self.dictMarkerList)
                        del self.dictMarkerList[i]
                        print(self.dictMarkerList)
                        del self.listLabel[i-1]
                        widget.hide()
                        widget.setParent(None)
                        self.delButtonClicked()
                        return
                    else:
                        self.dictMarkerList[i] = (text, color)
                        break

            widget.setText(text)
            widget.setStyleSheet("background-color:" + color)
            return

        text = argText
        color = argColor

        tmpLabel = QLabel()
        tmpLabel.setStyleSheet("background-color:" + color)
        tmpLabel.setAlignment(Qt.AlignRight)
        tmpLabel.setMaximumHeight(45)
        tmpLabel.setMinimumWidth(150)
        tmpLabel.setMaximumWidth(150)
        tmpLabel.setText(text)

        self.listLabel.append(tmpLabel)
        self.dictMarkerList.append((text, color))
        #self.lineEditList.append(tmpLabel)
        scrollAreaSize = min((self.ui.scrollArea.size() + QSize(0, 35)).height(), 350)
        self.ui.scrollArea.setMinimumHeight(scrollAreaSize)
        self.ui.scrollArea.setMaximumHeight(scrollAreaSize)
        self.ui.scrollAreaWidgetContents.layout().insertWidget(len(self.listLabel) - 1, tmpLabel)

    def loadPresetMarkers(self):
        if self.dictMarker:
            for key, value in self.dictMarker.items():
                self.addOrChangeMarker(key, value)

    def loadAllMarkers(self):

        self.ui.comboBox.currentIndexChanged.connect(self.onIndexChange)
        self.ui.comboBox.addItem("Add existing marker")
        for key, value in self.allMarkerDict.items():
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor(value))
            icon = QIcon(pixmap)
            fakeIndex = self.ui.comboBox.count()
            self.ui.comboBox.addItem(key)
            self.ui.comboBox.setItemIcon(fakeIndex, icon)

# IMPORTANT : Add a function that updates the main marker list when self.addOrChangeMarker(self) is called
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MarkerPresetWindow()
    widget.show()
    sys.exit(app.exec())
'''
