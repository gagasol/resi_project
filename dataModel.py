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



        if "rgp" in datasource.lower():
            self._data = self._readDataFromRGP(datasource)
            self.fileDefaultSavePath = '/'.join(datasource.split('/')[:-1])

            self._name = datasource.split(".")[0].split("/")[-1]
            self._depthMsmt = self._data["depthMsmt"]
        elif 'rif' in datasource.lower() or datasource == "":
            self.fileDefaultSavePath = '/'.join(datasource.split('/')[:-1])
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
                    if (len(datePart) == 1):
                        datePart = "0" + datePart

                    date = datePart + "." + date
                    if ("dateDay" in line):
                        tmpData.append("date; " + date[:-1])

                    line = f.readline()
                    continue
                elif (any(s in line for s in ["timeHour", "timeMinute", "timeSecond"])):
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

                tmpData.append(line.replace("\"", "").replace(",", "").replace(":",";"))
                line = f.readline()

        return self._formatListToDict(tmpData)


    # @todo check if the name/color pairs of each marker fits the name/color pair of the nameToColorDict
    # if it doesnt dont change the color but create a seperate dict with that
    def _readDataFromCustom(self, file):
        loadedState = self.jsonData
        try:
            self._data = loadedState["data"]
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
        return self._data[key]

    def getNameByKey(self, key):
        return self._dataNameDict[key]

    def changeCustomDataEntry(self, row, column, entry):
        if (column == 1):
            if (row == 0):
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
                              "deviceLength": self._depthMsmt,
                              "dataDrill": self._dataDrill,
                              "dataFeed": self._dataFeed}

        print(f'time in dataModel.getSaveState: {keyValuePairs["time"]}')

        commentDic = {"commentRight": self.commentRight}
        defaultMarkerNameDic = {"fileDefaultPresetName": self.fileDefaultPresetName}
        keyValuePairs.update(commentDic)
        keyValuePairs.update(defaultMarkerNameDic)
        keyValuePairs.update(graphDataKeyValues)
        return keyValuePairs

