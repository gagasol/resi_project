# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
                               QHBoxLayout, QLabel, QLineEdit, QRadioButton,
                               QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
                               QVBoxLayout, QWidget, QCheckBox, QComboBox)

class Ui_printWindow(object):
    def setupUi(self, printWindow):
        if not printWindow.objectName():
            printWindow.setObjectName(u"printWindow")
        printWindow.resize(668, 600)

        self.checkedNameCount = 0
        self.checkedBoxes = []
        #######################
        self.verticalLayout_7 = QVBoxLayout(printWindow)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget = QWidget(printWindow)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widgetLayout = QWidget(self.widget)
        self.widgetLayout.setObjectName(u"widgetLayout")
        self.verticalLayout_3 = QVBoxLayout(self.widgetLayout)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.widgetLayout)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.lineEditPrintName = QLineEdit(self.widgetLayout)
        self.lineEditPrintName.setObjectName(u"lineEditPrintName")

        self.verticalLayout_3.addWidget(self.lineEditPrintName)

        self.scrollAreaLayout = QScrollArea(self.widgetLayout)
        self.scrollAreaLayout.setObjectName(u"scrollAreaLayout")
        self.scrollAreaLayout.setMaximumSize(QSize(16777215, 100))
        self.scrollAreaLayout.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 293, 68))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioButtonPresetsPlaceholder = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButtonPresetsPlaceholder.setObjectName(u"radioButtonPresetsPlaceholder")

        self.verticalLayout.addWidget(self.radioButtonPresetsPlaceholder)

        self.verticalSpacer = QSpacerItem(20, 129, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollAreaLayout.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollAreaLayout)

        self.widgetPageOrientation = QWidget(self.widgetLayout)
        self.widgetPageOrientation.setObjectName(u"widgetPageOrientation")
        self.verticalLayout_4 = QVBoxLayout(self.widgetPageOrientation)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.comboBoxSuffix = QComboBox(self.widgetPageOrientation)
        self.comboBoxSuffix.setObjectName(u"comboBoxSuffix")
        self.comboBoxSuffix.setMaximumSize(QSize(80, 16777215))
        self.comboBoxSuffix.currentIndexChanged.connect(self.onComboBoxSuffixChanged)

        self.verticalLayout_4.addWidget(self.comboBoxSuffix)

        ### dimensions

        self.widget_4 = QWidget(self.widgetPageOrientation)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_5 = QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_5.addWidget(self.label_3)

        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 5, -1, 3)
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.lineEditDimWidth = QLineEdit(self.widget_5)
        self.lineEditDimWidth.setObjectName(u"lineEditDimWidth")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditDimWidth.sizePolicy().hasHeightForWidth())
        self.lineEditDimWidth.setSizePolicy(sizePolicy)
        self.lineEditDimWidth.setMaximumSize(QSize(50, 16777215))
        self.lineEditDimWidth.setLayoutDirection(Qt.LeftToRight)
        self.lineEditDimWidth.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.lineEditDimWidth)

        self.verticalLayout_5.addWidget(self.widget_5)

        self.widget_41 = QWidget(self.widgetPageOrientation)
        self.widget_41.setObjectName(u"widget_41")
        self.verticalLayout_51 = QVBoxLayout(self.widget_41)
        self.verticalLayout_51.setSpacing(0)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalLayout_51.setContentsMargins(0, -1, -1, -1)

        self.label_2 = QLabel(self.widget_41)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_51.addWidget(self.label_2)

        self.comboBoxPageOrient = QComboBox(self.widget_41)
        self.comboBoxPageOrient.setObjectName(u"comboBoxPageOrient")
        self.comboBoxPageOrient.setMaximumSize(QSize(80, 16777215))

        self.verticalLayout_51.addWidget(self.comboBoxPageOrient)

        self.verticalLayout_4.addWidget(self.widget_41)

        self.widget_6 = QWidget(self.widget_4)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.label_5 = QLabel(self.widget_6)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.lineEditDimHeight = QLineEdit(self.widget_6)
        self.lineEditDimHeight.setObjectName(u"lineEditDimHeight")
        self.lineEditDimHeight.setMaximumSize(QSize(50, 16777215))
        self.lineEditDimHeight.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.lineEditDimHeight)

        self.verticalLayout_5.addWidget(self.widget_6)

        self.verticalLayout_4.addWidget(self.widget_4)

        self.widget_7 = QWidget(self.widgetPageOrientation)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_6 = QVBoxLayout(self.widget_7)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.label_6 = QLabel(self.widget_7)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_6.addWidget(self.label_6)

        self.widget_8 = QWidget(self.widget_7)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 5, -1, 3)
        self.label_7 = QLabel(self.widget_8)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.spinBoxRowTotal = QSpinBox(self.widget_8)
        self.spinBoxRowTotal.setObjectName(u"spinBoxRowTotal")
        self.spinBoxRowTotal.setMaximumSize(QSize(40, 16777215))
        self.spinBoxRowTotal.setMinimum(1)

        self.horizontalLayout_7.addWidget(self.spinBoxRowTotal)

        self.verticalLayout_6.addWidget(self.widget_8)

        self.widget_9 = QWidget(self.widget_7)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.label_8 = QLabel(self.widget_9)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_8.addWidget(self.label_8)

        self.spinBoxColumnTotal = QSpinBox(self.widget_9)
        self.spinBoxColumnTotal.setObjectName(u"spinBoxColumnTotal")
        self.spinBoxColumnTotal.setMaximumSize(QSize(40, 16777215))
        self.spinBoxColumnTotal.setMinimum(1)

        self.horizontalLayout_8.addWidget(self.spinBoxColumnTotal)

        self.verticalLayout_6.addWidget(self.widget_9)

        self.verticalLayout_4.addWidget(self.widget_7)

        self.checkBoxShowTop = QCheckBox(self.widgetPageOrientation)
        self.checkBoxShowTop.setObjectName(u"checkBoxShowTop")
        self.checkBoxShowTop.setChecked(True)

        self.verticalLayout_4.addWidget(self.checkBoxShowTop)

        self.checkBoxShowBottom = QCheckBox(self.widgetPageOrientation)
        self.checkBoxShowBottom.setObjectName(u"checkBoxShowBottom")
        self.checkBoxShowBottom.setChecked(True)

        self.verticalLayout_4.addWidget(self.checkBoxShowBottom)

        self.checkBoxShowData = QCheckBox(self.widgetPageOrientation)
        self.checkBoxShowData.setObjectName(u"checkBoxShowData")

        self.verticalLayout_4.addWidget(self.checkBoxShowData)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.verticalLayout_3.addWidget(self.widgetPageOrientation)

        self.horizontalLayout.addWidget(self.widgetLayout)

        self.scrollAreaGraphNames = QScrollArea(self.widget)
        self.scrollAreaGraphNames.setObjectName(u"scrollAreaGraphNames")
        self.scrollAreaGraphNames.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 311, 532))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollAreaGraphNames.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout.addWidget(self.scrollAreaGraphNames)

        self.verticalLayout_7.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(printWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Abort | QDialogButtonBox.Save)

        self.verticalLayout_7.addWidget(self.buttonBox)

        self.retranslateUi(printWindow)
        ####################################
        self.comboBoxSuffix.addItems(['pdf', 'png'])
        self.comboBoxPageOrient.addItems(['horizontal', 'vertical'])
        # list of all checkboxes that handle if a specific widget is shown or hidden
        self.showHideCheckBoxGroup = [self.checkBoxShowTop, self.checkBoxShowBottom, self.checkBoxShowData]
        self.fileNameDic = {}

        QMetaObject.connectSlotsByName(printWindow)
    # setupUi

    def retranslateUi(self, printWindow):
        printWindow.setWindowTitle(QCoreApplication.translate("printWindow", u"printWindow", None))
        self.label.setText(QCoreApplication.translate("printWindow", u"Filename:", None))
        self.radioButtonPresetsPlaceholder.setText(QCoreApplication.translate("printWindow", u"RadioButton", None))
        self.comboBoxSuffix.setPlaceholderText("")
        self.label_3.setText(QCoreApplication.translate("printWindow", u"Dimensions", None))
        self.label_4.setText(QCoreApplication.translate("printWindow", u"Width", None))
        self.lineEditDimWidth.setText(QCoreApplication.translate("printWindow", u"1920", None))
        self.label_5.setText(QCoreApplication.translate("printWindow", u"Height", None))
        self.lineEditDimHeight.setText(QCoreApplication.translate("printWindow", u"1080", None))
        self.label_6.setText(QCoreApplication.translate("printWindow", u"TextLabel", None))
        self.label_7.setText(QCoreApplication.translate("printWindow", u"Rows", None))
        self.label_8.setText(QCoreApplication.translate("printWindow", u"Columns", None))
        self.label_2.setText(QCoreApplication.translate("printWindow", u"Page Orientation", None))
        self.comboBoxPageOrient.setPlaceholderText("")
        self.checkBoxShowTop.setText(QCoreApplication.translate("printWindow", u"Show top", None))
        self.checkBoxShowBottom.setText(QCoreApplication.translate("printWindow", u"Show bottom", None))
        self.checkBoxShowData.setText(QCoreApplication.translate("printWindow", u"Show data in graph", None))

    # retranslateUi




    def createNameList(self, names: list[str]):
        for name in names:
            widgetNamesPlaceholder = QWidget(self.scrollAreaWidgetContents_2)
            widgetNamesPlaceholder.setObjectName(u"widgetNamesPlaceholder")
            horizontalLayout_2 = QHBoxLayout(widgetNamesPlaceholder)
            horizontalLayout_2.setObjectName(u"horizontalLayout_2")
            widget_2 = QWidget(widgetNamesPlaceholder)
            widget_2.setObjectName(u"widget_2")
            horizontalLayout_3 = QHBoxLayout(widget_2)
            horizontalLayout_3.setObjectName(u"horizontalLayout_3")
            checkBox = QCheckBox(widget_2)
            checkBox.setText(name)
            checkBox.stateChanged.connect(self.createCheckStateFunction(checkBox))
            checkBox.setMinimumSize(QSize(125, 0))

            horizontalLayout_3.addWidget(checkBox)

            horizontalLayout_2.addWidget(widget_2)
            widget_3 = QWidget(widgetNamesPlaceholder)
            widget_3.setObjectName(u"widget_3")
            horizontalLayout_4 = QHBoxLayout(widget_3)
            horizontalLayout_4.setObjectName(u"horizontalLayout_4")
            label = QLabel(widget_3)
            label.setObjectName(u"label")

            horizontalLayout_4.addWidget(label)

            lineEdit = QLineEdit(widget_3)
            lineEdit.setObjectName(u"lineEdit")
            lineEdit.setMinimumSize(QSize(25, 0))
            lineEdit.setMaximumSize(QSize(25, 16777215))

            horizontalLayout_4.addWidget(lineEdit)

            horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

            horizontalLayout_4.addItem(horizontalSpacer)

            horizontalLayout_2.addWidget(widget_3)

            self.verticalLayout_2.addWidget(widgetNamesPlaceholder)

        verticalSpacer_2 = QSpacerItem(20, 493, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(verticalSpacer_2)

    def createCheckStateFunction(self, checkBox):
        return lambda: self.checkBoxStateChanged(checkBox)
    def checkBoxStateChanged(self, checkbox):
        state = checkbox.checkState()
        parentWidget = checkbox.parent().parent()

        lineEdit = None

        for i in range(parentWidget.layout().count()):
            widget = parentWidget.layout().itemAt(i).widget()
            if isinstance(widget, QWidget):
                for j in range(widget.layout().count()):
                    childWidget = widget.layout().itemAt(j).widget()
                    if isinstance(childWidget, QLineEdit):
                        lineEdit = childWidget
                        break

        if lineEdit is None:
            return

        if state == Qt.Checked:
            self.checkedNameCount += 1
            lineEdit.setText(str(self.checkedNameCount))
            checkbox.setObjectName(str(self.checkedNameCount))
            self.addRifName(checkbox.text())
            self.checkedBoxes.append(checkbox)
        elif state == Qt.Unchecked:
            self.checkedNameCount -= 1
            lineEdit.setText('')
            checkbox.setObjectName('')
            self.removeRifName(checkbox.text())
            self.checkedBoxes.remove(checkbox)

    def addRifName(self, name):
        currentName = self.lineEditPrintName.text()
        projectName, projectNumber = name.rsplit('M', 1)

        if projectName in self.fileNameDic.keys():
            if projectNumber not in self.fileNameDic[projectName]:
                self.fileNameDic[projectName].append(projectNumber)
        else:
            self.fileNameDic.update({projectName: [projectNumber]})

        newName = ''
        for name in self.fileNameDic.keys():
            newName += name + '('
            for number in self.fileNameDic[name]:
                newName += str(number) + ','
            newName = newName[:-1]
            newName += ')-'

        newName = newName[:-1]

        if projectName not in currentName:
            if currentName:
                currentName += '-' + projectName
            else:
                currentName = projectName

        self.lineEditPrintName.setText(newName)

    def removeRifName(self, name):
        currentName = self.lineEditPrintName.text()
        projectName, projectNumber = name.rsplit('M', 1)
        currentProjectNames = currentName.split('-')

        for currentProject in currentProjectNames:
            if projectName in currentProject:
                if len(self.fileNameDic[projectName]) > 1:
                    if self.fileNameDic[projectName][0] == projectNumber:
                        currentName = currentName.replace(projectNumber + ',', '')
                    else:
                        currentName = currentName.replace(',' + projectNumber, '')
                    self.fileNameDic[projectName].remove(projectNumber)
                else:
                    currentName = currentName.replace(projectNumber, '')
                    currentName = currentName.replace(projectName + '()', '')
                    self.fileNameDic.pop(projectName)

        self.lineEditPrintName.setText(currentName)

        if projectName in currentName:

            if projectNumber in currentName:
                currentName = currentName.replace(projectNumber, '')


    def onComboBoxSuffixChanged(self):
        suffix = self.comboBoxSuffix.currentText()
        if 'pdf' in suffix:
            self.widget_4.hide()
            self.widget_41.show()
        else:
            self.widget_4.show()
            self.widget_41.hide()
