from threading import Thread
from time import sleep

class PumpControl(object):
    # Class for storing and sending pump controlling data to Arduino
    
    def __init__(self):
        # Initializes class vars to default values and mode
        self.SDAC = 0
        self.EDAC = 1
        self.MS = 5
        self.mode = self.constant
        self.serialMode = 'constant'
        
    def updateMode(self, mode):
        # Changes class mode if changed on GUI, defaults to constant
        self.serialMode = mode.lower()
        if mode.lower() == 'constant':
            self.mode = self.constant
        elif mode.lower() == 'pulse':
            self.mode = self.pulse
        elif mode.lower() == 'ramp':
            self.mode = self.ramp
        else:
            self.mode = self.constant
            
    def updateParams(self, start=None, end=None, ms=None):
        # Updates and input parameters for class
        if not start is None:
            self.SDAC = int(start)
            
        if not end is None:
            self.EDAC = int(end)
            
        if not ms is None:
            self.MS = int(ms)
            
    def getSerialData(self):
        # Gets serial data string to output based on current mode
        return self.mode(self.SDAC, self.EDAC, self.MS)
        
    def constant(self, start, end=0, ms=0):
        """
            If in constant mode, outputs...
            PYSIG,constant,VOLT_LOW,
        """
        self.serialMode = 'constant'
        params = [str(i) for i in [start]]
        
        return self.serialSignalFormat(params)
        
    def pulse(self, start, end, ms):
        """
            If in pulse mode, outputs...
            PYSIG,pulse,VOLT_LOW,VOLT_HIGH,TIME_INTERVAL,
        """
        self.serialMode = 'pulse'
        params = [str(i) for i in [start, end, ms]]
        
        return self.serialSignalFormat(params)
        
    def ramp(self, start, end, ms):
        """
            If in ramp mode, outputs...
            PYSIG,ramp,VOLT_LOW,VOLT_HIGH,TIME_INTERVAL,
        """
        # Sets mode and converts params to strings in one list
        self.serialMode = 'ramp'
        params = [str(i) for i in [start, end, ms]]
        
        return self.serialSignalFormat(params)
        
    def serialSignalFormat(self, params):
        """
            Function for formatting serial string based on inputs
            NOTE 1: Delimiter between fields MUST be comma or else 
                Arduino will not parse correctly
            NOTE 2: String MUST end with a comma or else last fields
                will not be parsed on Arduino
            NOTE 3: Newline character (\n) MUST be at start of serial
                string. This is because newline character when sent
                by python adds another invalid char as well. If no newline
                character is used, Arduino will not know each sent
                signal are separate. If newline character is at the end
                of string, last line (which is the only line read by Arduino)
                is invalid char and then skipped by Arduino so no data will
                be parsed or set on output.
        """
        params = ','.join(params)
        mode = self.serialMode
        serialData = '\nPYSIG,%s,%s,' % (mode, params)
        
        return serialData
        
class PumpTimer(object):
    # Timer for syncronously sending and reading data along serial buffer
    def __init__(self, pumpGui, timer):
        # Takes pump GUI object for sending data and timer for how long
        # to pause in between samples
        self.pumpGui = pumpGui
        self.timer = timer
        
        # Starts timer as new thread so other processes are not on hold
        t1 = Thread(target=self.startTimer)
        t1.start()
        
    def startTimer(self):
        # While the PumpGUI is not closed, loops
        while self.pumpGui.open:
            sleep(self.timer) # Delays for timer amount (timer in ms)
            self.pumpGui.readSerialPort() # Reads serial port
            if self.pumpGui.changed: # If changed state is detected on GUI
                self.pumpGui.sendSerialData() #Sends data and resets changed state