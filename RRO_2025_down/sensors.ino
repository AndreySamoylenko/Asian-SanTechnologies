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
  tone(BZ_PIN, freq);
  delay(dur);
  noTone(BZ_PIN);
  delay(10);
}