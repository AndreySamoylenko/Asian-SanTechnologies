

uint32_t timeeer = 0;

String last_comand = "zz";
void processDataFromPi(int stat) {
  if (Serial2.available()) {                              // Если есть данные
    String receivedData = Serial2.readStringUntil('\n');  // Читаем до '\n', тобеш сообщение должно выглядеть "@$\n" @ - символ действия, $ - цифра-параметр
    if (receivedData.length() == 2) {
      char motion = receivedData[0];
      int number = receivedData[1] - '0';
      Serial.print(motion);
      Serial.print(" ");
      Serial.println(number);
      if (stat == 1) {


        switch (motion) {
          case 'O':
            digitalWrite(SIGNAL_PIN, 1);
            while (digitalRead(BTN_PIN))
              ;
            delay(100);
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'X':
            digitalWrite(SIGNAL_PIN, 1);
            pidXN(pid_speed, number);
            digitalWrite(SIGNAL_PIN, 0);
            last_comand = "zz";

            break;

          case 'x':
            digitalWrite(SIGNAL_PIN, 1);
            pidXN(-pid_speed, number);
            digitalWrite(SIGNAL_PIN, 0);
            last_comand = "zz";

            break;

          case 'R':
            digitalWrite(SIGNAL_PIN, 1);
            turnL(turn_speed, 1, 1, number);
            digitalWrite(SIGNAL_PIN, 0);
            break;
          case 'r':
            digitalWrite(SIGNAL_PIN, 1);
            turnL(turn_speed, 1, -1, number);
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'L':
            digitalWrite(SIGNAL_PIN, 1);
            turnL(turn_speed, -1, 1, number);
            digitalWrite(SIGNAL_PIN, 0);
            break;
          case 'l':
            digitalWrite(SIGNAL_PIN, 1);
            turnL(turn_speed, -1, -1, number);
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'F':
            digitalWrite(SIGNAL_PIN, 1);
            if (number >= 0 and number <= 1) {
              if (number == 1) {
                FromNormalToInverse(1 + (last_comand == "F0"));
                last_comand = "F1";
              } else{
                FromInverseToNormal(1 + (last_comand == "F1"));
                last_comand = "F0";
            }
            }
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'f':
            digitalWrite(SIGNAL_PIN, 1);
            if (number >= 0 and number <= 1) {
              if (number == 1) {
                FromNormalToInverse(-1 - (last_comand == "f0"));
                last_comand = "f1";
              } else {
                FromInverseToNormal(-1 - (last_comand == "f1"));
                last_comand = "f0";
              }
            }
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'G':
            digitalWrite(SIGNAL_PIN, 1);
            GrabTheTube();
            delay(200);
            LayTheTubeIntoStorage();
            delay(200);
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'P':
            digitalWrite(SIGNAL_PIN, 1);
            pickTubeFromStorage(tubes_collected);
            tubes_collected--;
            delay(200);
            PutTheTubeOntoStand();
            delay(200);
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'B':
            digitalWrite(SIGNAL_PIN, 1);
            beep((number + 1) * 280, 100);
            delay(200);
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'T':
            digitalWrite(SIGNAL_PIN, 1);
            tubes_collected = number;
            delay(200);
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'A':
            digitalWrite(SIGNAL_PIN, 1);
            floor_distinction();
            delay(200);
            digitalWrite(SIGNAL_PIN, 0);
            break;

          case 'a':
            digitalWrite(SIGNAL_PIN, 1);
            inverse = number - 1;
            delay(200);
            digitalWrite(SIGNAL_PIN, 0);
            break;
        }
        delay(10);

      } else if (stat == 0) {
        if (motion == '9')  // сообщение "99" говорит о том что распберри запустилась
          if (number == 9)
            if (start_flag == 0)
              start_flag = 1;
      }
    }
  }
}




void StateMachine() {
  switch (state) {
    case 0:  // waiting for pi to boot
      processDataFromPi(0);
      digitalWrite(SIGNAL_PIN, 0);
      if (start_flag == 1) {
        state = 1;
        beep(700, 100);
        delay(150);
        beep(900, 150);
        delay(150);
        beep(1100, 100);
        delay(150);
      }
      break;
    case 1:  // waiting for user to press the button
      if (digitalRead(BTN_PIN) == 0) {
        state = 2;
        digitalWrite(SIGNAL_PIN, 1);
        delay(100);
        for (int i = 10; i < cam_ready; i++) {
          camserv.write(i);
          delay(6);
        }
        digitalWrite(SIGNAL_PIN, 0);
      }
      break;
    case 2:
      processDataFromPi(1);
      if (start_flag == 0) {
        state = 1;
      }
      break;
  }
}