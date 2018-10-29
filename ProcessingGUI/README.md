# Pump GUI

*NOTE:* .pde file is from previous team's work... .py file is from current team's work

### Setup and Running
1. Must have Python 3.x installed
2. From root of this repo (one level up) in command line/terminal run...
```
pip3 install -r requirements.txt
```
3. Then enter this directory from command line/terminal and run...
```
python3 PumpGUI.py
```
4. If Arduino is not connected and already running virtual COM ports will be access for serial communication
    - If error is occured from no virtual COMs running, install com0com and set it up with default settings
    - To start Arduino, set it up on serial COM7 and run PneumaticArduino.ino from Arduino IDE