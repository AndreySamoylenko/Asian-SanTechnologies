#include <Servo.h>

//----------------- I love arduino! and kinda hate esp(( ---------------//

Servo aserv;
Servo bserv;
Servo cserv;
Servo dserv;

//----------------------servo pins
#define servoa 36
#define servob 38
#define servoc 5
#define servod 3

#define servoClaw 40
#define servoArm 7

#define ASF 143  // A servo Forward position
#define ASD 94   // A servo Diagonal position
#define ASS 46   // A servo Sideways position

#define BSS 137
#define BSD 88
#define BSF 39

#define CSF 142
#define CSD 93
#define CSS 46

#define DSS 137
#define DSD 88
#define DSF 39

/*----------------------MOTORS-------------------------*/
#define ma1 2
#define ma2 4

#define mb1 6
#define mb2 8

#define mc1 10
#define mc2 12

#define md1 11
#define md2 9


/*----------------------SENSORS-------------------------*/
#define sa A3
#define sb A0
#define sc A2
#define sd A1

/*-----------------------MISC---------------------------*/
#define BTN_PIN A5

#define BZ_PIN A13

int datamin = 595;
int datbmin = 640;
int datcmin = 640;
int datdmin = 590;


int datamax = 975;
int datbmax = 975;
int datcmax = 975;
int datdmax = 975;

volatile int countl = 0;
volatile int countr = 0;


float e_old = 0;
float dat1, dat2 = 0;

void setup() {
  /*---------SERIAL----------*/
  Serial.begin(9600);
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
  buttonWait(1);
}

void loop() {
  
  buttonWait(0);
  pidX(4, 0.0, 0, 200, 380, 1);

  turnL(250, 1, 1);
  delay(200);
  turnL(250, 1, 1);


  // pidEnc(2, 0.05, 3, 200, 800, 1);
  // delay(10000);
}

uint32_t tim = 0;
void buttonWait(int flag) {
  while (1) {
    // Serial.println(digitalRead(BTN_PIN));
    if (digitalRead(BTN_PIN) == 0)
      break;
    else if (millis() - tim > 200) {
      tim = millis();
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
