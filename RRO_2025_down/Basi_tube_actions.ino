void GrabTheTube() {
  ArmDown();
  openClaw();
  delay(500);
  pidEnc(3, 0.1, 1, 200, 850, 1);
  delay(600);
  closeClaw();
  delay(600);
  ArmTube(1);
  pidEnc(1, 0.1, 1, 200, 400, 1);
  pidXN(-250, 1);
}

void LayTheTubeIntoStorage() {
  switch (tubes_collected) {
    case 0:
      ArmTube(4);
      delay(400);
      for (int i = CLAW_CLOSED; i < CLAW_OPEN; i++) {
        clawserv.write(i);
        armserv.write(map(i, CLAW_CLOSED, CLAW_OPEN, ARM_FIRST_TUBE, ARM_SECOND_TUBE));
        delay(8);
      }
      ArmTube(1);
      delay(200);
      closeClaw();
      delay(200);
      ArmTube(3);
      break;
    case 1:
      ArmTube(3);
      delay(400);
      for (int i = CLAW_CLOSED; i < CLAW_OPEN; i++) {
        clawserv.write(i);
        armserv.write(map(i, CLAW_CLOSED, CLAW_OPEN, ARM_SECOND_TUBE, ARM_THIRD_TUBE));
        delay(8);
      }
      ArmTube(1);
      delay(200);
      closeClaw();
      delay(200);
      ArmTube(2);
      break;
    case 2:
      ArmTube(2);
      break;
  }
  tubes_collected++;
}

void PutTheTubeOntoStand() {
  ArmTube(1);
  pidX(3, 0.1, 1, 120, 120, 1);
  delay(300);
  ArmDown();
  delay(400);
  clawserv.write(CLAW_OPEN);
  delay(500);
  pidXN(-200, 1);
  ArmTube(1);
  closeClaw();
  delay(200);

}

void pickTubeFromStorage(int tube_number) {  // tube_number - номер трубы начиная снизу (1 - нижняя, 2 - верхняя)

  switch (tube_number) {
    case 3:
      closeClaw();
      break;
    case 2:
      clawserv.write(CLAW_OPEN);
      delay(200);
      ArmTube(2);
      delay(200);
      for (int i = CLAW_OPEN; i > CLAW_CLOSED; i--) {
        clawserv.write(i);
        armserv.write(map(i, CLAW_CLOSED, CLAW_OPEN, ARM_SECOND_TUBE, ARM_THIRD_TUBE - 0));
        delay(12);
      }

      closeClaw();

      break;
    case 1:
      clawserv.write(CLAW_OPEN);
      delay(200);
      ArmTube(3);
      delay(500);
      for (int i = CLAW_OPEN; i > CLAW_CLOSED; i--) {
        clawserv.write(i);
        armserv.write(map(i, CLAW_CLOSED, CLAW_OPEN, ARM_FIRST_TUBE + 5, ARM_SECOND_TUBE + 3));
        delay(12);
      }

      closeClaw();

      break;
  }
  ArmTube(1);

  tube_number--;
}

