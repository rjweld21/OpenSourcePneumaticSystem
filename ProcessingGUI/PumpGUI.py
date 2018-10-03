import os
import sys
from control.PumpControl import PumpControl
from time import sleep
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                            QMenu, QPushButton, QRadioButton, QVBoxLayout, 
                            QHBoxLayout, QWidget, QSlider, QLabel,
                            QShortcut)


class PumpGUI(QWidget):
    def __init__(self, parent=None):
        super(PumpGUI, self).__init__(parent)
        self.pump = PumpControl()
        
        # Create grid for main screen
        grid = QGridLayout()
        
        buttons = ['CONSTANT', 'PULSE', 'RAMP']
        
        grid.addWidget(self.radioButtons(buttons, 'Signal Type'), 0, 0)
        
        # Create slider 1, tick interval and text value box (Starting DAC)
        self.intSDAC = 1
        sBoxSDAC, self.sliderSDAC = self.createSlider('Set Starting DAC',
                                                      tickStep=self.intSDAC,
                                                      tickInterval=4095/10,
                                                      max=4095)
        self.sliderSDAC.setValue(self.pump.SDAC)
        self.sliderSDAC.valueChanged.connect(self.updateSDAC)
        lBoxSDAC, self.labelSDAC = self.createLabel(self.pump.SDAC, 'Starting DAC')
        
        # Add slider 2 and text value box (Ending DAC)
        self.intEDAC = 1
        sBoxEDAC, self.sliderEDAC = self.createSlider('Set Ending DAC',
                                                      tickStep=self.intEDAC,
                                                      tickInterval=4096/10,
                                                      max=4096)
        self.sliderEDAC.setValue(self.pump.EDAC)
        self.sliderEDAC.valueChanged.connect(self.updateEDAC)
        lBoxEDAC, self.labelEDAC = self.createLabel(self.pump.EDAC, 'Ending DAC')
        
        # Add slider 3 and text value box (MS interval)
        self.intMS = 1
        sBoxMS, self.sliderMS = self.createSlider('Set ms Interval',
                                                  tickStep=self.intMS)
        self.sliderMS.setValue(self.pump.MS)
        self.sliderMS.valueChanged.connect(self.updateMS)
        lBoxMS, self.labelMS = self.createLabel(self.pump.MS, 'ms Interval')
        
        
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
        
    def createLabel(self, text, labelTitle='', center=True):
        label = QLabel()
        label.setText(str(text))
        
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
        
        self.sendSerialData()
        
    def updateSDAC(self):
        start = self.sliderSDAC.value()
        
        self.labelSDAC.setText(str(start))
        
        if start > self.sliderEDAC.value():
            self.sliderEDAC.setValue(start+self.intEDAC)
        
        self.pump.updateParams(start=start)
        
        self.sendSerialData()
        
    def updateEDAC(self):
        end = self.sliderEDAC.value()
        
        self.labelEDAC.setText(str(end))
        
        if end < self.sliderSDAC.value():
            self.sliderSDAC.setValue(end+self.intSDAC)
            
        self.pump.updateParams(end=end)
        
        self.sendSerialData()

    def updateMS(self):
        ms = self.sliderMS.value()
        
        self.labelMS.setText(str(ms))
        
        self.pump.updateParams(ms=ms)
        
        self.sendSerialData()
        
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
        
    def sendSerialData(self):
        data = self.pump.getSerialData()
        bounds = data.split(',')[2:4] if len(data.split(',')) > 3 else [0, 1]
        if int(bounds[0]) < int(bounds[1]):
            print(data)
        else:
            print('FAIL:', data)
            
    def readSerialPort(self):
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join('content', 'icon.png')))
    gui = PumpGUI()
    gui.show()
    sys.exit(app.exec_())