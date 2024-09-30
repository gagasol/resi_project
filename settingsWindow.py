import sys

from PySide6.QtWidgets import QDialog


class SettingsWindow(QDialog):
    def __init__(self, defaultSettingsDict: dict, parent=None):
        super().__init__(parent)

        self.defaultSettingsDict = defaultSettingsDict

    def getSettingsVariable(self, variableName):
        return self.defaultSettingsDict[variableName]

    def setSettingsVariable(self, variableName, value):
        self.defaultSettingsDict[variableName] = value

