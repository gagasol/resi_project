# This Python file uses the following encoding: utf-8
import json
import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, QRect, QSize, QObject
from PySide6.QtGui import QIcon, QCursor, QAction
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
        self.lastDirectory = ''

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
        # TEMPORARY FIX
        '''
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

        with open("./settings/settings.json", "r") as file:
            loadedFile = json.load(file)
            keysDefault = set(settingsDict)
            keysLoaded = set(loadedFile[0])
            for key in keysDefault - keysLoaded:
                loadedFile[0][key] = settingsDict[key]
            self.settingsWindow = SettingsWindow(loadedFile[0], mainWindow=self)
            self.defaultMarkerDictName = self.settingsWindow.getSettingsVariable("defaultMarkerDictName")
            self.nameToColorDict = loadedFile[1]
            self.markerPresetList = loadedFile[2]
            print('581 executed in main.py.loadPreset()')
            
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
                self.markerPresetList = loadedFile[2]
                print('581 executed in main.py.loadPreset()')
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
        '''
        # END TEMPORARY FIX

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
        self.ui.pushButtonTabView.clicked.connect(self.tabButtonClicked)
        self.ui.pushButtonWindowView.clicked.connect(self.windowButtonClicked)
        self.ui.pushButtonPdf.clicked.connect(self.pdfButtonClicked)
        self.ui.pushButtonToggleOverlay.clicked.connect(self.toggleOverlayButtonClicked)
        self.ui.pushButtonPng.clicked.connect(self.pngButtonClicked)
        self.ui.pushButtonSettings.clicked.connect(self.settingsButtonClicked)
        self.ui.actionOpenDefaultFolder.triggered.connect(self.openDefaultFolderDialog)
        self.ui.pushButtonApplyDataTable.clicked.connect(self.applyDataToMultiple)

    #TDL!!!!

        #self.openButtonClicked(self.test_file_path)


    # functionality for QPushButtons

    # functionality for the pushButtonOpen QPushButton
    # @todo add multiple file input
    # @todo get rid of the fileName argument befeore release
    def openButtonClicked(self, fileName=None):
        self.logger.info("~~~~~~~~~~~~ openButtonClicked ~~~~~~~~~~~~")
        if not fileName:
            fileName, _ = QFileDialog.getOpenFileName(None, "Select File", self.lastDirectory,
                                                      "*.rgp *.rif;;*.rgp;;*.rif")
            if fileName:
                self.lastDirectory = '/'.join(fileName.split('/')[:-1])
                print(self.lastDirectory)

        self.logger.info("filename :{0}".format(fileName))
        if fileName == "":
            return
        self.nameOfFile = fileName.split(".")[0].split("/")[-1]
        if ".rif" in fileName:
            if fileName not in self.settingsWindow.getSettingsVariable('recentFiles'):
                self.settingsWindow.addRecentFile(fileName)

            with open(fileName, "r") as file:
                loadedState = json.load(file)


            print("loadedState len = 1")
            logging.info(" canvas :{0}".format(loadedState))
            widget = WidgetGraph(self, "", loadedState)
            self.listGraphWidgets.append(widget)
            self.ui.tabWidget.addTab(widget, self.nameOfFile)
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

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

        self.loadOpenMenu()

        #self.ui.tabWidget.addTab(widget, widget.name)

    def openActionClicked(self):
        action = self.sender()
        filePath = action.data()
        if '.rif' in filePath:
            print('Rif detected opening file')
            self.openButtonClicked(filePath)
        else:
            print('Opening Folder now..')
            fileName, _ = QFileDialog.getOpenFileName(None, "Select File", filePath,
                                                      "*.rgp *.rif;;*.rgp;;*.rif")
            if fileName:
                self.openButtonClicked(fileName)

    def openDefaultFolderDialog(self):
        folderPath = self.settingsWindow.getSettingsVariable('defaultFolderPath')
        fileName, _ = QFileDialog.getOpenFileName(None, "Select File", folderPath,
                                                  "*.rgp *.rif;;*.rgp;;*.rif")

        if fileName:
            self.openButtonClicked(fileName)

    def addEntriesToOpenMenu(self, names: list[str], paths: list[str]):
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

        for i in range(len(openMenu.actions())-3, -1, -1):
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


    def showSaveFileDialog(self):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        defaultName = graphWidget.name + ".rif"
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",
                                                  defaultName, "All Files (*);;Text Files (*.txt)", options=options)

        fileName = fileName if ".rif" in fileName else fileName + ".rif"

        if fileName:
            self.saveGraphState(graphWidget, fileName)


    def saveGraphState(self, graphWidget, path=""):
        if graphWidget:
            if path == "":
                with open("./data/" + graphWidget.name + ".rif", "w") as file:
                    json.dump(graphWidget.getCurrentState(), file)
            else:
                with open(path, "w") as file:
                    json.dump(graphWidget.getCurrentState(), file)
        else:
            for widget in self.listGraphWidgets:
                with open("./data/" + widget.name + ".rif", "w") as file:
                    json.dump(widget.getCurrentState(), file)


    # functionality for the pushButtonTabView QPushButton
    def tabButtonClicked(self):
        if (self.ui.stackedWidgetWorkArea.currentIndex() != 0):
            for graphWidget in self.listGraphWidgets:
                graphWidget.setParent(None)
                self.ui.mdiArea.closeAllSubWindows()
                self.ui.tabWidget.addTab(graphWidget, graphWidget.name)

        self.ui.stackedWidgetWorkArea.setCurrentIndex(0)


    def closeTab(self, index):
        tabWidget = self.ui.tabWidget.widget(index)
        reply = QMessageBox.question(self, QObject.tr("Confirm close"), QObject.tr("Save before you close?"),
                                     QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if (reply == QMessageBox.Save):
            if tabWidget is not None:
                with open(tabWidget.name + ".rif", "w") as file:
                    json.dump(tabWidget.getCurrentState(), file)
                tabWidget.deleteLater()
                self.listGraphWidgets.remove(tabWidget)
            self.ui.tabWidget.removeTab(index)

        elif (reply == QMessageBox.No):
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
        PrintWindow(graphWidget, self.settingsWindow, 'pdf', filename)


    def pngButtonClicked(self):
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        filename = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        PrintWindow(graphWidget, self.settingsWindow, 'png', filename)


    def settingsButtonClicked(self):
        self.markerPresetWin = MarkerPresetWindow(self, self.nameToColorDict, self.markerPresetList, calledByGraph=False)
        if self.settingsWindow.exec():
            for canvas in self.listGraphWidgets:
                canvas.updateUi()
            with open("./settings/settings.json", "w") as file:
                json.dump(self.settingsWindow.defaultSettingsDict, file, indent=2)

    def toggleOverlayButtonClicked(self):
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
        currentWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())

        fileNames = {widget.name: widget for widget in self.listGraphWidgets if widget is not currentWidget}
        customData = {
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
                    entry = currentWidget.dataModel.getDataByKey(data)
                    row = int(data.split("_")[0])
                    print(f'entry: {entry}; row: {row}')
                    fileNames[name].changeTableTopEntry(row, 5, entry)

    def updateGraphWidgets(self):
        for graph in self.listGraphWidgets:
            graph.canvasGraph.repaintGrid()

    def openPickMarker(self, defaultPresetName):
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
        # generate window at cursor and check if window is in screen, if not create at corner
        mousePos = QCursor.pos()
        screenGeometry = QApplication.primaryScreen().availableGeometry()

        xEnd = mousePos.x() + self.pickMarkerWin.width()
        yEnd = mousePos.y() + self.pickMarkerWin.height()
        moveX = mousePos.x() if xEnd < screenGeometry.width() else screenGeometry.width()-self.pickMarkerWin.width()
        moveY = mousePos.y() if yEnd < screenGeometry.height() else screenGeometry.height()-self.pickMarkerWin.height()
        movePos = QPoint(moveX, moveY)

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
        graphWidget = self.ui.tabWidget.widget(self.ui.tabWidget.currentIndex())
        return graphWidget.defaultMarkerDictName

    def openChangeMarkerPreset(self, defaultPresetName=None):
        markerPresetWin = MarkerPresetWindow(self, self.nameToColorDict, self.markerPresetList)
        if (markerPresetWin.exec()):
            for markerDict in self.markerPresetList:
                if (defaultPresetName in markerDict.values()):
                    return markerDict
        else:
            return None


    def loadPreset(self):
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
                self.markerPresetList = loadedFile[2]
                print('581 executed in main.py.loadPreset()')
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




    def closeEvent(self, event):
        if self.defaultMarkerDictName is not None:
            saveData = [self.settingsWindow.defaultSettingsDict, self.nameToColorDict, self.markerPresetList]
        else:
            saveData = [self.settingsWindow.defaultSettingsDict, self.nameToColorDict, self.markerPresetList]
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
