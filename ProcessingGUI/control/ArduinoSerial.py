import serial
from time import sleep

class SerialArduino(object):
    """
        Class for controlling serial ports and their data flows
        NOTE: Serial port communication is 2 data wire protocol
                There is a wire which python reads from and the
                arduino writes to then another wire where python
                writes and arduino reads. In the case of this
                file, the input buffer is wire which python
                reads from and the output buffer is the wire
                which python writes to.
    """
    def __init__(self, port='COM7', br=9600, timeout=1, virtual=0):
        # Create serial object with pySerial on input port
        self.SA = serial.Serial(port, br, timeout=timeout, rtscts=0,
                                writeTimeout=3)
                                
        # Clear input and output buffers of any floating data
        self.SA.reset_input_buffer()
        self.SA.reset_output_buffer()
        
        # Initialize class variables
            # Old variable is for any incomplete data lines sent
            # by arduino. This can occur when python reads as
            # arduino is writing
            # Data variable is for all buffer data read in at one
            # time. Since the port is buffer data, you can only read
            # once.
        self.old = b''
        self.data = b''
        self.virtual = virtual
        
    def write_buffer(self, data):
        """
            Function to write output serial buffer
            
            INPUT
                :data: String or int of data to send to Arduino
        """
        # Encode data to bytes
        if type(data) == str:
            data = data.encode('utf-8')
        elif type(data) == int:
            data = str(data).encode('utf-8')
            
        # Ensure that data is of type bytes
        if not type(data) == bytes:
            print('Data must be int, string or bytes!')
            print('No data written to serial.')
            return
            
        try:
            # Try to write buffer
            self.SA.write(data)
        except:
            # If write fails, output to user
                # Write never failed during testing but this is for 
                # random error catching
            print('Write failed!')
            print(data)
            print()

    def read_buffer(self, byteLen=0, parse=True):
        """
            Function to read input buffer data
            
            :byteLen: Amount of bytes to load
                        (If 0, whole buffer is read)
            :parse: Whether to parse data or not
        """
        # Gets buffer size if chosen to read whole buffer
        if not byteLen:
            byteLen = self.bufferSize()
            
        # Adds old buffer data to new buffer data
        self.data = self.old + self.SA.read(byteLen)
        
        # If told to parse and if there is data to parse...
        if parse and len(self.data) > 0:
            self.parseData()
            
    def parseData(self):
        """
            Function for parsing serial data retrieved
        """
        # If last char is newline, complete serial buffer was read...
        if self.data[-1] == '\n':
            # Reset old var and exit
            self.old = b''
            return
            
        try:
            # Try to decode bytes to string then parse each line
            parsed = self.data.decode('utf-8').split('\n')
        except:
            print('FAILED ON:', self.data)
            self.data = ''
            parsed = ['Failed to read']
            
        # Rejoin parsed data except for last line into data
            # Set old data to last (incomplete) data line
        self.data = '\n'.join(parsed[:-1]).encode('utf-8')
        self.old = parsed[-1].encode('utf-8')
        
    def bufferSize(self):
        # Find amount of bytes in buffer to read
        return self.SA.in_waiting
        
    def close(self):
        # Close serial comm connection
        self.SA.close()
        del self.SA
        
def connectVirtualComs(ports=['\\\\.\\CNCA0',
                                '\\\\.\\CNCB0'],
                        br=38400, timeout=0):
    # Virtual serial comms set up during testing of reading/writing of data
    ser = []
    
    for p in ports:
        ser.append(SerialArduino(p, br, timeout, 1))
        
    return ser
    
def parseData(data):
    # Same as above parseData function. This may be depreciated but keeping
        # just incase it is used somewhere
    if data[-1] == '\n':
        return data, b''
        
    parsed = data.decode('utf-8').split('\n')
    data = '\n'.join(parsed[:-1])
    oldData = parsed[-1].encode('utf-8')
    
    return data, oldData