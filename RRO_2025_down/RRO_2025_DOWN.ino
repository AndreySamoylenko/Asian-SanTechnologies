#include <Servo.h>

//----------------- I love arduino! and kinda hate esp(( ---------------//

Servo aserv;
Servo bserv;
Servo cserv;
Servo dserv;

Servo clawserv;
Servo armserv;

Servo camserv;

//----------------------servo pins
#define servoa 36
#define servob 38
#define servoc 5
#define servod 3

#define servoClaw 40
#define servoArm 7

#define servoCatapult A9

#define ASF 143  // A servo Forward position
#define ASD 88   // A servo Diagonal position
#define ASS 46   // A servo Sideways position

#define BSS 137
#define BSD 92
#define BSF 39

#define CSF 142
#define CSD 89
#define CSS 46

#define DSS 137
#define DSD 94
#define DSF 39

#define ARM_DOWN 44
#define ARM_SEMIDOWN 70
#define ARM_FIRST_TUBE 140  // нижняя труба
#define ARM_SECOND_TUBE 140 - 14
#define ARM_THIRD_TUBE 140 - 14 - 15

#define CLAW_OPEN 80
#define CLAW_CLOSED 28
#define CLAW_OPEN_ENOUGH 50

#define cam_ready 150

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

#define SIGNAL_PIN 15

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

int pid_speed = 255;
int turn_speed = 200;

void setup() {
  /*---------SERIAL----------*/
  Serial.begin(9600);
  Serial2.begin(9600);
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
  pinMode(SIGNAL_PIN, OUTPUT);
  /*------Servos------*/
  // delay(500);
  aserv.attach(servoa);
  bserv.attach(servob);
  cserv.attach(servoc);
  dserv.attach(servod);
  armserv.attach(servoArm);
  clawserv.attach(servoClaw);
  camserv.attach(servoCatapult);

  // AllDiagonal();
  // ArmTube(0);
  // delay(500);
  stop();
  AllForward();
  ArmTube(2);
  camserv.write(0);
  clawserv.write(CLAW_CLOSED);
  delay(500);

  // beep(200, 200);
  do_megalovania();
  // camserv.write(cam_ready);

  Serial.println("Start successful");
  // buttonWait(1);
}
void loop() {
  /*buttonWait(0);
  // pidEnc(1, 0, 1, 255, 2700, 1);
  // delay(1000);
  */
  StateMachine();
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
