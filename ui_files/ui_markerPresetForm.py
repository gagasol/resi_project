# -*- coding: utf-8 -*-



from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QComboBox, QDialogButtonBox,
                               QHBoxLayout, QLineEdit, QPushButton, QScrollArea,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QMessageBox)

from pickMarkerWindow import CustomLabel


class CustomLabelContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.listMarkerLabels = []
        self.dictMarkerLabels = {}

    def deleteWidget(self):
        label = self.sender().parent().layout().itemAt(0).widget()
        name = label.text()
        response = QMessageBox.question(self, 'Confirm Delete', f'Are you sure you want to delete \"{name}\"?',
                                        QMessageBox.Yes | QMessageBox.Cancel)

        if response == QMessageBox.Yes:
            index = label.index
            for widget in self.listMarkerLabels[index:]:
                widget.layout().itemAt(0).widget().index -= 1

            self.listMarkerLabels[index].deleteLater()
            self.listMarkerLabels.pop(index)


    def addMarkerLabel(self, name, col):
        print(f'name: {name}')
        markerLabel = QWidget(self)
        index = len(self.listMarkerLabels)
        print(f'index in addMarkerLabel: {index}')
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        tmpMarkerLabel = CustomLabel(col, index)
        tmpMarkerLabel.setText(name)
        tmpMarkerLabel.setMaximumHeight(20)
        tmpMarkerLabel.setMinimumWidth(100)
        horizontalLayout.addWidget(tmpMarkerLabel)

        buttonUp = self._createUpButton(markerLabel)
        horizontalLayout.addWidget(buttonUp)

        buttonDown = self._createDownButton(markerLabel)
        horizontalLayout.addWidget(buttonDown)

        buttonDeleteMarker = self._createDeleteMarker(markerLabel)
        horizontalLayout.addWidget(buttonDeleteMarker)
        markerLabel.setLayout(horizontalLayout)
        self.listMarkerLabels.append(markerLabel)
        self.layout().insertWidget(index, markerLabel)

    def upButtonPressed(self):
        widget = self.sender().parent()
        index = widget.layout().itemAt(0).widget().index

        if 0 < index:
            widgetAbove = self.listMarkerLabels[index-1]
            indexAbove = widgetAbove.layout().itemAt(0).widget().index

            widget.setParent(None)
            widgetAbove.setParent(None)

            self.layout().removeWidget(widgetAbove)
            self.layout().removeWidget(widget)

            self.listMarkerLabels[index] = widgetAbove
            self.listMarkerLabels[index-1] = widget

            widget.layout().itemAt(0).widget().index -= 1
            widgetAbove.layout().itemAt(0).widget().index += 1

            self.layout().insertWidget(indexAbove, widget)
            self.layout().insertWidget(index, widgetAbove)

            QCoreApplication.processEvents()

    def downButtonPressed(self):
        widget = self.sender().parent()
        index = widget.layout().itemAt(0).widget().index

        if index < len(self.listMarkerLabels) - 1:
            widgetBelow = self.listMarkerLabels[index + 1]
            indexBelow = widgetBelow.layout().itemAt(0).widget().index

            widgetBelow.setParent(None)
            widget.setParent(None)

            self.layout().removeWidget(widgetBelow)
            self.layout().removeWidget(widget)

            self.listMarkerLabels[index] = widgetBelow
            self.listMarkerLabels[index + 1] = widget

            widget.layout().itemAt(0).widget().index += 1
            widgetBelow.layout().itemAt(0).widget().index -= 1

            self.layout().insertWidget(index, widgetBelow)
            self.layout().insertWidget(indexBelow, widget)

            QCoreApplication.processEvents()

    def getAllMarkers(self):
        returnList = []
        for widget in self.listMarkerLabels:
            if isinstance(widget, QWidget):
                label = widget.layout().itemAt(0).widget()
                if isinstance(label, CustomLabel):
                    name = label.text()
                    color = label.color
                    returnList.append((name, color))

        return returnList

    def _createDeleteMarker(self, parent):
        pushButtonDelMrk = QPushButton(parent)
        pushButtonDelMrk.setMinimumSize(QSize(20, 0))
        pushButtonDelMrk.setMaximumSize(QSize(20, 20))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/minus-square.svg", QSize(), QIcon.Normal, QIcon.Off)
        pushButtonDelMrk.setIcon(icon2)
        pushButtonDelMrk.setIconSize(QSize(20, 20))
        pushButtonDelMrk.clicked.connect(self.deleteWidget)
        self._setButtonStyleShield(pushButtonDelMrk)

        return pushButtonDelMrk

    def _createUpButton(self, parent):
        pushButtonUp = QPushButton(parent)
        pushButtonUp.setMinimumSize(QSize(20, 0))
        pushButtonUp.setMaximumSize(QSize(20, 20))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/arrow_upward_30dp.svg", QSize(), QIcon.Normal, QIcon.Off)
        pushButtonUp.setIcon(icon2)
        pushButtonUp.setIconSize(QSize(20, 20))
        pushButtonUp.clicked.connect(self.upButtonPressed)
        self._setButtonStyleShield(pushButtonUp)

        return pushButtonUp

    def _createDownButton(self, parent):
        pushButtonDown = QPushButton(parent)
        pushButtonDown.setMinimumSize(QSize(20, 0))
        pushButtonDown.setMaximumSize(QSize(20, 20))
        icon = QIcon()
        icon.addFile(u':/icons/icons/arrow_downward_30dp.svg', QSize(), QIcon.Normal, QIcon.Off)
        pushButtonDown.setIcon(icon)
        pushButtonDown.setIconSize(QSize(20, 20))
        pushButtonDown.clicked.connect(self.downButtonPressed)
        self._setButtonStyleShield(pushButtonDown)

        return pushButtonDown

    @staticmethod
    def _setButtonStyleShield(button):
        button.setStyleSheet(u"QPushButton{\n"
                           "border: none;\n"
                           "padding-left: -2px;\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover{\n"
                           "	background-color: white;\n"
                           "}\n"
                           "\n"
                           "QPushButton:pressed{\n"
                           "	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                           "                                      stop: 0 #FFFFFF, stop: 1 #dadbde);\n"
                           "}")


