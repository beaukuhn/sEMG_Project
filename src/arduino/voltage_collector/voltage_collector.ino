#define BYTES 2

static const int analogPins[] = {0, 1, 2, 3, 4};
byte byteArray[BYTES];

void setup() {
  // put your setup code here, to run when Arduino is powered on:
  Serial.begin(9600);  // Opens the Serial Port w/ a baud rate of 38400
  delay(5);
}

void loop() {
  // Store the incoming voltage from each pin [int is 2 bytes (16 bits)]
  for (int pin = 0; pin < 5 ; pin++) {
    int val = analogRead(analogPins[pin]);
    byteArray[1] = highByte(val);
    byteArray[0] = lowByte(val);
    Serial.write(byteArray, 2);
    delay(3);  // This is fickle
    // Serial.flush();
  }
}
