# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
    QStackedWidget, QVBoxLayout, QWidget)
import rc_icons

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
        self.widget_2.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_2.setStyleSheet(u"QPushButton{\n"
"text-align: bottom left; \n"
"background: none; \n"
"border: 0px solid black; \n"
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
        self.pushButtonGraph.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButtonGraph.setCheckable(False)

        self.verticalLayout_2.addWidget(self.pushButtonGraph)

        self.pushButtonPref = QPushButton(self.widget_2)
        self.pushButtonPref.setObjectName(u"pushButtonPref")
        self.pushButtonPref.setFont(font)
        self.pushButtonPref.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.pushButtonPresets.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.stackedWidget.addWidget(self.page_3)
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
        self.widget_6 = QWidget(self.scrollAreaWidgetContents)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

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


        self.verticalLayout_4.addWidget(self.widget_6)

        self.widget_7 = QWidget(self.scrollAreaWidgetContents)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.widget_7)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit = QLineEdit(self.widget_7)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.pushButtonColor_0 = QPushButton(self.widget_7)
        self.pushButtonColor_0.setObjectName(u"pushButtonColor_0")
        icon = QIcon()
        icon.addFile(u":/icons/icons/palette.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonColor_0.setIcon(icon)
        self.pushButtonColor_0.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.pushButtonColor_0)

        self.label_4 = QLabel(self.widget_7)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.lineEdit_2 = QLineEdit(self.widget_7)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.pushButtonColor_1 = QPushButton(self.widget_7)
        self.pushButtonColor_1.setObjectName(u"pushButtonColor_1")
        icon = QIcon()
        icon.addFile(u":/icons/icons/palette.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonColor_1.setIcon(icon)
        self.pushButtonColor_1.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.pushButtonColor_1)


        self.verticalLayout_4.addWidget(self.widget_7)

        self.widget_5 = QWidget(self.scrollAreaWidgetContents)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(303, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.label_5 = QLabel(self.widget_5)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.lineEdit_3 = QLineEdit(self.widget_5)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_4.addWidget(self.lineEdit_3)

        self.pushButtonColor_2 = QPushButton(self.widget_5)
        self.pushButtonColor_2.setObjectName(u"pushButtonColor_2")
        icon = QIcon()
        icon.addFile(u":/icons/icons/palette.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonColor_2.setIcon(icon)
        self.pushButtonColor_2.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.pushButtonColor_2)


        self.verticalLayout_4.addWidget(self.widget_5)

        self.widget_4 = QWidget(self.scrollAreaWidgetContents)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(226, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.label_6 = QLabel(self.widget_4)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.lineEdit_4 = QLineEdit(self.widget_4)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMaximumSize(QSize(55, 16777215))
        self.lineEdit_4.setFrame(True)

        self.horizontalLayout_5.addWidget(self.lineEdit_4)

        self.pushButtonColor_3 = QPushButton(self.widget_4)
        self.pushButtonColor_3.setObjectName(u"pushButtonColor_3")
        icon = QIcon()
        icon.addFile(u":/icons/icons/palette.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonColor_3.setIcon(icon)
        self.pushButtonColor_3.setIconSize(QSize(24, 24))

        self.horizontalLayout_5.addWidget(self.pushButtonColor_3)


        self.verticalLayout_4.addWidget(self.widget_4)

        self.widget_3 = QWidget(self.scrollAreaWidgetContents)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(293, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.doubleSpinBox = QDoubleSpinBox(self.widget_3)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")

        self.horizontalLayout_6.addWidget(self.doubleSpinBox)


        self.verticalLayout_4.addWidget(self.widget_3)

        self.widget_8 = QWidget(self.scrollAreaWidgetContents)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_5 = QSpacerItem(240, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.label_2 = QLabel(self.widget_8)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.widget_8)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")

        self.horizontalLayout_7.addWidget(self.doubleSpinBox_2)


        self.verticalLayout_4.addWidget(self.widget_8)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.pageGraphSettings)
        self.pagePrefSettings = QWidget()
        self.pagePrefSettings.setObjectName(u"pagePrefSettings")
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
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.pushButtonPresets.setDefault(False)
        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButtonGraph.setText(QCoreApplication.translate("Dialog", u"Graph", None))
        self.pushButtonPref.setText(QCoreApplication.translate("Dialog", u"Preferences", None))
        self.pushButtonPresets.setText(QCoreApplication.translate("Dialog", u"Presets", None))
        self.labelTopPerc.setText(QCoreApplication.translate("Dialog", u"Size of top Table", None))
        self.labelGraphPerc.setText(QCoreApplication.translate("Dialog", u"Size of Graph", None))
        self.labelBotPerc.setText(QCoreApplication.translate("Dialog", u"Size of bot Table", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Feed color", None))
        self.pushButtonColor_0.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Drill color", None))
        self.pushButtonColor_1.setText("")
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Graph background color", None))
        self.pushButtonColor_2.setText("")
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Graph background color while marking", None))
        self.lineEdit_4.setText("")
        self.pushButtonColor_3.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Marker height (% of total height)", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Marker detection height (% of total height)", None))
    # retranslateUi

