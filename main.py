# This Python file uses the following encoding: utf-8
import json
import logging
import os
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, QRect, QSize, QObject
from PySide6.QtGui import QIcon, QCursor, QAction, QGuiApplication
from PySide6.QtWidgets import QApplication, QFileDialog, QMdiArea, QMdiSubWindow, \
    QMessageBox, QDialog, QHBoxLayout, QVBoxLayout, QCheckBox, QGroupBox, QDialogButtonBox, QWidget

from markerpresetwindow import MarkerPresetWindow
from pickMarkerWindow import PickMarker
from printWindow import PrintWindow
from settingsWindow import SettingsWindow
from ui_files.ui_mainwindow import Ui_MainWindow
from widgetGraph import WidgetGraph


class CustomQMdiArea(QMdiArea):
    def tileSubWindowsH(self):
        if len(self.subWindowList()) == 0:
            return

        position = QPoint(0, 0)
        windowWidth = self.width() // 3
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
        self.tileSubWindowsV()
        print(f"New size: {self.size()}")
        super().resizeEvent(event)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Initializes the MainWindow class.

        :return: None
        """
        super(MainWindow, self).__init__()
        self.markerWindow = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.ui.tabWidget.tabCloseRequested.connect(self.closeTab)

        file_handler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

        file_handler.setFormatter(formatter)

        # add file handler to logger
        self.logger.addHandler(file_handler)

        matplotlib_logger = logging.getLogger('matplotlib')
        matplotlib_logger.setLevel(logging.WARNING)

        # testing area @todo TBD!!!

        self.test_file_path = "C:/Users/Heisenberg/Documents/Programming/Python/resi_project/resi/resiProject/Ka_Adl2M001.rgp"

        # variable setup

        self.pickMarkerWin = None
        self.markerPresetWin = None
        self.settingsWindow = None
        # @todo IMPORTANT make the nameToColorDict into a real thing!
        self.listGraphWidgets = []
        self.nameToColorDict = {}
        self.listNameKeys = []
        self.markerPresetList = []
        self.nameOfFile = ''

        self.defaultMarkerDictName = ""

        # @todo delete later
        self.nameToColorDict = {
            "Red": "#FF0000",
            "Blue": "#0000FF",
            "Yellow": "#FFFF00",
            "Black": "#000000",
            "White": "#FFFFFF",
            "Aloof": "#7B68EE",
            "Cherish": "#FFB6C1",
            "Divine": "#FFA07A",
            "Elapse": "#8B0000",
            "Green": "#00FF00",
            "Coral": "#FF7F50",
            "Cyan": "#00FFFF",
            "Chocolate": "#D2691E",
            "Crimson": "#DC143C"
        }
        print('115 executed in main.py')
        self.loadPreset()
        try:
            self.lastDirectory = self.settingsWindow.getSettingsVariable('defaultFolderPath')
        except AttributeError as e:
            self.lastDirectory = '.'

        self.loadOpenMenu()
        print('118 executed in main.py')

        self.listNameKeys = ["idNumber", "date"]

        # flags
        self.flagWindowClosedByUserSignal = False
        # endregion

        # button events
        # clicked events
        self.ui.pushButtonOpen.clicked.connect(self.openButtonClicked)
        self.ui.pushButtonSave.clicked.connect(self.saveButtonClicked)
        self.ui.actionSaveAs.triggered.connect(self.showSaveFileDialog)
        self.ui.actionSaveAll.triggered.connect(self.saveAllOpenTabs)
        self.ui.pushButtonTabView.clicked.connect(self.tabButtonClicked)
        self.ui.pushButtonWindowView.clicked.connect(self.windowButtonClicked)
        self.ui.pushButtonPdf.clicked.connect(self.pdfButtonClicked)
        self.ui.pushButtonPrint.clicked.connect(self.printButtonClicked)
        self.ui.pushButtonToggleOverlay.clicked.connect(self.toggleOverlayButtonClicked)
        self.ui.pushButtonPng.clicked.connect(self.pngButtonClicked)
        self.ui.pushButtonSettings.clicked.connect(self.settingsButtonClicked)
        self.ui.actionOpenDefaultFolder.triggered.connect(self.openDefaultFolderDialog)
        self.ui.actionOpenAllInFolder.triggered.connect(self.openAllRifInFolder)
        self.ui.actionOpenAllRGPInFolder.triggered.connect(self.openAllRGPInFolder)
        self.ui.pushButtonApplyDataTable.clicked.connect(self.applyDataToMultiple)

    #TDL!!!!

    #self.openButtonClicked(self.test_file_path)

    # functionality for QPushButtons

    # functionality for the pushButtonOpen QPushButton
    # @todo add multiple file input
    # @todo get rid of the fileName argument befeore release
    def openButtonClicked(self, pathToFile=None):

        if not pathToFile:
            pathToFiles = QFileDialog.getOpenFileNames(None, 'Select Files', self.lastDirectory,
                                                       '*.rgp * .rif;;*.rgp;;*.rif')

            for pathToFile in pathToFiles[0]:
                print(pathToFile)
                if 'rif' or 'rgp' in pathToFile:
                    self.lastDirectory = '/'.join(pathToFile.split('/')[:-1])

                self.openNewFile(pathToFile)
        '''
        self.logger.info("~~~~~~~~~~~~ openButtonClicked ~~~~~~~~~~~~")
        if not pathToFile:
            pathToFile, _ = QFileDialog.getOpenFileName(None, "Select File", self.lastDirectory,
                                                        "*.rgp *.rif;;*.rgp;;*.rif")
            if pathToFile and 'rif' or 'rgp' in pathToFile:
                self.lastDirectory = '/'.join(pathToFile.split('/')[:-1])

        self.logger.info("filename :{0}".format(pathToFile))
        if pathToFile == "":
            return
            
        if ".rif" in fileName:
            if fileName not in self.settingsWindow.getSettingsVariable('recentFiles'):
                self.settingsWindow.addRecentFile(fileName)
            try:
                with open(fileName, "r") as file:
                    loadedState = json.load(file)

                logging.info(" canvas :{0}".format(loadedState))
                widget = WidgetGraph(self, fileName, loadedState)
                self.listGraphWidgets.append(widget)
                self.ui.tabWidget.addTab(widget, self.nameOfFile)
                self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

            except FileNotFoundError:
                print('File not found')
                self.settingsWindow.removeRecentFile(fileName)



        elif ".project" in fileName:
            with open(fileName, "r") as file:
                loadedState = json.load(file)

            for canvas in loadedState:
                print("loadedState len > 1")
                logging.info(" canvas :{0}".format(canvas))
                widget = WidgetGraph(self, "",  canvas)
                self.listGraphWidgets.append(widget)
                self.ui.tabWidget.addTab(widget, self.nameOfFile)

        else:
            widget = WidgetGraph(self, fileName)
            print(fileName)
            self.listGraphWidgets.append(widget)
            self.ui.tabWidget.addTab(widget, self.nameOfFile+".rgp")

            self.ui.tabWidget.setCurrentIndex(len(self.listGraphWidgets) - 1)
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

        pathName = '/'.join(fileName[0:-1].split('/')[0:-1])
        if pathName not in self.settingsWindow.getSettingsVariable('recentFolders'):
            self.settingsWindow.addRecentFolder(pathName)

        self.loadOpenMenu()'''

        #self.ui.tabWidget.addTab(widget, widget.name)

    def openNewFile(self, pathToFile):

        filename = pathToFile.split('/')[-1]

        nameOfFile, suffix = filename.rsplit('.', 1)

        print(f' pathToFile: {pathToFile}\n filename: {filename}\n suffix: {suffix}')

        if suffix == "rif":
            if pathToFile not in self.settingsWindow.getSettingsVariable('recentFiles'):
                self.settingsWindow.addRecentFile(pathToFile)
                print(f'YAHZI!: {pathToFile}')
            try:
                with open(pathToFile, "r") as file:
                    loadedState = json.load(file)

                logging.info(" canvas :{0}".format(loadedState))
                widget = WidgetGraph(self, pathToFile, loadedState)
                self.listGraphWidgets.append(widget)
                self.ui.tabWidget.addTab(widget, nameOfFile)
                self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

            except FileNotFoundError:
                print('File not found')
                self.settingsWindow.removeRecentFile(pathToFile)



        elif suffix == 'project':
            with open(pathToFile, "r") as file:
                loadedState = json.load(file)

            for canvas in loadedState:
                print("loadedState len > 1")
                logging.info(" canvas :{0}".format(canvas))
                widget = WidgetGraph(self, "", canvas)
                self.listGraphWidgets.append(widget)
                self.ui.tabWidget.addTab(widget, nameOfFile)

        else:
            widget = WidgetGraph(self, pathToFile)
            self.listGraphWidgets.append(widget)
            self.ui.tabWidget.addTab(widget, nameOfFile + ".rgp")

            self.ui.tabWidget.setCurrentIndex(len(self.listGraphWidgets) - 1)
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

        pathToFileFolder = '/'.join(pathToFile[0:-1].split('/')[0:-1])
        if pathToFileFolder not in self.settingsWindow.getSettingsVariable('recentFolders'):
            self.settingsWindow.addRecentFolder(pathToFileFolder)

        self.loadOpenMenu()

    def openActionClicked(self):
        action = self.sender()
        filePath = action.data()
        if '.rif' in filePath:
            print('Rif detected opening file')
            self.openNewFile(filePath)
        else:
            pathToFiles = QFileDialog.getOpenFileNames(None, 'Select Files', self.lastDirectory,
                                                       '*.rgp * .rif;;*.rgp;;*.rif')

            for pathToFile in pathToFiles[0]:
                print(pathToFile)
                if 'rif' or 'rgp' in pathToFile:
                    self.lastDirectory = '/'.join(pathToFile.split('/')[:-1])

                self.openNewFile(pathToFile)

    def openDefaultFolderDialog(self):
        folderPath = self.settingsWindow.getSettingsVariable('defaultFolderPath')
        pathToFiles = QFileDialog.getOpenFileNames(None, 'Select Files', folderPath,
                                                   '*.rgp * .rif;;*.rgp;;*.rif')

        for pathToFile in pathToFiles[0]:
            print(pathToFile)
            if 'rif' or 'rgp' in pathToFile:
                self.lastDirectory = '/'.join(pathToFile.split('/')[:-1])

            self.openNewFile(pathToFile)

    def openAllRifInFolder(self):
        folderPath = QFileDialog.getExistingDirectory(None, 'Select Folder')
        for dirPath, dirNames, fileNames in os.walk(folderPath):
            for fileName in fileNames:
                filepath = os.path.join(dirPath, fileName)
                if '.rif' in filepath:
                    self.openNewFile(filepath)

    def openAllRGPInFolder(self):
        folderPath = QFileDialog.getExistingDirectory(None, 'Select Folder')
        for dirPath, dirNames, fileNames in os.walk(folderPath):
            for fileName in fileNames:
                filepath = os.path.join(dirPath, fileName)
                if '.rgp' in filepath:
                    self.openNewFile(filepath)

    def addEntriesToOpenMenu(self, names: list[str], paths: list[str]):
        """
        This function adds new QAction entries to the 'open' menu of the application GUI.
        Each QAction entry corresponds to a recent file, with a name from the 'names' list and a path
        from the 'paths' list.

        Args:
            names (list[str]): List of names of recent files to add to 'open' menu.
            paths (list[str]): List of full paths for each of the recent files.
        """
        openMenu = self.ui.menuOpenButton
        openMenu.insertSeparator(openMenu.actions()[0])

        for i in range(len(names)):
            name = names[i]
            path = paths[i]
            tooltip = paths[i]
            actionOpenRecentFile = QAction(name)
            actionOpenRecentFile.setData(path)
            actionOpenRecentFile.triggered.connect(self.openActionClicked)
            actionOpenRecentFile.setToolTip(tooltip)

            actionAtIndexZero = openMenu.actions()[0]
            openMenu.insertAction(actionAtIndexZero, actionOpenRecentFile)

    def loadOpenMenu(self):
        """
        initialize the context menu for the open button

        Parameters:
        None

        Return:
        None

        Notes:
            shows recent files, recent folders, default folder and an option to open all files in a folder
        """
        openMenu = self.ui.menuOpenButton
        staticMenuActions = 2
        seperatorCount = 2

        filepaths = self.settingsWindow.getSettingsVariable('recentFiles')
        filenames = [path.split('/')[-1] for path in filepaths]

        folderPaths = self.settingsWindow.getSettingsVariable('recentFolders')
        folderNames = []
        for folderPath in folderPaths:
            pathArr = folderPath.split('/')
            lenFolderName = 4 if len(folderPath) > 4 else len(pathArr)
            folderName = '...' + '/'.join(pathArr[-lenFolderName:])
            folderNames.append(folderName)

        for i in range(len(openMenu.actions()) - 3, -1, -1):
            action = openMenu.actions()[i]
            openMenu.removeAction(action)

        self.addEntriesToOpenMenu(folderNames, folderPaths)
        self.addEntriesToOpenMenu(filenames, filepaths)

    # functionality for the pushButtonSave QPushButton
    def saveButtonClicked(self):
        tabWidget = self.ui.tabWidget
        currentIndex = tabWidget.currentIndex()

        if ".rgp" in tabWidget.tabText(currentIndex):
            tabWidget.setTabText(currentIndex, tabWidget.tabText(currentIndex).split(".rgp")[0])

        graphWidget = tabWidget.widget(currentIndex)

        self.saveGraphState(graphWidget)
        print("saveButtonClicked")

    def saveAllOpenTabs(self):
        tabWidget = self.ui.tabWidget

        for i in range(tabWidget.count()):
            if ".rgp" in tabWidget.tabText(i):
                tabWidget.setTabText(i, tabWidget.tabText(i).split(".rgp")[0])
            graphWidget = tabWidget.widget(i)
            self.saveGraphState(graphWidget)


    def showSaveFileDialog(self):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        defaultName = graphWidget.name + ".rif"
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",
                                                  defaultName, "All Files (*);;Text Files (*.txt)", options=options)

        fileName = fileName if ".rif" in fileName else fileName + ".rif"

        if fileName:
            defaultFilePath = '/'.join(fileName.split('/')[:-1])
            print(f'defaultFilePath in main: {defaultFilePath}')
            graphWidget.dataModel.fileDefaultSavePath = defaultFilePath
            self.saveGraphState(graphWidget, fileName)

    # @todo change this
    def saveGraphState(self, graphWidget, path=""):
        """
        this method saves the current state of the graphWidget
        Args:
            graphWidget (WidgetGraph): the widgetGraph to save
            path (str): non mandatory variable for a different path to save the file, else it'll be the file default

        Returns:

        """
        if graphWidget:
            if path == "":
                if graphWidget.dataModel.fileDefaultSavePath == '':
                    path = self.settingsWindow.getSettingsVariable('defaultFolderPath')
                else:
                    path = graphWidget.dataModel.fileDefaultSavePath
                print(f'path in saveGraphState: {path}')
                print(f'filename in saveGraphState: {graphWidget.name}')
                with open(path + '/' + graphWidget.name + ".rif", "w") as file:
                    json.dump(graphWidget.getCurrentState(), file)
                    graphWidget.canvasGraph.canvasSaved()
            else:
                with open(path, "w") as file:
                    json.dump(graphWidget.getCurrentState(), file)
                    graphWidget.canvasGraph.canvasSaved()
        else:
            for widget in self.listGraphWidgets:
                path = self.settingsWindow.getSettingsVariable('defaultFolderPath')
                with open(path + '/' + graphWidget.name + ".rif", "w") as file:
                    json.dump(widget.getCurrentState(), file)
                    graphWidget.canvasGraph.canvasSaved()

    # functionality for the pushButtonTabView QPushButton
    def tabButtonClicked(self):
        if self.ui.stackedWidgetWorkArea.currentIndex() != 0:
            for graphWidget in self.listGraphWidgets:
                graphWidget.setParent(None)
                self.ui.mdiArea.closeAllSubWindows()
                self.ui.tabWidget.addTab(graphWidget, graphWidget.name)

        self.ui.stackedWidgetWorkArea.setCurrentIndex(0)

    def closeTab(self, index):
        """
        this method checks if the user wants to save a tab before it gets closed by the user
        Args:
            index:

        Returns:

        """
        tabWidget = self.ui.tabWidget.widget(index)
        needsSaving = tabWidget.canvasGraph.canvasNeedsSave()
        if needsSaving:
            reply = QMessageBox.question(self, QObject.tr("Confirm close"), QObject.tr("Save before you close?"),
                                         QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                if tabWidget is not None:
                    with open(tabWidget.name + ".rif", "w") as file:
                        json.dump(tabWidget.getCurrentState(), file)
                    tabWidget.deleteLater()
                    self.listGraphWidgets.remove(tabWidget)
                self.ui.tabWidget.removeTab(index)

            elif reply == QMessageBox.No:
                if tabWidget is not None:
                    tabWidget.deleteLater()
                    self.listGraphWidgets.remove(tabWidget)
                self.ui.tabWidget.removeTab(index)

            return

        if tabWidget is not None:
            tabWidget.deleteLater()
            self.listGraphWidgets.remove(tabWidget)
            self.ui.tabWidget.removeTab(index)

    # functionality for the pushButtonWindowView QPushButton
    def windowButtonClicked(self):
        QMessageBox.warning(self, "Under construction", "This function is still under construction")
        return

        if (self.ui.stackedWidgetWorkArea.currentIndex() != 1):
            for graphWidget in self.listGraphWidgets:
                self.ui.tabWidget.clear()
                subwindow = QMdiSubWindow()
                widget = graphWidget
                widget.setParent(None)
                subwindow.setWidget(widget)
                subwindow.show()
                widget.show()
                self.ui.mdiArea.addSubWindow(widget)

        self.ui.stackedWidgetWorkArea.setCurrentIndex(1)
        self.ui.mdiArea.tileSubWindows()

    def pdfButtonClicked(self):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        filename = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        PrintWindow([graphWidget], self.settingsWindow).quickExportAs(graphWidget, 'pdf', filename)


        '''
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        filename = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        PrintWindow(graphWidget, self.settingsWindow, 'pdf', filename)
        '''
    def pngButtonClicked(self):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        filename = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        PrintWindow([graphWidget], self.settingsWindow, ).quickExportAs(graphWidget, 'png', filename)

    def printButtonClicked(self):
        printWindow = PrintWindow(self.listGraphWidgets, self.settingsWindow)
        printWindow.exec()


    def settingsButtonClicked(self):
        self.markerPresetWin = MarkerPresetWindow(self, self.nameToColorDict, self.markerPresetList,
                                                  calledByGraph=False)
        if self.settingsWindow.exec():
            for canvas in self.listGraphWidgets:
                canvas.updateUi()
            with open("./settings/settings.json", "w") as file:
                json.dump(self.settingsWindow.defaultSettingsDict, file, indent=2)

    def toggleOverlayButtonClicked(self):
        """
        this method is called when the toggleOverlayButton is clicked and shows or hides the overlay menu
        Returns:

        """
        # If overlay_widget visible, hide it, else show it
        if self.ui.widgetOverlay.isVisible():
            self.ui.widgetOverlay.hide()
            self.ui.horizontalSpacerManual1.changeSize(0, 17)
            icon_in = QIcon()
            icon_in.addFile(u":/icons/icons/text-outdent.svg", QSize(), QIcon.Normal, QIcon.On)
            self.ui.pushButtonToggleOverlay.setIcon(icon_in)
            self.ui.pushButtonToggleOverlay.setIconSize(QSize(25, 25))
        else:
            self.ui.widgetOverlay.show()
            spacerWidth = self.ui.widgetOverlay.width() - self.ui.pushButtonToggleOverlay.width()
            self.ui.horizontalSpacerManual1.changeSize(spacerWidth, 17)
            icon_in = QIcon()
            icon_in.addFile(u":/icons/icons/text-indent.svg", QSize(), QIcon.Normal, QIcon.On)
            self.ui.pushButtonToggleOverlay.setIcon(icon_in)
            self.ui.pushButtonToggleOverlay.setIconSize(QSize(25, 25))

    def applyDataToMultiple(self):
        """
        This method creates a dialog with checkboxes from which the user can select data that he wants to apply
        to multiple opened files
        Returns:
            None
        """
        currentWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())

        fileNames = {widget.name: widget for widget in self.listGraphWidgets if widget is not currentWidget}
        customData = {
            "idNumber": QObject.tr('ID-Nummer'),
            "0_diameter": QObject.tr('Durchmesser'),
            "1_mHeight": QObject.tr('Messhöhe'),
            "2_mDirection": QObject.tr('Messrichtung'),
            "3_objecttype": QObject.tr('Objektart'),
            "4_location": QObject.tr('Standort'),
            "5_name": QObject.tr('Name')
        }

        dialog = QDialog(self)

        boxWidget = QWidget(dialog)
        boxLayout = QHBoxLayout(boxWidget)

        nameGroupBoxes = QGroupBox('Open files')
        dataGroupBoxes = QGroupBox('Data')

        vLayout = QVBoxLayout(dialog)
        vLayoutNames = QVBoxLayout(nameGroupBoxes)
        vLayoutData = QVBoxLayout(dataGroupBoxes)

        checkboxesNames = []
        checkboxesData = []

        for name, widget in fileNames.items():
            checkboxName = QCheckBox(name, boxWidget)
            checkboxesNames.append(checkboxName)
            vLayoutNames.addWidget(checkboxName)
        nameGroupBoxes.setLayout(vLayoutNames)

        for var, data in customData.items():
            checkboxData = QCheckBox(data, boxWidget)
            checkboxData.setObjectName(var)
            checkboxesData.append(checkboxData)
            vLayoutData.addWidget(checkboxData)
        dataGroupBoxes.setLayout(vLayoutData)

        boxLayout.addWidget(dataGroupBoxes)
        boxLayout.addWidget(nameGroupBoxes)
        boxWidget.setLayout(boxLayout)

        vLayout.addWidget(boxWidget)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        vLayout.addWidget(buttonBox)

        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        dialog.setLayout(vLayout)
        dialog.show()

        result = dialog.exec()

        if result == QDialog.Accepted:
            selectedNames = [cb.text() for cb in checkboxesNames if cb.isChecked()]
            selectedData = [cb.objectName() for cb in checkboxesData if cb.isChecked()]

            for name in selectedNames:
                for data in selectedData:
                    if '_' in data:
                        entry = currentWidget.dataModel.getDataByKey(data)
                        row = int(data.split("_")[0])
                        print(f'entry: {entry}; row: {row}')
                        fileNames[name].changeTableTopEntry(row, 5, entry)
                    else:
                        entry = currentWidget.dataModel.getDataByKey(data)
                        row = 1
                        fileNames[name].changeTableTopEntry(row, 1, entry)

    def updateGraphWidgets(self):
        for graph in self.listGraphWidgets:
            graph.canvasGraph.repaintGrid()

    def openPickMarker(self, defaultPresetName):
        """
        this method shows the PickMarker dialog from which the user can pick a name and color for a marker and
        returns the name and color of a marker if the user clicks on the entry
        Args:
            defaultPresetName: the preset of markers to be shown in the dialog

        Returns:
            None if any error occurs, else the name and color of the picked marker

        Notes:
            - if the dictionary isn't available it will use the default dic and print an error message

        """
        if not self.markerPresetList:
            QMessageBox.warning(self, QObject.tr("Warning"), QObject.tr("No preset available"))
            return None, None
        defaultDict = None

        for presetDict in self.markerPresetList:
            if defaultPresetName in presetDict.values():
                defaultDict = presetDict
                break
        if defaultDict is None:
            for presetDict in self.markerPresetList:
                if self.defaultMarkerDictName in presetDict.values():
                    defaultDict = presetDict
            QMessageBox.warning(self, QObject.tr("Warning"),
                                QObject.tr(f"Preset {defaultPresetName} not found, changing to default"))

        self.pickMarkerWin = PickMarker(self, defaultDict)
        self.overridePickMarkerDict(defaultDict)

        # check if the dialog would be at the edge of the screen and compensates accordingly
        mousePos = QCursor.pos()
        screen = QGuiApplication.screenAt(mousePos)

        if screen is None:  # In case the mouse is not on any screen (shouldn't usually happen)
            screen = QGuiApplication.primaryScreen()

        screenGeometry = screen.geometry()

        localMousePos = mousePos - screenGeometry.topLeft()

        moveX = max(0, min(localMousePos.x(), screenGeometry.width() - self.pickMarkerWin.width()))
        moveY = max(0, min(localMousePos.y(), screenGeometry.height() - self.pickMarkerWin.height()))

        movePos = screenGeometry.topLeft() + QPoint(moveX, moveY)

        self.pickMarkerWin.move(movePos)

        if self.pickMarkerWin.exec():
            return self.pickMarkerWin.markerName, self.pickMarkerWin.markerColor
        else:
            return None, None

    def overridePickMarkerDict(self, markerDict=None, name="", col=""):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        if name != "":
            self.pickMarkerWin.markerName = name
            self.pickMarkerWin.markerColor = col
            self.pickMarkerWin.accept()
            self.pickMarkerWin.close()
        elif markerDict is not None:
            graphWidget.changeFileDefaultPresetName(markerDict["_NameForPreset"])
            self.pickMarkerWin.markerDict = markerDict
            self.pickMarkerWin.loadMarkerDict(markerDict)
            self.pickMarkerWin.accept()
            self.pickMarkerWin.close()
        else:
            graphWidget.changeFileDefaultPresetName(self.defaultMarkerDictName)

    def getGraphDefaultMarkerDictName(self):
        """
        This method returns the default marker dictionary name of the currently selected widgetGraph
        Returns:
            current index graphWidgtet default marker name
        """
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        return graphWidget.defaultMarkerDictName

    def openChangeMarkerPreset(self, defaultPresetName=None):
        """
        executes and shows a MarkerPresetWindow
        Args:
            defaultPresetName:

        Returns:

        """
        markerPresetWin = MarkerPresetWindow(self, self.nameToColorDict, self.markerPresetList)
        if markerPresetWin.exec():
            for markerDict in self.markerPresetList:
                if defaultPresetName in markerDict.values():
                    return markerDict
        else:
            return None

    def loadPreset(self):
        """
        This method loads preset settings from the settings.json file.

        This method initializes a SettingsWindow object with saved or default settings. It also handles missing keys in
        the loaded settings by filling with default values, and prompts for a settings reset if required. The method also
        loads marker presets from the markerPresets.json file if they exist.

        If settings.json or markerPresets.json is not found, it handles these exceptions and initializes with default values
        or shows a message accordingly.

        Note: Strings to show in graph are hard-coded into this method.

        Args:
            None.

        Returns:
            None. The method updates the settingsWindow, defaultMarkerDictName, nameToColorDict, and markerPresetList
            attributes of the instance.
        """
        strsToShowInGraph = ["number", "0_diameter", "1_mHeight", "3_objecttype", "5_name"]
        settingsDict = {"defaultMarkerDictName": "",
                        "heightWidgetTopPerc": 15,
                        "heightWidgetGraphPerc": 75,
                        "heightWidgetBottomPerc": 10,
                        "colorBackground": "#dfe5e6",
                        "colorBackgroundMarking": "#8b888f",
                        "labelFontSize": 12,
                        "printLabelFontSize": 26,
                        'colorLabel': '#000000',
                        "minorTicksInterval": 5,
                        "fontSize": 14,
                        "fontName": "Arial",
                        "colorFeedPlot": "#5c08c9",
                        "colorDrillPlot": "#eda31a",
                        "markerHeightPerc": 0.02,
                        "printHeightWidgetTopPerc": 20,
                        "printHeightWidgetGraphPerc": 60,
                        "printHeightWidgetBottomPerc": 20,
                        "printFontSize": 20,
                        "printFontName": "Arial",
                        "strsToShowInGraph": strsToShowInGraph,
                        "gridColor": '#000000',
                        'gridOpacity': 100,
                        'defaultGridIntervalX': 5,
                        'defaultGridIntervalY': 5,
                        'defaultFolderPath': './data/',
                        'recentFiles': [],
                        'recentFilesAmount': 2,
                        'recentFolders': [],
                        'recentFoldersAmount': 2
                        }
        try:
            with open("./settings/settings.json", "r") as file:
                loadedFile = json.load(file)
                keysDefault = set(settingsDict)
                keysLoaded = set(loadedFile[0])
                for key in keysDefault - keysLoaded:
                    loadedFile[0][key] = settingsDict[key]
                self.settingsWindow = SettingsWindow(loadedFile[0], mainWindow=self)
                self.defaultMarkerDictName = self.settingsWindow.getSettingsVariable("defaultMarkerDictName")
                self.nameToColorDict = loadedFile[1]
        except FileNotFoundError:

            self.settingsWindow = SettingsWindow(settingsDict, mainWindow=self)
            self.defaultMarkerDictName = self.settingsWindow.getSettingsVariable("defaultMarkerDictName")
            print("First startup detected")

        except KeyError as ke:
            if str(ke) in settingsDict:
                response = QMessageBox.question(self, 'Reset Settings', f'{str(ke)} was not found in settings.json,'
                                                                        f'do you want to reset the file?',
                                                QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    print('yes')
                    self.settingsWindow = SettingsWindow(settingsDict, mainWindow=self)
                elif response == QMessageBox.No:
                    print('no')

        try:
            with open('./settings/markerPresets.json', 'r') as file:
                self.markerPresetList = json.load(file)

        except FileNotFoundError:
            print('No presets file found')

    def savePreset(self):
        with open('./settings/markerPresets.json', 'w') as file:
            json.dump(self.markerPresetList, file, indent=2)

    def closeEvent(self, event):
        if self.defaultMarkerDictName is not None:
            saveData = [self.settingsWindow.defaultSettingsDict, self.nameToColorDict]
        else:
            saveData = [self.settingsWindow.defaultSettingsDict, self.nameToColorDict]
        with open("./settings/settings.json", "w") as f:
            json.dump(saveData, f, indent=2)

    # algorithms

    # TDL functions I use for things


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

# todo Linux zeigt keiine Schrift außer im Hover -> setColorText black
# todo name von preset statt Pick Marker
# todo save each file on its own
# todo keep marking after one click
# todo toggle marking active on key input
# todo change pick system to a List of labels in the current default preset
# todo table data change row with tab not column
# todo set certain ifnormation as constant in table data
# todo icons add a down arrow for overriding the options
# todo show marking area while marking
# todo give option to show markers behind graph
# todo add project option
