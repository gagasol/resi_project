# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QMainWindow, QMdiArea, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTabWidget,
    QVBoxLayout, QWidget)
import rc_icons

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1277, 626)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frameTop = QFrame(self.centralwidget)
        self.frameTop.setObjectName(u"frameTop")
        self.frameTop.setMinimumSize(QSize(0, 35))
        self.frameTop.setMaximumSize(QSize(16777215, 40))
        self.frameTop.setStyleSheet(u"QPushButton{\n"
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
        self.frameTop.setFrameShape(QFrame.StyledPanel)
        self.frameTop.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frameTop)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonOpen = QPushButton(self.frameTop)
        self.pushButtonOpen.setObjectName(u"pushButtonOpen")
        self.pushButtonOpen.setMinimumSize(QSize(30, 30))
        self.pushButtonOpen.setMaximumSize(QSize(30, 30))
        icon = QIcon()
        icon.addFile(u":/icons/icons/folder-open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonOpen.setIcon(icon)
        self.pushButtonOpen.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonOpen)

        self.pushButtonSave = QPushButton(self.frameTop)
        self.pushButtonSave.setObjectName(u"pushButtonSave")
        self.pushButtonSave.setMinimumSize(QSize(30, 30))
        self.pushButtonSave.setMaximumSize(QSize(30, 30))
        self.pushButtonSave.setCursor(QCursor(Qt.ArrowCursor))
        self.pushButtonSave.setAutoFillBackground(False)
        self.pushButtonSave.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/new/saveIcon/icons/floppy-disk.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile(u":/new/saveIcon/icons/floppy-disk-back.svg", QSize(), QIcon.Normal, QIcon.On)
        icon1.addFile(u":/new/saveIcon/icons/floppy-disk-back.svg", QSize(), QIcon.Active, QIcon.On)
        icon1.addFile(u":/new/saveIcon/icons/floppy-disk-back.svg", QSize(), QIcon.Selected, QIcon.Off)
        icon1.addFile(u":/new/saveIcon/icons/floppy-disk-back.svg", QSize(), QIcon.Selected, QIcon.On)
        self.pushButtonSave.setIcon(icon1)
        self.pushButtonSave.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonSave)

        self.pushButtonPdf = QPushButton(self.frameTop)
        self.pushButtonPdf.setObjectName(u"pushButtonPdf")
        self.pushButtonPdf.setMinimumSize(QSize(30, 30))
        self.pushButtonPdf.setMaximumSize(QSize(30, 30))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/file-pdf.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonPdf.setIcon(icon2)
        self.pushButtonPdf.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonPdf)

        self.pushButtonTabView = QPushButton(self.frameTop)
        self.pushButtonTabView.setObjectName(u"pushButtonTabView")
        self.pushButtonTabView.setMinimumSize(QSize(30, 30))
        self.pushButtonTabView.setMaximumSize(QSize(30, 30))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/tabs.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonTabView.setIcon(icon3)
        self.pushButtonTabView.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonTabView)

        self.pushButtonWindowView = QPushButton(self.frameTop)
        self.pushButtonWindowView.setObjectName(u"pushButtonWindowView")
        self.pushButtonWindowView.setMinimumSize(QSize(30, 30))
        self.pushButtonWindowView.setMaximumSize(QSize(30, 30))
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/cards-three.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonWindowView.setIcon(icon4)
        self.pushButtonWindowView.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonWindowView)

        self.pushButtonSettings = QPushButton(self.frameTop)
        self.pushButtonSettings.setObjectName(u"pushButtonSettings")
        self.pushButtonSettings.setMinimumSize(QSize(30, 30))
        self.pushButtonSettings.setMaximumSize(QSize(30, 30))
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/gear-six.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonSettings.setIcon(icon5)
        self.pushButtonSettings.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonSettings)

        self.horizontalSpacer = QSpacerItem(1020, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.checkBoxVLine = QCheckBox(self.frameTop)
        self.checkBoxVLine.setObjectName(u"checkBoxVLine")

        self.horizontalLayout.addWidget(self.checkBoxVLine)


        self.verticalLayout.addWidget(self.frameTop)

        self.frameBottom = QFrame(self.centralwidget)
        self.frameBottom.setObjectName(u"frameBottom")
        self.frameBottom.setFrameShape(QFrame.StyledPanel)
        self.frameBottom.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frameBottom)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidgetWorkArea = QStackedWidget(self.frameBottom)
        self.stackedWidgetWorkArea.setObjectName(u"stackedWidgetWorkArea")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_2 = QHBoxLayout(self.page)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.page)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMovable(True)

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.stackedWidgetWorkArea.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_3 = QHBoxLayout(self.page_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.mdiArea = QMdiArea(self.page_2)
        self.mdiArea.setObjectName(u"mdiArea")

        self.horizontalLayout_3.addWidget(self.mdiArea)

        self.stackedWidgetWorkArea.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidgetWorkArea, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frameBottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidgetWorkArea.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButtonOpen.setText("")
        self.pushButtonSave.setText("")
        self.pushButtonPdf.setText("")
        self.pushButtonTabView.setText("")
        self.pushButtonWindowView.setText("")
        self.pushButtonSettings.setText("")
        self.checkBoxVLine.setText("")
    # retranslateUi

