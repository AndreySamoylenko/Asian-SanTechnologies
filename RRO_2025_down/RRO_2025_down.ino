
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
  attachInterrupt(digitalPinToInterrupt(47), encr, RISING);
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

  beep(1000, 400);
  delay(50);
  beep(1500, 300);
}

void loop() {
  buttonWait(0);

  beep(1000, 300);

  pidX(0.6, 0.01, 3, 170, 90, 1);

  beep(1000, 400);
  delay(50);
  beep(1500, 300);
  buttonWait(0);

  

  turn(120, 1, 90);
  // pidEnc(0.6, 0.01, 3, 170, 1000, 1);
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
          Serial.println('\n');
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
  delay(100);
}
