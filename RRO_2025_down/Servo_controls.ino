void AllForward() {
  aserv.write(ASF);
  bserv.write(BSF);
  cserv.write(CSF);
  dserv.write(DSF);
  // delay(100);
}

void AllDiagonal() {
  aserv.write(ASD);
  bserv.write(BSD);
  cserv.write(CSD);
  dserv.write(DSD);
  // delay(100);
}
void AllSideways() {
  aserv.write(ASS);
  bserv.write(BSS);
  cserv.write(CSS);
  dserv.write(DSS);
  delay(100);
}

void ArmDown() {
  armserv.write(ARM_DOWN);
}

void ArmTube(int tube) {
  switch (tube) {
    case 1:
      armserv.write(ARM_SEMIDOWN);
      break;
    case 2:
      armserv.write(ARM_THIRD_TUBE);
      break;
    case 3:
      armserv.write(ARM_SECOND_TUBE);
      break;
    case 4:
      armserv.write(ARM_FIRST_TUBE);
      break;
    default:
      ArmDown();
      break;
  }
}

void openClaw() {
  clawserv.write(CLAW_OPEN_ENOUGH);
}

void closeClaw() {
  clawserv.write(CLAW_CLOSED);
}