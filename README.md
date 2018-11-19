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
Other Python 3 subversions will most likely work but have not been tested.

## Repository Contents
1. [Bill of materials for this project](#bill-of-materials)
2. [Schematic for electronics connectivity and setup](#schematics)
3. [Python 3.6.3 setup](#python-3.6.3-setup)
4. [Arduino UNO setup](#arduino-uno-setup)
5. [Repository setup](#repository-setup)

## Bill of materials
The complete Bill-of-Materials for this [Arduino](https://www.arduino.cc/)-based 
system are provided in the document `Pneumatic System Bill of Materials` located 
in this repository. Currently, required items are roughly $500 and the grand 
total for all recommended items (including the required items) is roughly $1,200.

## Schematics

## Python 3.6.3 setup
1. Download the [Python 3.6.3](https://www.python.org/downloads/release/python-363/) 
executable installer for your computer. For 32-bit computers, download the x86 
version and for 64-bit computers, download the x86-64 version.
    1. Run installer and select custom installation
    2. Keep all Optional Features default and press next
    3. Under Advanced Options check "Add Python to environment variables" and press install.
2. Open Powershell or Command Terminal and type...
```bash
python
```
  
1. If python session starts you have set it up correctly and are now done with this section.
2. If command is not recognized try running "python3" instead in the terminal.
3. If neither commands are recognized continue to next step.
3. Follow the steps in [this StackOverflow post](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows/32609129#32609129) 
for how to add Python to environment 
variables. This will allow you to run python scripts from command line. *NOTE: This
post was written for python 2.7 so you will have to figure out what directory
Python was installed to on your computer. 
    1. Retry commands run in step 2 and they should now work.
    
## Arduion UNO setup

## Repository setup