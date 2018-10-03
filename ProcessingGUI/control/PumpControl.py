

class PumpControl(object):
    def __init__(self):
        self.SDAC = 0
        self.EDAC = 10
        self.MS = 5
        self.mode = self.constant
        
    def updateMode(self, mode):
        if mode == 'constant':
            self.mode = self.constant
        elif mode == 'pulse':
            self.mode = self.pulse
        elif mode == 'ramp':
            self.mode = self.ramp
        else:
            self.mode = self.constant
            
    def constant(self, start, end=0):
        pass
        
    def pulse(self, start, end):
        pass
        
    def ramp(self, start, end):
        pass
        