/***************************************************************************
 * Designed to test the ADS1299 bridge with an ESP32 processor. 
 * Tested and developed on an Adafruit Huzzah32.
 * 
 * Author: Ian Romano
 ***************************************************************************/

#include <SPI.h>
#include <ADS1299.h>

#define BME_CS 14
#define ADS_DRDY 15
#define ADS_START 27
#define ADS_RESET 32

#define CHANNELS 8

SleepSure_ADS1299 ads(BME_CS, ADS_DRDY, ADS_START, ADS_RESET);

int* values;

void setup() 
{
    Serial.begin(115200);
    while(!Serial);
    Serial.println("ADS1299 test");
    
    values = new int[CHANNELS];

    bool pass = ads.begin();
    if (!pass)
    {
        Serial.println("ADS1299 ID not recieved correctly.");
    }
    Serial.print("Detected sensor ID: ");
    Serial.println(ads.getID(), 16);
}


void loop()
{ 
    ads.readChannels(values, CHANNELS);
    printValues();
    delay(100);
}

void printValues()
{
  for(int i=1; i<CHANNELS +1; i++)
  {
        Serial.print("Channel ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(values[i]);
  }

}