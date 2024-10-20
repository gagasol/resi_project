import re

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox

from ui_settingsWindow import Ui_Dialog


class Validator:
    def __init__(self):
        self.toValidateDict = {}

    def addToValidator(self, funcName: str, widgets: list, conditions: list):
        if funcName in self.toValidateDict:
            self.toValidateDict[funcName]['widgets'].append(widgets)
        else:
            self.toValidateDict[funcName] = {
                'widgets': widgets,
                'conditions': conditions
            }

    def isFormValid(self, parWidget=None):
        for name, data in self.toValidateDict.items():
            widgets = data['widgets']
            conditions = data['conditions']

            if parWidget and parWidget not in widgets:
                continue

            if any(self.entryInvalid(name, widget, conditions) for widget in widgets):
                return False

        return True

    def entryInvalid(self, funcName, widget, conditions: list):
        value = None
        if 'text' in funcName:
            value = widget.text()
        elif 'value' in funcName:
            value = widget.value()
        else:
            raise ValueError(f'Unexpected function name: {funcName}')

        if not all(condition(value) for condition in conditions):
            return True

        return False


def notEmpty(text):
    return bool(text.strip())


def isHexColor(s):
    return bool(re.match('^#(?:[0-9a-fA-F]{3}){1,2}$', s))


def isInRange(number):
    return 0 < number < 100


