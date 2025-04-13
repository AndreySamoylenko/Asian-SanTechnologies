
#define MIN_SPEED 80
#define MIN_SPEED 80

void floor_distinction() {
  AllDiagonal();
  delay(300);
  MoveSync(150, -150, 90, 1);
  delay(200);
}

void FromNormalToInverse(int way) {
  if (abs(way) == 1) {
    pidEnc(2, 0, 1, way * 200, 400, 0);
    MoveSync(way * 255, way * 255, 50, 0);
  }
  inverse = 1;
  pidEnc(1.5, 0.01, 0.2, way * 255, 2800 - (abs(way) == 1) * 400, 1);
}

void FromInverseToNormal(int way) {
  int deg = 0;
  if (abs(way) > 1) {
    way /= 2;
    deg = 1400;
    beep(200, 200);
    pidEnc(3, 0, 1, way * 240, 400, 0);
  }

  pidEnc(3, 0, 1, way * 110, 900, 0);
  pidEnc(3, 0, 1, way * 80, 1650 - deg, 1);

  inverse = 0;
  // pidEnc(3, 0, 1, way * 80, 100, 1);
}


void turnL(int speed, int side_of_turn, int way_to_drive, int number) {
  AllDiagonal();
  delay(300);
  for (int i = 0; i < number; i++) {
    int dat1 = 0;
    Serial.println("aaaaa");
    if (side_of_turn == 1) {
      if (way_to_drive == 1)
        dat1 = 3;
      else
        dat1 = 1;
    } else if (side_of_turn == -1) {
      if (way_to_drive == 1)
        dat1 = 2;
      else
        dat1 = 4;
    }

    if (inverse) {
      drive(side_of_turn * speed, side_of_turn * speed, -side_of_turn * speed, -side_of_turn * speed);
      delay(50);

      while (sensors(dat1) > 100)
        drive(side_of_turn * speed, side_of_turn * speed, -side_of_turn * speed, -side_of_turn * speed);

      while (sensors(dat1) < 200)
        drive(side_of_turn * speed, side_of_turn * speed, -side_of_turn * speed, -side_of_turn * speed);

      while (sensors(dat1) > 90)
        drive(side_of_turn * speed, side_of_turn * speed, -side_of_turn * speed, -side_of_turn * speed);
    } else {
      drive(side_of_turn * speed, side_of_turn * speed, -side_of_turn * speed, -side_of_turn * speed);
      delay(50);
      while (sensors(dat1) < 160)
        drive(side_of_turn * speed, side_of_turn * speed, -side_of_turn * speed, -side_of_turn * speed);

      while (sensors(dat1) > 40)
        drive(side_of_turn * speed * 0.8, side_of_turn * speed * 0.8, -side_of_turn * speed * 0.8, -side_of_turn * speed * 0.8);

      while (sensors(dat1) < 240)
        drive(side_of_turn * speed * 0.6, side_of_turn * speed * 0.6, -side_of_turn * speed * 0.6, -side_of_turn * speed * 0.6);
    }

    drive(-side_of_turn * 255, -side_of_turn * 255, side_of_turn * 255, side_of_turn * 255);
    delay(map(abs(speed), 0, 255, 0, 25));
    stop();
    delay(60);
  }
  AllForward();
  delay(300);
}

void MoveSync(float sped1, float sped2, uint32_t dist, int stopp) {
  dist = (dist / 29) * 102;
  // drive(0, 0, 0, 0);

  float e = 0;
  float eold = 0;
  float sped11 = sped1;
  float sped22 = sped2;
  countr = 0;
  countl = 0;
  int timer = millis();
  float deg = 0;
  while (deg < dist) {

    if (sped1 != 0 and sped2 != 0) {
      if (abs(sped1) > abs(sped2)) {
        deg = countl;
        e = countl - countr * abs(sped1) / abs(sped2);
      } else {
        deg = countr;
        e = countl * abs(sped2) / abs(sped1) - countr;
      }

      // if ((dist > 50 and deg < 300 and deg < 0.7 * dist) and (millis() - timer) < 200) {
      //   sped1 = MIN_SPEED + ((millis() - timer) / 200) * (sped1 - MIN_SPEED);
      //   sped2 = MIN_SPEED + ((millis() - timer) / 200) * (sped2 - MIN_SPEED);
      // } else if (dist > 150 and (sped1 >= 150 and sped2 >= 150) and dist - deg < 90) {
      //   sped1 = sped11 * 0.6;
      //   sped2 = sped22 * 0.6;
      // } else {
      sped1 = sped11;
      sped2 = sped22;
      // }

      float u = e * 4 + (e - eold) * 8;
      float mot1 = sped1 - u * sped1 / abs(sped1);
      float mot2 = sped2 + u * sped2 / abs(sped2);
      if (sped1 > 0)
        mot1 = constrain(mot1, 0, 255);
      else
        mot1 = constrain(mot1, -255, 0);

      if (sped2 > 0)
        mot2 = constrain(mot2, 0, 255);
      else
        mot2 = constrain(mot2, -255, 0);

      drive(mot1, mot1, mot2, mot2);
      e_old = e;
    } else {
      drive(sped1, sped1, sped2, sped2);
      if (sped1 != 0) deg = countl;
      if (sped2 != 0) deg = countr;
    }
  }
  if (stopp > 0) {  //резко тормоз
    drive(-255 * sped1 / abs(sped1), -255 * sped1 / abs(sped1), -255 * sped2 / abs(sped2), -255 * sped2 / abs(sped2));
    delay(((abs(sped1) + abs(sped2)) / 2) / 255 * 30);
    stop();
    delay(50);
  }
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