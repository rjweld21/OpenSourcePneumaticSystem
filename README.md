# Open-source, Arduino-based pneumatic system for Dr. Galie's lab at Rowan University
### This project is a modified version of the [MillerLab Pneumatic System](https://github.com/MillerLabFTW/OpenSourcePneumaticSystem)

Developed and documented by R.J. Weld and Kishan Patel

## Overview
This is an open-source pneumatic control system utilizing an Arduino UNO and the 
Python 3 programming language. Python is used for GUI control which sends signals 
to the Arduino via serial port. Arduino reads these signals and outputs accordingly 
for the transducer.

More specifically, Python 3.6.3 was used in the development of this project 
and is the version that will be outlined for setup within this document.
Other Python 3 subversions (any 3.x.x) will most likely work but have not been tested.

## Repository Contents
1. [Bill of materials for this project](#bill-of-materials)
2. [Python 3.6.3 setup](#python-3.6.3-setup)
3. [Arduino UNO setup](#arduino-uno-setup)
4. [Repository setup](#repository-setup)
5. [Schematic for electronics connectivity and setup](#schematics)

## Bill of materials
The complete Bill-of-Materials for this [Arduino](https://www.arduino.cc/)-based 
system are provided in the document `Pneumatic System Bill of Materials` located 
in this repository. Currently, required items are roughly $500 and the grand 
total for all recommended items (including the required items) is roughly $1,200.

## Python 3.6.3 setup
1. Download the [Python 3.6.3](https://www.python.org/downloads/release/python-363/) 
executable installer for your computer. For 32-bit computers, download the x86 
version and for 64-bit computers, download the x86-64 version.
    1. Run installer, check "Add Python to PATH" and select custom installation
    2. Keep all Optional Features default and press next
    3. Under Advanced Options check "Add Python to environment variables" and press install.
2. Open Powershell or Command Terminal and enter "python"
    1. If python session starts you have set it up correctly and can continue to step 4.
    2. If command is not recognized try running ```python3``` instead in the terminal.
    3. If neither commands are recognized continue to next step.
3. Follow the steps in [this StackOverflow post](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows/32609129#32609129) 
for how to add Python to environment 
variables. This will allow you to run python scripts from command line. 
    1. *NOTE: This post was written for python 2.7 so you will have to figure out 
what directory Python was installed to on your computer. It may have defaulted to
C:\Users\YOURUSER\AppData\Local\Programs\Python\Python36*
    2. Retry commands run in step 2 and they should now work.
4. Open command prompt and enter ```pip3```
    1. If command is recognized and large help prompt is output, continue to step 5.
    2. If command is not recognized, enter ```where pip```
        - If there is a resulting path or more than one path, ensure that a python3 folder is within the first resulting path and continue to step 5.
        - If a python2 folder is in the first resulting path, go to subbullet iii below.
    3. Copy and paste the following commands, entering them into the command line
        - ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
        - ```python3 get-pip.py```
5. Navigate to the root of this repo within the command terminal *NOTE: You will need to follow download instructions in [repository setup](#repository-setup) section before this is possible.*
    1. This can be done using ```cd [NextDirectoryName]``` to move to the next folder or ```cd ..``` to move back a folder
    2. Likewise, you can copy the repo root directory from the file explorer and paste to ```cd [PastedRepoPath]```
6. Use pip or pip3, whichever command worked from step 4 and run...
    1. ```pip3 install -r requirements.txt``` in command prompt
    
## Arduino UNO setup
1. Download the latest version of Arduino for your OS from [https://www.arduino.cc/en/Main/Software](https://www.arduino.cc/en/Main/Software). 
1. Connect Arduino UNO to your computer via USB connection and open Arduino IDE.
1. On the Arduino taskbar, navigate to `Tools`->`Board` and select `Arduino Uno`. Next, navigate to `Tools`->`Port` and select the port assigned to Arduino.
On Windows, the correct COM port can be determined by locating `Arduino Uno` under the `Ports` dropdown in Device Manager.
2. We recommend using the blink sketch included in the Arduino software to test the connection to Arduino. To do this, follow `File`->`Examples`->`01.Basics`->`Blink`.

### Uploading PneumaticFirmware to Arduino
1. Open `PneumaticFirmware.ino` in Arduino and upload to Arduino using the upload button. 

## Repository setup
1. Navigate to [this README's repo](https://github.com/rjweld21/OpenSourcePneumaticSystem)
2. Click the large green "Clone or Download" button
3. Click "Download ZIP"
4. Within file explorer, navigate to where repo ZIP file was downloaded and extract its contents to your desired file location
5. Install python libraries (steps 4 - 6 of [Python 3.6.3 setup](#python-3.6.3-setup)
6. Open command prompt and navigate to "ProcessingGUI" directory of repo
7. Run ```python3 PumpGUI.py```
    1. Alternatively, with Windows, double clicking the "run.bat" file within the "ProcessingGUI" directory will launch the python script
    2. If ```python3``` does not work for you, you will need to right-click and open the "run.bat" file with notepad, change "python3" to "python"
    on the first line, save the file then re-run the batch script
        - If ```python3``` does not work for you but ```python``` does, the original "run.bat" will simply open and close the command prompt
        

## Schematics
