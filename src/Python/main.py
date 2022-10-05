from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
import os
import obd
import time
import screen_brightness_control as sbc

global startTime = time.time()
global connection = None
global guageLabels = {"Data_11" : "AFR", "Data_12" : "Coolant",
                      "Data_21" : "MAP", "Data_22" : "Ambient",
                      "Data_31" : "IAT", "Data_32" : "Fuel Pressure"}
global gaugeData = {"AFR" : None, "Coolant" : None,
                    "MAP" : None, "Ambient" : None,
                    "IAT" : None, "Fuel Pressure" : None,
                    "Battery" : None}
global commandLookup = {"AFR" : COMMANDED_EQUIV_RATIO, "Coolant" : COOLANT_TEMP,
                        "MAP" : INTAKE_PRESSURE, "Ambient" : AMBIANT_AIR_TEMP,
                        "IAT" : INTAKE_TEMP, "Fuel Pressure" : FUEL_PRESSURE,
                        "Battery" : CONTROL_MODULE_VOLTAGE}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        path = os.path.dirname(os.path.realpath(__file__))
        #in obd2/src/python
        uic.loadUi(path+'../../Dashboard_GUI/gauges.ui', self)

        self.Brightness_Slider.valueChanged.connect(self.updateBrightness)

    def updateBrightness(self):
        brightness = self.Brightness_Slider.value()
        sbc.set_brightness(brightness)

    def start_read(self):
        self.data_thread = dataThread()
        self.data_thread.start()
        self.gui_thread = guiThread()
        self.gui_thread.start()
        self.gui_thread.updateGUI.connect(self.updateGUI)

    def updateGui:
        self.Data_Label_11.setText(guageLabels["Data_11"])
        self.Data_Label_12.setText(guageLabels["Data_12"])
        self.Data_Label_21.setText(guageLabels["Data_21"])
        self.Data_Label_22.setText(guageLabels["Data_22"])
        self.Data_Label_31.setText(guageLabels["Data_31"])
        self.Data_Label_32.setText(guageLabels["Data_32"])

        self.Data_Value_11.setValue(gaugeData[guageLabels["Data_11"]])
        self.Data_Value_12.setValue(gaugeData[guageLabels["Data_12"]])
        self.Data_Value_21.setValue(gaugeData[guageLabels["Data_21"]])
        self.Data_Value_22.setValue(gaugeData[guageLabels["Data_22"]])
        self.Data_Value_31.setValue(gaugeData[guageLabels["Data_31"]])
        self.Data_Value_32.setValue(gaugeData[guageLabels["Data_32"]])
        self.Battery.setValue(gaugeData["Battery"])

        self.showErrors()

    def showErrors:
        if(connection.status() != OBDStatus.CAR_CONNECTED)
            self.Connection_Status.setText("Not Connected")
            self.Connection_Status.setStyleSheet("background-color: red; color: white; font: 15pt; border-radius: 15px;")
        else:
            self.self.Connection_Status.setText("Connected")
            self.Connection_Status.setStyleSheet("background-color: lime; color: black; font: 15pt; border-radius: 15px;")

class dataThread(QThread):
    def run(self):
        while(1):
            try:
                #get data
                for place in guageLabels:
                    response = connection.query(obd.commands.commandLookup[guageLabels[place]])

                    if(guageLabels[place] == "AFR"): #convert lambda to AFR
                        guageData[guageLabels[place]] = response.value.magnitude * 14.63
                    else: 
                        gaugeData[guageLabels[place]] = response.value.magnitude 


class guiThread(QThread):
    updateGUI = pyqtSignal()

    def run(self):
        while(1):
            #update the screen every 1/2 second
            if((time.time() - startTime) > 0.5):
                startTime = time.time()
                self.updateGUI.emit

def main():
    app = QtWidgest.QApplication(sys.arg)
    Gauges = MainWindow()
    Gauges.show()
    Guages.showFullScreen()
    connection = obd.OBD() #auto connect obd with com and baudrate
    Guages.start_read()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
