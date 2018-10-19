from ArduinoSerial import connectVirtualComs

if __name__ == '__main__':
    [D, ser] = connectVirtualComs()
    D.SA.close()
    del D
    
    print('Monitoring virtual COM port')
    while True:
        ser.read_buffer()
        if len(ser.data)-len(ser.old) > 0:
            print('Data found!')
            print(ser.data)
            print()
            
    ser.close()