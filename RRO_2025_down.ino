
/*----------------------MOTORS-------------------------*/
#define ma1 4
#define ma2 5
#define mb1 6
#define mb2 7
#define mc1 15
#define mc2 16
#define md1 17
#define md2 18
/*-----------------------MISC---------------------------*/
#define BTN_PIN 14
#define BZ_PIN 1


void setup() {
  /*--------ADC---------*/
  adc_power_on();
  adc1_config_channel_atten(9, 11);
  adc2_config_channel_atten(0, 11);
  adc2_config_channel_atten(1, 11);
  adc2_config_channel_atten(2, 11);
  adc1_config_width(12);
  adc2_config_width(12);
  // put your setup code here, to run once:
}

void loop() {
  Serial.print(adc1_get_raw(9));
  Serial.print('\t');
  Serial.print(adc2_get_raw(0));
  Serial.print('\t');
  Serial.print(adc2_get_raw(1));
  Serial.print('\t');
  Serial.print(adc2_get_raw(2));
  Serial.print('\t');
  // put your main code here, to run repeatedly:
}

void driveAngle(uint8_t sped, float angle) {
  float spa, spb, spc, spd;
  angle = -angle + 45;

  spa = cos(rads(angle)) * sped;
  spc = spa /* *k */;
  spb = sin(rads(angle)) * sped;
  spd = spb /* *k */;

  drive(spa, spb, spc, spd);
}

double rads(double a) {
  return (a / 180.0) * 3.141592653589;
}

void drive(float spa, float spb, float spc, float spd) {
  spa = constrain(sp1, -255, 255);
  spb = constrain(sp1, -255, 255);
  spc = constrain(sp1, -255, 255);
  spd = constrain(sp1, -255, 255);

  analogWrite(ma1, spa > 0 ? spa : 0);
  analogWrite(ma2, spa < 0 ? spa : 0);

  analogWrite(mb1, spb > 0 ? spb : 0);
  analogWrite(mb2, spb < 0 ? spb : 0);

  analogWrite(mc1, spc > 0 ? spc : 0);
  analogWrite(mc2, spc < 0 ? spc : 0);

  analogWrite(md1, spd > 0 ? spd : 0);
  analogWrite(md2, spd < 0 ? spd : 0);
}

// 1000 шагов энкодера это примерно 37.5 см
