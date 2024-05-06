# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, \
    QInputDialog, QLabel
from PySide6.QtGui import QColor, QPixmap, QIcon
from PySide6.QtCore import Qt
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

class SelectMarkerWindow(QWidget):
    def __init__(self, MarkerPresetWindow, argDictMarker=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_markerPresetWindow()
        self.ui.setupUi(self)

        self.markerPresetWindow = MarkerPresetWindow

        self.allMarkerDict = self.markerPresetWindow.dictAllMarkers
        # variable setup
        self.labelDict = {}
        self.presetDict = {}
        self.dictMarker = argDictMarker if argDictMarker else {}

        self.ui.pushButtonChgMrk.clicked.connect(self.addButtonClicked)
        self.ui.pushButtonDelMrk.clicked.connect(self.delButtonClicked)

        self.loadAllMarkers()
        self.loadPresetMarkers()

    def mousePressEvent(self, event):
        widget = self.childAt(event.pos())

        if (type(widget) == QLabel):
            text = widget.text()
            col = widget.palette().color(widget.backgroundRole()).name()
            self.addOrChangeMarker(text, col, True, widget)


    def addButtonClicked(self):

        dialog = QInputDialog()
        dialog.exec()

        text = dialog.textValue()
        color = QtWidgets.QColorDialog.getColor().name()

        self.addOrChangeMarker(argText=text, argColor=color)


    def chgButtonClicked(self):

        print(self.ui.comboBox.currentText())

    def delButtonClicked(self):

        layout = QVBoxLayout()
        self.ui.widget_3.setLayout(layout)
        print("DEATH AND DESTRUCTION")

    def onIndexChange(self, index):
        print(self.sender().currentText())

    def addOrChangeMarker(self, argText, argColor, changeFlag=False, widget=None):

        text = argText
        color = argColor

        if (changeFlag):
            dialog = QInputDialog()
            dialog.exec()

            text = dialog.textValue()
            color = QtWidgets.QColorDialog.getColor().name()
            print(changeFlag, argText, argColor)
            color = argColor if color == "#ffffff" else color
            text = argText if text == "" else text
            print(self.labelDict[argText])
            widget.setParent(None)
            self.ui.widget_3.layout().removeWidget(widget)
            del self.presetDict[argText]
            del self.labelDict[argText]

        tmpLabel = QLabel()
        tmpLabel.setStyleSheet("background-color:" + color)
        tmpLabel.setAlignment(Qt.AlignCenter)
        tmpLabel.setMaximumHeight(45)
        tmpLabel.setText(text)

        self.labelDict.update({text: tmpLabel})
        self.presetDict.update({text: color})
        #self.lineEditList.append(tmpLabel)
        self.ui.widget_3.layout().insertWidget(len(self.labelDict) - 1, tmpLabel)

    def loadPresetMarkers(self):
        if self.dictMarker:
            for key, value in self.dictMarker.items():
                self.addOrChangeMarker(key, value)
    def loadAllMarkers(self):

        self.ui.comboBox.currentIndexChanged.connect(self.onIndexChange)
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
