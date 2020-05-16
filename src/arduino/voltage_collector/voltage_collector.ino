static const int analogPins[] = {0, 1, 2, 3, 4};
int numSamples = 0;
void setup()
{
  Serial.begin(115200);

  ADCSRA = 0;             // clear ADCSRA register
  ADCSRB = 0;             // clear ADCSRB register
  ADMUX |= (0 & 0x07);    // set A0 analog input pin
  ADMUX |= (1 << REFS0);  // set reference voltage
  ADMUX |= (1 << ADLAR);  // left align ADC value to 8 bits from ADCH register

  // sampling rate is [ADC clock] / [prescaler] / [conversion clock cycles]
  // for Arduino Uno ADC clock is 16 MHz and a conversion takes 13 clock cycles
  //ADCSRA |= (1 << ADPS2) | (1 << ADPS0);    // 32 prescaler for 38.5 KHz
  ADCSRA |= (1 << ADPS2);                     // 16 prescaler for 76.9 KHz
  //ADCSRA |= (1 << ADPS1) | (1 << ADPS0);    // 8 prescaler for 153.8 KHz

  ADCSRA |= (1 << ADATE); // enable auto trigger
  ADCSRA |= (1 << ADIE);  // enable interrupts when measurement complete
  ADCSRA |= (1 << ADEN);  // enable ADC
  ADCSRA |= (1 << ADSC);  // start ADC measurements
}


void loop() {
//  int i = 0;
  // Store the incoming voltage from each pin [int is 2 bytes (16 bits)]
  for (int pin = 0; pin < 5 ; pin++) {
    int val = analogRead(analogPins[pin]);
    Serial.print(val);
    if (pin < 4) {
      Serial.print(','); 
    }
//    Serial.print(String(val) + '-' + String(pin));
//    Serial.print(',');
//    Serial.println();
//    delay(.1);  // This is fickle; decide if necessary
//    Serial.flush();
  }
//  i += 1;
//  serial.print(i);
  Serial.println();
  Serial.flush();
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
