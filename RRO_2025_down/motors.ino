
void encl() {
  countl++;
}
void encr() {
  countr++;
}



double rads(double a) {
  return (a / 180.0) * 3.141592653589;
}

void drive(float spa, float spb, float spc, float spd) {
  spa = constrain(spa, -255, 255);
  spb = constrain(spb, -255, 255);
  spc = constrain(spc, -255, 255);
  spd = constrain(spd, -255, 255);


  analogWrite(ma1, spa > 0 ? spa : 0);
  analogWrite(ma2, spa < 0 ? -spa : 0);

  analogWrite(mb1, spb > 0 ? spb : 0);
  analogWrite(mb2, spb < 0 ? -spb : 0);

  analogWrite(mc1, spc > 0 ? spc : 0);
  analogWrite(mc2, spc < 0 ? -spc : 0);

  analogWrite(md1, spd > 0 ? spd : 0);
  analogWrite(md2, spd < 0 ? -spd : 0);

  // Serial.println(abs(spc));
}

void stop(){
  digitalWrite(ma1,1);
  digitalWrite(ma2,1);
  digitalWrite(mb1,1);
  digitalWrite(mb2,1);
  digitalWrite(mc1,1);
  digitalWrite(mc2,1);
  digitalWrite(md1,1);
  digitalWrite(md2,1);
}
