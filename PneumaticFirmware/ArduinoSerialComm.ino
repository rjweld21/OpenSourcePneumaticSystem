#include <string.h>
#include <stdio.h>

struct setting
{
  String mode="None";
  int interval=0;
  int low=0;
  int high=0;
  bool changed=false;
};

bool debug = true;
String data;
char *cData, *i, *token;
int mode=0, charlen; //0 - constant, 1 - pulse, 2 - ramp
const char delim = ',';
setting prevControl, control;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

setting setupConstant(char *pyData, setting prevControl)
{
  setting params;
  char *r;

  Serial.println(pyData);

  //Get token for PYSIG and "constant" indices
  token = strtok_r(pyData, ",", &r);
  Serial.println(token);
  token = strtok_r(NULL, ",", &r);
  
  //Get voltage level for constant
  token = strtok_r(NULL, ",", &r);
  Serial.println(token);
  
  params.mode = "constant";
  params.low = (int)*token;
  

  return params;
}

void checkChange(setting *currentSetting, setting *previousSetting)
{
  if (currentSetting->mode != previousSetting->mode || 
      currentSetting->low != previousSetting->low ||
      currentSetting->high != previousSetting->high ||
      currentSetting->interval != previousSetting->interval)
  {
    currentSetting->changed = true;
  }
}

void loop() {
  
  
  // Enter loop to read serial buffer
  while (Serial.available() > 0)
  {
    // Read line of serial data from computer
    data = Serial.readStringUntil('\n');

    // If on last pass for reading...
    if (Serial.available() == 0)
    {
      if (debug) {Serial.println("\n=");}
      
      //charlen = (int)strlen(data)
      char tempChar[data.length()];
      data.toCharArray(tempChar, data.length());
      cData = tempChar;

      /* DATA FORMATS
       * CONSTANT: PYSIG,constant,VOLT_LEVEL 
       * PULSE:    PYSIG,pulse,VOLT_LOW,VOLT_HIGH,TIME_INTERVAL
       * RAMP:     PYSIG,ramp,VOLT_LOW,VOLT_HIGH,TIME_INTERVAL
      */
      
      // Confirm data has been sent by GUI python program
      token = strtok_r(cData, ",", &i);

      // Check if current data is NOT from python GUI
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

      if (debug)
      {
        Serial.print("FIRST: ");
        Serial.println(token);
      }

      // Get second field within python data (mode)
      token = strtok_r(NULL, ",", &i);

      // Re-init control struct to reset fields to default
      setting control;
      if (strcmp(token, "constant")==0) //CONSTANT MODE PROCESSING
      {
        //Set struct mode and then set voltage level to struct low var
        control.mode = "constant";
        control.low = atoi(strtok_r(NULL, ",", &i)); //Gets constant voltage level to set
      }
      else if (strcmp(token, "pulse")==0) //PULSE MODE PROCESSING
      {
        //Set struct variables
        control.mode = "pulse";
        control.low = atoi(strtok_r(NULL, ",", &i)); //Gets VOLT_LOW
        control.high = atoi(strtok_r(NULL, ",", &i)); //Gets VOLT_HIGH
        control.interval = atoi(strtok_r(NULL, ",", &i)); //Gets TIME_INTERVAL
      }
      else if (strcmp(token, "ramp")==0) //RAMP MODE PROCESSING
      {
        //Set struct variables
        control.mode = "ramp";
        control.low = atoi(strtok_r(NULL, ",", &i)); //Gets VOLT_LOW
        control.high = atoi(strtok_r(NULL, ",", &i)); //Gets VOLT_HIGH
        control.interval = atoi(strtok_r(NULL, ",", &i)); //Gets TIME_INTERVAL
      }
      else
      {
        Serial.println("Unrecognized");
        Serial.println(token);
        continue;
      }

      if (debug)
      {
        Serial.println("MODE: " + control.mode);
        Serial.println("LOW: " + String(control.low));
        Serial.println("HIGH: " + String(control.high));
        Serial.println("MS: " + String(control.interval));
      }

      // Check if current control params and params from last iteration have changed
      checkChange(&control, &prevControl);
      Serial.println("CHANGED: " + String(control.changed));

      // Set prevControl to current controls just before starting next iteration
      prevControl = control;
    }
  }
}
