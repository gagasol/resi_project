from PySide6.QtGui import QBrush, QColor, Qt, QFont
from PySide6.QtWidgets import QTableWidgetItem, QTextEdit, QLabel
from PySide6.QtCore import QObject
import json


class DataModel:
    def __init__(self, datasource, listNameKeys, jsonData=None):
        self._name = ""
        self._dataDrill = None
        self._dataFeed = None
        self._deviceLength = None
        self._customData = {
            "diameter": "---",
            "mHeight": "---",
            "mDirection": "---",
            "objecttype": "---",
            "location": "---",
            "name": "---"
        }
        self.jsonData = jsonData
        self.markerStateList = []
        self.dx_xlim = 0

        if ("rgp" in datasource.lower()):
            self._data = self._readDataFromRGP(datasource)
            print(self._data)
            for nameKey in listNameKeys:
                self._name = self._name + str(self._data[nameKey]) + "_"

            self._name = self._name[:-1]
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
        print(loadedState["markerState"])
        for markerState in loadedState["markerState"]:
            self.markerStateList.append(markerState)
        self.dx_xlim = loadedState["dx_xlim"]


    def _formatListToDict(self, tmpData):
        print(tmpData)
        for element in tmpData:
            if (len(element.split(";"))!= 2):
                print(element)

        dictData = dict((x.strip(), y.strip())
                        for x, y in (element.split(";")
                                     for element in tmpData))

        dictData.update(self._customData)
        return dictData


    def getGraphData(self):
        return [self._name, self._deviceLength, self._dataDrill, self._dataFeed]


    def getTablaTopData(self):#c44a04
        result_dict = {
            #"number": 'Messung Nr.',
            "idNumber": 'ID-Nummer',
            "depthMsmt": 'Bohrtiefe',
            "date": 'Datum',
            "time": 'Uhrzeit',
            "speedFeed": 'Vorschub',
            "speedDrill": 'Drehzahl',
            "tiltAngle": 'Neigung',
            "result": 'Nadelstatus',
            "offset": 'Offset',
            "graphAvgShow": 'Mittelung',
            "diameter": 'Durchmesser',
            "mHeight": 'Messhöhe',
            "mDirection": 'Messrichtung',
            "objecttype": 'Objektart',
            "location": 'Standort',
            "name": 'Name'
        }
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
            "diameter": QObject.tr('Durchmesser'),
            "mHeight": QObject.tr('Messhöhe'),
            "mDirection": QObject.tr('Messrichtung'),
            "objecttype": QObject.tr('Objektart'),
            "location": QObject.tr('Standort'),
            "name": QObject.tr('Name')
        }
        collectedTableNames = []
        collectedTableData = []

        for key, value in result_dict.items():
            tableTextEditEntry = QTableWidgetItem('{0}\t:'.format(value))
            font = QFont()
            font.setWeight(QFont.Bold)
            brush = QBrush(QColor("#c44a04"))
            tableTextEditEntry.setFont(font)
            tableTextEditEntry.setForeground(brush)
            tableTextEditEntry.setFlags(tableTextEditEntry.flags() & ~Qt.ItemIsEditable)
            collectedTableNames.append(tableTextEditEntry)
            print("[Debug Info] " + key)
            if(value == ""):
                print("A")
                tableItemDataEntry = QTableWidgetItem("")
            else:
                tableItemDataEntry = QTableWidgetItem(self._data[key] + "  ")

            collectedTableData.append(tableItemDataEntry)

        """
        collectedTableData.append(QLabel(QObject.tr("ID-Nummer\t: ") + self._data["idNumber"]))
        collectedTableData.append(
            QLabel(QObject.tr("Bohrtiefe\t: ") + self._data["depthMsmt"] + " cm"))
        collectedTableData.append(QLabel(
            QObject.tr("Datum\t: ") + self._data["date"]))
        collectedTableData.append(QLabel(
            QObject.tr("Uhrzeit\t: ") + self._data["time"].replace(";",":")))
        collectedTableData.append(
            QLabel(QObject.tr("Vorschub\t: ") + self._data["speedFeed"] + " cm/min"))
        collectedTableData.append(
            QLabel(QObject.tr("Drehzahl\t: ") + self._data["speedDrill"] + QObject.tr(" U/min")))
        collectedTableData.append(QLabel(QObject.tr("Nadelstatus\t: ---")))
        collectedTableData.append(QLabel(QObject.tr("Neigung\t: ") + self._data["tiltAngle"]))
        collectedTableData.append(QLabel(
            QObject.tr("Offset\t: ") + self._data["offsetFeed"] + " / " + self._data["offsetDrill"]))
        collectedTableData.append(QLabel(QObject.tr("Mitteilung\t: ") + self._data["remark"]))
        collectedTableData.append(QLabel(QObject.tr("Durchmesser\t: ") + self._data["diameter"]))
        collectedTableData.append(QLabel(QObject.tr("Messhöhe\t: ") + self._data["mHeight"]))
        collectedTableData.append(QLabel(QObject.tr("Messrichtung\t: ") + self._data["mDirection"]))
        collectedTableData.append(QLabel(QObject.tr("Objektart\t: ") + self._data["objecttype"]))
        collectedTableData.append(QLabel(QObject.tr("Standort\t: ") + self._data["location"]))
        collectedTableData.append(QLabel(QObject.tr("Name\t: ") + self._data["name"]))
        """
        return [collectedTableNames, collectedTableData]


    def getSaveState(self):
        dataKeys = ["number", "idNumber", "depthMsmt", "date", "time", "speedFeed", "speedDrill", "tiltAngle",
                    "result", "offset", "remark"]
        dataKeys.extend(list(self._customData.keys()))

        keyValuePairs = {}
        for key in dataKeys:
            try:
                value = self._data[key]
                keyValuePairs[key] = value
            except KeyError:
                print(f"Warning: Key '{key}' not found in self._data.")

        graphDataKeyValues = {"selfName": self._name,
                              "deviceLength": self._deviceLength,
                              "dataDrill": self._dataDrill,
                              "dataFeed": self._dataFeed}

        keyValuePairs.update(graphDataKeyValues)
        return keyValuePairs

