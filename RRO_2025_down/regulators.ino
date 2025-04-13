void pidXN(float sped, int n) {
  if (n > 1)
    for (int i = 1; i < n; i++) {
      pidX(1.5, 0.03, 0.9, sped, 100, 0);
    }
  int overdrive = 560;
  pidX(3, 0.01, 0.8, sped, overdrive, 1);
}




void pidX(float kp, float ki, float kd, float sped, int overdrive, int stopp) {
  float speed = abs(sped);

  int dat1 = 255;
  int dat2 = 255;

  int minx = 60;
  if (inverse == 1) {
    minx = 230;
    dat1 = 0;
    dat2 = 0;
  }

  int err_i = 0;
  float sum = 0;
  float errors[10] = { 0 };
  e_old = 0;
  int way = sped / abs(sped);

  int counter = 0;
  while (counter < 10) {

    if (inverse == 1 ? (dat1 < minx or dat2 < minx) : (dat1 > minx or dat2 > minx))
      counter = 0;

    else
      counter++;



    if (sped > 0) {
      dat1 = sensors(2);
      dat2 = sensors(3);
    } else {
      dat1 = sensors(1);
      dat2 = sensors(4);
    }

    float e = (dat2 - dat1);
    if (inverse) e = -e;
    if (abs(e) < 4)
      e = 0;

    errors[err_i] = e;
    // err_i = (err_i + 1) % 10;
    sum = sum + e - errors[err_i];

    float Up = e * kp;
    float Ud = (e - errors[err_i]) * kd;
    float Ui = sum * ki;

    float U = Up + Ui + Ud;

    float mot1 = speed - U;
    float mot2 = speed + U;
    mot1 = constrain(mot1, 0, 1.3 * speed);
    mot2 = constrain(mot2, 0, 1.3 * speed);

    mot1 = mot1 * way;
    mot2 = mot2 * way;
    int deg = constrain(U * 0.025, -3, 3);
    // deg *= way;
    bserv.write(BSF - deg);
    cserv.write(CSF - deg);
    dserv.write(DSF + deg);
    aserv.write(ASF + deg);


    drive(mot1, mot1, mot2, mot2);
  }
  AllForward();
  if (overdrive > 0)
    pidEnc(kp, ki, kd, sped, overdrive, stopp);
  else if (stopp == 1) {  //резко тормоз
    int tormoz_speed = -way * 255;
    drive(tormoz_speed, tormoz_speed, tormoz_speed, tormoz_speed);
    delay(((abs(sped) + abs(sped)) / 2) / 255 * 30);
    stop();
    delay(50);
  } else delay(50);
}

void pidEnc(float kp, float ki, float kd, float sped, int enc, int stopp) {
  // 800 enc - > 125 mm
  // 100 enc - > 15.625 mm

  float speed = abs(sped);
  countl = 0;
  countr = 0;
  int err_i = 0;
  float sum = 0;
  float errors[10] = { 0 };
  e_old = 0;

  int way = sped / abs(sped);
  while ((countl + countr) < enc) {


    if (sped > 0) {
      dat1 = sensors(2);
      dat2 = sensors(3);
    } else {
      dat1 = sensors(1);
      dat2 = sensors(4);
    }

    float e = (dat2 - dat1);
    if (inverse) e = -e;
    if (abs(e) < 4)
      e = 0;

    errors[err_i] = e;
    // err_i = (err_i + 1) % 10;
    sum = sum + e - errors[err_i];

    float Up = e * kp;
    float Ud = (e - errors[err_i]) * kd;
    float Ui = sum * ki;

    float U = Up + Ui + Ud;

    float mot1 = speed - U;
    float mot2 = speed + U;
    mot1 = constrain(mot1, 0, 1.3 * speed);
    mot2 = constrain(mot2, 0, 1.3 * speed);

    mot1 = mot1 * way;
    mot2 = mot2 * way;
    int deg = constrain(U * 0.025, -3, 3);
    // deg *= way;
    bserv.write(BSF - deg);
    cserv.write(CSF - deg);
    dserv.write(DSF + deg);
    aserv.write(ASF + deg);

    if (inverse) {
      if (way == 1) {
        if (mot1 > mot2)
          drive(mot1, mot1, mot2, 255);
        else
          drive(255, mot1, mot2, mot2);
      } else {
        if (mot1 < mot2)
          drive(mot1, mot1, -255, mot2);
        else
          drive(mot1, -255, mot2, mot2);
      }
    } else
      drive(mot1, mot1, mot2, mot2);
  }

  if (stopp == 1) {  //резко тормоз
    int tormoz_speed = -way * 255;
    drive(tormoz_speed, tormoz_speed, tormoz_speed, tormoz_speed);
    delay(((abs(sped) + abs(sped)) / 2) / 255 * 30);
    stop();
  }
  delay(50);
}