#include <Servo.h>

//----------------- I love arduino! and kinda hate esp(( ---------------//

Servo aserv;
Servo bserv;
Servo cserv;
Servo dserv;

//----------------------servo pins
#define servoa 24
#define servob 13
#define servoc 6
#define servod 2

#define servoClaw 22
#define servoArm 4

#define ASF 136  // A servo Forward position
#define ASD 89   // A servo Diagonal position
#define ASS 43   // A servo Sideways position

#define BSS 137
#define BSD 92
#define BSF 46

#define CSF 130
#define CSD 85
#define CSS 38

#define DSS 137
#define DSD 90
#define DSF 45

/*----------------------MOTORS-------------------------*/
#define ma1 5
#define ma2 3

#define mb1 10
#define mb2 11

#define mc1 8
#define mc2 12

#define md1 9
#define md2 7


/*----------------------SENSORS-------------------------*/
#define sa A3
#define sb A0
#define sc A2
#define sd A1

/*-----------------------MISC---------------------------*/
#define BTN_PIN A5

#define BZ_PIN A13

int datamin = 490;
int datbmin = 600;
int datcmin = 540;
int datdmin = 555;


int datamax = 975;
int datbmax = 985;
int datcmax = 980;
int datdmax = 800;

int countl = 0;
int countr = 0;

float e_old = 0;
float dat1, dat2 = 0;

void setup() {
  /*---------SERIAL----------*/
  Serial.begin(115200);
  /*-------INTERRUPTS---------*/
  attachInterrupt(digitalPinToInterrupt(18), encl, RISING);
  attachInterrupt(digitalPinToInterrupt(19), encr, RISING);
  /*--------PWM---------*/
  pinMode(ma1, OUTPUT);
  pinMode(ma2, OUTPUT);
  pinMode(mb1, OUTPUT);
  pinMode(mb2, OUTPUT);
  pinMode(mc1, OUTPUT);
  pinMode(mc2, OUTPUT);
  pinMode(md1, OUTPUT);
  pinMode(md2, OUTPUT);
  /*-------PINS---------*/
  pinMode(BTN_PIN, INPUT_PULLUP);
  pinMode(BZ_PIN, OUTPUT);
  /*------Servos------*/
  // delay(500);
  aserv.attach(servoa);
  bserv.attach(servob);
  cserv.attach(servoc);
  dserv.attach(servod);

  AllDiagonal();
  delay(500);
  AllForward();
  delay(500);

  // beep(1000, 300);
  // delay(50);
  // beep(700, 70);
  // delay(10);
  // beep(900, 80);
  // delay(50);
  // beep(1500, 300);

  Serial.println("Start successful");
  buttonWait(0);
}

void loop() {
  // buttonWait(0);
  pidX(3, 0.03, 5, 200, 550, 1);

  turnL(160, 1, 1);
  turnL(160, 1, 1);
  turnL(160, 1, 1);


  // drive(0, 0, 0, 0);



  // pidX(0.6, 0.01, 3, 200, 100, 1);
  // pidX(0.6, 0.01, 3, -200, 100, 1);
  // pidX(0.6, 0.01, 3, -200, 100, 1);
  // pidX(0.6, 0.01, 3, 110, 100, 1);
  // pidX(0.6, 0.01, 3, 180, 100, 1);
  //
  // buttonWait(0);
  //
  // pidEnc(0.6, 0.01, 3, 180, 1000, 1);

  // delay(500);
  // beep(700, 200);
  // delay(50);
  // beep(1000, 150);
}


void buttonWait(int flag) {
  while (1) {
    // Serial.println(digitalRead(BTN_PIN));
    if (digitalRead(BTN_PIN) == 0)
      break;
    else {
      switch (flag) {
        case (1):

          Serial.print(analogRead(sa));
          Serial.print('\t');
          Serial.print(analogRead(sb));
          Serial.print('\t');
          Serial.print(analogRead(sc));
          Serial.print('\t');
          Serial.print(analogRead(sd));
          Serial.print("\t\t");
          Serial.print(sensors(1));
          Serial.print('\t');
          Serial.print(sensors(2));
          Serial.print('\t');
          Serial.print(sensors(3));
          Serial.print('\t');
          Serial.print(sensors(4));
          Serial.print("\t\t");
          Serial.print(countl);
          Serial.print('\t');
          Serial.print(countr);
          Serial.println('\n');
          break;
        default:
          break;
      }
    }
  }
  beep(500, 100);
  delay(50);
}
