# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsWindow.ui'
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
                               QDoubleSpinBox, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
                               QStackedWidget, QVBoxLayout, QWidget, QSpinBox)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(784, 552)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.widget_2.setStyleSheet(u"QPushButton{\n"
"text-align: bottom left; \n"
"background: none; \n"
"border: 1px solid black; \n"
"border-radius: 2px;\n"
"}\n"
"QPushButton:hover {\n"
"border: 1px solid lightblue;\n"
"background-color: lightblue;\n"
"}\n"
"QPushButton:focus {\n"
"background-color: lightblue;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButtonGraph = QPushButton(self.widget_2)
        self.pushButtonGraph.setObjectName(u"pushButtonGraph")
        font = QFont()
        font.setPointSize(11)
        self.pushButtonGraph.setFont(font)
        self.pushButtonGraph.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButtonGraph.setCheckable(False)

        self.verticalLayout_2.addWidget(self.pushButtonGraph)

        self.pushButtonPref = QPushButton(self.widget_2)
        self.pushButtonPref.setObjectName(u"pushButtonPref")
        self.pushButtonPref.setFont(font)
        self.pushButtonPref.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButtonPref.setCheckable(False)

        self.verticalLayout_2.addWidget(self.pushButtonPref)

        self.pushButtonPrint = QPushButton(self.widget_2)
        self.pushButtonPrint.setObjectName(u"pushButtonPrint")
        self.pushButtonPrint.setFont(font)
        self.pushButtonPrint.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.pushButtonPrint)

        self.pushButtonPresets = QPushButton(self.widget_2)
        self.pushButtonPresets.setObjectName(u"pushButtonPresets")
        self.pushButtonPresets.setFont(font)
        self.pushButtonPresets.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButtonPresets.setCheckable(False)
        self.pushButtonPresets.setFlat(False)

        self.verticalLayout_2.addWidget(self.pushButtonPresets)

        self.verticalSpacer = QSpacerItem(20, 381, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget_2)

        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(80)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.stackedWidget.setStyleSheet(u"QPushButton{\n"
"border: none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: white;\n"
"}\n"
"\n"
"QPushButton:background-color{\n"
"background-color:rgb(138, 20, 255);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #FFFFFF, stop: 1 #dadbde);\n"
"}")
        self.pagePrintSettings = QWidget()
        self.pagePrintSettings.setObjectName(u"pagePrintSettings")
        self.verticalLayout_7 = QVBoxLayout(self.pagePrintSettings)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.scrollArea_3 = QScrollArea(self.pagePrintSettings)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 574, 466))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_11 = QWidget(self.scrollAreaWidgetContents_3)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.labelTopPerc_2 = QLabel(self.widget_11)
        self.labelTopPerc_2.setObjectName(u"labelTopPerc_2")

        self.horizontalLayout_8.addWidget(self.labelTopPerc_2)

        self.doubleSpinBoxTopPerc_2 = QDoubleSpinBox(self.widget_11)
        self.doubleSpinBoxTopPerc_2.setObjectName(u"doubleSpinBoxTopPerc_2")
        self.doubleSpinBoxTopPerc_2.setMaximumSize(QSize(60, 16777215))
        self.doubleSpinBoxTopPerc_2.setDecimals(1)

        self.horizontalLayout_8.addWidget(self.doubleSpinBoxTopPerc_2)

        self.labelGraphPerc_2 = QLabel(self.widget_11)
        self.labelGraphPerc_2.setObjectName(u"labelGraphPerc_2")

        self.horizontalLayout_8.addWidget(self.labelGraphPerc_2)

        self.doubleSpinBoxGraphPerc_2 = QDoubleSpinBox(self.widget_11)
        self.doubleSpinBoxGraphPerc_2.setObjectName(u"doubleSpinBoxGraphPerc_2")
        self.doubleSpinBoxGraphPerc_2.setMaximumSize(QSize(60, 16777215))
        self.doubleSpinBoxGraphPerc_2.setDecimals(1)

        self.horizontalLayout_8.addWidget(self.doubleSpinBoxGraphPerc_2)

        self.labelBotPerc_2 = QLabel(self.widget_11)
        self.labelBotPerc_2.setObjectName(u"labelBotPerc_2")

        self.horizontalLayout_8.addWidget(self.labelBotPerc_2)

        self.doubleSpinBoxBotPerc_2 = QDoubleSpinBox(self.widget_11)
        self.doubleSpinBoxBotPerc_2.setObjectName(u"doubleSpinBoxBotPerc_2")
        self.doubleSpinBoxBotPerc_2.setMaximumSize(QSize(60, 16777215))
        self.doubleSpinBoxBotPerc_2.setDecimals(1)

        self.horizontalLayout_8.addWidget(self.doubleSpinBoxBotPerc_2)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)


        self.verticalLayout_8.addWidget(self.widget_11)

        self.widget_10 = QWidget(self.scrollAreaWidgetContents_3)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_11 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label = QLabel(self.widget_10)
        self.label.setObjectName(u"label")

        self.horizontalLayout_11.addWidget(self.label)

        self.lineEditPrintLabelSize = QLineEdit(self.widget_10)
        self.lineEditPrintLabelSize.setObjectName(u"lineEditPrintLabelSize")
        self.lineEditPrintLabelSize.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_11.addWidget(self.lineEditPrintLabelSize)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_9)


        self.verticalLayout_8.addWidget(self.widget_10)

        self.widget_12 = QWidget(self.scrollAreaWidgetContents_3)
        self.widget_12.setObjectName(u"widget_12")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_2 = QLabel(self.widget_12)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_10.addWidget(self.label_2)

        self.lineEditTableFontSize = QLineEdit(self.widget_12)
        self.lineEditTableFontSize.setObjectName(u"lineEditTableFontSize")
        self.lineEditTableFontSize.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_10.addWidget(self.lineEditTableFontSize)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_10)


        self.verticalLayout_8.addWidget(self.widget_12)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_4)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_7.addWidget(self.scrollArea_3)

        self.stackedWidget.addWidget(self.pagePrintSettings)
        self.pageGraphSettings = QWidget()
        self.pageGraphSettings.setObjectName(u"pageGraphSettings")
        self.verticalLayout_5 = QVBoxLayout(self.pageGraphSettings)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.scrollArea = QScrollArea(self.pageGraphSettings)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 574, 466))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_7 = QWidget(self.scrollAreaWidgetContents)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelFeedColor = QLabel(self.widget_7)
        self.labelFeedColor.setObjectName(u"labelFeedColor")

        self.horizontalLayout_3.addWidget(self.labelFeedColor)

        self.lineEditFeedColor = QLineEdit(self.widget_7)
        self.lineEditFeedColor.setObjectName(u"lineEditFeedColor")
        self.lineEditFeedColor.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEditFeedColor)

        self.pushButtonColor_0 = QPushButton(self.widget_7)
        self.pushButtonColor_0.setObjectName(u"pushButtonColor_0")

        self.horizontalLayout_3.addWidget(self.pushButtonColor_0)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addWidget(self.widget_7)

        self.widget_8 = QWidget(self.scrollAreaWidgetContents)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.labelDrillColor = QLabel(self.widget_8)
        self.labelDrillColor.setObjectName(u"labelDrillColor")

        self.horizontalLayout_9.addWidget(self.labelDrillColor)

        self.lineEditDrillColor = QLineEdit(self.widget_8)
        self.lineEditDrillColor.setObjectName(u"lineEditDrillColor")
        self.lineEditDrillColor.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_9.addWidget(self.lineEditDrillColor)

        self.pushButtonColor_1 = QPushButton(self.widget_8)
        self.pushButtonColor_1.setObjectName(u"pushButtonColor_1")

        self.horizontalLayout_9.addWidget(self.pushButtonColor_1)

        self.horizontalSpacer_5 = QSpacerItem(416, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)


        self.verticalLayout_4.addWidget(self.widget_8)

        self.widget_5 = QWidget(self.scrollAreaWidgetContents)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelGraphBackground = QLabel(self.widget_5)
        self.labelGraphBackground.setObjectName(u"labelGraphBackground")

        self.horizontalLayout_4.addWidget(self.labelGraphBackground)

        self.lineEditGraphBackgroundColor = QLineEdit(self.widget_5)
        self.lineEditGraphBackgroundColor.setObjectName(u"lineEditGraphBackgroundColor")
        self.lineEditGraphBackgroundColor.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_4.addWidget(self.lineEditGraphBackgroundColor)

        self.pushButtonColor_2 = QPushButton(self.widget_5)
        self.pushButtonColor_2.setObjectName(u"pushButtonColor_2")

        self.horizontalLayout_4.addWidget(self.pushButtonColor_2)

        self.horizontalSpacer_2 = QSpacerItem(303, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addWidget(self.widget_5)

        self.widget_4 = QWidget(self.scrollAreaWidgetContents)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelMarkingGraphBackground = QLabel(self.widget_4)
        self.labelMarkingGraphBackground.setObjectName(u"labelMarkingGraphBackground")

        self.horizontalLayout_5.addWidget(self.labelMarkingGraphBackground)

        self.lineEditMarkingGraphBackgroundColor = QLineEdit(self.widget_4)
        self.lineEditMarkingGraphBackgroundColor.setObjectName(u"lineEditMarkingGraphBackgroundColor")
        self.lineEditMarkingGraphBackgroundColor.setMaximumSize(QSize(55, 16777215))
        self.lineEditMarkingGraphBackgroundColor.setFrame(True)

        self.horizontalLayout_5.addWidget(self.lineEditMarkingGraphBackgroundColor)

        self.pushButtonColor_3 = QPushButton(self.widget_4)
        self.pushButtonColor_3.setObjectName(u"pushButtonColor_3")

        self.horizontalLayout_5.addWidget(self.pushButtonColor_3)

        self.horizontalSpacer_3 = QSpacerItem(226, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addWidget(self.widget_4)

        self.widget_3 = QWidget(self.scrollAreaWidgetContents)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelMarkerHeight = QLabel(self.widget_3)
        self.labelMarkerHeight.setObjectName(u"labelMarkerHeight")

        self.horizontalLayout_6.addWidget(self.labelMarkerHeight)

        self.doubleSpinBoxMarkerHeight = QDoubleSpinBox(self.widget_3)
        self.doubleSpinBoxMarkerHeight.setObjectName(u"doubleSpinBoxMarkerHeight")

        self.horizontalLayout_6.addWidget(self.doubleSpinBoxMarkerHeight)

        self.horizontalSpacer_4 = QSpacerItem(293, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.verticalLayout_4.addWidget(self.widget_3)

        self.widget_9 = QWidget(self.scrollAreaWidgetContents)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelLabelSize = QLabel(self.widget_9)
        self.labelLabelSize.setObjectName(u"labelLabelSize")

        self.horizontalLayout_7.addWidget(self.labelLabelSize)

        self.spinBoxLabelSize = QSpinBox(self.widget_9)
        self.spinBoxLabelSize.setObjectName(u"spinBoxLabelSize")

        self.horizontalLayout_7.addWidget(self.spinBoxLabelSize)

        self.labelLabelColor = QLabel(self.widget_9)
        self.labelLabelColor.setObjectName(u"labelLabelColor")

        self.horizontalLayout_7.addWidget(self.labelLabelColor)

        self.lineEditLabelColor = QLineEdit(self.widget_9)
        self.lineEditLabelColor.setObjectName(u"lineEditLabelColor")
        self.lineEditLabelColor.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_7.addWidget(self.lineEditLabelColor)

        self.pushButtonColor_4 = QPushButton(self.widget_9)
        self.pushButtonColor_4.setObjectName(u"pushButtonColor_4")

        self.horizontalLayout_7.addWidget(self.pushButtonColor_4)

        self.horizontalSpacer_7 = QSpacerItem(268, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.verticalLayout_4.addWidget(self.widget_9)

        self.widget_13 = QWidget(self.scrollAreaWidgetContents)
        self.widget_13.setObjectName(u"widget_13")
        self.horizontalLayout_11 = QHBoxLayout(self.widget_13)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.pushButtonGraphdisplayData = QPushButton(self.widget_13)
        self.pushButtonGraphdisplayData.setObjectName(u"pushButtonGraphdisplayData")

        self.pushButtonGraphdisplayData.setText(u"Graphdisplay Data")

        self.horizontalLayout_11.addWidget(self.pushButtonGraphdisplayData)

        self.horizontalSpace_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpace_11)

        self.verticalLayout_4.addWidget(self.widget_13)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.pageGraphSettings)
        self.pagePrefSettings = QWidget()
        self.pagePrefSettings.setObjectName(u"pagePrefSettings")
        self.verticalLayout_3 = QVBoxLayout(self.pagePrefSettings)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea_2 = QScrollArea(self.pagePrefSettings)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 574, 466))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget_6 = QWidget(self.scrollAreaWidgetContents_2)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelTopPerc = QLabel(self.widget_6)
        self.labelTopPerc.setObjectName(u"labelTopPerc")

        self.horizontalLayout_2.addWidget(self.labelTopPerc)

        self.doubleSpinBoxTopPerc = QDoubleSpinBox(self.widget_6)
        self.doubleSpinBoxTopPerc.setObjectName(u"doubleSpinBoxTopPerc")
        self.doubleSpinBoxTopPerc.setMaximumSize(QSize(60, 16777215))
        self.doubleSpinBoxTopPerc.setDecimals(1)

        self.horizontalLayout_2.addWidget(self.doubleSpinBoxTopPerc)

        self.labelGraphPerc = QLabel(self.widget_6)
        self.labelGraphPerc.setObjectName(u"labelGraphPerc")

        self.horizontalLayout_2.addWidget(self.labelGraphPerc)

        self.doubleSpinBoxGraphPerc = QDoubleSpinBox(self.widget_6)
        self.doubleSpinBoxGraphPerc.setObjectName(u"doubleSpinBoxGraphPerc")
        self.doubleSpinBoxGraphPerc.setMaximumSize(QSize(60, 16777215))
        self.doubleSpinBoxGraphPerc.setDecimals(1)

        self.horizontalLayout_2.addWidget(self.doubleSpinBoxGraphPerc)

        self.labelBotPerc = QLabel(self.widget_6)
        self.labelBotPerc.setObjectName(u"labelBotPerc")

        self.horizontalLayout_2.addWidget(self.labelBotPerc)

        self.doubleSpinBoxBotPerc = QDoubleSpinBox(self.widget_6)
        self.doubleSpinBoxBotPerc.setObjectName(u"doubleSpinBoxBotPerc")
        self.doubleSpinBoxBotPerc.setMaximumSize(QSize(60, 16777215))
        self.doubleSpinBoxBotPerc.setDecimals(1)

        self.horizontalLayout_2.addWidget(self.doubleSpinBoxBotPerc)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout_6.addWidget(self.widget_6)

        self.verticalSpacer_3 = QSpacerItem(20, 397, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_3.addWidget(self.scrollArea_2)

        self.stackedWidget.addWidget(self.pagePrefSettings)
        self.pagePresetSettings = QWidget()
        self.pagePresetSettings.setObjectName(u"pagePresetSettings")
        self.stackedWidget.addWidget(self.pagePresetSettings)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)

        self.pushButtonPresets.setDefault(False)
        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
            Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
            self.pushButtonGraph.setText(QCoreApplication.translate("Dialog", u"Graph", None))
            self.pushButtonPref.setText(QCoreApplication.translate("Dialog", u"Preferences", None))
            self.pushButtonPrint.setText(QCoreApplication.translate("Dialog", u"Print", None))
            self.pushButtonPresets.setText(QCoreApplication.translate("Dialog", u"Presets", None))
            self.labelTopPerc_2.setText(QCoreApplication.translate("Dialog", u"Printsize of top Table", None))
            self.labelGraphPerc_2.setText(QCoreApplication.translate("Dialog", u"Printsize of Graph", None))
            self.labelBotPerc_2.setText(QCoreApplication.translate("Dialog", u"Printsize of bot Table", None))
            self.label.setText(QCoreApplication.translate("Dialog", u"Print labelsize", None))
            self.label_2.setText(QCoreApplication.translate("Dialog", u"Print table font size", None))
            self.labelFeedColor.setText(QCoreApplication.translate("Dialog", u"Feed color", None))
            self.pushButtonColor_0.setText("")
            self.labelDrillColor.setText(QCoreApplication.translate("Dialog", u"Drill color", None))
            self.pushButtonColor_1.setText("")
            self.labelGraphBackground.setText(QCoreApplication.translate("Dialog", u"Graph background color", None))
            self.pushButtonColor_2.setText("")
            self.labelMarkingGraphBackground.setText(
                    QCoreApplication.translate("Dialog", u"Graph background color while marking", None))
            self.lineEditMarkingGraphBackgroundColor.setText("")
            self.pushButtonColor_3.setText("")
            self.labelMarkerHeight.setText(
                    QCoreApplication.translate("Dialog", u"Marker height (% of total height)", None))
            self.labelLabelSize.setText(QCoreApplication.translate("Dialog", u"Label Size", None))
            self.labelLabelColor.setText(QCoreApplication.translate("Dialog", u"Label Color", None))
            self.pushButtonColor_4.setText("")
            self.labelTopPerc.setText(QCoreApplication.translate("Dialog", u"Size of top Table", None))
            self.labelGraphPerc.setText(QCoreApplication.translate("Dialog", u"Size of Graph", None))
            self.labelBotPerc.setText(QCoreApplication.translate("Dialog", u"Size of bot Table", None))
    # retranslateUi
    # retranslateUi

