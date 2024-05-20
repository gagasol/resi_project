# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pickMarkerWindow.ui'
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
import rc_icons



class Ui_PickMarker(object):
    def setupUi(self, PickMarker):
        if not PickMarker.objectName():
            PickMarker.setObjectName(u"PickMarker")
        PickMarker.resize(100, 100)
        PickMarker.setMinimumSize(QSize(100, 0))
        PickMarker.setMaximumSize(QSize(100, 300))
        PickMarker.setWindowOpacity(0.85)
        PickMarker.setStyleSheet(""" 
            QLabel{margin:2px; 
            border-radius: 2px;}
            """)
        self.verticalLayout = QVBoxLayout(PickMarker)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(PickMarker)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 100, 80))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.widget = QWidget(PickMarker)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.pushButtonOpenPresets = QPushButton(self.widget)
        self.pushButtonOpenPresets.setObjectName(u"pushButtonOpenPresets")
        self.pushButtonOpenPresets.setMinimumSize(QSize(0, 25))
        self.pushButtonOpenPresets.setMaximumSize(QSize(60, 25))

        self.horizontalLayout.addWidget(self.pushButtonOpenPresets)

        self.pushButtonClose = QPushButton(self.widget)
        self.pushButtonClose.setObjectName(u"pushButtonClose")
        self.pushButtonClose.setMinimumSize(QSize(25, 25))
        self.pushButtonClose.setMaximumSize(QSize(25, 25))
        icon = QIcon()
        icon.addFile(u":/icons/icons/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonClose.setIcon(icon)
        self.pushButtonClose.setIconSize(QSize(25, 25))
        self.pushButtonClose.setStyleSheet(u"QPushButton{\n"
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

        self.horizontalLayout.addWidget(self.pushButtonClose)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(PickMarker)

        QMetaObject.connectSlotsByName(PickMarker)
    # setupUi

    def retranslateUi(self, PickMarker):
        PickMarker.setWindowTitle(QCoreApplication.translate("PickMarker", u"PickMarker", None))
        self.pushButtonOpenPresets.setText(QCoreApplication.translate("PickMarker", u"Presets...", None))
        self.pushButtonClose.setText("")
    # retranslateUi

