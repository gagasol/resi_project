# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'markerPresetForm.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialogButtonBox,
    QHBoxLayout, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_markerPresetWindow(object):
    def setupUi(self, markerPresetWindow):
        if not markerPresetWindow.objectName():
            markerPresetWindow.setObjectName(u"markerPresetWindow")
        markerPresetWindow.resize(400, 150)
        self.verticalLayout = QVBoxLayout(markerPresetWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(markerPresetWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(600, 45))
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
        self.comboBox = QComboBox(self.widget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.comboBox)

        self.lineEditName = QLineEdit(self.widget)
        self.lineEditName.setObjectName(u"lineEditName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditName.sizePolicy().hasHeightForWidth())
        self.lineEditName.setSizePolicy(sizePolicy)
        self.lineEditName.setMinimumSize(QSize(60, 0))
        self.lineEditName.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout.addWidget(self.lineEditName)

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

        self.pushButtonDelMrk = QPushButton(self.widget)
        self.pushButtonDelMrk.setObjectName(u"pushButtonDelMrk")
        self.pushButtonDelMrk.setMinimumSize(QSize(25, 0))
        self.pushButtonDelMrk.setMaximumSize(QSize(25, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/minus-square.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonDelMrk.setIcon(icon2)
        self.pushButtonDelMrk.setIconSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.pushButtonDelMrk)


        self.verticalLayout.addWidget(self.widget)

        self.widget_3 = QWidget(markerPresetWindow)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setStyleSheet(u"QLabel{\n"
"	font: 12pt \"NSimSun\";\n"
"	border-style: none outset outset none;\n"
"	border-width: 4px;\n"
"	border-color: black;\n"
"	text-decoration: underline;\n"
"}")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.scrollArea = QScrollArea(self.widget_3)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setMinimumSize(QSize(190, 0))
        self.scrollArea.setMaximumSize(QSize(190, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 168, 48))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 27, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

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
        self.pushButtonDelMrk.setText("")
    # retranslateUi

