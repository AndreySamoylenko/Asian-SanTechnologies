#include <ESP32Servo.h>

Servo Aserv;
Servo Bserv;
Servo Cserv;
Servo Dserv;

#define ASF 135  // A servo Forward position
#define ASD 89   // A servo Diagonal position
#define ASS 45   // A servo Sideways position

#define BSS 137
#define BSD 92
#define BSF 48

#define CSF 130
#define CSD 85
#define CSS 38

#define DSS 137
#define DSD 90
#define DSF 48

/*----------------------MOTORS-------------------------*/
#define ma1 4
#define ma2 5
#define mb1 6
#define mb2 7
#define mc2 15
#define mc1 16
#define md2 17
#define md1 18

/*----------------------SENSORS-------------------------*/
#define sa 11
#define sb 10
#define sc 12
#define sd 13

/*-----------------------MISC---------------------------*/
#define BTN_PIN 14
#define BZ_PIN 1

int datamin = 1165;
int datbmin = 1561;
int datcmin = 1341;
int datdmin = 1041;


int datamax = 3983;
int datbmax = 4044;
int datcmax = 4035;
int datdmax = 3703;

int countl = 0;
int countr = 0;

float e_old = 0;
float dat1, dat2 = 0;

void setup() {
  /*---------SERIAL----------*/
  Serial.begin(115200);
  /*-------INTERRUPTS---------*/
  attachInterrupt(digitalPinToInterrupt(2), encl, RISING);
  attachInterrupt(digitalPinToInterrupt(48), encr, RISING);
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
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  Aserv.setPeriodHertz(50);
  Aserv.attach(35, 0, 15000);
  Bserv.attach(36, 0, 15000);
  Cserv.attach(37, 0, 12000);
  Dserv.attach(38, 0, 12000);
  delay(1000);

  AllDiagonal();
  delay(500);
  AllForward();
  delay(500);

  beep(1000, 300);
  delay(50);
  beep(700, 70);
  delay(10);
  beep(900, 80);
  delay(50);
  beep(1500, 300);
  // buttonWait(0);
}

void loop() {
  buttonWait(0);
  AllDiagonal();
  delay(100);

  buttonWait(0);
  AllForward();
  delay(100);

  buttonWait(0);
  AllSideways();
  delay(100);
  // pidX(0.6, 0.01, 3, 200, 100, 1);
  // pidX(0.6, 0.01, 3, 200, 100, 1);
  // pidX(0.6, 0.01, 3, -200, 100, 1);
  // pidX(0.6, 0.01, 3, -200, 100, 1);
  // turnL(160, 1, 1);
  // pidX(0.6, 0.01, 3, 110, 100, 1);
  // turnL(160, 1, 1);
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
