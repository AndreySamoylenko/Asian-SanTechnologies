
/*----------------------MOTORS-------------------------*/
#define ma1 4
#define ma2 5
#define mb1 6
#define mb2 7
#define mc2 15
#define mc1 16
#define md2 17
#define md1 18
/*-----------------------MISC---------------------------*/
#define BTN_PIN 14
#define BZ_PIN 1


void setup() {
  Serial.begin(115200);
  /*--------PWM---------*/
  pinMode(ma1, OUTPUT);
  pinMode(ma2, OUTPUT);
  pinMode(mb1, OUTPUT);
  pinMode(mb2, OUTPUT);
  pinMode(mc1, OUTPUT);
  pinMode(mc2, OUTPUT);
  pinMode(md1, OUTPUT);
  pinMode(md2, OUTPUT);

  /*--------ADC---------*/
  // adc_power_on();
  // adc1_config_channel_atten(9, 11);
  // adc2_config_channel_atten(0, 11);
  // adc2_config_channel_atten(1, 11);
  // adc2_config_channel_atten(2, 11);
  // adc1_config_width(12);
  // adc2_config_width(12);
  // put your setup code here, to run once:
}

void loop() {

  // for(int i = -180;i<=180;i++){
  //   driveAngle(255,i);
  //   delay(30);
  // }
  for(int i = 0;i<1024;i++){
  driveAngle(i, 0);
  delay(30);
  }
  delay(5000);
  // Serial.print(adc1_get_raw(9));
  // Serial.print('\t');
  // Serial.print(adc2_get_raw(0));
  // Serial.print('\t');
  // Serial.print(adc2_get_raw(1));
  // Serial.print('\t');
  // Serial.print(adc2_get_raw(2));
  // Serial.print('\t');
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
  spa = constrain(spa, -255, 1000);
  spb = constrain(spb, -255, 1000);
  spc = constrain(spc, -255, 1000);
  spd = constrain(spd, -255, 1000);


  analogWrite(ma1, spa > 0 ? spa : 0);
  analogWrite(ma2, spa < 0 ? -spa : 0);
  // Serial.print(spa > 0 ? spa : 0);
  // Serial.print('\t');
  // Serial.println(spa < 0 ? spa : 0);

  analogWrite(mb1, spb > 0 ? spb : 0);
  analogWrite(mb2, spb < 0 ? -spb : 0);

  analogWrite(mc1, spc > 0 ? spc : 0);
  analogWrite(mc2, spc < 0 ? -spc : 0);

  analogWrite(md1, spd > 0 ? spd : 0);
  analogWrite(md2, spd < 0 ? -spd : 0);
}

// 1000 шагов энкодера это примерно 37.5 см
