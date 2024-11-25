from PySide6.QtGui import QBrush, QColor, Qt, QFont
from PySide6.QtWidgets import QTableWidgetItem, QTextEdit, QLabel
from PySide6.QtCore import QObject
import json
import logging


class DataModel:
    """
    Class that represents a data model object that handles the widgetGraph data

    Args:
    datasource (str): the path to the data source
    listNameKeys (list): List of keys to identify data names.
    jsonData (dict): Optional JSON data to initialize the model.

    Attributes:
    _name (str): Name of the data model.
    _dataDrill (list): Data related to drilling.
    _dataFeed (list): Data related to feed.
    _depthMsmt (str): Measurement of depth.
    _customData (dict): Custom data fields.
    jsonData (dict): JSON data for the model.
    markerStateList (list): List of marker states.
    dx_xlim (int): Limit on x-axis.
    commentRight (str): Right comment for the data model.
    _dataNameDict (dict): Dictionary for mapping data names.
    fileDefaultPresetName (str): Default preset name for the file.
    fileDefaultSavePath (str): Default save path for the file.

    Raises:
    Exception: If the extension of the datasource is not valid.

    Methods:
    _readDataFromRGP(file): Read data from RGP file format.
    _readDataFromCustom(file): Read data from custom file format.
    _formatListToDict(tmpData): Format a list to dictionary.
    setComment(comment): Set a comment for the data model.
    getComment(): Get the comment for the data model.
    getGraphData(): Get the graph data for the data model.

    """
    def __init__(self, datasource, listNameKeys, jsonData=None):
        self._name = ""
        self._dataDrill = None
        self._dataFeed = None
        self._depthMsmt = None
        self._customData = {
            "0_diameter": "---",
            "1_mHeight": "---",
            "2_mDirection": "---",
            "3_objecttype": "---",
            "4_location": "---",
            "5_name": "---"
        }
        self.jsonData = jsonData
        self.markerStateList = []
        self.dx_xlim = 0
        self.commentRight = ""
        self._dataNameDict = {}
        self.fileDefaultPresetName = ""
        self.fileDefaultSavePath = ''
        # todo add this to settings so that the user can choose which data to display
        # TODO need to change the behaviour on which cells are eidtable from constant to variable!!!
        self._dataNameDict = {
            "number": QObject.tr('Messung Nr.'),
            "idNumber": QObject.tr('ID-Nummer'),
            "depthMsmt": QObject.tr('Bohrtiefe'),
            "date": QObject.tr('Datum'),
            "time": QObject.tr('Uhrzeit'),
            "speedFeed": QObject.tr('Vorschub'),
            "speedDrill": QObject.tr('Drehzahl'),
            "tiltAngle": QObject.tr('Neigung'),
            "ncState": QObject.tr('Nadelstatus'),
            "offset": QObject.tr('Offset'),
            "graphAvgShow": QObject.tr('Mittelung'),
            "empty": "",
            "0_diameter": QObject.tr('Durchmesser'),
            "1_mHeight": QObject.tr('Messhöhe'),
            "2_mDirection": QObject.tr('Messrichtung'),
            "3_objecttype": QObject.tr('Objektart'),
            "4_location": QObject.tr('Standort'),
            "5_name": QObject.tr('Name')
        }



        if "rgp" in datasource.lower():
            self._data = self._readDataFromRGP(datasource)
            self.fileDefaultSavePath = '/'.join(datasource.split('/')[:-1])

            self._name = datasource.split('/')[-1].split('.')[0]
            self._depthMsmt = self._data["depthMsmt"]
        elif 'rif' in datasource.lower() or datasource == "":
            self.fileDefaultSavePath = '/'.join(datasource.split('/')[:-1])
            self._readDataFromCustom()

        else:
            raise Exception("ERROR: extension '{0}' is not valid".format(datasource.split(".")[-1]))

    def _readDataFromRGP(self, file: str):

        """
        Reads data from a file in RGP format and converts the extracted data into a dictionary.

        Args:
            file (str): Path to the data file.

        Returns:
            dict: Processed data from RGP file in dictionary format.

        Notes:
            - The data is read line by line and specific information is extracted, like 'drill', 'feed', 'date', 'time', etc.
            - Certain lines that contain red flag characters are skipped.
            - Some data is formatted for specific fields of the dictionary. For example, date and time readings are combined into one entry.
            - If any exceptions are encountered, those are simply printed out and process continues with the next line.
        """
        tmpData = []

        charsRedFlags = ("{", "}", "wi", "\"dd\"", "pole", "\"set\"", "p2", "\"res\"", "ssd", "p1",
                         "profile", "checksum", "wiPoleResult", "app")
        time = ""
        date = ""
        offset = ""
        avg = ""
        # @todo find out why the character at the end of the drill line can't be decoded to UTF-8 in Linux
        with (open(file, 'r', errors="ignore") as f):
            line = f.readline()
            while line:
                if any(flag in line for flag in charsRedFlags):
                    line = f.readline()
                    continue
                if "\"drill\"" in line:
                    strList = line.split("[")[1].replace("]", "").strip().split(",")[0:-1]
                    self._dataDrill = [float(num) for num in strList]
                    line = f.readline()
                    continue
                elif "\"feed\"" in line:
                    strList = line.split("[")[1].replace("]", "").strip().split(",")[0:-1]
                    self._dataFeed = [float(num) for num in strList]
                    line = f.readline()
                    continue
                elif any(s in line for s in ["dateYear", "dateMonth", "dateDay"]):
                    datePart = line.split(":")[1].strip()[:-1]
                    if len(datePart) == 1:
                        datePart = "0" + datePart

                    date = datePart + "." + date
                    if "dateDay" in line:
                        tmpData.append("date; " + date[:-1])

                    line = f.readline()
                    continue
                elif any(s in line for s in ["timeHour", "timeMinute", "timeSecond"]):
                    timePart = line.split(":")[1].strip()[:-1]
                    if (len(timePart) == 1):
                        timePart = "0" + timePart
                    time = time + ":" + timePart
                    if ("timeSecond" in line):
                        tmpData.append("time; " + time[1:])

                    line = f.readline()
                    continue
                elif (any(s in line for s in ["offsetFeed", "offsetDrill"])):
                    offsetPart = line.split(":")[1].strip()[:-1]
                    if ("Drill" in line):
                        offset = offset + offsetPart
                        tmpData.append("offset; " + offset)
                        line = f.readline()
                        continue
                    offset = offsetPart + " / "
                    line = f.readline()
                    continue
                elif (any(s in line for s in ["graphDrillAvgShow", "graphFeedAvgShow"])):
                    avgPart = line.split(":")[1].strip()[:-1]
                    if ("0" in avgPart):
                        avgPart = "aus"
                    else:
                        avgPart = "an"

                    if ("Feed" in line):
                        avg = avg + avgPart
                        tmpData.append("graphAvgShow; " + avg)
                        line = f.readline()
                        continue
                    avg = avgPart + " / "
                    line = f.readline()
                    continue

                elif ("diameter" in line):
                    if (float(line.split(":")[1].strip()[:-1]) == 0):
                        self._customData["0_diameter"] = ""
                    else:
                        self._customData["0_diameter"] = float(line.split(":")[1].strip()[:-1])

                elif ("object\":" in line):
                    try:
                        objectData = line.split(":")[1].strip().replace("[", "").replace("]", "").replace("\"", "")[:-1].split(",")
                        self._customData["1_mHeight"] = objectData[0]
                        self._customData["2_mDirection"] = objectData[1]
                        self._customData["3_objecttype"] = objectData[2]
                        self._customData["4_location"] = objectData[3]
                        self._customData["5_name"] = objectData[4]
                    except IndexError:
                        print("welp")
                elif 'assessment' in line:
                    self.commentRight = line.split(':')[1].strip().replace('\"', '')

                tmpData.append(line.replace("\"", "").replace(",", "").replace(":",";"))
                line = f.readline()

        return self._formatListToDict(tmpData)


    # @todo check if the name/color pairs of each marker fits the name/color pair of the nameToColorDict
    # if it doesnt dont change the color but create a seperate dict with that
    def _readDataFromCustom(self):
        """
        This method reads and assigns data from a loaded JSON state to specific attributes of the class.

        It extracts information related to the name, comment rights, presets,
        data related to drilling and feeding, depth measurement, and marker states.

        If any data is not found, a KeyError is caught and a message is printed.

        The JSON state is assumed to be stored in the class attribute `jsonData`.

        Parameter:
        file: The file from which the data is read.
              Note: The parameter `file` isn't used in the code block and might be removed if not necessary.

        Returns:
        None

        Raises:
        KeyError: If expected data is not found in the JSON state.
        """
        loadedState = self.jsonData
        try:
            self._data = loadedState["data"]
            self._data.update({'ncState': 0})
            self._name = self._data["selfName"]
            self.commentRight = self._data["commentRight"]
            self.dx_xlim = loadedState["dx_xlim"]
            self.fileDefaultPresetName = self._data["fileDefaultPresetName"]
            self._depthMsmt = self._data["depthMsmt"]
            self._dataDrill = self._data["dataDrill"]
            self._dataFeed = self._data["dataFeed"]
            for markerState in loadedState["markerState"]:
                self.markerStateList.append(markerState)
        except KeyError as ke:
            print(f'KeyError: {ke}')



    def _formatListToDict(self, tmpData):
        dictData = dict((x.strip(), y.strip())
                        for x, y in (element.split(";")
                                     for element in tmpData))

        dictData.update(self._customData)
        return dictData


    def setComment(self, comment: str):
        self.commentRight = comment

    def getComment(self):
        return self.commentRight

    def getGraphData(self):
        return [self._name, self._depthMsmt, self._dataDrill, self._dataFeed]


    def getTablaTopData(self):
        """
        This method formats the data specified by `self._dataNameDict` into lists of QTableWidgetItems
        representing names and associated data.

        The table entries are formatted and styled within the function. Entries that aren't custom and are
        read from the rgp file are not editable, same goes for the name strings

        Returns:
        list: A list containing two lists. The first list contains QTableWidgetItems for the names,
            and the second list contains associated data as QTableWidgetItems.
        """
        result_dict = self._dataNameDict
        collectedTableNames = []
        collectedTableData = []
        totalCharactersPerRow = []
        maxLen = 0
        for i, (key, value) in enumerate(result_dict.items()):
            if i % 6 == 0 and i > 0:
                totalCharactersPerRow.append(maxLen+2)
                maxLen = 0

            maxLen = max(len(value), maxLen)

        totalCharactersPerRow.append(maxLen + 2)

        for i, (key, value) in enumerate(result_dict.items()):
            textString = value.ljust(totalCharactersPerRow[i // 6])
            tableTextEditEntry = QTableWidgetItem(textString)
            font = QFont()
            font.setFamily("Tahoma")
            font.setWeight(QFont.Bold)
            brush = QBrush(QColor("#000000"))
            tableTextEditEntry.setFont(font)
            tableTextEditEntry.setForeground(brush)
            tableTextEditEntry.setFlags(tableTextEditEntry.flags() & ~Qt.ItemIsEditable)
            tableTextEditEntry.setFlags(tableTextEditEntry.flags() & ~Qt.ItemIsSelectable)
            collectedTableNames.append(tableTextEditEntry)
            if value == "":
                tableItemDataEntry = QTableWidgetItem("")
            else:
                fontDataEntry = QFont()
                font.setFamily("Tahoma")
                brush = QBrush(QColor("#1f1bf7"))
                if key == "tiltAngle":
                    tableItemDataEntry = QTableWidgetItem(': ' +
                                                          str(int(round(float(self._data[key]) + 0.001, 0) - 90))+"  ")
                else:
                    tableItemDataEntry = QTableWidgetItem(": "+str(self._data[key]) + "  ")
                tableItemDataEntry.setFont(fontDataEntry)
                tableItemDataEntry.setForeground(brush)
            if (1 < i < 12):
                tableItemDataEntry.setFlags(tableItemDataEntry.flags() & ~Qt.ItemIsEditable)
                tableItemDataEntry.setFlags(tableItemDataEntry.flags() & ~Qt.ItemIsSelectable)

            collectedTableData.append(tableItemDataEntry)

        return [collectedTableNames, collectedTableData]


    def getDataByKey(self, key):
        """
        this method returns data corresponding to a key
        Args:
            key: the key to look for

        Returns:
            _data entry corresponding to the key
        """
        return self._data[key]

    def getNameByKey(self, key):
        """
        this method returns the name of a key
        Args:
            key: the key to look for

        Returns:
            the name corresponding to the key
        """
        return self._dataNameDict[key]

    def changeCustomDataEntry(self, row: int, column: int, entry):
        """
        Updates the custom data in the data model.

        Changes the value of a specific attribute in the data model given the table row and column
        where the attribute is represented.

        Args:
            row (int): The row index of the table where the attribute is located.
            column (int): The column index of the table where the attribute is located.
            entry (str): The new value to set for the attribute.

        Notes:
            - If the value to be changed is located in column 1, the modified fields will be either "number"
              (if the row is 0) or "idNumber" (for other rows).
            - If the value is in a different column, it's associated with custom data. In this case,
              the index for identifying the right key in the data dictionary is computed based on
              the row and column position, and the entry in the dict is updated accordingly.
        """
        if column == 1:
            if row == 0:
                self._data["number"] = entry
            else:
                self._data["idNumber"] = entry
        else:
            index = row + column - 5
            for key, value in self._data.items():
                if str(index) + "_" in key:
                    self._data[key] = entry
                    break



    def getSaveState(self):
        """
        This method gathers necessary data for saving the state of the current instance.

        It collects data values from `self._data` and custom data from `self._customData`,
        as well as other attributes of the class such as `self._name`, `self._depthMsmt`,
        `self._dataDrill`, `self._dataFeed`, `self.commentRight`, and `self.fileDefaultPresetName`.

        If a key is not found in `self._data`, a warning is logged.

        Returns:
        dict: A dictionary containing key-value pairs representing the state of the instance.
        """
        dataKeys = ["number", "idNumber", "depthMsmt", "date", "time", "speedFeed", "speedDrill", "tiltAngle",
                    "ncState", "offset", "remark", "graphAvgShow"]
        dataKeys.extend(list(self._customData.keys()))

        keyValuePairs = self._data.copy()
        '''
        for key in dataKeys:
            try:
                value = self._data[key]
                keyValuePairs[key] = value
            except KeyError as kE:
                logging.exception(f"Warning: Key '{kE.args[0]}' not found in self._data.")
        '''
        graphDataKeyValues = {"selfName": self._name,
                              "deviceLength": self._depthMsmt,
                              "dataDrill": self._dataDrill,
                              "dataFeed": self._dataFeed}

        commentDic = {"commentRight": self.commentRight}
        defaultMarkerNameDic = {"fileDefaultPresetName": self.fileDefaultPresetName}
        # keyValuePairs.update(self._customData)
        keyValuePairs.update(commentDic)
        keyValuePairs.update(defaultMarkerNameDic)
        keyValuePairs.update(graphDataKeyValues)
        return keyValuePairs

