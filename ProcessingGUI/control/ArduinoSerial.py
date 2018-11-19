import serial
from time import sleep

class SerialArduino(object):
    def __init__(self, port='COM7', br=9600, timeout=1, virtual=0):
        self.SA = serial.Serial(port, br, timeout=timeout, rtscts=0,
                                writeTimeout=3)
        self.old = b''
        self.data = b''
        self.virtual = virtual
        
    def write_buffer(self, data):
        if type(data) == str:
            data = data.encode('utf-8')
        elif type(data) == int:
            data = str(data).encode('utf-8')
            
        if not type(data) == bytes:
            print('Data must be int, string or bytes!')
            print('No data written to serial.')
            return
            
        try:
            self.SA.write(data)
        except:
            print('Write failed!')
            print(data)
            print()

    def read_buffer(self, byteLen=0, parse=True):
        if not byteLen:
            byteLen = self.bufferSize()
            
        self.data = self.old + self.SA.read(byteLen)
        
        if parse and len(self.data) > 0:
            self.parseData()
            
    def parseData(self):
        if self.data[-1] == '\n':
            self.old = b''
            return
            
        parsed = self.data.decode('utf-8').split('\n')
        self.data = '\n'.join(parsed[:-1]).encode('utf-8')
        self.old = parsed[-1].encode('utf-8')
        
    def bufferSize(self):
        return self.SA.in_waiting
        
    def close(self):
        self.SA.close()
        del self.SA
        
def connectVirtualComs(ports=['\\\\.\\CNCA0',
                                '\\\\.\\CNCB0'],
                        br=38400, timeout=0):
    ser = []
    
    for p in ports:
        ser.append(SerialArduino(p, br, timeout, 1))
        
    return ser
    
def parseData(data):
    if data[-1] == '\n':
        return data, b''
        
    parsed = data.decode('utf-8').split('\n')
    data = '\n'.join(parsed[:-1])
    oldData = parsed[-1].encode('utf-8')
    
    return data, oldData
    
    
if __name__ == '__main__':
    try:
        print('Trying arduino...')
        port2 = 'COM7'
        ser2 = SerialArduino()
        print('Connected!')
    except Exception as e:
        print('\n\n' + '!'*40 + '\n\nFAILED CONNECTING TO ARDUINO\n')
        print('!'*40, '\n\n')
        print('\nError:', e, '\n\n')
        [ser1, ser2] = connectVirtualComs()

    while True:
        print('='*40)
        print('BYTES IN BUFFER:',ser2.bufferSize())
        ser2.read_buffer()
        if len(ser2.data)-len(ser2.old) > 0:
            print('DATA FROM BUFFER:', ser2.data)
            print('DATA DECODED:', ser2.data.decode('utf-8'))
            print('='*40, '\n')
            ser2.write_buffer(b'PYSERIAL,constant,0\n')
        else:
            print('No more data... Sleeping...')
            print('='*40, '\n')
            sleep(2)

    ser1.close()
    ser2.close()
