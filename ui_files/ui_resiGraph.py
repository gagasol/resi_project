# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resiGraph.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QListWidget,
    QListWidgetItem, QSizePolicy, QSpacerItem, QTableView,
    QTextEdit, QVBoxLayout, QWidget)

from main import MplCanvas


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(993, 642)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widgetTop = QWidget(Form)
        self.widgetTop.setObjectName(u"widgetTop")
        self.widgetTop.setMaximumSize(QSize(16777215, 90))
        self.horizontalLayout = QHBoxLayout(self.widgetTop)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableView = QTableView(self.widgetTop)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setShowGrid(False)
        self.tableView.setGridStyle(Qt.DashLine)
        self.tableView.horizontalHeader().setVisible(False)
        self.tableView.verticalHeader().setVisible(False)

        self.horizontalLayout.addWidget(self.tableView)

        self.horizontalSpacer = QSpacerItem(472, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.widgetTop)

        self.widgetGraph = MplCanvas(self, width=6, height=4, dpi=100)

        self.widgetGraph.setObjectName(u"widgetGraph")

        self.verticalLayout_2.addWidget(self.widgetGraph)

        self.widgetBottom = QWidget(Form)
        self.widgetBottom.setObjectName(u"widgetBottom")
        self.widgetBottom.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout_2 = QHBoxLayout(self.widgetBottom)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listWidgetAnalysis = QListWidget(self.widgetBottom)
        self.listWidgetAnalysis.setObjectName(u"listWidgetAnalysis")

        self.horizontalLayout_2.addWidget(self.listWidgetAnalysis)

        self.horizontalSpacer_2 = QSpacerItem(369, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.textEditComment = QTextEdit(self.widgetBottom)
        self.textEditComment.setObjectName(u"textEditComment")
        self.textEditComment.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_2.addWidget(self.textEditComment)


        self.verticalLayout_2.addWidget(self.widgetBottom)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

