//
//  ADS1299.h
//  
//  Created by Conor Russomanno on 6/17/13.
//

#ifndef ____ADS1299__
#define ____ADS1299__

#include <stdio.h>
#include "Arduino.h"
#include <Adafruit_Sensor.h>
#include <SPI.h>
#include "Definitions.h"


class ADS1299 {
public:
    
    void setup(int8_t _DRDY, int8_t _CS);
    
    //ADS1299 SPI Command Definitions (Datasheet, Pg. 35)
    //System Commands
    void WAKEUP();
    void STANDBY();
    void RESET();
    void START();
    void STOP();
    
    //Data Read Commands
    void RDATAC();
    void SDATAC();
    void RDATA();
    
    //Register Read/Write Commands
    void getDeviceID();
    void RREG(byte _address);
    void RREG(byte _address, byte _numRegistersMinusOne); //to read multiple consecutive registers (Datasheet, pg. 38)
    
    void printRegisterName(byte _address);
    
    void WREG(byte _address, byte _value); //
    void WREG(byte _address, byte _value, byte _numRegistersMinusOne); //
    
    void updateData();
    
    //SPI Arduino Library Stuff
    /*byte transfer(byte _data);*/

    //------------------------//
    void attachInterrupt();
    void detachInterrupt(); // Default
    void begin(); // Default
    void end();
    void setBitOrder(uint8_t);
    void setDataMode(uint8_t);
    void setClockDivider(uint8_t);
    //------------------------//
    
    float tCLK;
    int8_t DRDY, CS; //pin numbers for "Data Ready" (DRDY) and "Chip Select" CS
    int32_t _sensorID;

    int8_t outputCount;
    
protected:
    SPIClass *_spi = &SPI;
    
};

#endif