class Ui_markerPresetWindow(object):
    def setupUi(self, markerPresetWindow):
        if not markerPresetWindow.objectName():
            markerPresetWindow.setObjectName(u"markerPresetWindow")
        markerPresetWindow.resize(300, 250)


        self.verticalLayout = QVBoxLayout(markerPresetWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.widgetM_0 = QWidget(markerPresetWindow)

        self.horizontalLayoutM_0 = QHBoxLayout(self.widgetM_0)
        self.horizontalLayoutM_0.setObjectName(u"horizontalLayoutM_0")

        self.lineEditPresetName = QLineEdit(self.widgetM_0)
        self.lineEditPresetName.setObjectName(u"lineEditPresetName")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        # sizePolicy3.setHeightForWidth(self.labelPresetName.sizePolicy().hasHeightForWidth())
        self.lineEditPresetName.setSizePolicy(sizePolicy3)
        self.lineEditPresetName.setMaximumSize(5000, 100)
        self.lineEditPresetName.setStyleSheet(u"font: 700 30pt \"Bahnschrift\";\n"
                                              "border: none;\n"
                                              "background-color: transparent")

        #self.horizontalSpacerM_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        #self.horizontalLayoutM_0.addItem(self.horizontalSpacerM_2)
        self.horizontalLayoutM_0.addWidget(self.lineEditPresetName)

        self.verticalLayout.addWidget(self.widgetM_0)

        self.widget_4 = QWidget(markerPresetWindow)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 45))
        self.widget_4.setMaximumSize(QSize(16777215, 45))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)


        self.comboBoxAddExistingMarker = QComboBox(self.widget_4)
        self.comboBoxAddExistingMarker.setObjectName(u"comboBoxAddExistingMarker")
        self.comboBoxAddExistingMarker.setMinimumSize(QSize(0, 0))
        self.comboBoxAddExistingMarker.setStyleSheet(u"QComboBox QAbstractItemView {\n"
                       "  border: 1px solid grey;\n"
                       "  background: white;\n"
                       "  selection-background-color: blue;\n"
                       "color: black;\n"
                       "}")

        self.horizontalLayout_3.addWidget(self.comboBoxAddExistingMarker)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.verticalLayout.addWidget(self.widget_4)

        self.widget = QWidget(markerPresetWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(400, 45))
        self.widget.setMaximumSize(QSize(16777215, 25))
        self.widget.setStyleSheet(u"QPushButton{\n"
"border: none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: white;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #FFFFFF, stop: 1 #dadbde);\n"
"}QPushButton{\n"
"border: none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: white;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #FFFFFF, stop: 1 #dadbde);\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.horizontalSpacerManuel_0 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacerManuel_0)

        self.lineEditName = QLineEdit(self.widget)
        self.lineEditName.setObjectName(u"lineEditName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditName.sizePolicy().hasHeightForWidth())
        self.lineEditName.setSizePolicy(sizePolicy)
        self.lineEditName.setMinimumSize(QSize(60, 0))
        self.lineEditName.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout.addWidget(self.lineEditName)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.lineEditColor = QLineEdit(self.widget)
        self.lineEditColor.setObjectName(u"lineEditColor")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEditColor.sizePolicy().hasHeightForWidth())
        self.lineEditColor.setSizePolicy(sizePolicy1)
        self.lineEditColor.setMinimumSize(QSize(60, 0))
        self.lineEditColor.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.lineEditColor)

        self.pushButtonColorPick = QPushButton(self.widget)
        self.pushButtonColorPick.setObjectName(u"pushButtonColorPick")
        self.pushButtonColorPick.setMinimumSize(QSize(20, 0))
        self.pushButtonColorPick.setMaximumSize(QSize(25, 16777215))
        self.pushButtonColorPick.setStyleSheet(u"QPushButton{\n"
"border: none;\n"
"padding-left: -2px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: white;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #FFFFFF, stop: 1 #dadbde);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/icons/palette.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonColorPick.setIcon(icon)
        self.pushButtonColorPick.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.pushButtonColorPick)

        self.pushButtonChgMrk = QPushButton(self.widget)
        self.pushButtonChgMrk.setObjectName(u"pushButtonChgMrk")
        self.pushButtonChgMrk.setMinimumSize(QSize(25, 0))
        self.pushButtonChgMrk.setMaximumSize(QSize(25, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/plus-square.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonChgMrk.setIcon(icon1)
        self.pushButtonChgMrk.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.pushButtonChgMrk)

        #self.horizontalLayout.addWidget(self.pushButtonDelMrk)


        self.verticalLayout.addWidget(self.widget)

        self.widget_3 = QWidget(markerPresetWindow)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setStyleSheet(u"QLabel{\n"
"	font: 12pt \"NSimSun\";\n"
"	text-decoration: underline;\n"
"}")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        #self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.scrollArea = QScrollArea(self.widget_3)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setMinimumSize(QSize(200, 0))
        self.scrollArea.setMaximumSize(QSize(400, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = CustomLabelContainer()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 168, 48))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 27, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.scrollArea.setStyleSheet(u"QScrollArea {border: none;}\n")


        self.verticalLayout_2.addItem(self.verticalSpacer)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_3.addWidget(self.scrollArea)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_2 = QWidget(markerPresetWindow)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 45))
        self.widget_2.setMaximumSize(QSize(16777215, 45))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.buttonBox = QDialogButtonBox(self.widget_2)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(markerPresetWindow)

        QMetaObject.connectSlotsByName(markerPresetWindow)
    # setupUi

    def retranslateUi(self, markerPresetWindow):
        markerPresetWindow.setWindowTitle(QCoreApplication.translate("markerPresetWindow", u"markerPresetWindow", None))
        self.lineEditColor.setText("")
        self.pushButtonColorPick.setText("")
        self.pushButtonChgMrk.setText("")
        #self.pushButtonDelMrk.setText("")
    # retranslateUi

