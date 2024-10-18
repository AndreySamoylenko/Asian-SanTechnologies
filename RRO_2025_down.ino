#define ma1
#define ma2
#define mb1
#define mb2
#define mc1
#define mc2
#define md1
#define md2


void setup() {
  // put your setup code here, to run once:
}

void loop() {
  // put your main code here, to run repeatedly:
}

void driveAngle(uint8_t sped, float angle) {
  float spa, spb, spc, spd;
  angle = -angle+45;

  spa = cos(rads(angle)) * sped;
  spc = spa /* *k */;
  spb = sin(rads(angle)) * sped;
  spd = spb /* *k */;
  
  drive(spa,spb,spc,spd);
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
// Я считаю, что этот код слишком сложный для моего понимания
