void pidX(float kp, float ki, float kd, float sped, int overdrive, int stop) {
  float speed = abs(sped);

  int dat1 = 255;
  int dat2 = 255;

  int minx = 50;
  int err_i = 0;
  float sum = 0;
  float errors[10] = { 0 };
  e_old = 0;

  while (dat1 > minx or dat2 > minx) {

    if (sped > 0) {
      dat1 = sensors(2);
      dat2 = sensors(1);
    } else {
      dat1 = analogRead(sd);
      dat2 = analogRead(sc);
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
    // Serial.println(e);
    drive(mot1 * sped / abs(sped), mot2 * sped / abs(sped), mot2 * sped / abs(sped) * 0.9, mot1 * sped / abs(sped) * 0.9);
  }

  if (overdrive > 0)
    pidEnc(kp, ki, kd, sped * 0.8, overdrive, stop);
  else if (stop==1) {  //резко тормоз
    driveAngle(-255 * sped / abs(sped), 0);
    delay(((abs(sped) + abs(sped)) / 2) / 255 * 70);
    drive(0, 0, 0, 0);
    delay(50);
  }
  else delay(50);
}

void pidEnc(float kp, float ki, float kd, float sped, int enc, int stop) {
  float speed = abs(sped);

  countl = 0;
  countr = countl;

  int minx = 50;
  int err_i = 0;
  float sum = 0;
  float errors[10] = { 0 };
  e_old = 0;

  while (countl + countr < 2 * enc) {

    if (sped > 0) {
      dat1 = sensors(2);
      dat2 = sensors(1);
    } else {
      dat1 = analogRead(sd);
      dat2 = analogRead(sc);
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
    // Serial.println(e);
    drive(mot1 * sped / abs(sped), mot2 * sped / abs(sped), mot2 * sped / abs(sped) * 0.9, mot1 * sped / abs(sped) * 0.9);
  }

  if (stop) {
    driveAngle(-255 * sped / abs(sped), 0);
    delay(((abs(sped) + abs(sped)) / 2) / 255 * 50);
    drive(0, 0, 0, 0);
  }
  delay(50);
}