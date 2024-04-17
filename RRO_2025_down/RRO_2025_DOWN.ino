#include <Servo.h>

//----------------- I love arduino! and kinda hate esp(( ---------------//

Servo aserv;
Servo bserv;
Servo cserv;
Servo dserv;

Servo clawserv;
Servo armserv;

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

#define ARM_DOWN 44
#define ARM_SEMIDOWN 70
#define ARM_FIRST_TUBE 140  // нижняя труба
#define ARM_SECOND_TUBE 140 - 25
#define ARM_THIRD_TUBE 140 - 25 - 25

#define CLAW_OPEN 80
#define CLAW_CLOSED 25
#define CLAW_OPEN_ENOUGH 60


/*----------------------MOTORS-------------------------*/
#define ma1 2
#define ma2 4

#define mb1 8
#define mb2 6

#define mc1 12
#define mc2 10

#define md1 11
#define md2 9


/*----------------------SENSORS-------------------------*/
#define sa A1
#define sb A0
#define sc A2
#define sd A3

/*-----------------------MISC---------------------------*/
#define BTN_PIN A7

#define BZ_PIN A5

#define SIGNAL_PIN 13

int datamin = 620;
int datbmin = 620;
int datcmin = 600;
int datdmin = 600;


int datamax = 975;
int datbmax = 975;
int datcmax = 975;
int datdmax = 975;

volatile int countl = 0;
volatile int countr = 0;

int inverse = 0;
float e_old = 0;
float dat1, dat2 = 0;

int tubes_collected = 0;
int state = 0;
uint8_t start_flag = 0;


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
  armserv.attach(servoArm);
  clawserv.attach(servoClaw);

  // AllDiagonal();
  // ArmTube(0);
  // delay(500);
  AllForward();
  ArmTube(2);
  clawserv.write(CLAW_CLOSED);
  delay(500);

  beep(1000, 300);
  delay(50);
  beep(700, 70);
  delay(10);
  beep(900, 80);
  delay(50);
  beep(1500, 300);

  Serial.println("Start successful");
  // buttonWait(0);
}

void loop() {

  buttonWait(0);
  drive(255,255,255,255);
//  pidXN(250, 1);
//
//  turnL(250, -1, 1);
//  pidXN(200, 2);
//  turnL(250, 1, 1);
//
//  GrabTheTube();
//  turnL(250, -1, 1);
//
//  pidXN(-200, 2);
//
//  turnL(250, 1, 1);
//  pidXN(200, 4);
//  clawserv.write(CLAW_OPEN_ENOUGH);
//  ArmTube(2);
//  turnL(250, -1, 1);
//  FromNormalToInverse();
//  pidXN(200, 2);










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
