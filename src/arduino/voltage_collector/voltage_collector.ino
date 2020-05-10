//#include <iostream>
//#include <sstream>
//#include <string>
static const int analogPins[] = {0, 1, 2, 3, 4};
static byte out[20];


void setup() {
  // put your setup code here, to run when Arduino is powered on:
  Serial.begin(2000000);  // Opens the Serial Port w/ a baud rate of 38400
//  delay(5); // Just to be safe
}

void loop() {
  // Store the incoming voltage from each pin [int is 2 bytes (16 bits)]
  for (int pin = 0; pin < 5 ; pin++) {
    int val = analogRead(analogPins[pin]);
    Serial.println(val);
//    delay(.1);  // This is fickle; decide if necessary
//    Serial.flush();
  }
}

//void loop() {
//  // Store the incoming voltage from each pin [int is 2 bytes (16 bits)]
////  byte out[] = new byte[20];
//  for (int pin = 0; pin < 5 ; pin++) {
//    int val = analogRead(analogPins[pin]);
//    out[pin * 2] = highByte(val);
//    out[pin * 2 + 1] = lowByte(val);
//    out[pin*2 + 2] = byte('\r');
//    out[pin*2 + 3] = byte('\n');
////    Serial.println(val);
////    delay(.1);  // This is fickle; decide if necessary
////    Serial.flush();
//  }
//  Serial.write(out, 20);
//  Serial.flush();
//}

//void loop() {
//  // Store the incoming voltage from each pin [int is 2 bytes (16 bits)]
//  String s = "";
//  for (int pin = 0; pin < 5 ; pin++) {
//    int val = analogRead(analogPins[pin]);
////    Serial.println(val);
////    delay(.1);  // This is fickle; decide if necessary
////    Serial.flush();
//    s += String(val) + "\n" + "\r"; // + "\n";
//  }
//  Serial.print(s);
//}
