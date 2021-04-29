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

SleepSure_ADS1299 ads(BME_CS, ADS_DRDY, ADS_START, ADS_RESET);

void setup() 
{
    Serial.begin(115200);
    while(!Serial);
    Serial.println("ADS1299 test");

    unsigned status;

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
    delay(delayTime);
}