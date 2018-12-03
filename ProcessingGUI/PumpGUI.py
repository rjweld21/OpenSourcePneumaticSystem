import os
import sys
from control.PumpControl import PumpControl, PumpTimer
from control import config
from time import sleep
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                            QMenu, QPushButton, QRadioButton, QVBoxLayout, 
                            QHBoxLayout, QWidget, QSlider, QLabel,
                            QShortcut, QLineEdit)

from control.ArduinoSerial import SerialArduino, connectVirtualComs

CONFIG_FILE = os.path.join('content', 'ard.config')
ARD_INDEX = 'ArduinoComPort'
NUM_MAX = 255
PERIOD_MAX = 1000

class PumpGUI(QWidget):
    def __init__(self, parent=None):
        self.open = True
        self.changed = False
        
        #os.system('start powershell')
        super(PumpGUI, self).__init__(parent)
        self.pump = PumpControl()
        self.initSerial()
        
        # Create grid for main screen
        grid = QGridLayout()
        
        buttons = ['CONSTANT', 'PULSE', 'RAMP']
        
        grid.addWidget(self.radioButtons(buttons, 'Signal Type'), 0, 0)
        
        # Create slider 1, tick interval and text value box (Starting DAC)
        self.intSDAC = 1
        sBoxSDAC, self.sliderSDAC = self.createSlider('Set Starting DAC',
                                                      tickStep=self.intSDAC,
                                                      tickInterval=NUM_MAX/10,
                                                      max=NUM_MAX)
        self.sliderSDAC.setValue(self.pump.SDAC)
        self.sliderSDAC.valueChanged.connect(self.updateSDAC)
        lBoxSDAC, self.labelSDAC = self.createEditLabel(self.pump.SDAC, 
                                                        'Starting DAC',
                                                        changeFunc=self.textSDAC)
        
        # Add slider 2 and text value box (Ending DAC)
        self.intEDAC = 1
        sBoxEDAC, self.sliderEDAC = self.createSlider('Set Ending DAC',
                                                      tickStep=self.intEDAC,
                                                      tickInterval=NUM_MAX/10,
                                                      max=NUM_MAX)
        self.sliderEDAC.setValue(self.pump.EDAC)
        self.sliderEDAC.valueChanged.connect(self.updateEDAC)
        lBoxEDAC, self.labelEDAC = self.createEditLabel(self.pump.EDAC, 
                                                        'Ending DAC',
                                                        changeFunc=self.textEDAC)
        
        # Add slider 3 and text value box (MS interval)
        self.intMS = 1
        sBoxMS, self.sliderMS = self.createSlider('Set ms Interval',
                                                  tickStep=self.intMS,
                                                  tickInterval=PERIOD_MAX/10,
                                                  max=PERIOD_MAX)
        self.sliderMS.setValue(self.pump.MS)
        self.sliderMS.valueChanged.connect(self.updateMS)
        lBoxMS, self.labelMS = self.createEditLabel(self.pump.MS, 
                                                    'ms Interval',
                                                    changeFunc=self.textMS)
        
        
        # Add keyboard shortcuts
        QShortcut(QKeySequence(Qt.Key_W), self).activated.connect(self.incrementSDAC)
        QShortcut(QKeySequence(Qt.Key_Q), self).activated.connect(self.decrementSDAC)
        QShortcut(QKeySequence(Qt.Key_S), self).activated.connect(self.incrementEDAC)
        QShortcut(QKeySequence(Qt.Key_A), self).activated.connect(self.decrementEDAC)
        QShortcut(QKeySequence(Qt.Key_X), self).activated.connect(self.incrementMS)
        QShortcut(QKeySequence(Qt.Key_Z), self).activated.connect(self.decrementMS)
        
        # Add sliders and labels to grid
        grid.addWidget(sBoxSDAC, 1, 0)
        grid.addWidget(lBoxSDAC, 1, 1)
        grid.addWidget(sBoxEDAC, 2, 0)
        grid.addWidget(lBoxEDAC, 2, 1)
        grid.addWidget(sBoxMS, 3, 0)
        grid.addWidget(lBoxMS, 3, 1)
        
        # Set grid
        self.setLayout(grid)
        
        self.setWindowTitle('PumpGUI')
        self.resize(400, 300)
        
        self.changed = True
        
    def createSlider(self, sliderName='Slider',
                           tickInterval=10,
                           tickStep=1,
                           min=0, max=50):
        groupBox = QGroupBox(sliderName)
        
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(tickInterval)
        slider.setSingleStep(tickStep)
        slider.setMinimum(min)
        slider.setMaximum(max)
        
        vbox=QVBoxLayout()
        vbox.addWidget(slider)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        
        return groupBox, slider
        
    def radioButtons(self, buttonNames, groupTitle='Radio Buttons'):
        assert type(buttonNames) == list
        
        # Create group for radio buttons
        groupBox = QGroupBox(groupTitle)
        hbox = QHBoxLayout()
        
        # Create list for radio button variables
        self.buttons = []
        
        # Create radio buttons
        for name in buttonNames:
            self.buttons.append(QRadioButton(name))
            self.buttons[-1].toggled.connect(self.changeMode)
            hbox.addWidget(self.buttons[-1])
            
        self.buttons[0].setChecked(True)
            
        groupBox.setLayout(hbox)
        
        return groupBox
        
    def createEditLabel(self, text, labelTitle='', center=True, changeFunc=None):
        label = QLineEdit()
        label.setText(str(text))
        if not changeFunc == None:
            label.textChanged.connect(changeFunc)
        
        if center:
            label.setAlignment(Qt.AlignCenter)
            
        groupBox = QGroupBox(labelTitle)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch()
        
        groupBox.setLayout(vbox)
        
        return groupBox, label
    
    def changeMode(self):
        name = None
        for b in self.buttons:
            if b.isChecked():
                name = b.text()
                break
                
        self.pump.updateMode(name)
        
        self.changed = True
        
        #self.sendSerialData()
        
    def updateSDAC(self):
        start = self.sliderSDAC.value()
        
        self.labelSDAC.setText(str(start))
        
        if start > self.sliderEDAC.value():
            self.sliderEDAC.setValue(start+self.intEDAC)
        
        self.pump.updateParams(start=start)
        
        self.changed = True
        
        #self.sendSerialData()
        
    def textSDAC(self):
        if not len(self.labelSDAC.text()):
            self.labelSDAC.setText('0')
            
        try:
            start = int(self.labelSDAC.text())
        except:
            self.labelSDAC.setText((' ' + self.labelSDAC.text())[:-1].replace(' ', ''))
            return
            
        if start > NUM_MAX:
            start = NUM_MAX
            
        self.sliderSDAC.setValue(start)
        self.updateSDAC()
        
    def updateEDAC(self):
        end = self.sliderEDAC.value()
        
        self.labelEDAC.setText(str(end))
        
        if end < self.sliderSDAC.value():
            self.sliderSDAC.setValue(end+self.intSDAC)
            
        self.pump.updateParams(end=end)
        
        self.changed = True
        
        #self.sendSerialData()
        
    def textEDAC(self):
        if not len(self.labelEDAC.text()):
            self.labelEDAC.setText('0')
            
        try:
            end = int(self.labelEDAC.text())
        except:
            self.labelEDAC.setText((' ' + self.labelEDAC.text())[:-1].replace(' ', ''))
            return
            
        if end > NUM_MAX:
            end = NUM_MAX
            
        self.sliderEDAC.setValue(end)
        self.updateEDAC()

    def updateMS(self):
        ms = self.sliderMS.value()
        
        self.labelMS.setText(str(ms))
        
        self.pump.updateParams(ms=ms)
        
        self.changed = True
        
        #self.sendSerialData()
        
    def textMS(self):
        if not len(self.labelMS.text()):
            self.labelMS.setText('0')
            
        try:
            ms = int(self.labelMS.text())
        except:
            self.labelMS.setText((' ' + self.labelMS.text())[:-1].replace(' ', ''))
            return
            
        if ms > PERIOD_MAX:
            ms = PERIOD_MAX
            
        self.sliderMS.setValue(ms)
        self.updateMS()
        
    def incrementSDAC(self):
        self.sliderSDAC.setValue(self.sliderSDAC.value() + self.intSDAC)
        
    def decrementSDAC(self):
        self.sliderSDAC.setValue(self.sliderSDAC.value() - self.intSDAC)
        
    def incrementEDAC(self):
        self.sliderEDAC.setValue(self.sliderEDAC.value() + self.intEDAC)
        
    def decrementEDAC(self):
        self.sliderEDAC.setValue(self.sliderEDAC.value() - self.intEDAC)
        
    def incrementMS(self):
        self.sliderMS.setValue(self.sliderMS.value() + self.intMS)
        
    def decrementMS(self):
        self.sliderMS.setValue(self.sliderMS.value() - self.intMS)
        
    def initSerial(self):
        try:
            ardCom = config_data[ARD_INDEX]
            SA = SerialArduino(port=ardCom)
            
        except Exception as e:
            print('Exception raised: %s' % type(e))
            print('Exception desc: %s' % e)
            raise RuntimeError('No arduino detected on %s' % ardCom)
            
            print('Reverting to virtual COM ports for testing...')
            
            [SA, _] = connectVirtualComs(timeout=5)
            
        sleep(1)
        self.SA = SA
        print('COM connection initialized!')
        
    def sendSerialData(self):
        print('=' * 40, '\nSENDING TO ARDUINO...')
        data = self.pump.getSerialData()
        bounds = data.split(',')[2:4] if len(data.split(',')) > 4 else [0, 1]
        if int(bounds[0]) < int(bounds[1]):
            print('Data: ', data)
            self.SA.write_buffer(str(data) + '\n')
            
        else:
            print('FAILED:', data)
            
        self.changed = False
            
        #print(bounds)
            
    def readSerialPort(self):
        self.SA.read_buffer()
        
        try:
            data = self.SA.data.decode('utf-8', 'ignore')
            if len(data):
                print('READING FROM ARDUINO...')
                print('Read: ', data + '\n')
        except:
            print('Failed to read!')
        
    def closeEvent(self, pos1=None, pos2=None):
        self.open=False
        
if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        params = [ARD_INDEX]
        help=['This is the COM port your Arduino UNO is listed as within '
                'your computer\'s device manager.']
        config.setup(filename=CONFIG_FILE, config_params=params,
                        help=help)
    
    config_data = config.load_config(CONFIG_FILE)
    
    UPDATE_RATE_HZ = 10
    UPDATE_RATE = 1/UPDATE_RATE_HZ
    
    try:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(os.path.join('content', 'icon.png')))
        gui = PumpGUI()
        serialTimer = PumpTimer(gui, timer=UPDATE_RATE)
        gui.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)