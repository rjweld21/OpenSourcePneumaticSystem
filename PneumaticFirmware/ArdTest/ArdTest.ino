#include <string.h>
#include <stdio.h>

String data;
char *cData;
int mode=0; //0 - constant, 1 - pulse, 2 - ramp
int SDAC, EDAC, MS;
int charlen;
const char delim[2] = ",";
char *token;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("HELLO");
}

void sWrite(String header, char *s)
{
  Serial.println(header);
  Serial.println(s);
}

void loop() {
  
  // Enter loop to read serial buffer
  while (Serial.available() > 0)
  {
    // Read line of serial data from computer
    data = Serial.readStringUntil('\n');

    // Rewrite data back to buffer
    //Serial.println(data);

    // If on last pass for reading...
    if (Serial.available() == 0)
    {
      //charlen = (int)strlen(data)
      data.toCharArray(cData, data.length());

      Serial.println("Char Data ");
      for (int i=0; i<data.length(); i++)
      {
        Serial.print(&cData[i]);
      }
      //sWrite("CHAR DATA", cData);
      Serial.println("DATA");
      Serial.println(data);
      Serial.println(data.length());
      
      // Confirm data has been sent by GUI python program
      token = strtok(cData, delim);
      Serial.println("FIRST");
      Serial.println(token);
      
      if (~(token == "PYSIG")) // Otherwise, exit
      {
        Serial.println("Skipping...");
        Serial.println(token);
        continue;
      }
      
      token = strtok(NULL, delim);
      Serial.println("SECOND");
      Serial.println(token);
      
      if (token == "constant")
      {
        Serial.println("constant");
      }
      else if (token == "pulse")
      {
        Serial.println("pulse");
      }
      else
      {
        Serial.println("ramp");
      }
    }
  }
}
