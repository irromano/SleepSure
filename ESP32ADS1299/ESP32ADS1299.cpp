//
//  ADS1299.cpp
//  
//  Created by Conor Russomanno on 6/17/13.
//
#include "arduino.h"

#include <SPI.h>
#include "pins_arduino.h"
#include "ESP32ADS1299.h"

void ADS1299::setup(int8_t _DRDY, int8_t _CS){
    
    DRDY = _DRDY;
    CS = _CS;
    pinMode(DRDY, INPUT);
    pinMode(CS, OUTPUT);
    //Initialize SPI
    _spi->begin();
    _spi->setDataMode(SPI_MODE1);

    //Set clock speed to 80MHz
    //SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));

    // Set direction register for SCK and MOSI pin.
    // MISO pin automatically overrides to INPUT.
    // When the SS pin is set as OUTPUT, it can be used as
    // a general purpose output port (it doesn't influence
    // SPI operations).
    /*
    pinMode(SCK, OUTPUT);
    pinMode(MOSI, OUTPUT);
    pinMode(SS, OUTPUT);
    
    digitalWrite(SCK, LOW);
    digitalWrite(MOSI, LOW);
    digitalWrite(SS, HIGH);
    */
    // Warning: if the CS pin ever becomes a LOW INPUT then SPI
    // automatically switches to Slave, so the data direction of
    // the CS pin MUST be kept as OUTPUT.

    //SPCR |= _BV(MSTR);  // Sets ESP to master
    //SPCR |= _BV(SPE);   // Enable SPI
    
    //set clock divider 
    //SPCR = (SPCR & ~SPI_CLOCK_MASK) | (SPI_CLOCK_DIV16 & SPI_CLOCK_MASK);  //Divides 16MHz clock by 16 to set CLK speed to 1MHz
    //SPSR = (SPSR & ~SPI_2XCLOCK_MASK) | ((SPI_CLOCK_DIV16 >> 2) & SPI_2XCLOCK_MASK); //Divides 16MHz clock by 16 to set CLK speed to 1MHz
    
    //set data mode SPI_MODE1
    //SPCR = (SPCR & ~SPI_MODE_MASK) | SPI_DATA_MODE; //clock polarity = 0; clock phase = 1 (pg. 8)
    
    //set bit order
    //SPCR &= ~(_BV(DORD)); // SPI data format is MSB (pg. 25)
    
    tCLK = 0.000488; //488 ns (Datasheet, pg. 8)
    outputCount = 0;
}

//System Commands
void ADS1299::WAKEUP() {
    digitalWrite(CS, LOW); //Low to communicate
    _spi->transfer(_WAKEUP);
    digitalWrite(CS, HIGH); //High to end communication
    delay(4.0*tCLK);  //must way at least 4 tCLK cycles before sending another command (Datasheet, pg. 35)
}
void ADS1299::STANDBY() {
    digitalWrite(CS, LOW);
    _spi->transfer(_STANDBY);
    digitalWrite(CS, HIGH);
}
void ADS1299::RESET() {
    digitalWrite(CS, LOW);
    _spi->transfer(_RESET);
    delay(10);
//    delay(18.0*tCLK); //must wait 18 tCLK cycles to execute this command (Datasheet, pg. 35)
    digitalWrite(CS, HIGH);
}
void ADS1299::START() {
    digitalWrite(CS, LOW);
    _spi->transfer(_START);
    digitalWrite(CS, HIGH);
}
void ADS1299::STOP() {
    digitalWrite(CS, LOW);
    _spi->transfer(_STOP);
    digitalWrite(CS, HIGH);
}
//Data Read Commands
void ADS1299::RDATAC() {
    digitalWrite(CS, LOW);
    _spi->transfer(_RDATAC);
    digitalWrite(CS, HIGH);
}
void ADS1299::SDATAC() {
    digitalWrite(CS, LOW);
    _spi->transfer(_SDATAC);
    digitalWrite(CS, HIGH);
}
void ADS1299::RDATA() {
    digitalWrite(CS, LOW);
    _spi->transfer(_RDATA);
    digitalWrite(CS, HIGH);
}

//Register Read/Write Commands
void ADS1299::getDeviceID() {
    digitalWrite(CS, LOW); //Low to communicated
    _spi->transfer(_SDATAC); //SDATAC
    _spi->transfer(_RREG); //RREG
    _spi->transfer(0x00); //Asking for 1 byte
    byte data = _spi->transfer(0x00); // byte to read (hopefully 0b???11110)
    _spi->transfer(_RDATAC); //turn read data continuous back on
    digitalWrite(CS, HIGH); //Low to communicated
    Serial.println(data, BIN);
}

void ADS1299::RREG(byte _address) {
    byte opcode1 = _RREG + _address; //001rrrrr; _RREG = 00100000 and _address = rrrrr
    digitalWrite(CS, LOW); //Low to communicated
    _spi->transfer(_SDATAC); //SDATAC
    _spi->transfer(opcode1); //RREG
    _spi->transfer(0x00); //opcode2
    byte data = _spi->transfer(0x00); // returned byte should match default of register map unless edited manually (Datasheet, pg.39)
    printRegisterName(_address);
    Serial.print("0x");
    if(_address<16) Serial.print("0");
    Serial.print(_address, HEX);
    Serial.print(", ");
    Serial.print("0x");
    if(data<16) Serial.print("0");
    Serial.print(data, HEX);
    Serial.print(", ");
    for(byte j = 0; j<8; j++){
        Serial.print(bitRead(data, 7-j), BIN);
        if(j!=7) Serial.print(", ");
    }
    _spi->transfer(_RDATAC); //turn read data continuous back on
    digitalWrite(CS, HIGH); //High to end communication
    Serial.println();
}

