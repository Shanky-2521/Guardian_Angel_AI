#include <Wire.h>

void setup() {
  Serial.begin(115200);
  while(!Serial){}
  Wire.begin();
  Serial.println("I2C Scanner");
}

void loop() {
  byte count = 0;
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("Found: 0x");
      if (address < 16) Serial.print("0");
      Serial.print(address, HEX);
      Serial.println();
      count++;
    }
  }
  Serial.print("Devices: ");
  Serial.println(count);
  delay(2000);
}
