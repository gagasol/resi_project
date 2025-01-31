from PySide6.QtWidgets import QWidget


class CustomLabelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.listLabelWidgets = []
        self.dictLabelWidgets = {}

    def upButtonPressed(self):
        pass
    def downButtonPressed(self):
        pass
    def deleteButtonPressed(self):
        pass