void ADS1299::RREG(byte _address, byte _numRegistersMinusOne) {
    byte opcode1 = _RREG + _address; //001rrrrr; _RREG = 00100000 and _address = rrrrr
    digitalWrite(CS, LOW); //Low to communicated
    _spi->transfer(_SDATAC); //SDATAC
    _spi->transfer(opcode1); //RREG
    _spi->transfer(_numRegistersMinusOne); //opcode2
    for(byte i = 0; i <= _numRegistersMinusOne; i++){
        byte data = _spi->transfer(0x00); // returned byte should match default of register map unless previously edited manually (Datasheet, pg.39)
        printRegisterName(i);
        Serial.print("0x");
        if(i<16) Serial.print("0"); //lead with 0 if value is between 0x00-0x0F to ensure 2 digit format
        Serial.print(i, HEX);
        Serial.print(", ");
        Serial.print("0x");
        if(data<16) Serial.print("0"); //lead with 0 if value is between 0x00-0x0F to ensure 2 digit format
        Serial.print(data, HEX);
        Serial.print(", ");
        for(byte j = 0; j<8; j++){
            Serial.print(bitRead(data, 7-j), BIN);
            if(j!=7) Serial.print(", ");
        }
        Serial.println();
    }
    _spi->transfer(_RDATAC); //turn read data continuous back on
    digitalWrite(CS, HIGH); //High to end communication
}

void ADS1299::WREG(byte _address, byte _value) {
    byte opcode1 = _WREG + _address; //001rrrrr; _RREG = 00100000 and _address = rrrrr
    digitalWrite(CS, LOW); //Low to communicated
    _spi->transfer(_SDATAC); //SDATAC
    _spi->transfer(opcode1);
    _spi->transfer(0x00);
    _spi->transfer(_value);
    _spi->transfer(_RDATAC);
    digitalWrite(CS, HIGH); //Low to communicated
    Serial.print("Register 0x");
    Serial.print(_address, HEX);
    Serial.println(" modified.");
}
//
//void ADS1299::WREG(byte _address, byte _value, byte _numRegistersMinusOne) {
//    
//}

void ADS1299::updateData(){
    if(digitalRead(DRDY) == LOW){
        digitalWrite(CS, LOW);
//        long output[100][9];
        long output[9];
        long dataPacket;
        for(int i = 0; i<9; i++){
            for(int j = 0; j<3; j++){
                byte dataByte = _spi->transfer(0x00);
                dataPacket = (dataPacket<<8) | dataByte;
            }
//            output[outputCount][i] = dataPacket;
            output[i] = dataPacket;
            dataPacket = 0;
        }
        digitalWrite(CS, HIGH);
        Serial.print(outputCount);
        Serial.print(", ");
        for (int i=0;i<9; i++) {
            Serial.print(output[i], HEX);
            if(i!=8) Serial.print(", ");
            
        }
        Serial.println();
        outputCount++;
    }
}

// String-Byte converters for RREG and WREG
void ADS1299::printRegisterName(byte _address) {
    if(_address == ID){
        Serial.print("ID, ");
    }
    else if(_address == CONFIG1){
        Serial.print("CONFIG1, ");
    }
    else if(_address == CONFIG2){
        Serial.print("CONFIG2, ");
    }
    else if(_address == CONFIG3){
        Serial.print("CONFIG3, ");
    }
    else if(_address == LOFF){
        Serial.print("LOFF, ");
    }
    else if(_address == CH1SET){
        Serial.print("CH1SET, ");
    }
    else if(_address == CH2SET){
        Serial.print("CH2SET, ");
    }
    else if(_address == CH3SET){
        Serial.print("CH3SET, ");
    }
    else if(_address == CH4SET){
        Serial.print("CH4SET, ");
    }
    else if(_address == CH5SET){
        Serial.print("CH5SET, ");
    }
    else if(_address == CH6SET){
        Serial.print("CH6SET, ");
    }
    else if(_address == CH7SET){
        Serial.print("CH7SET, ");
    }
    else if(_address == CH8SET){
        Serial.print("CH8SET, ");
    }
    else if(_address == BIAS_SENSP){
        Serial.print("BIAS_SENSP, ");
    }
    else if(_address == BIAS_SENSN){
        Serial.print("BIAS_SENSN, ");
    }
    else if(_address == LOFF_SENSP){
        Serial.print("LOFF_SENSP, ");
    }
    else if(_address == LOFF_SENSN){
        Serial.print("LOFF_SENSN, ");
    }
    else if(_address == LOFF_FLIP){
        Serial.print("LOFF_FLIP, ");
    }
    else if(_address == LOFF_STATP){
        Serial.print("LOFF_STATP, ");
    }
    else if(_address == LOFF_STATN){
        Serial.print("LOFF_STATN, ");
    }
    else if(_address == GPIO){
        Serial.print("GPIO, ");
    }
    else if(_address == MISC1){
        Serial.print("MISC1, ");
    }
    else if(_address == MISC2){
        Serial.print("MISC2, ");
    }
    else if(_address == CONFIG4){
        Serial.print("CONFIG4, ");
    }
}

//SPI communication methods
/*byte ADS1299::transfer(byte _data) {
    return SPI.transfer(_data);
    /*SPDR = _data;
    while (!(SPSR & _BV(SPIF)))
        ;
    return SPDR;
}*/
