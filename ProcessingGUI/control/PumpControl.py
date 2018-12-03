from threading import Thread
from time import sleep

class PumpControl(object):
    def __init__(self):
        self.SDAC = 0
        self.EDAC = 10
        self.MS = 5
        self.mode = self.constant
        
    def updateMode(self, mode):
        if mode.lower() == 'constant':
            self.mode = self.constant
        elif mode.lower() == 'pulse':
            self.mode = self.pulse
        elif mode.lower() == 'ramp':
            self.mode = self.ramp
        else:
            self.mode = self.constant
            
    def updateParams(self, start=None, end=None, ms=None):
        if not start is None:
            self.SDAC = int(start)
            
        if not end is None:
            self.EDAC = int(end)
            
        if not ms is None:
            self.MS = int(ms)
            
    def getSerialData(self):
        return self.mode(self.SDAC, self.EDAC, self.MS)
        
    def constant(self, start, end=0, ms=0):
        serialMode = 'constant'
        params = [str(i) for i in [start]]
        
        return self.serialSignalFormat(serialMode, params)
        
    def pulse(self, start, end, ms):
        serialMode = 'pulse'
        params = [str(i) for i in [start, end, ms]]
        
        return self.serialSignalFormat(serialMode, params)
        
    def ramp(self, start, end, ms):
        serialMode = 'ramp'
        params = [str(i) for i in [start, end, ms]]
        
        return self.serialSignalFormat(serialMode, params)
        
    def serialSignalFormat(self, mode, params):
        params = ','.join(params)
        serialData = 'PYSIG,%s,%s,\n' % (mode, params)
        
        return serialData
        
class PumpTimer(object):
    def __init__(self, pumpGui, timer):
        self.pumpGui = pumpGui
        self.timer = timer
        
        t1 = Thread(target=self.startTimer)
        t1.start()
        
    def startTimer(self):
        while self.pumpGui.open:
            sleep(self.timer)
            self.pumpGui.readSerialPort()
            if self.pumpGui.changed:
                self.pumpGui.sendSerialData()