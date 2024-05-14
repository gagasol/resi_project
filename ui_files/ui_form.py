# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_SelectMarkerWindow(object):
    def setupUi(self, SelectMarkerWindow):
        if not SelectMarkerWindow.objectName():
            SelectMarkerWindow.setObjectName(u"SelectMarkerWindow")
        SelectMarkerWindow.resize(400, 600)
        self.verticalLayout = QVBoxLayout(SelectMarkerWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(SelectMarkerWindow)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 392, 81))
        self.scrollAreaWidgetContents.setStyleSheet(u"QComboBox QAbstractItemView {\n"
"  border: 1px solid grey;\n"
"  background: white;\n"
"  selection-background-color: blue;\n"
"color: black;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacerslcMrkWnd = QSpacerItem(20, 483, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacerslcMrkWnd)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.widget = QWidget(SelectMarkerWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 40))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(509, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonAddPreset = QPushButton(self.widget)
        self.pushButtonAddPreset.setObjectName(u"pushButtonAddPreset")

        self.horizontalLayout.addWidget(self.pushButtonAddPreset)

        self.pushButtonChangePreset = QPushButton(self.widget)
        self.pushButtonChangePreset.setObjectName(u"pushButtonChangePreset")

        self.horizontalLayout.addWidget(self.pushButtonChangePreset)

        self.pushButtonCancel = QPushButton(self.widget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(SelectMarkerWindow)

        QMetaObject.connectSlotsByName(SelectMarkerWindow)
    # setupUi

    def retranslateUi(self, SelectMarkerWindow):
        SelectMarkerWindow.setWindowTitle(QCoreApplication.translate("SelectMarkerWindow", u"SelectMarkerWindow", None))
        self.pushButtonAddPreset.setText(QCoreApplication.translate("SelectMarkerWindow", u"Add Preset", None))
        self.pushButtonChangePreset.setText(QCoreApplication.translate("SelectMarkerWindow", u"Change Preset", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("SelectMarkerWindow", u"Cancel", None))
    # retranslateUi

