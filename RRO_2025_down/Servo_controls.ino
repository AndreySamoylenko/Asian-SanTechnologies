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