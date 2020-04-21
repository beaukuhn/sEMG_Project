#define BUFFER_LENGTH 40  // 10 bytes (5 integers)
#define BYTES 2

byte buf[BUFFER_LENGTH];
static const int analogPins[] = {0, 1, 2, 3, 4};
byte byteArray[BYTES];

void setup() {
  // put your setup code here, to run when Arduino is powered on:
  Serial.begin(9600);  // Opens the Serial Port w/ a baud rate of 38400
  delay(5);
}

/**
   Splits integer into 2 bytes and stores in bytearray

   @param num is the input integer to be split
   @return byteArray containing 2 bytes w/ each representing 1/2 of the integer
*/
//byte* getBytes(int num) {
//  Serial.write((num >> 8) && 0xFF);
////  Serial.print(num);
//  //  Serial.print(num);
//  //  Serial.print('\n');
//  byte t = (byte) ((num >> 8) && 0xFF);
////  Serial.print(t);
////  Serial.print('\n');
//  byteArray[1] = (byte) ((num >> 8) && 0xFF);  // get first byte
//  byteArray[0] = (byte) (num && 0xFF);  // get second byte
//  //  Serial.print(byteArray[0]);
//  //  Serial.print("\n");
//  //  Serial.print(sizeof(num));
//  return byteArray;
//}

/**
   Stores byte array within adjacent cells in buffer

   @param byteArray is a length 2 byte array that represents an int
   @param index location where first half of read int is stored in buffer
*/
//void storeBytes (byte* byteArray, int index) {
//  //  Serial.print(byteArray[0]);
//  //  Serial.print(byteArray[1]);
//  buf[index] = byteArray[0];
//  buf[index + 1] = byteArray[1];
//}

void loop() {
  // Store the incoming voltage [int is 2 bytes (16 bits)]
  for (int pin = 0; pin < 5 ; pin++) {
    int val = analogRead(analogPins[pin]);
    byteArray[1] = highByte(val);
    byteArray[0] = lowByte(val);
    Serial.write(byteArray, 2);
    delay(3);
//    Serial.flush();
  }
}
