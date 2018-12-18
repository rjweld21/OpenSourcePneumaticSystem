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

# Inits config file path, Arduino port index, max DAC and max time interval
CONFIG_FILE = os.path.join('content', 'ard.config')
ARD_INDEX = 'ArduinoComPort'
MAX_DAC_INDEX = 'MaxDAC'
MS_INDEX = 'PeriodMax'
NUM_MAX = 255
PERIOD_MAX = 1000

class PumpGUI(QWidget):
    # Graphic User Interface (GUI) which is used for controlling Arduino
    def __init__(self, parent=None):
        self.open = True # Bool for being open for timer
        self.changed = False # For checking if data should be sent to Arduino
        
        # Don't really know what super is for but always have to do it
            # with PyQt5 main windows
        super(PumpGUI, self).__init__(parent)
        self.pump = PumpControl() # Set up pump controller
        self.initSerial() # Initialize serial connection with Arduino
        self.userFeedback = {}
        
        # Create grid for main screen
        grid = QGridLayout()
        
        # Mode buttons
        buttons = ['CONSTANT', 'PULSE', 'RAMP']
        
        # Adds mode buttons to layout
        grid.addWidget(self.radioButtons(buttons, 'Signal Type'), 0, 0)
        
        # Create slider 1, tick interval and text value box (Starting DAC)
        self.intSDAC = 1
        sBoxSDAC, self.sliderSDAC = self.createSlider('Set Starting DAC',
                                                      tickStep=self.intSDAC,
                                                      tickInterval=NUM_MAX/10,
                                                      max=NUM_MAX)
        self.sliderSDAC.setValue(self.pump.SDAC)
        # When slider value changes, run updateSDAC
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
        # When slider value changes, run updateEDAC
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
        # When slider value changes, run updateMS
        self.sliderMS.valueChanged.connect(self.updateMS)
        lBoxMS, self.labelMS = self.createEditLabel(self.pump.MS, 
                                                    'ms Interval',
                                                    changeFunc=self.textMS)
        
        # Create user feedback fields. Create field names then add their 
            # static text. Any static text should include %s for string formatting
        fields = ['ms']
        staticText = ['Waveform Period: %s ms']
        userFeedbackBox = self.userFeedbackTextBox(fields, staticText, 
                                                center=True, 
                                                boxName='User Feedback')
                                                
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
        grid.addWidget(userFeedbackBox, 4, 0)
        
        # Set grid
        self.setLayout(grid)
        
        self.setWindowTitle('PumpGUI')
        self.resize(400, 300)
        
        # Set as if data has changes so Arduino is given initial output
        self.changed = True
        self.updateMS()
        
    def createSlider(self, sliderName='Slider',
                           tickInterval=10,
                           tickStep=1,
                           min=0, max=50):
        """
            Function to create slider on main window
            
            INPUTS
                :sliderName: String of what label to put on slider
                :tickInterval: Interval of how much hotkey should increment by
                :tickStep: What is the minimum amount of change that can occur on slider
                :min: Min value of slider
                :max: Max value of slider
                
            OUTPUTS
                :groupBox: PyQt5 object for bbox of slider and contents
                :slider: Resulting set slider object
        """
        groupBox = QGroupBox(sliderName) # Create container for GUI objects
        
        slider = QSlider(Qt.Horizontal) # Create slider
        slider.setFocusPolicy(Qt.StrongFocus) # Set style
        slider.setTickPosition(QSlider.TicksBothSides) # Set functionality
        slider.setTickInterval(tickInterval) # Set tick interval
        slider.setSingleStep(tickStep) # Set min step
        slider.setMinimum(min) # Set min value
        slider.setMaximum(max) # Set max balue
        
        vbox=QVBoxLayout() # Put slider in bbox then add to container
        vbox.addWidget(slider)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        
        return groupBox, slider
        
    def radioButtons(self, buttonNames, groupTitle='Radio Buttons'):
        """
            Function to iterate through list of buttons and set them up
                on GUI
            
            INPUTS
                :buttonNames: List of strings to name each radio button
                :groupTitle: String to label box of buttons
                
            OUTPUT
                :groupBox: PyQt5 container of buttons and associated objects
        """
        # Make sure buttonNames is list
        assert type(buttonNames) == list
        
        # Create group for radio buttons
        groupBox = QGroupBox(groupTitle)
        hbox = QHBoxLayout()
        
        # Create list for radio button variables
        self.buttons = []
        
        # Create radio buttons and add to bbox
        for name in buttonNames:
            self.buttons.append(QRadioButton(name))
            self.buttons[-1].toggled.connect(self.changeMode)
            hbox.addWidget(self.buttons[-1])
            
        self.buttons[0].setChecked(True)
            
        groupBox.setLayout(hbox)
        
        return groupBox
        
    def createEditLabel(self, text, labelTitle='', center=True, changeFunc=None):
        """
            Function to create text entry boxes
            
            INPUTS
                :text: Default value to put in entry box
                :labelTitle: String label to associate with box on GUI
                :center: Bool of whether to center in bbox or not
                :changeFunc: Function to connect entry box to. If value in
                    entry box is changed, this function is run
                    
            OUTPUTS
                :groupBox: PyQt5 container for entry box and contents
                :label: Resulting entry box object
        """
        # Create entry box object
        label = QLineEdit()
        label.setText(str(text)) # Set text in entry box
        if not changeFunc == None: #If function input, connect to box
            label.textChanged.connect(changeFunc)
        
        if center: # Center box if chosen to
            label.setAlignment(Qt.AlignCenter)
            
        groupBox = QGroupBox(labelTitle) #Set up bbox and add entry box
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch()
        
        groupBox.setLayout(vbox)
        
        return groupBox, label
        
    def userFeedbackTextBox(self, fields, staticText, center=True, 
                                boxName='User Feedback'):
        """
            Function to create vertical box of user feedback fields
            Currently only field used is for period output
        """
        self.userFeedback['text'] = {}
        self.userFeedback['static'] = {}
        
        groupbox = QGroupBox(boxName)
        vbox = QVBoxLayout()
        
        for i, f in enumerate(fields):
            self.userFeedback['text'][f] = QLabel()
            self.userFeedback['static'][f] = staticText[i]
            self.userFeedback['text'][f].setText(staticText[i])
            vbox.addWidget(self.userFeedback['text'][f])
            
        vbox.addStretch()
        groupbox.setLayout(vbox)
        
        return groupbox
        
    def changeMode(self):
        """
            Function for changing mode if user selected new radio box
        """
        # Init name just in case no buttons are detected to be checked
            # This case shouldn't happen but is just for error catching
        name = None
        for b in self.buttons: # Iterate through radio buttons
            # Find which button is checked, set name then break
            if b.isChecked():
                name = b.text()
                break
                
        # Tell pump controller to update the mode
        self.pump.updateMode(name)
        
        try:
            self.updateMS()
        except Exception as e:
            print(e)
        
        # Set changed state to update serial buffer
        self.changed = True
        
    def updateSDAC(self):
        """
            Function for changing SDAC if start DAC slider is moved
        """
        # Get slider value
        start = self.sliderSDAC.value()
        
        # Set value to entry box value
        self.labelSDAC.setText(str(start))
        
        # Check if start DAC is larger than end DAC
        if start > self.sliderEDAC.value():
            # If so, change end DAC value to above start value
            self.sliderEDAC.setValue(start+self.intEDAC)
        
        # Update pump controller with new start DAC
        self.pump.updateParams(start=start)
        
        # Set changed state to update serial buffer
        self.changed = True
        self.updateMS()
        
    def textSDAC(self):
        """
            Function for changing SDAC if entry box is edited
        """
        # If no contents in entry box, set to 0
        if not len(self.labelSDAC.text()):
            self.labelSDAC.setText('0')
            
        try:
            # Try to get box value as int
            start = int(self.labelSDAC.text())
            if start < 0: # If entered value lower than 0, reset to 0
                self.labelSDAC.setText('0')
                start = 0
        except:
            # If cannot be converted (aka if non-numerical character was entered)
                # delete last character and return
            self.labelSDAC.setText((' ' + self.labelSDAC.text())[:-1].replace(' ', ''))
            return
            
        # Check if start value is larger than max slider value
        if start > NUM_MAX:
            # If so, set to max slider value
            start = NUM_MAX
            
        # Update slider value with text value then run above function
        self.sliderSDAC.setValue(start)
        self.updateSDAC()
        
    def updateEDAC(self):
        """
            Function for changing EDAC if end DAC slider is moved
        """
        # Get slider value
        end = self.sliderEDAC.value()
        
        # Set entry box value to value of slider
        self.labelEDAC.setText(str(end))
        
        # If end slider value is less than start slider value
        if end < self.sliderSDAC.value():
            # Reset start slider value to lower than ending slider value
            self.sliderSDAC.setValue(end-self.intSDAC)
            
        # Update pump controller params
        self.pump.updateParams(end=end)
        
        # Change state so serial buffer gets updated
        self.changed = True
        self.updateMS()
        
    def textEDAC(self):
        """
            Function for changing EDAC if entry box is edited
        """
        # If no contents in entry box, set to 0
        if not len(self.labelEDAC.text()):
            self.labelEDAC.setText('0')
            
        try:
            # Try to get box value as int
            end = int(self.labelEDAC.text())
            if end < 0: # If entered value lower than 0, reset to 0
                self.labelEDAC.setText('0')
                end = 0
        except:
            # If cannot be converted (aka if non-numerical character was entered)
                # delete last character and return
            self.labelEDAC.setText((' ' + self.labelEDAC.text())[:-1].replace(' ', ''))
            return
            
        # Check if end value is larger than max slider value
        if end > NUM_MAX:
            end = NUM_MAX
            
        self.sliderEDAC.setValue(end)
        self.updateEDAC()

    def updateMS(self):
        ms = self.sliderMS.value()
        
        self.labelMS.setText(str(ms))
        
        self.updateFeedback(ms)
                        
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
    
    def updateFeedback(self, ms):
        p = self.calcPeriod(ms, self.pump.serialMode)
        self.userFeedback['text']['ms'].setText(
                        self.userFeedback['static']['ms'] % p)
                        
    def calcPeriod(self, ms, mode):
        if mode == 'pulse':
            p = ms*2
            if p < ms:
                p = ms
        elif mode == 'ramp':
            # Divide by 2 because of step size set in arduino firmware
            p = ((self.pump.EDAC-self.pump.SDAC)/2)*ms
            if p < ms:
                p = ms
        else:
            p = 'N/A'
            
        return str(p)
    def incrementSDAC(self):
        # Function for hotkey incrementing
        self.sliderSDAC.setValue(self.sliderSDAC.value() + self.intSDAC)
        
    def decrementSDAC(self):
        # Function for hotkey decrementing
        self.sliderSDAC.setValue(self.sliderSDAC.value() - self.intSDAC)
        
    def incrementEDAC(self):
        # Function for hotkey incrementing
        self.sliderEDAC.setValue(self.sliderEDAC.value() + self.intEDAC)
        
    def decrementEDAC(self):
        # Function for hotkey decrementing
        self.sliderEDAC.setValue(self.sliderEDAC.value() - self.intEDAC)
        
    def incrementMS(self):
        # Function for hotkey incrementing
        self.sliderMS.setValue(self.sliderMS.value() + self.intMS)
        
    def decrementMS(self):
        # Function for hotkey decrementing
        self.sliderMS.setValue(self.sliderMS.value() - self.intMS)
        
    def initSerial(self):
        """
            Function for initializing serial communication
        """
        try:
            # Tries to connect to arduino COM port
                # from config data
            ardCom = config_data[ARD_INDEX]
            SA = SerialArduino(port=ardCom)
            
        except Exception as e:
            # If cannot connect to arduino, raises custom error
                # Connection errors may be from no arduino connected
                    # or incorrect com port to connect to
            print('Exception raised: %s' % type(e))
            print('Exception desc: %s' % e)
            raise RuntimeError('No arduino detected on %s' % ardCom)
            
            print('Reverting to virtual COM ports for testing...')
            
            [SA, _] = connectVirtualComs(timeout=5)
            
        # Delay a second to allow Serial to fully initialize
        sleep(1)
        self.SA = SA # Set to class variable
        print('COM connection initialized!')
        
    def sendSerialData(self):
        """
            Function for sending pump control parameters to serial buffer
        """
        # Gives user output
        print('=' * 40, '\nSENDING TO ARDUINO...')
        # Get data to output
        data = self.pump.getSerialData()
        # Gets SDAC and EDAC
        bounds = data.split(',')[2:4] if len(data.split(',')) > 4 else [0, 1]
        
        # Checks that EDAC is not smaller than SDAC and vice versa
        if int(bounds[0]) <= int(bounds[1]):
            # User output and writes buffer
            print('Data: ', data)
            self.SA.write_buffer(str(data) + '\n')
            
        else: # If bounds error, outputs data
            print(bounds)
            print('FAILED:', data)
        
        # Resets state to skip buffer write until next GUI update
        self.changed = False
        
            
    def readSerialPort(self):
        """
            Function to read serial buffer port of data Arduino has 
                sent back to Python
        """
        # Read buffer
        self.SA.read_buffer()
        
        try:
            # Decode from bytes to string
            data = self.SA.data.decode('utf-8', 'ignore')
            
            # If data is present, output to user
            if len(data):
                print('READING FROM ARDUINO...')
                print('Read: ', data + '\n')
        except:
            # If decoding fails, output to user
            print('Failed to read!')
        
    def closeEvent(self, pos1=None, pos2=None):
        # If user closes GUI, update bool for timer to stop
        self.open=False
        
