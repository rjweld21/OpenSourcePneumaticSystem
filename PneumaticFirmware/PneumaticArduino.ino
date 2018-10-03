//#include <Indio.h>
//#include <Wire.h>
//#include <UC1701.h>
#include <String.h>

char temp[10] = '';
int index = 0;
int output[3];
void mode = constant;

void constant()
{
  aChar = ''
}

void pulse()
{
  aChar = ''
}

void ramp()
{
  aChar = ''
}

void setup()
{
  Serial.begin(9800);
}

void loop()
{
  while(Serial.available() > 0)
  {
    char aChar = Serial.read();

    if(aChar == '\n')
    {
      index = 0;
      inData[index] = NULL; 
    }
    else
    {
      temp[index] = aChar;
      index++;
      temp[index] = '\0';
    }
  }
}
