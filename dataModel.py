from PySide6.QtGui import QBrush, QColor, Qt, QFont
from PySide6.QtWidgets import QTableWidgetItem, QTextEdit, QLabel
from PySide6.QtCore import QObject
import json
import logging


class DataModel:
    def __init__(self, datasource, listNameKeys, jsonData=None):
        self._name = ""
        self._dataDrill = None
        self._dataFeed = None
        self._deviceLength = None
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

        if ("rgp" in datasource.lower()):
            self._data = self._readDataFromRGP(datasource)

            self._name = datasource.split(".")[0].split("/")[-1]
            self._deviceLength = self._data["deviceLength"]
        elif (datasource == ""):
            self._readDataFromCustom(datasource)

        else:
            raise Exception("ERROR: extension '{0}' is not valid".format(datasource.split(".")[-1]))

    def _readDataFromRGP(self, file):
        tmpData = []

        charsRedFlags = ("{", "}", "wi", "\"dd\"", "pole", "\"set\"", "p2", "\"res\"", "ssd", "p1",
                         "profile", "checksum", "wiPoleResult", "app", "assessment")
        time = ""
        date = ""
        offset = ""
        avg = ""
        # @todo find out why the character at the end of the drill line can't be decoded to UTF-8 in Linux
        with (open(file, 'r', errors="ignore") as f):
            line = f.readline()
            while line:
                if (any(flag in line for flag in charsRedFlags)):
                    line = f.readline()
                    continue
                if ("\"drill\"" in line):
                    strList = line.split("[")[1].replace("]", "").strip().split(",")[0:-1]
                    self._dataDrill = [float(num) for num in strList]
                    line = f.readline()
                    continue
                elif ("\"feed\"" in line):
                    strList = line.split("[")[1].replace("]", "").strip().split(",")[0:-1]
                    self._dataFeed = [float(num) for num in strList]
                    line = f.readline()
                    continue
                elif (any(s in line for s in ["dateYear", "dateMonth", "dateDay"])):
                    datePart = line.split(":")[1].strip()[:-1]
                    date = datePart + "." + date
                    if ("dateDay" in line):
                        tmpData.append("date; " + date[:-1])

                    line = f.readline()
                    continue
                elif (any(s in line for s in ["timeHour", "timeMinute", "timeSecond"])):
                    timePart = line.split(":")[1].strip()[:-1]
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

                tmpData.append(line.replace("\"", "").replace(",", "").replace(":",";"))
                line = f.readline()

        return self._formatListToDict(tmpData)


    # @todo check if the name/color pairs of each marker fits the name/color pair of the nameToColorDict
    # if it doesnt dont change the color but create a seperate dict with that
    def _readDataFromCustom(self, file):
        loadedState = self.jsonData

        self._data = loadedState["data"]
        self._name = self._data["selfName"]
        self._deviceLength = self._data["deviceLength"]
        self._dataDrill = self._data["dataDrill"]
        self._dataFeed = self._data["dataFeed"]
        for markerState in loadedState["markerState"]:
            self.markerStateList.append(markerState)
        self.dx_xlim = loadedState["dx_xlim"]


    def _formatListToDict(self, tmpData):
        dictData = dict((x.strip(), y.strip())
                        for x, y in (element.split(";")
                                     for element in tmpData))

        dictData.update(self._customData)
        return dictData


    def getGraphData(self):
        return [self._name, self._deviceLength, self._dataDrill, self._dataFeed]


    def getTablaTopData(self):#c44a04
        result_dict = {
            "number": QObject.tr('Messung Nr.'),
            "idNumber": QObject.tr('ID-Nummer'),
            "depthMsmt": QObject.tr('Bohrtiefe'),
            "date": QObject.tr('Datum'),
            "time": QObject.tr('Uhrzeit'),
            "speedFeed": QObject.tr('Vorschub'),
            "speedDrill": QObject.tr('Drehzahl'),
            "tiltAngle": QObject.tr('Neigung'),
            "result": QObject.tr('Nadelstatus'),
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
        collectedTableNames = []
        collectedTableData = []
        totalCharactersPerRow = []
        maxLen = 0
        for i, (key, value) in enumerate(result_dict.items()):
            if (i % 6 == 0 and i > 0):
                totalCharactersPerRow.append(maxLen+2)
                maxLen = 0

            maxLen = max(len(value), maxLen)

        totalCharactersPerRow.append(maxLen + 2)

        for i, (key, value) in enumerate(result_dict.items()):
            textString = value.ljust(totalCharactersPerRow[i // 6]-len(value))
            tableTextEditEntry = QTableWidgetItem(textString)
            font = QFont()
            font.setWeight(QFont.Bold)
            brush = QBrush(QColor("#c44a04"))
            tableTextEditEntry.setFont(font)
            tableTextEditEntry.setForeground(brush)
            tableTextEditEntry.setFlags(tableTextEditEntry.flags() & ~Qt.ItemIsEditable)
            collectedTableNames.append(tableTextEditEntry)
            if(value == ""):
                tableItemDataEntry = QTableWidgetItem("")
            else:
                tableItemDataEntry = QTableWidgetItem(self._data[key] + "  ")
            if (1 < i < 12):
                tableItemDataEntry.setFlags(tableItemDataEntry.flags() & ~Qt.ItemIsEditable)

            collectedTableData.append(tableItemDataEntry)

        return [collectedTableNames, collectedTableData]


    def changeCustomDataEntry(self, row, column, entry):
        if (column == 1):
            if (row == 0):
                self._data["number"] = entry
            else:
                self._data["idNumber"] = entry
        else:
            index = row + column - 5
            for key, value in self._data.items():
                if (str(index)+"_" in key):
                    self._data[key] = entry
                    break



    def getSaveState(self):
        dataKeys = ["number", "idNumber", "depthMsmt", "date", "time", "speedFeed", "speedDrill", "tiltAngle",
                    "result", "offset", "remark", "graphAvgShow"]
        dataKeys.extend(list(self._customData.keys()))

        keyValuePairs = {}
        for key in dataKeys:
            try:
                value = self._data[key]
                keyValuePairs[key] = value
            except KeyError as kE:
                logging.exception(f"Warning: Key '{kE.args[0]}' not found in self._data.")

        graphDataKeyValues = {"selfName": self._name,
                              "deviceLength": self._deviceLength,
                              "dataDrill": self._dataDrill,
                              "dataFeed": self._dataFeed}

        keyValuePairs.update(graphDataKeyValues)
        return keyValuePairs

