
void encl() {
  countl++;
}
void encr() {
  countr++;
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

  analogWrite(mb1, spb > 0 ? spb : 0);
  analogWrite(mb2, spb < 0 ? -spb : 0);

  analogWrite(mc1, spc > 0 ? spc : 0);
  analogWrite(mc2, spc < 0 ? -spc : 0);

  analogWrite(md1, spd > 0 ? spd : 0);
  analogWrite(md2, spd < 0 ? -spd : 0);
}

void stop(){
  drive(0,0,0,0);
}