if __name__ == '__main__':
    # If PumpGUI.py is run (rather than imported to another script)...
    
    # Check if config file exists
    if not os.path.exists(CONFIG_FILE):
        # If no config file, output to user and start process to create
            # config file
        print('\n\nNo configuration file found, this is standard on first run or if config file cannot be found...\n')
        print('Enter config data based on prompts...\n')
        params = [ARD_INDEX, MAX_DAC_INDEX, MS_INDEX]
        help=['This is the COM port your Arduino UNO is listed as within '
                'your computer\'s device manager.', 'default', 'default']
        defaults = [255, 10000]
        config.setup(filename=CONFIG_FILE, config_params=params,
                        help=help, defaults=defaults)
    # Once config file exists, get dictionary of contents
    config_data = config.load_config(CONFIG_FILE)
    NUM_MAX = config_data['MaxDAC']
    PERIOD_MAX = config_data['PeriodMax']
    
    # Timer sampling rate
    UPDATE_RATE_HZ = 10
    UPDATE_RATE = 1/UPDATE_RATE_HZ
    
    try:
        # Send system arguments to app
        app = QApplication(sys.argv)
        # Set dock icon for app
        app.setWindowIcon(QIcon(os.path.join('content', 'icon.png')))
        # Open app
        gui = PumpGUI()
        # Create serial writing timer
        serialTimer = PumpTimer(gui, timer=UPDATE_RATE)
        # Show app
        gui.show()
        # idk what this does but what I do know is that it's necessary
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
