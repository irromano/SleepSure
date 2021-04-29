/***************************************************************************
 * ADS1299 SPI Bridge
 * Tested and developed on an Adafruit Huzzah32.
 * 
 * Author: Ian Romano
 ***************************************************************************/

#include "ADS1299.h"
#include "Arduino.h"
#include <SPI.h>

/*
 *  @brief class constructor for SleepSure_ADS1299
 */
SleepSure_ADS1299::SleepSure_ADS1299(int8_t cspin, int8_t drdypin, int8_t startpin, int8_t resetpin, SPIClass *theSPI)
{
    _cs = cspin;
    _drdy = drdypin;
    _mosi = _miso = _sck = -1;
    start = startpin;
    _reset = resetpin;
    _spi = theSPI;
}
SleepSure_ADS1299::SleepSure_ADS1299(int8_t cspin, int8_t drdypin, int8_t mosipin, int8_t misopin, int8_t sckpin, int8_t startpin, int8_t resetpin)
    : _cs(cspin), _drdy(drdypin), _mosi(mosipin), _miso(misopin), _sck(sckpin), start(startpin), _reset(resetpin) {}

SleepSure_ADS1299::~SleepSure_ADS1299() {};

/*!
 *   @brief  Initialise sensor with given parameters / settings
 *   @returns true on success, false otherwise
 */
bool SleepSure_ADS1299::begin()
{
    digitalWrite(_cs, HIGH);
    pinMode(_cs, OUTPUT);
    pinMode(_drdy, INPUT);
    digitalWrite(start, LOW);
    digitalWrite(_reset, HIGH);
    pinMode(start, OUTPUT);
    pinMode(_reset, OUTPUT);
    _spi->begin();
    _spi->setFrequency(ADS1299_SPI_FREQ);

    delay(1);
    command(ADS1299_COMMAND_RESET);
    // check if sensor, i.e. the chip ID is correct
    _sensorID = read8(ADS1299_REGISTER_ID);
    if(_sensorID != 0x3E) { return false; }
    
    return true;

}

uint8_t SleepSure_ADS1299::command(uint8_t cmd)
{
    uint8_t value;
    _spi->beginTransaction(SPISettings(ADS1299_SPI_FREQ, MSBFIRST, SPI_MODE1));
    digitalWrite(_cs, LOW);
    _spi->transfer(cmd);
    value = _spi->transfer(0);
    digitalWrite(_cs, HIGH);
    _spi->endTransaction(); // release the SPI bus
    if (cmd == ADS1299_COMMAND_RESET) { delay(1); }
    return value;
}

/*!
 *   @brief  Reads a 8 bit value SPI
 *   @param reg the register address to read from
 *   @returns the 8 bit data value read from the device
 */
uint8_t SleepSure_ADS1299::read8(uint8_t reg)
{
    uint8_t value;

    _spi->beginTransaction(SPISettings(ADS1299_SPI_FREQ, MSBFIRST, SPI_MODE1));
    digitalWrite(_cs, LOW);

    _spi->transfer(ADS1299_COMMAND_SDATAC);
    uint8_t commandReg = ADS1299_COMMAND_RREG | reg;
    //_spi->transfer(ADS1299_COMMAND_START);
    _spi->transfer(commandReg);
    _spi->transfer(0);
    value = _spi->transfer(0);
    _spi->transfer(ADS1299_COMMAND_RDATAC);

    digitalWrite(_cs, HIGH);
    _spi->endTransaction(); // release the SPI bus

    return value;
}

uint8_t SleepSure_ADS1299::getID()
{
    return _sensorID;
}

