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
                               QVBoxLayout, QWidget, QMenu)
import rc_icons


class CustomQMdiArea(QMdiArea):
    def tileSubWindowsH(self):
        if len(self.subWindowList()) == 0:
            return

        position = QPoint(0, 0)
        windowWidth = self.width() // 2
        for window in self.subWindowList():
            rect = QRect(0, 0, self.height(), windowWidth)
            window.setGeometry(rect)
            window.move(position)
            position.setX(position.x() + windowWidth)

    def tileSubWindowsV(self):
        if len(self.subWindowList()) == 0:
            return

        position = QPoint(0, 0)
        windowHeight = self.height() // 3
        for window in self.subWindowList():
            rect = QRect(0, 0, self.width(), windowHeight)
            window.setGeometry(rect)
            window.move(position)
            position.setY(position.y() + windowHeight)

    def resizeEvent(self, event):
        print(f"New size: {self.size()}")
        super().resizeEvent(event)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 902)
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
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.pushButtonOpen = QPushButton(self.frameTop)
        self.pushButtonOpen.setObjectName(u"pushButtonOpen")
        self.pushButtonOpen.setMinimumSize(QSize(30, 30))
        self.pushButtonOpen.setMaximumSize(QSize(30, 30))
        icon = QIcon()
        icon.addFile(u":/icons/icons/folder-open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonOpen.setIcon(icon)
        self.pushButtonOpen.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonOpen)

        self.horizontalSpacer_2 = QSpacerItem(6, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

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

        self.pushButton = QPushButton(self.frameTop)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(20, 25))
        self.pushButton.setMaximumSize(QSize(20, 25))
        self.pushButton.setStyleSheet(u"QPushButton::menu-indicator{ image: none; }")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/keyboard_double_arrow_down_40dp_FILL0_wght400_GRAD0_opsz24.svg", QSize(),
                      QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QSize(15, 25))

        self.menu = QMenu(self.pushButton)

        self.actionSaveAs = self.menu.addAction(QObject.tr('Save as..'))

        self.pushButton.setMenu(self.menu)

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_3 = QSpacerItem(6, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.pushButtonPdf = QPushButton(self.frameTop)
        self.pushButtonPdf.setObjectName(u"pushButtonPdf")
        self.pushButtonPdf.setMinimumSize(QSize(30, 30))
        self.pushButtonPdf.setMaximumSize(QSize(30, 30))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/file-pdf.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonPdf.setIcon(icon3)
        self.pushButtonPdf.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonPdf)

        self.horizontalSpacer_4 = QSpacerItem(6, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.pushButtonPng = QPushButton(self.frameTop)
        self.pushButtonPng.setObjectName(u"pushButtonPng")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/file-png.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonPng.setIcon(icon4)
        self.pushButtonPng.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonPng)

        self.horizontalSpacer_5 = QSpacerItem(6, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.pushButtonTabView = QPushButton(self.frameTop)
        self.pushButtonTabView.setObjectName(u"pushButtonTabView")
        self.pushButtonTabView.setMinimumSize(QSize(30, 30))
        self.pushButtonTabView.setMaximumSize(QSize(30, 30))
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/tabs.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonTabView.setIcon(icon5)
        self.pushButtonTabView.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonTabView)

        self.pushButtonWindowView = QPushButton(self.frameTop)
        self.pushButtonWindowView.setObjectName(u"pushButtonWindowView")
        self.pushButtonWindowView.setMinimumSize(QSize(30, 30))
        self.pushButtonWindowView.setMaximumSize(QSize(30, 30))
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/cards-three.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonWindowView.setIcon(icon6)
        self.pushButtonWindowView.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonWindowView)

        self.horizontalSpacer_6 = QSpacerItem(6, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.pushButtonSettings = QPushButton(self.frameTop)
        self.pushButtonSettings.setObjectName(u"pushButtonSettings")
        self.pushButtonSettings.setMinimumSize(QSize(30, 30))
        self.pushButtonSettings.setMaximumSize(QSize(30, 30))
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/gear-six.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonSettings.setIcon(icon7)
        self.pushButtonSettings.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonSettings)

        self.horizontalSpacer = QSpacerItem(1020, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonToggleOverlay = QPushButton(self.frameTop)
        self.pushButtonToggleOverlay.setObjectName(u"pushButtonToggleOverlay")
        self.pushButtonToggleOverlay.setAutoFillBackground(False)
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/text-outdent.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonToggleOverlay.setIcon(icon6)
        self.pushButtonToggleOverlay.setIconSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButtonToggleOverlay)

        self.horizontalSpacerManual1 = QSpacerItem(0, 17, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacerManual1)

        self.verticalLayout.addWidget(self.frameTop)
        # this is newly edited may not work @todo delete comment if works
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(1)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(3, 3, 3, 3)
        # end
        self.frameBottom = QFrame(self.frame)
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
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.page)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.stackedWidgetWorkArea.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_3 = QHBoxLayout(self.page_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.mdiArea = CustomQMdiArea(self.page_2)
        self.mdiArea.setObjectName(u"mdiArea")

        self.horizontalLayout_3.addWidget(self.mdiArea)

        self.stackedWidgetWorkArea.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidgetWorkArea, 0, 0, 1, 1)

        self.horizontalLayout_4.addWidget(self.frameBottom)

        self.widgetOverlay = QFrame(self.frame)
        self.widgetOverlay.setObjectName(u"widgetOverlay")
        self.widgetOverlay.setMinimumSize(QSize(150, 0))
        self.widgetOverlay.setAutoFillBackground(True)

        self.horizontalLayout_4.addWidget(self.widgetOverlay)
        self.widgetOverlay.hide()
        self.widgetOverlay.raise_()

        self.verticalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidgetWorkArea.setCurrentIndex(0)
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
        self.pushButtonSettings.setText("")#if QT_CONFIG(tooltip)

        self.pushButtonPdf.setToolTip(QCoreApplication.translate("MainWindow", u"save as pdf", None))
        self.pushButtonPng.setToolTip(QCoreApplication.translate("MainWindow", u"save as png", None))
        self.pushButtonWindowView.setToolTip(QCoreApplication.translate("MainWindow", u"show graphs as windows", None))
        self.pushButtonTabView.setToolTip(QCoreApplication.translate("MainWindow", u"show graphs as tabs", None))
        self.pushButtonOpen.setToolTip(QCoreApplication.translate("MainWindow", u"open file", None))
        self.pushButtonSave.setToolTip(QCoreApplication.translate("MainWindow", u"save file", None))
        self.pushButtonSettings.setToolTip(QCoreApplication.translate("MainWindow", u"settings", None))
        self.pushButtonToggleOverlay.setToolTip(QCoreApplication.translate("MainWindow", u"Show/Hide Quick Access", None))
    # retranslateUi

