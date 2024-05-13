from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QObject
import json


class DataModel:
    def __init__(self, datasource, listNameKeys):
        self._name = ""
        self._dataDrill = None
        self._dataFeed = None
        self._deviceLength = None
        self._customData = {
            "diameter": "None",
            "mHeight": "None",
            "mDirection": "None",
            "objecttype": "None",
            "location": "None",
            "name": "None"
        }

        self.markerStateList = []

        if ("rgp" in datasource.lower()):
            self._data = self._readDataFromRGP(datasource)
            print(self._data)
            for nameKey in listNameKeys:
                self._name = self._name + str(self._data[nameKey]) + "_"

            self._name = self._name[:-1]
            self._deviceLength = self._data["deviceLength"]
        elif ("resi" in datasource.lower()):
            self._readDataFromCustom(datasource)

        else:
            raise Exception("ERROR: extension '{0}' is not valid".format(datasource.split(".")[-1]))

    def _readDataFromRGP(self, file):
        tmpData = []

        charsRedFlags = ("{", "}", "wi", "\"dd\"", "pole", "\"set\"", "p2", "\"res\"", "ssd", "p1",
                         "profile", "checksum", "wiPoleResult", "app", "assessment")
        time = ""
        date = ""
        # @todo find out why the character at the end of the drill line can't be decoded to UTF-8 in Linux
        with open(file, 'r', errors="ignore") as f:
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
                    break
                elif (any(s in line for s in ["dateYear", "dateMonth", "dateDay"])):
                    datePart = line.split(":")[1].strip()[:-1]
                    date = datePart + "." + date
                    if ("dateDay" in line):
                        tmpData.append("date: " + date[:-1])
                        print(tmpData[-1])

                    line = f.readline()
                    continue
                elif (any(s in line for s in ["timeHour", "timeMinute", "timeSecond"])):
                    timePart = line.split(":")[1].strip()[:-1]
                    time = time + ";" + timePart
                    if ("timeSecond" in line):
                        tmpData.append("time: " + time[1:])
                        print(tmpData[-1])

                    line = f.readline()
                    continue

                tmpData.append(line.replace("\"", "").replace(",", ""))
                line = f.readline()

        return self._formatListToDict(tmpData)


    def _readDataFromCustom(self, file):
        with open(file, 'r') as f:
            loadedState = json.load(f)

        self._data = loadedState["data"]
        self._name = self._data["selfName"]
        self._deviceLength = self._data["deviceLength"]
        self._dataDrill = self._data["dataDrill"]
        self._dataFeed = self._data["dataFeed"]

        for markerState in loadedState["marker"]:
            self.markerStateList.append(markerState)


    def _formatListToDict(self, tmpData):
        dictData = dict((x.strip(), y.strip())
                        for x, y in (element.split(":")
                                     for element in tmpData))

        dictData.update(self._customData)
        return dictData


    def getGraphData(self):
        return [self._name, self._deviceLength, self._dataDrill, self._dataFeed]


    def getTablaTopData(self):
        collectedTableData = []
        collectedTableData.append(QTableWidgetItem(QObject.tr("Messung Nr.\t: ") + self._data["number"]))
        collectedTableData.append(QTableWidgetItem(QObject.tr("ID-Nummer\t: ") + self._data["idNumber"]))
        collectedTableData.append(
            QTableWidgetItem(QObject.tr("Bohrtiefe\t: ") + self._data["depthMsmt"] + " cm"))
        collectedTableData.append(QTableWidgetItem(
            QObject.tr("Datum\t: ") + self._data["date"]))
        collectedTableData.append(QTableWidgetItem(
            QObject.tr("Uhrzeit\t: ") + self._data["time"].replace(";",":")))
        collectedTableData.append(
            QTableWidgetItem(QObject.tr("Vorschub\t: ") + self._data["speedFeed"] + " cm/min"))
        collectedTableData.append(
            QTableWidgetItem(QObject.tr("Drehzahl\t: ") + self._data["speedDrill"] + QObject.tr(" U/min")))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Nadelstatus\t: ---")))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Neigung\t: ") + self._data["tiltAngle"]))
        collectedTableData.append(QTableWidgetItem(
            QObject.tr("Offset\t: ") + self._data["offsetFeed"] + " / " + self._data["offsetDrill"]))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Mitteilung\t: ") + self._data["remark"]))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Durchmesser\t: ") + self._data["diameter"]))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Messhöhe\t: ") + self._data["mHeight"]))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Messrichtung\t: ") + self._data["mDirection"]))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Objektart\t: ") + self._data["objecttype"]))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Standort\t: ") + self._data["location"]))
        collectedTableData.append(QTableWidgetItem(QObject.tr("Name\t: ") + self._data["name"]))

        return collectedTableData


    def getSaveState(self):
        dataKeys = ["number", "idNumber", "depthMsmt", "date", "time", "speedFeed", "speedDrill", "tiltAngle",
                    "offsetFeed", "offsetDrill", "remark"]
        dataKeys.extend(list(self._customData.keys()))

        keyValuePairs = {}
        for key in dataKeys:
            try:
                print(key)
                value = self._data[key]
                keyValuePairs[key] = value
            except KeyError:
                print(f"Warning: Key '{key}' not found in self._data.")

        graphDataKeyValues = {"selfName": self._name,
                              "deviceLength": self._deviceLength,
                              "dataDrill": self._dataDrill,
                              "dataFeed": self._dataFeed}

        keyValuePairs.update(graphDataKeyValues)
        print(keyValuePairs)
        return keyValuePairs

