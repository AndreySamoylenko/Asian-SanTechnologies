float sensors(int dat) {
  float data = 0;
  switch (dat) {
    case 2:
      data = float(analogRead(sb) - datbmin) / (datbmax - datbmin);
      break;
    case 1:
      data = float(analogRead(sa) - datamin) / (datamax - datamin);
      break;
    case 3:
      data = float(analogRead(sc) - datcmin) / (datcmax - datcmin);
      break;
    case 4:
      data = float(analogRead(sd) - datdmin) / (datdmax - datdmin);
      break;
  }
  return constrain(data * 256, 0, 256);
}

void beep(int freq, int dur) {
  myTone(1.0 / float(freq), dur);
  delay(10);
}

void myTone(float per, int dur) {
  uint32_t tim = millis();
  while (millis() < tim + dur) {
    digitalWrite(BZ_PIN, 1);
    delayMicroseconds(per * 1e+5 * 5);
    digitalWrite(BZ_PIN, 0);
    delayMicroseconds(per * 1e+5 * 5);
  }
}

// some cringe calibration

void calibration() {
  digitalWrite(13, 1);
  while (digitalRead(BTN_PIN))
    ;
  delay(50);
  digitalWrite(13, 0);

  uint16_t suma, sumb;
  suma = 0;
  sumb = 0;
  for (int i = 0; i < 10; i++) {
    delay(10);
    suma += analogRead(sb);
    sumb += analogRead(sc);
  }
  suma = suma / 10;
  sumb = sumb / 10;
  datbmax = suma;
  datcmax = sumb;

  digitalWrite(13, 1);
  while (digitalRead(BTN_PIN))
    ;
  delay(50);
  digitalWrite(13, 0);

  suma = 0;
  sumb = 0;
  for (int i = 0; i < 10; i++) {
    delay(10);
    suma += analogRead(sa);
    sumb += analogRead(sd);
  }
  suma = suma / 10;
  sumb = sumb / 10;
  datamax = suma;
  datdmax = sumb;



  digitalWrite(13, 1);
  while (digitalRead(BTN_PIN))
    ;
  delay(50);
  digitalWrite(13, 0);

  suma = 0;
  sumb = 0;
  for (int i = 0; i < 10; i++) {
    delay(10);
    suma += analogRead(sb);
    sumb += analogRead(sc);
  }
  suma = suma / 10;
  sumb = sumb / 10;
  datbmin = suma;
  datcmin = sumb;

  digitalWrite(13, 1);
  while (digitalRead(BTN_PIN))
    ;
  delay(50);
  digitalWrite(13, 0);

  suma = 0;
  sumb = 0;
  for (int i = 0; i < 10; i++) {
    delay(10);
    suma += analogRead(sa);
    sumb += analogRead(sd);
  }
  suma = suma / 10;
  sumb = sumb / 10;
  datamin = suma;
  datdmin = sumb;
}
