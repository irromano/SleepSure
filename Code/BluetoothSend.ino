//This is based on the example code provided by the ESP32 board
//Author: Matias Saavedra Silva

#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
int count = 65;

void setup() {
  Serial.begin(9600);
  SerialBT.begin("SleepSure"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
}

void loop() {
  if(count > 500) {
    count = count-400;
  }
  String s = String(count);
  for(int i=0;i<s.length();i++) {
    SerialBT.write(int(s[i]));
  }
  SerialBT.write(10);
  count++;
//  if (Serial.available()) {
//    SerialBT.write(Serial.read());
//  }
//  if (SerialBT.available()) {
//    Serial.write(SerialBT.read());
//  }
  delay(100);
}
