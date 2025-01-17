
#define MIN_SPEED 80

void turn(float sped, int side, int angle) {
  delay(50);
  drive(side * sped, -side * sped, -side * sped, side * sped);
  MoveSync(side * sped, -side * sped, angle * 10.0 / 6.0, 1);
}

void turnL(int speed, int side, int way) {
  AllDiagonal();
  delay(100);
  int dat1 = 0;

  if (side == 1)
    dat1 = 1;
  else
    dat1 = 2;

  if (way == -1)
    dat1 += 2;  // 2+2 -> 4    1+2 -> 3

  while (sensors(dat1) < 160) {
    drive(side * speed, side * speed, -side * speed, -side * speed);
  }
  while (sensors(dat1) > 80) {
    drive(side * speed, side * speed, -side * speed, -side * speed);
  }
  while (sensors(dat1) < 90) {
    drive(side * speed, side * speed, -side * speed, -side * speed);
  }
  drive(-side * 255, -side * 255, side * 255, side * 255);
  delay(abs(speed) * 0.2);
  drive(0, 0, 0, 0);
}

void MoveSync(float sped1, float sped2, uint32_t dist, int stop) {
  dist = (dist / 28.5) * 100;
  drive(0, 0, 0, 0);

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

      if ((dist > 50 and deg < 300 and deg < 0.7 * dist) and (millis() - timer) < 200) {
        sped1 = MIN_SPEED + ((millis() - timer) / 200) * (sped1 - MIN_SPEED);
        sped2 = MIN_SPEED + ((millis() - timer) / 200) * (sped2 - MIN_SPEED);
      } else if (dist > 150 and (sped1 >= 150 and sped2 >= 150) and dist - deg < 90) {
        sped1 = sped11 * 0.6;
        sped2 = sped22 * 0.6;
      } else {
        sped1 = sped11;
        sped2 = sped22;
      }

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

      drive(mot1, mot2, mot2, mot1);
      e_old = e;
    } else {
      drive(sped1, sped2, sped2, sped1);
      if (sped1 != 0) deg = countl;
      if (sped2 != 0) deg = countr;
    }
  }
  if (stop > 0) {  //резко тормоз
    drive(-255 * sped1 / abs(sped1), -255 * sped2 / abs(sped2), -255 * sped2 / abs(sped2), -255 * sped1 / abs(sped1));
    delay(((abs(sped1) + abs(sped2)) / 2) / 255 * 10);
    drive(0, 0, 0, 0);
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

void stop() {
  drive(0, 0, 0, 0);
}