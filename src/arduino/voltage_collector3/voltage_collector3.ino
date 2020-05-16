volatile int numSamples=0;
volatile int currPin = 0;
volatile int r0, r0u;

void setup(){
  Serial.begin(2000000);
    ADMUX = 0;  // reset pins
    ADCSRA = 0;  // make sure ADC is on
    ADCSRB = 0;  // reset ADCSRB
    ADCSRA |= (1 << ADIE);  // interupt after single ADC
    ADCSRA |= (1 << ADATE); // auto-trigger
      // reset ADMUX; use internal power
    ADMUX |= (1 << MUX0);    // set 0th pin
    ADMUX &= ~(1 << ADLAR);
    ADMUX |= (1 << ADLAR);  // left align ADC value to 8 bits from ADCH register
    ADCSRB &= 0xF8;  // enable free running
  // sampling rate is [ADC clock] / [prescaler] / [conversion clock cycles]
  // for Arduino Uno ADC clock is 16 MHz and a conversion takes 13 clock cycles
  // ADCSRA |= (1 << ADPS2);                     // 76.9 KHz
    ADCSRA |= (1 << ADPS1) | (1 << ADPS0);    // 153.8 KHz
    ADCSRA |= (1 << ADSC);  // start conversions
}

ISR(ADC_vect) {
  r0 = ADCL;
  r0 |= ADCH << 8;
  if (curr_pin < 4) {
    curr_pin++;
  } else {
    curr_pin = 0;
  }
  ADMUX++;
}
  
void loop() {
  r0u = r0;
  Serial.print(r0u);
}
