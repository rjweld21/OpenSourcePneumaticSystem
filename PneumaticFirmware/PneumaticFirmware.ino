#include <string.h>
#include <stdio.h>

// Struct for python data to control output
struct setting
{
  String mode="None";
  int interval=0;
  int low=0;
  int high=0;
};

// debug for serial outputting, out bools for analogWrites at end of void loop
bool debug = true, outRamp=false, outOther=false;
String data; //Serial data var
char *cData, *i, *token; //Parsing char pointers to parse serial data
int current=0, STEP_SIZE=2; //Current output var and voltage stepping size
setting prevControl, control; //Previous control settings and current control settings

void setup() {
  pinMode(3, OUTPUT); //For analog writing on pin 3
  Serial.begin(9600);
  
}

// Special function for writing ramp output
int rampOutput(int lowV, int highV, int interval, int prevLevel, int stepSize)
{
  /*
   * :int lowV: Low voltage for ramp to start at
   * :int highV: High voltage for ramp to end at
   * :int interval: Time (ms) between steps
   * :int prevLevel: Previous output level
   * :int stepSize: Amount to increment prevLevel by
   */

  // OOB = Out of bounds
  // Checks if prevLevel is OOB or will be OOB after stepping
  if (prevLevel+stepSize > highV) // || prevLevel < lowV-1)
  {
    prevLevel = lowV-stepSize; //Sets to low-step so is at low after stepping
  }
  analogWrite(3, prevLevel+stepSize); //Steps up prevLevel and writes
  delay(interval); //Delays by interval

  int out = prevLevel + stepSize; //Gets current output level and returns it
  return out;
}

void loop() { //Endless loop
  // Enter loop to read serial buffer
  while (Serial.available() > 0)
  {
    // Read line of serial data from computer
    data = Serial.readStringUntil('\n');

    // If on last pass for reading...
    // Only last pass is considered so only most recent data is parsed and processed
    if (Serial.available() == 0)
    {
      if (debug) {Serial.println("\n=");} // Output for debugging

      // Creates temp char array to load in data then sets to char pointer for later parsing
      char tempChar[data.length()];
      data.toCharArray(tempChar, data.length());
      cData = tempChar;

      /* DATA FORMATS
       * CONSTANT: PYSIG,constant,VOLT_LEVEL 
       * PULSE:    PYSIG,pulse,VOLT_LOW,VOLT_HIGH,TIME_INTERVAL
       * RAMP:     PYSIG,ramp,VOLT_LOW,VOLT_HIGH,TIME_INTERVAL
      */

      // Gets first segment of serial data parse (should be PYSIG)
      token = strtok_r(cData, ",", &i);

      // Check if current data is NOT from python GUI
      // Sometimes unknown chars are sent by python for an unknown reason so this skips those instances
      if ((strcmp(token, "PYSIG")!=0))
      {
        // FOR DEBUGGING
        if (debug)
        {
          Serial.print("Skipping: ");
          Serial.println(token);
        }
        // If NOT from python GUI, loop iteration is skipped
        continue;
      }

      if (debug) // Debugging output
      {
        Serial.print("FIRST: ");
        Serial.println(token);
      }

      // Get second field within python data (mode)
      token = strtok_r(NULL, ",", &i);

      // Re-init control struct to reset fields to default for new pass
      setting control;
      if (strcmp(token, "constant")==0) //CONSTANT MODE PROCESSING
      {
        //Set struct mode and then set voltage level to struct low var
        control.mode = "constant";
        control.low = atoi(strtok_r(NULL, ",", &i)); //Gets constant voltage level to set
        control.high = control.low;
        outOther = true; //Sets bool so that constant analogWriting is used
        outRamp=false;
      }
      else if (strcmp(token, "pulse")==0) //PULSE MODE PROCESSING
      {
        //Set struct variables
        control.mode = "pulse";
        control.low = atoi(strtok_r(NULL, ",", &i)); //Gets VOLT_LOW
        control.high = atoi(strtok_r(NULL, ",", &i)); //Gets VOLT_HIGH
        control.interval = atoi(strtok_r(NULL, ",", &i)); //Gets TIME_INTERVAL
        outOther=true; //Sets bool so that pulse analogWriting is used
        outRamp=false;
      }
      else if (strcmp(token, "ramp")==0) //RAMP MODE PROCESSING
      {
        //Set struct variables
        control.mode = "ramp";
        control.low = atoi(strtok_r(NULL, ",", &i)); //Gets VOLT_LOW
        control.high = atoi(strtok_r(NULL, ",", &i)); //Gets VOLT_HIGH
        control.interval = atoi(strtok_r(NULL, ",", &i)); //Gets TIME_INTERVAL
        current = control.low;
        outRamp=true; //Sets bool so that ramp analogWriting is used
        outOther=false;
      }
      else //If unrecognized mode...
      {
        if (debug) //Debug output
        {
          Serial.println("Unrecognized");
          Serial.println(token);
        }
        continue;
      }

      if (debug) //Debug output
      {
        Serial.println("MODE: " + control.mode);
        Serial.println("LOW: " + String(control.low));
        Serial.println("HIGH: " + String(control.high));
        Serial.println("MS: " + String(control.interval));
      }
      // Set prevControl to current controls just before starting next iteration
      prevControl = control;
    }
  }
  if (outOther) //If constant or pulse mode
  {
    delay(prevControl.interval); //Delay for set inverval
    analogWrite(3, prevControl.high); //Set to high V
    delay(prevControl.interval); //Delay again
    analogWrite(3, prevControl.low); //Set to low V
  }
  else if (outRamp) //If ramp output...
  {
    //Go to special ramp function
    current = rampOutput(prevControl.low, prevControl.high, prevControl.interval, current, STEP_SIZE);
  }
}