class SettingsWindow(QDialog):
    def __init__(self, defaultSettingsDict: dict, mainWindow=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.mainWindow = mainWindow
        self.validator = Validator()

        self.defaultSettingsDict = defaultSettingsDict
        self.blockSave = False

        self._dataNameDict = {
            "number": QObject.tr('Messung Nr.'),
            "idNumber": QObject.tr('ID-Nummer'),
            "depthMsmt": QObject.tr('Bohrtiefe'),
            "date": QObject.tr('Datum'),
            "time": QObject.tr('Uhrzeit'),
            "speedFeed": QObject.tr('Vorschub'),
            "speedDrill": QObject.tr('Drehzahl'),
            "tiltAngle": QObject.tr('Neigung'),
            "result": QObject.tr('Nadelstatus'),
            "offset": QObject.tr('Offset'),
            "graphAvgShow": QObject.tr('Mittelung'),
            "empty": "",
            "0_diameter": QObject.tr('Durchmesser'),
            "1_mHeight": QObject.tr('Messhöhe'),
            "2_mDirection": QObject.tr('Messrichtung'),
            "3_objecttype": QObject.tr('Objektart'),
            "4_location": QObject.tr('Standort'),
            "5_name": QObject.tr('Name')
        }

        self.strsToShowInGraph = []

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.pushButtonGraph.clicked.connect(self.graphButtonClicked)
        self.ui.pushButtonPref.clicked.connect(self.preferenceButtonClicked)
        self.ui.pushButtonPrint.clicked.connect(self.printButtonClicked)
        self.ui.pushButtonPresets.clicked.connect(self.presetsButtonClicked)

        self.ui.doubleSpinBoxTopPerc.valueChanged.connect(self.syncWidgetSizeBoxes)
        self.ui.doubleSpinBoxGraphPerc.valueChanged.connect(self.syncWidgetSizeBoxes)
        self.ui.doubleSpinBoxBotPerc.valueChanged.connect(self.syncWidgetSizeBoxes)

        self.ui.lineEditFeedColor.textChanged.connect(self.validateField)
        self.ui.lineEditDrillColor.textChanged.connect(self.validateField)
        self.ui.lineEditGraphBackgroundColor.textChanged.connect(self.validateField)
        self.ui.lineEditMarkingGraphBackgroundColor.textChanged.connect(self.validateField)

        self.ui.pushButtonGraphdisplayData.clicked.connect(self.createCheckboxDialog)

        self.initUi()

        colorTextFields = [self.ui.lineEditFeedColor, self.ui.lineEditDrillColor, self.ui.lineEditGraphBackgroundColor,
                           self.ui.lineEditMarkingGraphBackgroundColor]
        spinBoxes = [self.ui.doubleSpinBoxMarkerHeight]

        self.validator.addToValidator('textColor', colorTextFields, [notEmpty, isHexColor])
        self.validator.addToValidator('valueSpinBoxes', spinBoxes, [isInRange])



    def initUi(self):
        self.ui.doubleSpinBoxTopPerc.setValue(self.getSettingsVariable("heightWidgetTopPerc"))
        self.ui.doubleSpinBoxGraphPerc.setValue(self.getSettingsVariable("heightWidgetGraphPerc"))
        self.ui.doubleSpinBoxBotPerc.setValue(self.getSettingsVariable("heightWidgetBottomPerc"))
        self.ui.lineEditFeedColor.setText(self.getSettingsVariable("colorFeedPlot"))
        self.ui.lineEditDrillColor.setText(self.getSettingsVariable("colorDrillPlot"))
        self.ui.lineEditGraphBackgroundColor.setText(self.getSettingsVariable("colorBackground"))
        self.ui.lineEditMarkingGraphBackgroundColor.setText(self.getSettingsVariable("colorBackgroundMarking"))
        self.ui.doubleSpinBoxMarkerHeight.setValue(self.getSettingsVariable("markerHeightPerc")*100)
        self.ui.spinBoxLabelSize.setValue(self.getSettingsVariable("labelFontSize"))
        self.ui.doubleSpinBoxTopPerc_2.setValue(self.getSettingsVariable("printHeightWidgetTopPerc"))
        self.ui.doubleSpinBoxGraphPerc_2.setValue(self.getSettingsVariable("printHeightWidgetGraphPerc"))
        self.ui.doubleSpinBoxBotPerc_2.setValue(self.getSettingsVariable("printHeightWidgetBottomPerc"))
        self.ui.lineEditPrintLabelSize.setText(str(self.getSettingsVariable("printLabelFontSize")))
        self.ui.lineEditTableFontSize.setText(str(self.getSettingsVariable("printFontSize")))
        self.strsToShowInGraph = self.getSettingsVariable("strsToShowInGraph")

    def accept(self):
        if self.validator.isFormValid() and not self.blockSave:
            overrideDict = {"heightWidgetTopPerc": self.ui.doubleSpinBoxTopPerc.value(),
                            "heightWidgetGraphPerc": self.ui.doubleSpinBoxGraphPerc.value(),
                            "heightWidgetBottomPerc": self.ui.doubleSpinBoxBotPerc.value(),
                            "colorFeedPlot": self.ui.lineEditFeedColor.text(),
                            "colorDrillPlot": self.ui.lineEditDrillColor.text(),
                            "colorBackground": self.ui.lineEditGraphBackgroundColor.text(),
                            "colorBackgroundMarking": self.ui.lineEditMarkingGraphBackgroundColor.text(),
                            "markerHeightPerc": self.ui.doubleSpinBoxMarkerHeight.value()/100,
                            "fontSize": 14,
                            "labelFontSize": self.ui.spinBoxLabelSize.value(),
                            "printHeightWidgetTopPerc": self.ui.doubleSpinBoxTopPerc_2.value(),
                            "printHeightWidgetGraphPerc": self.ui.doubleSpinBoxGraphPerc_2.value(),
                            "printHeightWidgetBottomPerc": self.ui.doubleSpinBoxBotPerc_2.value(),
                            "printFontSize": self.ui.lineEditTableFontSize.text(),
                            "printLabelFontSize": self.ui.lineEditPrintLabelSize.text(),
                            "strsToShowInGraph": self.strsToShowInGraph
                            }

            for key, value in overrideDict.items():
                self.setSettingsVariable(key, value)

        else:
            return

        super().accept()

    def reject(self):
        self.initUi()

        super().reject()

    def createCheckboxDialog(self):
        dialog = QDialog(self)
        layout = QVBoxLayout()

        checkboxes = []

        for key, value in self._dataNameDict.items():
            if key == "empty":
                continue
            checkbox = QCheckBox(value, dialog)

            if key in self.strsToShowInGraph:
                checkbox.setChecked(True)

            checkbox.setObjectName(key)
            checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)


        dialog.setLayout(layout)
        dialog.show()

        result = dialog.exec()

        if result == QDialog.Accepted:
            self.strsToShowInGraph = [cb.objectName() for cb in checkboxes if cb.isChecked()]

    def graphButtonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def preferenceButtonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def printButtonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def presetsButtonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.mainWindow.markerPresetWin.exec()

    def syncWidgetSizeBoxes(self, value):
        sender = self.sender()
        total = (self.ui.doubleSpinBoxTopPerc.value() + self.ui.doubleSpinBoxGraphPerc.value()
                 + self.ui.doubleSpinBoxBotPerc.value())

        if total > 100:
            self.blockSave = True
            self.ui.doubleSpinBoxTopPerc.setStyleSheet("border: 1px solid red;")
            self.ui.doubleSpinBoxGraphPerc.setStyleSheet("border: 1px solid red;")
            self.ui.doubleSpinBoxBotPerc.setStyleSheet("border: 1px solid red;")
        else:
            self.blockSave = False
            self.ui.doubleSpinBoxTopPerc.setStyleSheet("")
            self.ui.doubleSpinBoxGraphPerc.setStyleSheet("")
            self.ui.doubleSpinBoxBotPerc.setStyleSheet("")

    def validateField(self):
        sender = self.sender()

        if self.validator.isFormValid(self.sender()):
            sender.setStyleSheet("")
        else:
            sender.setStyleSheet("border: 1px solid red;")

    def validateFields(self):
        errorCount = 0

        le1 = self.ui.lineEditFeedColor
        le2 = self.ui.lineEditDrillColor
        le3 = self.ui.lineEditGraphBackground
        le4 = self.ui.lineEditMarkingGraphBackground
        sb4 = self.ui.doubleSpinBoxMarkerHeight

        for edit in (le1, le2, le3, le4):
            if not edit.text():
                edit.setStyleSheet("border: 1px solid red;")
                errorCount += 1
            else:
                if edit.text()[0] != '#':
                    edit.setText('#' + edit.text())

                if isHexColor(edit.text()):
                    edit.setStyleSheet("")
                else:
                    edit.setStyleSheet("border: 1px solid red;")
                    errorCount += 1

        if errorCount > 0:
            self.blockSave = True
        else:
            self.blockSave = False

    def getSettingsVariable(self, variableName):
        return self.defaultSettingsDict[variableName]

    def setSettingsVariable(self, variableName, value):
        self.defaultSettingsDict[variableName] = value


