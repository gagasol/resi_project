
# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, \
    QInputDialog, QLabel
from PySide6.QtGui import QColor
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


class SelectMarkerWindow(QWidget):
    def __init__(self, parent=None, lineEditsColors=[]):
        super().__init__(parent)
        self.ui = Ui_markerPresetWindow()
        self.ui.setupUi(self)

        # variable setup
        self.lineEditList = lineEditsColors
        self.labelDict = {}
        self.presetDict = {}

        self.ui.pushButtonAddMrk.clicked.connect(self.addButtonClicked)
        self.ui.pushButtonChgMrk.clicked.connect(self.chgButtonClicked)
        self.ui.pushButtonDelMrk.clicked.connect(self.delButtonClicked)

    def mousePressEvent(self, event):
        widget = self.childAt(event.pos())
        if (type(widget) == QLabel):
            self.addOrChangeMarker(True, widget)

        a = [1, 2, 3, 4, 5]
        print(a[-1])

    def addButtonClicked(self):

        self.addOrChangeMarker()

    def addOrChangeMarker(self, changeFlag=False, widget=None):

        dialog = QInputDialog()
        dialog.exec()
        #if(dialog.reject()): return

        text = dialog.textValue()

        color = QtWidgets.QColorDialog.getColor().name()

        if (changeFlag):
            argText = widget.text()
            argCol = widget.palette().color(widget.backgroundRole()).name()
            print(changeFlag, argText, argCol)
            color = argCol if color == "#ffffff" else color
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

    def chgButtonClicked(self):

        print(self.presetDict)

    def delButtonClicked(self):

        layout = QVBoxLayout()
        self.ui.widget_3.setLayout(layout)
        print("DEATH AND DESTRUCTION")


# IMPORTANT : Add a function that updates the main marker list when self.addOrChangeMarker(self) is called
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MarkerPresetWindow()
    widget.show()
    sys.exit(app.exec())
'''