import re

from PySide6.QtWidgets import QDialog

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

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.pushButtonGraph.clicked.connect(self.graphButtonClicked)
        self.ui.pushButtonPref.clicked.connect(self.preferenceButtonClicked)
        self.ui.pushButtonPresets.clicked.connect(self.presetsButtonClicked)

        self.ui.doubleSpinBoxTopPerc.valueChanged.connect(self.syncWidgetSizeBoxes)
        self.ui.doubleSpinBoxGraphPerc.valueChanged.connect(self.syncWidgetSizeBoxes)
        self.ui.doubleSpinBoxBotPerc.valueChanged.connect(self.syncWidgetSizeBoxes)

        self.ui.lineEditFeedColor.textChanged.connect(self.validateField)
        self.ui.lineEditDrillColor.textChanged.connect(self.validateField)
        self.ui.lineEditGraphBackground.textChanged.connect(self.validateField)
        self.ui.lineEditMarkingGraphBackground.textChanged.connect(self.validateField)

        self.initUi()

        colorTextFields = [self.ui.lineEditFeedColor, self.ui.lineEditDrillColor, self.ui.lineEditGraphBackground,
                           self.ui.lineEditMarkingGraphBackground]
        spinBoxes = [self.ui.doubleSpinBoxMarkerHeight]

        self.validator.addToValidator('textColor', colorTextFields, [notEmpty, isHexColor])
        self.validator.addToValidator('valueSpinBoxes', spinBoxes, [isInRange])



    def initUi(self):
        self.ui.doubleSpinBoxTopPerc.setValue(self.getSettingsVariable("heightWidgetTopPerc"))
        self.ui.doubleSpinBoxGraphPerc.setValue(self.getSettingsVariable("heightWidgetGraphPerc"))
        self.ui.doubleSpinBoxBotPerc.setValue(self.getSettingsVariable("heightWidgetBottomPerc"))
        self.ui.lineEditFeedColor.setText(self.getSettingsVariable("colorFeedPlot"))
        self.ui.lineEditDrillColor.setText(self.getSettingsVariable("colorDrillPlot"))
        self.ui.lineEditGraphBackground.setText(self.getSettingsVariable("colorBackground"))
        self.ui.lineEditMarkingGraphBackground.setText(self.getSettingsVariable("colorBackgroundMarking"))
        self.ui.doubleSpinBoxMarkerHeight.setValue(self.getSettingsVariable("markerHeightPerc"))

    def accept(self):
        if self.validator.isFormValid() and not self.blockSave:
            overrideDict = {"heightWidgetTopPerc": self.ui.doubleSpinBoxTopPerc.value(),
                            "heightWidgetGraphPerc": self.ui.doubleSpinBoxGraphPerc.value(),
                            "heightWidgetBottomPerc": self.ui.doubleSpinBoxBotPerc.value(),
                            "colorFeedPlot": self.ui.lineEditFeedColor.text(),
                            "colorDrillPlot": self.ui.lineEditDrillColor.text(),
                            "colorBackground": self.ui.lineEditGraphBackground.text(),
                            "colorBackgroundMarking": self.ui.lineEditMarkingGraphBackground.text(),
                            "markerHeightPerc": self.ui.doubleSpinBoxMarkerHeight.value()}

            for key, value in overrideDict.items():
                self.setSettingsVariable(key, value)

        else:
            return

        super().accept()

    def reject(self):
        self.initUi()

        super().reject()




    def graphButtonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def preferenceButtonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def presetsButtonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
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

def isHexColor(s):
    return bool(re.match('^#(?:[0-9a-fA-F]{3}){1,2}$', s))

