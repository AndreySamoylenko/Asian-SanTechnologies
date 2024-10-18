

float drive_deg(float angle, int sp) {
  int angle_2 = ceil(abs(angle));
  float spa, spb, spc, spd;

  if (angle_2 <= 45) {
    int vector_lenght = round(abs(sp) / sin(radians(90 - angle_2)));
    int final_impact = round(sqrt(pow(vector_lenght, 2) - pow(sp, 2)));
    if (angle < 0)
      final_impact* -1 ;

    Serial.println(final_impact);
  }

  if (angle_2 > 45) {
    int vector_lenght = round(abs(sp) / sin(radians(angle_2)));
    Serial.println(vector_lenght);
    int final_impact = round(sqrt(pow(vector_lenght, 2) - pow(sp, 2)));
    if (angle < 0)
      final_impact* -1 ;

 
    Serial.println(final_impact);
  }
}
