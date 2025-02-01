void GrabTheTube() {
  ArmDown();
  openClaw();
  delay(500);
  pidEnc(3, 0, 2, 150, 740, 1);
  delay(200);
  closeClaw();
  delay(200);
  ArmTube(1);
  pidXN(-200, 1);
}

void LayTheTubeIntoStorage() {
  switch (tubes_collected) {
    case 0:
      ArmTube(4);
      for (int i = CLAW_CLOSED; i < CLAW_OPEN; i++) {
        clawserv.write(i);
        armserv.write(map(i, CLAW_CLOSED, CLAW_OPEN, ARM_FIRST_TUBE, ARM_SECOND_TUBE));
        delay(7);
      }
      ArmTube(2);
      break;
    case 1:
      ArmTube(3);
      for (int i = CLAW_CLOSED; i < CLAW_OPEN; i++) {
        clawserv.write(i);
        armserv.write(map(i, CLAW_CLOSED, CLAW_OPEN, ARM_SECOND_TUBE, ARM_THIRD_TUBE));
        delay(7);
      }
      ArmTube(2);
      break;
  }
  tubes_collected++;
}

void PutTheTubeOntoStand() {
  pidEnc(3, 0, 1, 150, 1450, 1);
  delay(200);
  ArmDown();
  delay(200);
  openClaw();
  delay(400);
  pidXN(-200, 1);
}

void pickTubeFromStorage(int tube_number) {  // tube_number - номер трубы начиная снизу (1 - нижняя, 2 - верхняя)

  switch (tube_number) {
    case 1:
      clawserv.write(CLAW_OPEN);
      delay(200);
      ArmTube(4);
      delay(500);
      closeClaw();

      break;
  }
  tube_number--;
}