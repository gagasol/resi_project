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
    QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_markerPresetWindow(object):
    def setupUi(self, markerPresetWindow):
        if not markerPresetWindow.objectName():
            markerPresetWindow.setObjectName(u"markerPresetWindow")
        markerPresetWindow.resize(618, 180)
        self.verticalLayout = QVBoxLayout(markerPresetWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(markerPresetWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(600, 45))
        self.widget.setMaximumSize(QSize(16777215, 25))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox = QComboBox(self.widget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(400, 0))

        self.horizontalLayout.addWidget(self.comboBox)

        self.pushButtonAddMrk = QPushButton(self.widget)
        self.pushButtonAddMrk.setObjectName(u"pushButtonAddMrk")
        self.pushButtonAddMrk.setMinimumSize(QSize(50, 0))
        self.pushButtonAddMrk.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.pushButtonAddMrk)

        self.pushButtonChgMrk = QPushButton(self.widget)
        self.pushButtonChgMrk.setObjectName(u"pushButtonChgMrk")
        self.pushButtonChgMrk.setMinimumSize(QSize(50, 0))
        self.pushButtonChgMrk.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.pushButtonChgMrk)

        self.pushButtonDelMrk = QPushButton(self.widget)
        self.pushButtonDelMrk.setObjectName(u"pushButtonDelMrk")
        self.pushButtonDelMrk.setMinimumSize(QSize(50, 0))
        self.pushButtonDelMrk.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.pushButtonDelMrk)


        self.verticalLayout.addWidget(self.widget)

        self.widget_3 = QWidget(markerPresetWindow)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


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
        self.pushButtonAddMrk.setText("")
        self.pushButtonChgMrk.setText("")
        self.pushButtonDelMrk.setText("")
    # retranslateUi

