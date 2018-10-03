import serial

port1 = '\\\\.\\CNCA0'
ser1 = serial.Serial(port1, 38400, timeout=0)

port2 = '\\\\.\\CNCB0'
ser2 = serial.Serial(port2, 38400, timeout=0)

ser1.write(b'Hello\nMy Name Is\nRJ\n')
ser1.write(b'')
ser1.write(b'')

while True:
    print('='*40)
    print('BYTES IN BUFFER:',ser2.in_waiting)
    data = ser2.read(ser2.in_waiting)
    if len(data) > 0:
        print('DATA FROM BUFFER:', data)
        print('DATA DECODED:', data.decode('utf-8'))
        print('='*40, '\n')
    else:
        print('No more data... Exiting...')
        print('='*40, '\n')
        break

ser1.close()
ser2.close()
