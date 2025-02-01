void processDataFromPi() {
  if (Serial2.available()) {                              // Если есть данные
    String receivedData = Serial2.readStringUntil('\n');  // Читаем до '\n', тобеш сообщение должно выглядеть "@$\n" @ - символ действия, $ - цифра-параметр
    if (receivedData.length() == 2) {
      char motion = receivedData[0];
      int number = receivedData[1] - '0';
      switch (motion) {
        case 'X':
          digitalWrite(SIGNAL_PIN, 1);
          pidXN(200, number);
          digitalWrite(SIGNAL_PIN, 0);
          break;
        case 'x':
          digitalWrite(SIGNAL_PIN, 1);
          pidXN(-200, number);
          digitalWrite(SIGNAL_PIN, 1);
          break;

        case 'R':
          digitalWrite(SIGNAL_PIN, 1);
          for (int i = 0; i < number; i++)
            turnL(200, 1, 1);
          digitalWrite(SIGNAL_PIN, 1);
          break;
        case 'r':
          digitalWrite(SIGNAL_PIN, 1);
          for (int i = 0; i < number; i++)
            turnL(200, 1, -1);
          digitalWrite(SIGNAL_PIN, 1);
          break;

        case 'L':
          digitalWrite(SIGNAL_PIN, 1);
          for (int i = 0; i < number; i++)
            turnL(200, -1, 1);
          digitalWrite(SIGNAL_PIN, 1);
          break;
        case 'l':
          digitalWrite(SIGNAL_PIN, 1);
          for (int i = 0; i < number; i++)
            turnL(200, -1, -1);
          digitalWrite(SIGNAL_PIN, 1);
          break;

        case 'F':
          digitalWrite(SIGNAL_PIN, 1);
          if (number >= 0 and number <= 1)
            inverse = number;
          digitalWrite(SIGNAL_PIN, 1);
          break;

        case '9':  // сообщение "99" говорит о том что распберри запустилась
          if (number == 9)
            if (start_flag == 0)
              start_flag = 1;
          break;
      }
    }
  }
}



void StateMachine() {
  switch (state) {
    case 0:  // waiting for pi to boot
      processDataFromPi();
      if (start_flag == 1) {
        state = 1;
        beep(500, 200);
        delay(200);
        beep(600, 200);
        delay(200);
        beep(700, 200);
        delay(200);
      }
      break;
    case 1:  // waiting for user to press the button
      if (digitalRead(BTN_PIN) == 0)
        state = 2;
      break;
    case 2:
      break;
  }
}