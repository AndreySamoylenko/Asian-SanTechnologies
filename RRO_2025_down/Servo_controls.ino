void AllForward(){
  Aserv.write(ASF);
  Bserv.write(BSF);
  Cserv.write(CSF);
  Dserv.write(DSF);
  delay(100);
}

void AllDiagonal(){
  Aserv.write(ASD);
  Bserv.write(BSD);
  Cserv.write(CSD);
  Dserv.write(DSD);
  delay(100);
}
void AllSideways(){
  Aserv.write(ASS);
  Bserv.write(BSS);
  Cserv.write(CSS);
  Dserv.write(DSS);
  delay(100);
}