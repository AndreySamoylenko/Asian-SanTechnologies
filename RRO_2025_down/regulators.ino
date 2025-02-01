void pidXN(float sped, int n) {
  if (n > 1)
    for (int i = 1; i < n; i++)
      pidX(3, 0.0, 1, sped, 380, 0);
  pidX(3, 0.0, 1, sped, 380, 1);
}


void pidX(float kp, float ki, float kd, float sped, int overdrive, int stop) {
  AllForward();
  delay(100);
  float speed = abs(sped);

  int dat1 = 255;
  int dat2 = 255;

  int minx = 50;
  int err_i = 0;
  float sum = 0;
  float errors[10] = { 0 };
  e_old = 0;
  int way = sped / abs(sped);
  while (dat1 > minx or dat2 > minx) {

    if (sped > 0) {
      dat1 = sensors(2);
      dat2 = sensors(3);
    } else {
      dat1 = sensors(1);
      dat2 = sensors(4);
    }
    if (inverse) {
      dat1 = 255 - dat1;
      dat2 = 255 - dat2;
    }

    float e = (dat2 - dat1);
    if (abs(e) < 4)
      e = 0;

    errors[err_i] = e;
    err_i = (err_i + 1) % 10;
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
    int deg = constrain(U * 0.025, -20, 20);
    // deg *= way;
    // bserv.write(BSF - deg);
    // cserv.write(CSF - deg);
    // dserv.write(DSF + deg);
    // aserv.write(ASF + deg);


    drive(mot1, mot1, mot2, mot2);
  }
  AllForward();
  if (overdrive > 0)
    pidEnc(kp, ki, kd, sped * 0.6, overdrive, stop);
  else if (stop == 1) {  //резко тормоз
    int tormoz_speed = -way * 255;
    drive(tormoz_speed, tormoz_speed, tormoz_speed, tormoz_speed);
    delay(((abs(sped) + abs(sped)) / 2) / 255 * 30);
    drive(0, 0, 0, 0);
    delay(50);
  } else delay(50);
}

void pidEnc(float kp, float ki, float kd, float sped, int enc, int stop) {
  // 800 enc - > 125 mm
  // 100 enc - > 15.625 mm
  AllForward();
  delay(120);
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
    err_i = (err_i + 1) % 10;
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
    int deg = constrain(U * 0.025, -20, 20);
    // deg *= way;
    bserv.write(BSF - deg);
    cserv.write(CSF - deg);
    dserv.write(DSF + deg);
    aserv.write(ASF + deg);


    drive(mot1, mot1, mot2, mot2);
  }
  AllForward();


  if (stop == 1) {  //резко тормоз
    int tormoz_speed = -way * 255;
    drive(tormoz_speed, tormoz_speed, tormoz_speed, tormoz_speed);
    delay(((abs(sped) + abs(sped)) / 2) / 255 * 30);
    drive(0, 0, 0, 0);
  }
  delay(50);
}